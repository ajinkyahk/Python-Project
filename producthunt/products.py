from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from time import sleep
from bs4 import BeautifulSoup
import pandas as pd


data = pd.read_csv('product-hunt-topics2.csv')
link_data = data['Topics Link'].tolist()
print(link_data)

BASE_URL = "https://www.producthunt.com"

PRODUCT_NAME = []
PRODUCT_LINK = []
PRODUCT_DESCRIPTION = []
PRODUCT_COMMENT = []
PRODUCT_REVIEW = []
PRODUCT_UP_VOTES = []

chrome_driver_path = "C:\development\chromedriver.exe"

service = Service(executable_path=chrome_driver_path)
options = webdriver.ChromeOptions()
driver = webdriver.Chrome(service=service, options=options)


driver.maximize_window()
sleep(5)

driver.get(url=link_data[1])
sleep(20)
last_height = driver.execute_script("return document.body.scrollHeight")

while True:
    # Scroll down to bottom
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    # Wait to load page
    sleep(2)

    # Calculate new scroll height and compare with last scroll height
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        # If heights are the same it will exit the function
        break
    last_height = new_height



soup=BeautifulSoup(driver.page_source, 'html.parser')

try:
    product_category = soup.find('h1').get_text().strip()
    print(product_category)
except AttributeError:
    pass

main = soup.find('main')

li_tags = main.find_all('li')
for li_tag in li_tags:

    try:
        product_name = li_tag.find('a', class_='styles_title__jWi91')
        PRODUCT_NAME.append(product_name.text)
    except AttributeError:
        PRODUCT_NAME.append(None
                        )
    try:
        product_link = f"{BASE_URL}{li_tag.find('a', class_='styles_title__jWi91').get('href')}"
        PRODUCT_LINK.append(product_link)
    except AttributeError:
        PRODUCT_LINK.append(None)

    try:
        product_description = li_tag.find('a', class_='styles_tagline__j29pO')
        PRODUCT_DESCRIPTION.append(product_description.text.strip())
    except AttributeError:
        PRODUCT_DESCRIPTION.append(None)

    try:
        product_comments = li_tag.find('a', class_='styles_reset__opz7w styles_button__Pe4nq')
        PRODUCT_COMMENT.append(product_comments.text)
    except AttributeError:
        PRODUCT_COMMENT.append(None)

    try:
        product_reviews = li_tag.find('a', class_='styles_reviews__yVB1B')
        PRODUCT_REVIEW.append(product_reviews.text.split()[0])
    except AttributeError:
        PRODUCT_REVIEW.append(None)

    try:
        up_votes = li_tag.find('button',{'data-test':'vote-button'})
        PRODUCT_UP_VOTES.append(up_votes.text)
    except AttributeError:
        PRODUCT_UP_VOTES.append(None)


driver.close()
# print(PRODUCT_NAME)
# print(PRODUCT_LINK)
# print(PRODUCT_DESCRIPTION)
# print(PRODUCT_COMMENT)
# print(PRODUCT_REVIEW)
# print(PRODUCT_UP_VOTES)
# print(len(PRODUCT_NAME), len(PRODUCT_LINK), len(PRODUCT_DESCRIPTION), len(PRODUCT_COMMENT), len(PRODUCT_REVIEW), len(PRODUCT_UP_VOTES))

pro_data = pd.DataFrame({
    'Product Category':product_category,
    'Product Name':PRODUCT_NAME,
    'Product Link':PRODUCT_LINK,
    'Product_Description':PRODUCT_DESCRIPTION,
    'Product Comment':PRODUCT_COMMENT,
    'Product Review':PRODUCT_REVIEW,
    'Product Upvotes':PRODUCT_UP_VOTES,
})
pro_data.to_csv('tech-hunt.csv', index=False)

