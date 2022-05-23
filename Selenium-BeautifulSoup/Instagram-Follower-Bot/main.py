from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import ElementClickInterceptedException
import time

INSTAGRAM_EMAIL = "Enter Email"
INSTAGRAM_PASSWORD = "Enter Password"
CHROME_DRIVER_PATH = "C:\development\chromedriver.exe"

class InstaFollower:

    def __init__(self, driver_path):
        self.service = Service(executable_path=driver_path)
        self.options = webdriver.ChromeOptions()
        self.driver = webdriver.Chrome(service=self.service, options=self.options)


    def login(self):
        self.driver.get("https://www.instagram.com/accounts/login/")

        time.sleep(5)

        email = self.driver.find_element(by=By.XPATH, value='//*[@id="loginForm"]/div/div[1]/div/label/input')
        email.send_keys(INSTAGRAM_EMAIL)

        password = self.driver.find_element(by=By.XPATH, value='//*[@id="loginForm"]/div/div[2]/div/label/input')
        password.send_keys(INSTAGRAM_PASSWORD)
        password.send_keys(Keys.ENTER)

    def find_followers(self):
        time.sleep(5)
        self.driver.get("https://www.instagram.com/chefsteps/")
        time.sleep(5)
        followers = self.driver.find_element(by=By.XPATH, value='//*[@id="react-root"]/section/main/div/header/section/ul/li[2]/a/div')
        followers.click()
        time.sleep(5)

        modal = self.driver.find_element(by=By.XPATH, value='/html/body/div[6]/div/div/div/div[2]')
        for i in range(10):
            self.driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", modal)
            time.sleep(2)




    def follow(self):
        followers_list = self.driver.find_elements(by=By.CSS_SELECTOR, value="li button")

        for follower_button in followers_list:
            if follower_button.text != 'Follow':
                pass
            else:
                follower_button.click()
                time.sleep(2)



insta_bot = InstaFollower(CHROME_DRIVER_PATH)
insta_bot.login()
insta_bot.find_followers()
insta_bot.follow()

