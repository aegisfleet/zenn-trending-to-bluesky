import requests
from xml.etree import ElementTree as ET
from bs4 import BeautifulSoup

def fetch_trending_articles(url="https://zenn.dev/feed", max_articles=5):
    articles = []
    
    response = requests.get(url)
    root = ET.fromstring(response.content)

    for item in root.find('channel').findall('item')[:max_articles]:
        link = item.find('link').text
        title = item.find('title').text
        description = item.find('description').text
        articles.append((link, title, description))

    return articles

def fetch_article_content(url):
    response = requests.get(url)
    response.encoding = response.apparent_encoding

    soup = BeautifulSoup(response.text, 'html.parser')
    article_content_selector = 'article'
    article_content = soup.select_one(article_content_selector).text.strip()
    return article_content[:6000]
