import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from datetime import datetime
import logging
import os

def setup_logging():
    # Create logs directory if it does not exist
    if not os.path.exists('logs'):
        os.makedirs('logs')

    # Define the log filename with the logs directory
    log_filename = os.path.join('logs', datetime.now().strftime("exports_%Y%m%d_%H%M%S.log"))

    # Set up logging configuration
    logging.basicConfig(
        filename=log_filename,
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

def login(driver, username, password):
    # Open the Login page of edX
    driver.get("https://authn.edx.org/login")
    print("Waiting 10 seconds for the login page to load properly..")
    time.sleep(10)

    # Enter the username
    username_field = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "emailOrUsername"))
    )
    username_field.send_keys(username)
    print("Sending username")

    # Enter the password
    password_field = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "password"))
    )
    password_field.send_keys(password)
    print("Sending password")

    # Click the "sign-in" button
    sign_in_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.NAME, "sign-in"))
    )
    sign_in_button.click()
    print("Clicked sign in..")

    # Wait for the login process to complete
    print("Login done.. Wait 10 sec before proceeding..")
    time.sleep(10)

def export_course(driver, course_key):
    # Create 'exports' directory if it doesn't exist
    if not os.path.exists('exports'):
        os.makedirs('exports')
        
    # Open the course
    driver.get(f"https://studio.edx.org/course/course-v1:{course_key}")

    # Wait
    print("Wait 5 sec to open export page..")
    time.sleep(5)

    # Open the course export
    driver.get(f"https://course-authoring.edx.org/course/course-v1:{course_key}/export")

    # Wait
    print("Wait 5 sec to click export course content..")
    time.sleep(5)

    # Wait until the "Export course content" button is clickable, then click it
    try:
        export_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[text()='Export course content']"))
        )
        export_button.click()
        print("Clicked on 'Export course content' button.")
        
        # Wait for 1 minute to allow the export to complete
        print("Wait 60 sec for export to complete..")
        time.sleep(60)
        
        # Find the link that contains ".tar.gz"
        tar_gz_link = WebDriverWait(driver, 60).until(
            EC.presence_of_element_located((By.XPATH, "//a[contains(@href, '.tar.gz')]"))
        )
        download_url = tar_gz_link.get_attribute('href')
        print(f"Found the .tar.gz file at: {download_url}")
        
        # Download the file using the requests library
        filename = os.path.join('exports', f"{course_key}.tar.gz")
        response = requests.get(download_url, stream=True)
        
        with open(filename, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
        
        print(f"Downloaded the file as: {filename}")

    except:
        # Wait for 30 seconds before closing the browser
        print("Course error: " + course_key)
        logging.exception("Course error: " + course_key) 

def main():
    setup_logging()
    
    driver = webdriver.Firefox()
    username = "your_edx_email"
    password = "your_edx_password"
    
    # Perform login
    print("Perform login")
    login(driver, username, password)
    
    # Retrieve course keys from the text file and export each course
    with open('course_keys.txt', 'r') as file:
        course_keys = file.readlines()
    
    for course_key in course_keys:
        course_key = course_key.strip()  # Remove any surrounding whitespace or newlines
        print("Working on course: " + course_key)
        logging.info("Working on course: " + course_key)
        export_course(driver, course_key)

# Close the WebDriver and browser after processing all courses
    driver.quit()
    print("WebDriver and browser closed.")
    logging.info("WebDriver and browser closed.")

if __name__ == "__main__":
    main()
