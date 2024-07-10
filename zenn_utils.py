import requests
from xml.etree import ElementTree as ET
from bs4 import BeautifulSoup
from typing import Optional, List, Tuple

def fetch_trending_articles(url: str = "https://zenn.dev/feed", max_articles: int = 5) -> List[Tuple[str, str, str]]:
    articles: List[Tuple[str, str, str]] = []

    response = requests.get(url)
    root = ET.fromstring(response.content)

    channel = root.find('channel')
    if channel is not None:
        for item in channel.findall('item')[:max_articles]:
            link = item.find('link')
            title = item.find('title')
            description = item.find('description')

            if link is not None and title is not None and description is not None:
                articles.append((link.text or "", title.text or "", description.text or ""))

    return articles

def fetch_article_content(url: str) -> Optional[str]:
    response = requests.get(url)
    response.encoding = response.apparent_encoding

    soup = BeautifulSoup(response.text, 'html.parser')
    article_content_selector = 'article'
    article_content = soup.select_one(article_content_selector)

    if article_content is not None:
        return article_content.text.strip()[:6000]
    return None
