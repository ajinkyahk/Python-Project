from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
import time

facebook_email = "ENTER YOUR EMAIL ADDDRESS HERE"
facebook_password = "ENTER YOUR PASSWORD HERE"

chrome_driver_path = "C:\development\chromedriver.exe"

service = Service(executable_path=chrome_driver_path)

options = webdriver.ChromeOptions()

driver = webdriver.Chrome(service=service, options=options)

driver.get("https://tinder.com/")

time.sleep(5)
login = driver.find_element(by=By.CSS_SELECTOR, value="a.button")
login.click()

time.sleep(5)
facebook_login = driver.find_element(by=By.XPATH, value='//*[@id="u672211310"]/div/div/div[1]/div/div/div[3]/span/div[2]/button')
facebook_login.click()

base_window = driver.window_handles[0]
fb_login_window = driver.window_handles[1]
driver.switch_to.window(fb_login_window)
print(driver.title)

time.sleep(5)
email = driver.find_element(by=By.ID, value="email")
email.send_keys(f"{facebook_email}")

password = driver.find_element(by=By.ID, value="pass")
password.send_keys(f"{facebook_password}")

click_login = driver.find_element(by=By.ID, value='loginbutton')
click_login.click()

driver.switch_to.window(base_window)
print(driver.title)

time.sleep(10)
location = driver.find_element(by=By.XPATH, value='//*[@id="u672211310"]/div/div/div/div/div[3]/button[1]')
location.click()

time.sleep(5)
notification = driver.find_element(by=By.XPATH, value='//*[@id="u672211310"]/div/div/div/div/div[3]/button[2]')
notification.click()

time.sleep(2)
privacy = driver.find_element(by=By.XPATH, value='/html/body/div[1]/div/div[2]/div/div/div[1]/div[1]/button')
privacy.click()

for n in range(100):
    time.sleep(10)

    try:
        print("called")
        like_button = driver.find_element(by=By.XPATH, value='//*[@id="u-1894374910"]/div/div[1]/div/main/div[1]/div/div/div[1]/div[1]/div/div[4]/div/div[4]/button/span/span')
        like_button.click()
        print("liked")
    except NoSuchElementException:
        print("other like")
        like_button = driver.find_element(by=By.XPATH, value='//*[@id="u-1894374910"]/div/div[1]/div/main/div[1]/div/div/div[1]/div[1]/div/div[5]/div/div[4]/button/span/span')
        like_button.click()

    except ElementClickInterceptedException:
        try:
            match_popup = driver.find_element(by=By.CSS_SELECTOR, value=".itsAMatch a")
            match_popup.click()

        except NoSuchElementException:
            time.sleep(5)

driver.quit()
