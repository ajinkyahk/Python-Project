from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import time

email = "YOUR EMAIL"
password = "YOUR EMAIL PASSWORD"
chrome_driver_path = "C:\development\chromedriver.exe"




service = Service(executable_path=chrome_driver_path)

options = webdriver.ChromeOptions()

driver = webdriver.Chrome(service=service, options=options)

driver.get("https://www.linkedin.com/jobs/search/?f_AL=true&geoId=102257491&keywords=python%20developer&location=London%2C%20England%2C%20United%20Kingdom")

# signin = driver.find_element(by=By.CSS_SELECTOR, value="a.nav__button-secondary")
# signin.click()

time.sleep(2)
signin = driver.find_element(by=By.LINK_TEXT, value="Sign in")
signin.click()

time.sleep(5)

username = driver.find_element(by=By.ID, value="username")
username.send_keys(f"{email}")

linkedin_password = driver.find_element(by=By.ID, value="password")
linkedin_password.send_keys(f"{password}")

submit = driver.find_element(by=By.CSS_SELECTOR, value="button.btn__primary--large")
submit.click()

job_list = driver.find_elements(by=By.CSS_SELECTOR, value=".job-card-container--clickable")

# second_job = job_list[1]
# second_job.click()
for job in job_list:
    print("called")
    job.click()
    time.sleep(2)

    try:
        easy_apply = driver.find_element(by=By.CSS_SELECTOR, value="button.jobs-apply-button")
        easy_apply.click()
        time.sleep(5)
        phone_input = driver.find_element(by=By.CLASS_NAME, value="ember-text-field")
        if phone_input.text=="":
            print("phone number entered")
            phone_input.send_keys("1234")

        submit_application = driver.find_element(by=By.CSS_SELECTOR, value="footer button")
        print("not inside if")
        label = submit_application.get_attribute("aria-label")
        print(label)
        if label  == "Continue to next step":
            print("inside if")
            close_button = driver.find_element(by=By.CLASS_NAME, value="artdeco-modal__dismiss")
            print("close button clicked")
            close_button.click()

            time.sleep(2)
            discard_button = driver.find_element(by=By.CSS_SELECTOR, value="button.artdeco-modal__confirm-dialog-btn")
            discard_button.click()
            print("complex application skipped")
            continue
        else:
            submit_application.click()

        time.sleep(2)
        close_button = driver.find_element(by=By.CLASS_NAME, value="artdeco-modal__dismiss")
        print("click close button")
        close_button.click()
    except NoSuchElementException:
        print("No application button, skipped")
        continue

time.sleep(5)
driver.quit()


