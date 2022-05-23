from bs4 import BeautifulSoup
import requests
#import html5lib


response = requests.get("https://news.ycombinator.com/")
yc_web_page = response.text
soup = BeautifulSoup(yc_web_page, "html.parser")
#print(soup.prettify())

#print(soup.title.text)


article_text = []
article_links = []
articles = soup.find_all(name="a", class_="titlelink")
for article_tag in articles:
    article_text.append(article_tag.get_text())
    article_links.append(article_tag.get("href"))


article_upvotes = [score.get_text() for score in soup.find_all(name="span", class_="score")]
print(article_text)
print(article_links)
print(article_upvotes)

article_upvotes =[int(score.split()[0]) for score in article_upvotes]

largest_number = max(article_upvotes)
largest_index = article_upvotes.index(largest_number)
print(article_upvotes[largest_index])
print(article_text[largest_index])
print(article_links[largest_index])


































# #import lxml
#
#
# with open("website.html", encoding="utf8") as file:
#     contents = file.read()
#
# soup = BeautifulSoup(contents, "html.parser")
# # print(soup.title)
# # print(soup.title.name)
# # print(soup.title.text)
# # print(soup.title.string)
#
# # print(soup.prettify())
#
# # anchors = soup.find_all("a")
# # for link in anchors:
# #     print(link.text)
# #     print(link.get('href'))
# #     print(link)
#
# # heading = soup.find(name="h1", id="name")
# # print(heading)
# #
# # section_heading = soup.find(name="h3", class_="heading")
# # print(section_heading)
#
# # company_url = soup.select_one(selector="p a")
# # print(company_url)
#
# # heading = soup.find(name="h1", id="name")
# # name = heading.get_text()
# # print(name)
# #
# # name = soup.select_one("#name")
# # print(name)
# #
# # headings = soup.select(".heading")
# # print(headings)
#
# # print(soup.findAll("a"))
#
# class_name = soup.select_one("h3")
# print(class_name.get("class"))
