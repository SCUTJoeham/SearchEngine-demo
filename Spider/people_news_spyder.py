# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import json

base_url = "http://en.people.cn"
json_data = []
count = 0

def get_section_url():
    section_id_list = ["90780", "90785", "90777", "business", "90882", "90782", "202936", "90779",
                       "98649", "205040", "90786", "207872", "102775"]
    base_url_list = []
    for section_id in section_id_list:
        base_url_list.append(base_url + "/" + section_id)
    return base_url_list


def news_link_spyder(url):
    web_content = requests.get(url).content.decode("utf-8", 'ignore')
    soup = BeautifulSoup(web_content)
    data = soup.find("ul", {"class": "foreign_list8 cf"})
    for a in data.select('a'):
        try:
            news_url = base_url + a['href']
            news_content_spyder(news_url)
        except Exception as e:
            print("ERROR", e)


def news_content_spyder(url):
    web_content = requests.get(url).content.decode("utf-8", 'ignore')
    soup = BeautifulSoup(web_content)
    title = soup.find("h1").get_text()
    paragraph_list = soup.find("div", {"class": "w860 d2txtCon cf"}).findAll('p')
    main_body = ""
    for p in paragraph_list:
        main_body = main_body + p.get_text().strip()

    data = {}
    data['url'] = url
    data['title'] = title
    data['main_body'] = main_body
    global json_data
    json_data.append(data)
    global count
    count = count + 1
    print(count, url, title)


if __name__ == '__main__':
    section_url_list = get_section_url()
    for section_url in section_url_list:
        try:
            for i in range(1, 76):
                url = section_url + "/index" + str(i) + '.html'
                news_link_spyder(url)
        except Exception as e:
            print("ERROR", e)

    text = ""
    for item in json_data:
        text = text + json.dumps(item) + "\n"
    with open('data.txt', 'w') as f:
        f.write(text)
