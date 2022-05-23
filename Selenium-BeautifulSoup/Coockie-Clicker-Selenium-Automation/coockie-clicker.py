from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

chrome_driver_path = "C:\development\chromedriver.exe"

service = Service(executable_path=chrome_driver_path)
options = webdriver.ChromeOptions()
driver = webdriver.Chrome(service=service, options=options)

driver.get("http://orteil.dashnet.org/experiments/cookie/")

# get cookie to click on
cookie = driver.find_element(by=By.ID, value="cookie")

# Get upgrade item IDs
items = driver.find_elements(by=By.CSS_SELECTOR, value="#store div")
item_ids = [item.get_attribute("id") for item in items]
print(item_ids)

timeout = time.time() + 5
five_min = time.time() + 60 * 5  # 5 mintes

while True:
    cookie.click()

    # Every 5 seconds
    if time.time() > timeout:
        all_prices = driver.find_elements(by=By.CSS_SELECTOR, value="#store b")
        item_prices = []

        # convert <b> text into an integer price
        for price in all_prices:
            element_text = price.text
            if element_text != "":
                cost = int(element_text.split("-")[1].strip().replace(",", ""))
                item_prices.append(cost)

        # create dictionary of store items and prices
        cookie_upgrades = {}
        for n in range(len(item_prices)):
            cookie_upgrades[item_prices[n]] = item_ids[n]
        print(cookie_upgrades)

        # get current cookie count
        money_element = driver.find_element(by=By.ID, value="money").text
        if "," in money_element:
            money_element = money_element.replace(",", "")
        cookie_count = int(money_element)

        # find upgrades that we can currently afford
        affordable_upgrade = {}
        for cost, id in cookie_upgrades.items():
            if cookie_count > cost:
                affordable_upgrade[cost] = id
        print(affordable_upgrade)

        # purchase the most expensive affordable upgrade
        highest_price_affordable_upgrade = max(affordable_upgrade)
        print(highest_price_affordable_upgrade)
        to_purchase_id = affordable_upgrade[highest_price_affordable_upgrade]

        driver.find_element(by=By.ID, value=f"{to_purchase_id}").click()

        # add another timeout until the next check
        timeout = time.time() + 5

        # after 5 minutes stop the bot and check the cookie per second count
        if time.time() > five_min:
            cookie_per_sec = driver.find_element(by=By.ID, value="cps").text
            print(cookie_per_sec)
            break
