import requests
import json
import time
import re
import lxml
from bs4 import BeautifulSoup
from collections import OrderedDict


class NewsBase:

    links_url = OrderedDict([])


def new_docs(n):

    response = requests.get('https://interfax.ru')
    response.encoding = 'cp1251'

    soup = BeautifulSoup(response.text, 'lxml')
    soup.prettify()

    headers_list = []
    titles = soup.find_all('div', class_="timeline__group")
    for headers in titles:
        headers_list.append(headers.text)
    cnt = int(0)
    for h in headers_list:
        print(h)
        if cnt < n - 1:
            cnt = cnt + 1
        else:
            break


def new_topics(n):
    response = requests.get('https://interfax.ru/story')
    response.encoding = 'cp1251'

    soup = BeautifulSoup(response.text, 'lxml')
    soup.prettify()

    headers_list = []

    titles = soup.find_all('div', class_="title")
    for headers in titles:
        headers_list.append(headers.text)
    cnt = int(0)
    for h in headers_list:
        print(h)
        if cnt < n - 1:
            cnt = cnt + 1
        else:
            break
