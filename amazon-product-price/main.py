import requests
from bs4 import BeautifulSoup
import smtplib

URL = "https://www.amazon.com/SAMSUNG-Smartphone-Unlocked-Brightest-Processor/dp/B09MW19JW2/ref=sr_1_2?keywords=samsung%2Bgalaxy%2Bs22%2Bultra&qid=1649855719&sprefix=samsung%2Bgalaxy%2Bs%2Caps%2C277&sr=8-2&th=1"

Headers = {
    'Accept-Language':"en-US,en;q=0.9",
    'User-Agent':"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.88 Safari/537.36"
}

response = requests.get(url=URL, headers=Headers)
amazon_web_page = response.text

soup = BeautifulSoup(amazon_web_page, "html.parser")
price = soup.find(name="span", class_="a-offscreen").get_text()
product_price = price.split("$")[1]
product_price =product_price.split(",")
product_price = "".join(product_price)
price_as_float = float(product_price)

BUY_PRICE = 1300

title = soup.find(id="productTitle")
title = title.get_text().strip()

if price_as_float < BUY_PRICE:
    message = f"{title} is now {price}"

    with smtplib.SMTP(host="smtp.gmail.com", port=587) as connection:
        connection.starttls()
        connection.login(user="YOUR EMAIL TO LOGIN", password="YOUR EMAIL LOGIN PASSWORD")
        connection.sendmail(
            from_addr="EMAIL FROM",
            to_addrs="EMAIL TO",
            msg= f"Subject: Amazon Price Alert! \n\n{message}\n {URL}"
        )



