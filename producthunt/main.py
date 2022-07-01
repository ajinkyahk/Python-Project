from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from time import sleep
from bs4 import BeautifulSoup
import pandas as pd


BASE_URL = "https://www.producthunt.com"
chrome_driver_path = "C:\development\chromedriver.exe"

service = Service(executable_path=chrome_driver_path)
options = webdriver.ChromeOptions()
driver = webdriver.Chrome(service=service, options=options)

driver.maximize_window()
sleep(5)

driver.get("https://www.producthunt.com/topics")
sleep(20)
last_height = driver.execute_script("return document.body.scrollHeight")

while True:
    # Scroll down to bottom
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    # Wait to load page
    sleep(5)

    # Calculate new scroll height and compare with last scroll height
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        # If heights are the same it will exit the function
        break
    last_height = new_height

soup=BeautifulSoup(driver.page_source, 'html.parser')
topic_div = soup.find_all('div', class_='style_flex___KlcI style_direction-column__w77hU style_flex-1__YfiEx style_mx-4__xyb5_')
topics = [topic.find('h3').get_text().strip() for topic in topic_div]
print(topics)
print(len(topics))
topics_links = [f"{BASE_URL}{topic.find('a').get('href')}" for topic in topic_div]
print(topics_links)
print(len(topics_links))
topic_description = [topic.find('div').get_text().strip() for topic in topic_div]
print(topic_description)
print(len(topic_description))

data = pd.DataFrame({
    'Topics': topics,
    'Topics Link':topics_links,
})

data['Topics Description'] = pd.Series(topic_description)

data = data[['Topics', 'Topics Description', 'Topics Link']]
print(data)
data.to_csv('product-hunt-topics2.csv', index=False)

driver.close()

