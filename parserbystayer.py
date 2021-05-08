"""
    Collects html markers from website
"""
import requests
from bs4 import BeautifulSoup


class NewsBase:
    """
        Contains scenes and documents downloaded from the website
    """

    docs_list = []
    topics_list = []
    docs_url_list = []
    topics_url_list = []
    selected_topics_list = []

    def __init__(self) -> None:
        """
            Initializing the class
        """
        self.update_docs('https://interfax.ru')
        self.update_topics('https://interfax.ru/story')

    def update_docs(self, url: str) -> None:
        """
            Gets recent uses from the website

        :param url:
        :return:
        """
        response = requests.get(url)
        response.encoding = 'cp1251'

        soup = BeautifulSoup(response.text, 'lxml')
        soup.prettify()

        titles = soup.find_all('div', class_="timeline__group")

        for headers in titles:
            self.docs_url_list.append('https://interfax.ru{}'.format(headers.find('a').get('href')))
            self.docs_list.append(headers.text)

    def update_topics(self, url: str) -> None:
        """
        Gets most recent topics from the website

        :param url:
        :return:
        """
        response = requests.get(url)
        response.encoding = 'cp1251'

        soup = BeautifulSoup(response.text, 'lxml')
        soup.prettify()

        titles = soup.find_all('div', class_="title")
        for headers in titles:
            self.topics_url_list.append('https://interfax.ru{}'.format(headers.find('a').get(
                'href')))
            self.topics_list.append(headers.text)


news = NewsBase()


def new_docs(num: int) -> None:
    """
    Shows number of the most recent documents

    :param num:
    :return:
    """
    news.update_docs('https://interfax.ru')
    cnt = int(0)
    print('ТОП-{} самых свежих новостей к этому часу:'
          ''.format(num))
    for header in news.docs_list:
        if cnt < num:
            print(header)
            cnt = cnt + 1
        else:
            break


def new_topics(num: int) -> None:
    """
    Show the number of new topics

    :param num:
    :return:
    """
    news.update_topics('https://interfax.ru/story')
    cnt = int(0)
    print('ТОП-{} самых свежих тем для обсуждений к этому часу:'
          ''.format(num))
    for header in news.topics_list:
        if cnt < num:
            print(header)
            cnt = cnt + 1
        else:
            break


def topic(name_of_topic: str) -> None:
    """
    Show the description of the topic and 5 most recent news suitable for the aforementioned topic

    :param name_of_topic:
    :return:
    """

    print(name_of_topic)
    for num in range(len(news.topics_list)):
        if str(news.topics_list[num]) == str(name_of_topic):
            update_theme(news.topics_url_list[num])
            break


def update_theme(url: str) -> None:
    """
    Gets most recent docs from the particular theme

    :param url:
    :return:
    """
    print(url)
    response = requests.get(url)
    response.encoding = 'cp1251'

    soup = BeautifulSoup(response.text, 'lxml')
    soup.prettify()

    description = soup.find_all('div', class_='chronicles__text')
    for paragraphs in description:
        print(paragraphs.text)

    docs_list = []
    titles = soup.find_all('h3')

    for headers in titles:
        docs_list.append(headers.text)

    cnt = int(0)
    for doc in docs_list:
        if cnt < 5:
            print(doc)
            cnt = cnt + 1
        else:
            break

#new_docs(8)
#new_topics(8)
#topic(news.topics_list[6])
