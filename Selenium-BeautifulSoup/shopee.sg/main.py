from pprint import pprint
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from time import sleep
from bs4 import BeautifulSoup
import pandas as pd

options = uc.ChromeOptions()

# just some options passing in to skip annoying popups
options.add_argument('--no-first-run --no-service-autorun --password-store=basic')
options.add_argument('--user-data-dir=C://Users/AKON/AppData/Local/Google/Chrome/User Data/Profile 1')
driver = uc.Chrome(options=options, use_subprocess=True, version_main=111, driver_executable_path='C://development/chromedriver.exe')

Tags = []

data = pd.read_csv('E-commerce URL - input.csv', names=['links'], sep=',')
link_data = [f'{link.strip()}' for link in data['links']]
# print(link_data)

for link in link_data[100:]:
    driver.maximize_window()
    sleep(10)
    driver.get(link)
    sleep(10)

    try:
        arrow = driver.find_element(by=By.CLASS_NAME, value='icon-arrow-down')
        arrow.click()
    except NoSuchElementException:
        Tags.append(None)
        pass
    else:
        html = driver.page_source
        soup = BeautifulSoup(html, "html.parser")
        try:
            pop_div = soup.find_all('div', class_='_2TdGmR')
            # pprint(pop_div)
        except AttributeError:
            Tags.append(None)
        else:
            try:
                tags = [div.find('div', class_="AAaUS1") for div in pop_div]
                tags_text = [tag.get_text().strip() for tag in tags]
                tags_text = ', '.join(tags_text)
                # print(tags_text)
                Tags.append(tags_text)

            except AttributeError:
                Tags.append(None)
    print(Tags)
data = pd.DataFrame({
    "delivery": Tags
})
# print(data['delivery'])
data.to_csv('delivery.csv', mode='a', index=False, header=False)

driver.close()
