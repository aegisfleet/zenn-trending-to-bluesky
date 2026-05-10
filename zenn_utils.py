import requests
from xml.etree import ElementTree as ET
from bs4 import BeautifulSoup
from typing import Optional, List, Tuple
import artifact_utils

def _extract_article(item: ET.Element, previous_articles: List[str]) -> Optional[Tuple[str, str, str]]:
    """XMLのitem要素から記事情報を抽出し、未投稿であれば返す。"""
    link = item.find('link')
    title = item.find('title')
    description = item.find('description')

    if link is None or title is None or description is None:
        return None

    full_url = link.text or ""
    if full_url in previous_articles:
        return None

    return (full_url, title.text or "", description.text or "")

def fetch_trending_articles(url: str = "https://zenn.dev/feed", max_articles: int = 5) -> List[Tuple[str, str, str]]:
    previous_articles = artifact_utils.load_previous_results()
    articles: List[Tuple[str, str, str]] = []

    response = requests.get(url)
    root = ET.fromstring(response.content)

    channel = root.find('channel')
    if channel is None:
        artifact_utils.save_results(articles)
        return articles

    for item in channel.findall('item'):
        if len(articles) >= max_articles:
            break

        article = _extract_article(item, previous_articles)
        if article:
            articles.append(article)

    artifact_utils.save_results(articles)
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
