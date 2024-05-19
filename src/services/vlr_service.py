from bs4 import BeautifulSoup, PageElement, ResultSet, Tag
import json
import requests
import logging

from beans.news import News, CustomNewsEncoder
from beans.result import Result, CustomResultEncoder

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

    return json.dumps(news_mapping, cls=CustomNewsEncoder)


def get_recent_results() -> str:
    src = __get_html_from_url(__VLR_URL)
    soup = __get_soup_from_html(src)
    anchors: ResultSet = soup.select(
        '.js-home-matches-completed')[0].select('.mod-home-matches')[0].find_all('a')
    anchor: Tag
    results: list[Result] = []

    for anchor in anchors:
        link = anchor['href']
        result = Result(match_link=link)

        preview_container = anchor.select('.h-match-preview')[0]
        match_time: str
        match_time_ms: str
        match_event: str
        match_series: str
        for index, c in enumerate(preview_container.contents):
            logger.info(f'index is {index} __clean_string(c.text) is {
                        __clean_string(c.text)}')
            if isinstance(c, Tag):
                if 'h-match-preview-time' in c['class']:
                    match_time = __clean_string(c.text)
                    match_time_ms = __clean_string(c['data-utc-ts'])
                if 'h-match-preview-event' in c['class']:
                    match_event = __clean_string(c.text)
                if 'h-match-preview-series' in c['class']:
                    match_series = __clean_string(c.text)

        result.match_time = match_time
        result.match_time_ms = match_time_ms
        result.match_event = match_event
        result.match_series = match_series

        team_1_container = anchor.select('.h-match-team')[0]
        match_team_1: str
        match_team_1_score: str
        for index, c in enumerate(team_1_container.contents):
            logger.info(f'index is {index} __clean_string(c.text) is {
                        __clean_string(c.text)}')
            if isinstance(c, Tag):
                if 'h-match-team-name' in c['class']:
                    match_team_1 = __clean_string(c.text)
                if 'h-match-team-score' in c['class']:
                    match_team_1_score = __clean_string(c.text)

        result.match_team_1 = match_team_1
        result.match_team_1_score = match_team_1_score

        team_2_container = anchor.select('.h-match-team')[1]
        match_team_2: str
        match_team_2_score: str
        for index, c in enumerate(team_2_container.contents):
            logger.info(f'index is {index} __clean_string(c.text) is {
                        __clean_string(c.text)}')
            if isinstance(c, Tag):
                if 'h-match-team-name' in c['class']:
                    match_team_2 = __clean_string(c.text)
                if 'h-match-team-score' in c['class']:
                    match_team_2_score = __clean_string(c.text)

        result.match_team_2 = match_team_2
        result.match_team_2_score = match_team_2_score

        results.append(result)

    logger.debug(f'results is {results}')

    return json.dumps(results, cls=CustomResultEncoder)
