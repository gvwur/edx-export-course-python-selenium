import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time

driver = webdriver.Firefox()
courseKey = "WageningenX+AB101x+1T2024"

# Open the Login page of edX
driver.get("https://authn.edx.org/login")
print("Waiting 10 seconds for the login page to load properly..")
time.sleep(10)

# Enter the username
username_field = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.NAME, "emailOrUsername"))
)
username_field.send_keys("your_email@example.com")
print("Sending username")

# Enter the password
password_field = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.NAME, "example_password"))
)
password_field.send_keys("example")
print("Sending pw")

# Click the "sign-in" button
sign_in_button = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.NAME, "sign-in"))
)
sign_in_button.click()
print("Clicked sign in..")

# Wait
print("Login done.. Wait 10 sec to open course..")
time.sleep(5)

# Open the course
driver.get("https://studio.edx.org/course/course-v1:"+courseKey)

# Wait
print("Wait 5 sec to open to open export page..")
time.sleep(5)

# Open the course export
driver.get("https://course-authoring.edx.org/course/course-v1:"+courseKey+"/export")

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
    filename = f"{courseKey}.tar.gz"
    response = requests.get(download_url, stream=True)
    
    with open(filename, 'wb') as file:
        for chunk in response.iter_content(chunk_size=8192):
            file.write(chunk)
    
    print(f"Downloaded the file as: {filename}")

finally:
    # Wait for 1 minute to allow the export to complete
    print("Wait 30 sec before closing browser")
    time.sleep(30)

    # Optionally, close the browser after completion
    driver.quit()
