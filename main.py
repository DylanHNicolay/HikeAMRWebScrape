import undetected_chromedriver as uc
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC

import os
from dotenv import load_dotenv

load_dotenv()

def main():
    """
    Opens a website in a Chrome browser window using undetected_chromedriver,
    waits for the page to fully load, and then logs in with credentials from a .env file.
    """
    driver = None
    try:
        # Get credentials from environment variables
        username = os.getenv("USERNAME")
        password = os.getenv("PASSWORD")

        if not username or not password:
            print("Error: USERNAME and PASSWORD must be set in the .env file.")
            return

        # Set up the Chrome driver
        options = uc.ChromeOptions()
        driver = uc.Chrome(options=options, use_subprocess=True)

        # Open the website
        driver.get("https://hikeamr.org/")

        # Wait for the "Hiker Login/Reservation" link to be present in the DOM and click it
        try:
            link = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH, "//a[contains(text(), 'Hiker Login/Reservation')]"))
            )
            print(f"Found the link: {link.text}. Clicking it now.")
            link.click()

            # Wait for the new page to load
            WebDriverWait(driver, 10).until(
                lambda d: d.execute_script('return document.readyState') == 'complete'
            )
            print("New page loaded.")

            # Find the username input by placeholder and type into it
            username_input = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Username']"))
            )
            print("Found username input. Typing username.")
            username_input.send_keys(username)

            # Find the password input by placeholder and type into it
            password_input = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Password']"))
            )
            print("Found password input. Typing password.")
            password_input.send_keys(password)

            # Find the login button and click it
            login_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.ID, "btnSecureLogin"))
            )
            print("Found login button. Clicking it now.")
            login_button.click()

            # Wait for the "Reservations" button to be present and click it
            reservations_button = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//span[contains(text(), 'Reservations')]"))
            )
            print("Found 'Reservations' button. Clicking it now.")
            reservations_button.click()

            # Find the date input, clear it, and set a new date
            date_input = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "txtDate"))
            )
            print("Found date input. Clearing it and setting new date.")
            date_input.clear()
            date_input.send_keys("10/11/2025")

        except TimeoutException:
            print("Could not find an element within the time limit.")
            print("Dumping page source for debugging:")
            print(driver.page_source)

        # Keep the browser open for a while to see the result
        print("The browser will close in 10 seconds.")
        time.sleep(10)

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        if driver:
            # Close the browser
            driver.quit()
            print("Browser closed.")

if __name__ == "__main__":
    main()

