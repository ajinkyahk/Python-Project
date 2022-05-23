from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

chrome_driver_path = "C:\development\chromedriver.exe"

service = Service(executable_path=chrome_driver_path)
options = webdriver.ChromeOptions()
driver = webdriver.Chrome(service=service, options=options)

# driver.get("https://en.wikipedia.org/wiki/Main_Page")

# article_number = driver.find_element(by=By.ID, value="articlecount")
# article_number = driver.find_element(by=By.CSS_SELECTOR, value="#articlecount a")
#article_number = int(article_number.text.replace(",", ""))
# print(article_number)
# article_number.click()
# title = article_number.get_attribute("title")
# print(title)

# content_portal = driver.find_element(by=By.LINK_TEXT, value="Content portals")
# content_portal.click()

# search = driver.find_element(by=By.NAME, value="search")
# search.send_keys("Python")
# # search.submit()
# search.send_keys(Keys.ENTER)

# driver.get("http://secure-retreat-92358.herokuapp.com/")
# first_name = driver.find_element(by=By.NAME, value="fName")
# first_name.send_keys("Akon")
#
# last_name = driver.find_element(by=By.NAME, value="lName")
# last_name.send_keys("Stark")
#
# email = driver.find_element(by=By.NAME, value="email")
# email.send_keys("akonstark@gmail.com")

# sign_up = driver.find_element(by=By.CLASS_NAME, value="btn")
# sign_up.click()

# submit = driver.find_element(by=By.CSS_SELECTOR, value="form button")
# submit.click()

driver.get("https://www.google.co.in")

search = driver.find_element(by=By.NAME, value="q")
search.send_keys("images")
search.send_keys(Keys.ENTER)



# driver.quit()