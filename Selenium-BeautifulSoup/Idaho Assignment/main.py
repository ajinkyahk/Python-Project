import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from time import sleep
from bs4 import BeautifulSoup
from lxml import etree
import csv

options = uc.ChromeOptions()

# just some options passing in to skip annoying popups
options.add_argument('--no-first-run --no-service-autorun --password-store=basic')
options.add_argument('--user-data-dir=C://Users/AKON/AppData/Local/Google/Chrome/User Data/Profile 1')
driver = uc.Chrome(options=options, use_subprocess=True, version_main=111, driver_executable_path='C://development/chromedriver.exe')

URL = "https://qcpi.questcdn.com/cdn/posting/?group=1950787&provider=1950787"
BID = []
driver.maximize_window()
sleep(10)
# request to URL
driver.get(URL)
sleep(10)


def get_data():
    # get html page
    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")
    dom = etree.HTML(str(soup))

    # get quest no, est value, description, closing date

    quest_no = dom.xpath("//b[contains(text(), 'Quest Number:')]/text()")[0]
    # quest_no = int(''.join(filter(str.isdigit, quest_no)))
    quest_no = quest_no.split(':')[1].strip()


    est_val_notes = dom.xpath("//td[contains(text(), 'Est. Value Notes:')]//following-sibling::td/text()")[0]

    desc = dom.xpath("//td[contains(text(), 'Description:')]//following-sibling::td/text()")[0]

    close_date = dom.xpath("//td[contains(text(), 'Closing Date:')]//following-sibling::td/text()")[0]

    tup = (quest_no, est_val_notes, desc, close_date)

    print(tup)

    # write to file
    with open('bid.csv', 'a', newline='') as file:
        csv_writer = csv.writer(file)
        csv_writer.writerow(tup)

try:
    # find the first quest no and click
    quest_first = driver.find_element(by=By.XPATH, value="//a[contains(@onclick, 'prevnext')][1]")
    quest_first.click()
    sleep(10)

except NoSuchElementException:
    pass

else:
    # iterate through pages
    while True:
        # call function to get required fields and write to file
        get_data()

        # find next button and click until disabled
        next_btn = driver.find_element(by=By.XPATH, value="//button[contains(@id, 'id_prevnext_next')]")
        # print(next_btn.get_attribute('onclick'))

        if'prevnext()' not in str(next_btn.get_attribute('onclick')):
            sleep(5)
            next_btn.click()
            sleep(5)
            continue
        else:
            break

# close driver
driver.close()

