from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

CHROME_DRIVER_PATH = "C:\development\chromedriver.exe"
PROMISED_DOWN = 200
PROMISED_UP = 200
TWITTER_EMAIL = " Enter Email Address"
TWITTER_PASS = "Enter Password"

class InternetSpeedTwitterBot:
    def __init__(self, driver_path):
        self.service = Service(executable_path=driver_path)
        self.options = webdriver.ChromeOptions()
        self.driver = webdriver.Chrome(service=self.service, options=self.options)
        self.down = 0
        self.up = 0


    def get_internet_speed(self):
        self.driver.get("https://www.speedtest.net/")
        go_button = self.driver.find_element(by=By.XPATH, value='//*[@id="container"]/div/div[3]/div/div/div/div[2]/div[3]/div[1]/a/span[4]')
        go_button.click()

        while True:
            time.sleep(10)

            try:
                down_speed = self.driver.find_element(by=By.CLASS_NAME, value="download-speed")
                up_speed = self.driver.find_element(by=By.CLASS_NAME, value="upload-speed")
                self.down = down_speed.text.strip()
                self.up = up_speed.text.strip()

                if self.down != "" and self.up != "":
                    self.down = int(float(self.down))
                    self.up = int(float(self.up))


                    if self.down > 0 and self.up > 0:
                        break

            except NoSuchElementException:
                time.sleep(20)
                continue

        print(self.down, self.up)




    def tweet_at_provider(self):
        print(self.down, self.up)
        self.driver.get("https://twitter.com/i/flow/login")
        time.sleep(10)
        email = self.driver.find_element(by=By.XPATH, value='//*[@id="layers"]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[1]/div/div/div[5]/label/div/div[2]/div/input')
        email.send_keys(TWITTER_EMAIL)
        email.send_keys(Keys.ENTER)
        time.sleep(5)
        password = self.driver.find_element(by=By.XPATH, value='//*[@id="layers"]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[1]/div/div/div[3]/div/label/div/div[2]/div[1]/input')
        password.send_keys(TWITTER_PASS)
        password.send_keys(Keys.ENTER)

        time.sleep(10)
        tweet_input = self.driver.find_element(by=By.XPATH, value='//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div[1]/div/div[2]/div/div[2]/div[1]/div/div/div/div[2]/div[1]/div/div/div/div/div/div/div/div/div/label/div[1]/div/div/div/div/div[2]/div/div/div/div')
        tweet_input.send_keys(f"Internet Speed is down:{self.down}/ up:{self.up} "
                              f" but promised speed is down:{PROMISED_DOWN}/ up: {PROMISED_UP} ")
        tweet = self.driver.find_element(by=By.XPATH, value='//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div[1]/div/div[2]/div/div[2]/div[1]/div/div/div/div[2]/div[3]/div/div/div[2]/div/div/span/span')
        tweet.click()


bot = InternetSpeedTwitterBot(CHROME_DRIVER_PATH)
bot.get_internet_speed()
bot.tweet_at_provider()
