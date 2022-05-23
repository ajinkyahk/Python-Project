from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

chrome_driver_path = "C:\development\chromedriver.exe"

service = Service(executable_path=chrome_driver_path)
options = webdriver.ChromeOptions()
driver = webdriver.Chrome(service=service, options=options)

# driver.get("https://www.amazon.in/Kuvings-Multipot-Programmable-Stainless-Litres/dp/B09D8G42SB/ref=sr_1_1_sspa?crid=21LJ8CILV35N8&keywords=Instant%2BPot%2BDuo&qid=1650965548&s=kitchen&smid=A23NDS7BYKY0XY&sprefix=instant%2Bpot%2Bduo%2Ckitchen%2C261&sr=1-1-spons&spLa=ZW5jcnlwdGVkUXVhbGlmaWVyPUEyVkU0RkszODJDUDk3JmVuY3J5cHRlZElkPUExMDIzMjAxMUlSTzZHSVVBWE0xRiZlbmNyeXB0ZWRBZElkPUEwMDQ4ODc0M1NLTTlGVFg5TU45OSZ3aWRnZXROYW1lPXNwX2F0ZiZhY3Rpb249Y2xpY2tSZWRpcmVjdCZkb05vdExvZ0NsaWNrPXRydWU&th=1")
# price = driver.find_element(By.CLASS_NAME, "a-price")
# print(price.text)

driver.get("https://www.python.org/")

# search_bar  = driver.find_element(by=By.NAME, value="q")
# print(search_bar.tag_name)

# pythonlogo = driver.find_element(by=By.CLASS_NAME, value="python-logo")
# print(pythonlogo.size)

# link = driver.find_element(by=By.CSS_SELECTOR ,value=".documentation-widget a")
# print(link.text)

# bug_link = driver.find_element(by=By.XPATH, value='//*[@id="site-map"]/div[2]/div/ul/li[1]/a')
# print(bug_link.text)

event_dates = driver.find_elements(by=By.CSS_SELECTOR, value=".event-widget time")
# dates = [event.text for event in event_dates]
# print(dates)

event_names = driver.find_elements(by=By.CSS_SELECTOR, value=".event-widget li a")
# events = [event.text for event in event_names]
# print(events)

event_dict = dict(enumerate({"date": date.text, "name": name.text} for date, name in zip(event_dates, event_names)))
# event_dict = dict(enumerate(event_dict))

print(event_dict)



#driver.close()
driver.quit()