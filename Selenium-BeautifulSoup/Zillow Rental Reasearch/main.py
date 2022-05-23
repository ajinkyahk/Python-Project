import time
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service

CHROME_DRIVER_PATH = "C:\development\chromedriver.exe"



URL = "https://www.zillow.com/homes/for_rent/1-_beds/?searchQueryState=%7B%22pagination%22%3A%7B%7D%2C%22usersSearchTerm%22%3Anull%2C%22mapBounds%22%3A%7B%22west%22%3A-122.56276167822266%2C%22east%22%3A-122.30389632177734%2C%22south%22%3A37.69261345230467%2C%22north%22%3A37.857877098316834%7D%2C%22isMapVisible%22%3Atrue%2C%22filterState%22%3A%7B%22fr%22%3A%7B%22value%22%3Atrue%7D%2C%22fsba%22%3A%7B%22value%22%3Afalse%7D%2C%22fsbo%22%3A%7B%22value%22%3Afalse%7D%2C%22nc%22%3A%7B%22value%22%3Afalse%7D%2C%22cmsn%22%3A%7B%22value%22%3Afalse%7D%2C%22auc%22%3A%7B%22value%22%3Afalse%7D%2C%22fore%22%3A%7B%22value%22%3Afalse%7D%2C%22pmf%22%3A%7B%22value%22%3Afalse%7D%2C%22pf%22%3A%7B%22value%22%3Afalse%7D%2C%22mp%22%3A%7B%22max%22%3A3000%7D%2C%22price%22%3A%7B%22max%22%3A872627%7D%2C%22beds%22%3A%7B%22min%22%3A1%7D%7D%2C%22isListVisible%22%3Atrue%2C%22mapZoom%22%3A12%7D"
Headers = {
    'Accept-Language':"en-US,en;q=0.9",
    'User-Agent':"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.88 Safari/537.36"
}

response = requests.get(url=URL, headers=Headers)
zillio_web_page = response.text

soup = BeautifulSoup(zillio_web_page, "html.parser")

link_results = [link.get("href") for link in soup.select(selector=".list-card-info a" , class_="list-card-link")]
print(len(link_results))

address_results = [address.get_text() for address in soup.select(selector=".list-card-info address", class_="list-card-addr")]
print(len(address_results))

price_results = [price.get_text().strip("/mo").replace(',','').strip('+') for price in soup.select(selector=".list-card-heading div", class_="list-card-price")]
print(len(price_results))


class RentalProperty:
    def __init__(self, driver_path):
        self.servise = Service(executable_path=driver_path)
        self.options = webdriver.ChromeOptions()
        self.driver = webdriver.Chrome(service=self.servise, options=self.options)

    def submit_form(self):

        for i in range(len(link_results)):
            self.driver.get(
                "https://docs.google.com/forms/d/e/1FAIpQLScdU1dPU0HAdNzvXF_wKLu2t5unVjBX2lXMrdPyfMegRj-M-A/viewform?usp=sf_link")
            time.sleep(5)
            address_input = self.driver.find_element(by=By.XPATH,
                                                value='//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input')
            price_input = self.driver.find_element(by=By.XPATH,
                                              value='//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input')
            link_input = self.driver.find_element(by=By.XPATH,
                                             value='//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input')
            address_input.send_keys(address_results[i])
            price_input.send_keys(price_results[i])
            link_input.send_keys(link_results[i])
            submit = self.driver.find_element(by=By.XPATH,
                                         value='//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div[1]/div/span/span')
            submit.click()


bot = RentalProperty(CHROME_DRIVER_PATH)
bot.submit_form()

