from bs4 import BeautifulSoup, PageElement, ResultSet, Tag
import json
import requests
import logging

from beans.news import News, CustomEncoder

logger = logging.getLogger()

__VLR_URL = 'https://www.vlr.gg/'


def __clean_string(ip: str) -> str:
    #  remove \n and \t
    ip = ip.replace('\t', '').replace('\n', '')
    return ip.strip()


def __get_html_from_url(url: str) -> str:
    try:
        response = requests.get(url)
        if response.status_code == 200:
            logger.info(200)
            logger.info(response.text[0:10])
            return response.text
        else:
            logger.error(f'did not get resp 200 for url {
                         url} resp_code : {response.status_code}')
    except Exception:
        logger.exception('exception in __get_html_from_url')


def __get_soup_from_html(src: str) -> BeautifulSoup:
    return BeautifulSoup(src, 'html.parser')


def get_latest_news() -> str:
    src = __get_html_from_url(__VLR_URL)
    soup = __get_soup_from_html(src)
    home_news = soup.select('.js-home-news')
    modified_children = home_news[0].contents
    non_empty_children: list[PageElement] = []
    news_mapping: dict = {}

    for news_item in modified_children:
        if (news_item.text.strip() != ""):
            non_empty_children.append(news_item)

    # skipping last as it is the skip more button
    for index, news_item in enumerate(non_empty_children[0:-1]):
        date_key: str
        news: list[News] = []
        if (index % 2 == 0):
            cleaned_string = __clean_string(news_item.text)
            date_key = cleaned_string.replace(' ', '-')
            if (len(cleaned_string.split(' ')) > 2):
                date_key = '-'.join(cleaned_string.split(' ')[0:-1])
            logger.info(f'date_key is {date_key}')
            news_container = news_item.find_next_sibling('div')
            anchors: ResultSet = news_container.find_all('a')
            anchor: Tag
            for anchor in anchors:
                logger.info(f'anchor.attrs is {anchor.attrs}')
                link = anchor['href']
                title = __clean_string(
                    anchor.select('.news-item-title')[0].text)
                news.append(News(title, link))
            news_mapping[date_key] = news

    return json.dumps(news_mapping, cls=CustomEncoder)
