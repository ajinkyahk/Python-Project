import requests
from bs4 import BeautifulSoup
from time import sleep
import pandas as pd

URL = "https://www.amazon.in/s?k=bags&page="
PRODUCT_URL='https://www.amazon.in/'
Headers = {
    'Accept-Language':"en-US,en;q=0.9",
    'User-Agent':"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.88 Safari/537.36"
}
PRO_LIST = []
i=0
while i<20:
    print(f"Page No {i}")
    response = requests.get(url=f"{URL}{i}", headers=Headers)
    amazon_web_page = response.text

    soup = BeautifulSoup(amazon_web_page, "html.parser")


    links = soup.find_all('div', {'class': 's-result-item', 'data-component-type': 's-search-result'})

    print(len(links))
    for link in links:
        try:
            asin = link.get('data-asin')
            url=f"{PRODUCT_URL}{link.a.get('href')}"
            name=link.h2.text
            price=link.find('span', {'class': 'a-offscreen'}).get_text().replace(',','').strip('₹')
            rating=link.find('i', {'class':'a-icon'}).get_text().split(' ')[0]
            no_of_reviews=link.find('span', {'class':'a-size-base'}).get_text().replace(',','')
            PRO_LIST.append([url, name, price, rating, no_of_reviews, asin])
        except AttributeError:
            continue
    i+=1
    sleep(1.5)


for index,link in enumerate(PRO_LIST):
    response_page = requests.get(url=link[0], headers=Headers)
    product_page = response_page.text
    soup2 = BeautifulSoup(product_page, "html.parser")
    try:
        dec_list = soup2.find('div', {'id': 'featurebullets_feature_div'})
        pro_description = soup2.find('div', {'id':'productDescription'}).get_text().strip()

        description = [desc.get_text().strip() for desc in dec_list.find_all('li')]
        description = ''.join(description)

        pro_list = soup2.find('div', {'id': 'detailBulletsWrapper_feature_div'})
        details = pro_list.find_all('li')
        for detail in details:
            if 'Manufacturer' in detail.text and "Discontinued" not in detail.text:
                manufacturer = detail.text.split(':')[-1].split()[1:]
                manufacturer = ' '.join(manufacturer)
                break

        PRO_LIST[index].append(link.extend([description,manufacturer,pro_description]))
    except AttributeError:
        continue
    sleep(1.5)
    PRO_LIST[index]=PRO_LIST[index][:-1]
    print(PRO_LIST[index])


df = pd.DataFrame(PRO_LIST, columns=["product url", "product name", "product price", "rating", "number of reviews", "asin", "description", "manufacturer", "product description"])
df.to_csv('amazon.csv', index=False)





