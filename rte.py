import requests
from bs4 import BeautifulSoup
import time
import json
from os.path import exists
import pickle

home = "https://rte.ie/news"


class Article:
    def __init__(self, url, title, body=""):
        self.url = url
        self.title = title
        self.body = body

    def __str__(self):
        return self.title + 2 * "\n" + self.body

    def __eq__(self, other):
        return self.title == other.title and self.body == other.body


def get_soup(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "lxml")
    return soup


def get_page_articles(url=home):
    links = get_page_links(url)
    articles = [get_article(url + link) for link in links]

    return articles


def get_page_links(url=home):
    """
    Function to get all article urls from rte page

    return: urls: list of article urls of page
    """
    soup = get_soup(url)
    articles = soup.find_all(class_="image-link img-container")
    links = [article["href"] for article in articles]
    return links


def get_titles(url):
    """
    Function to get links and titles of everything on front page

    return: list of Article objects with links and titles
    """
    soup = get_soup(url)
    # get all articles
    articles = soup.find_all(class_="image-link img-container")
    links = [article["href"] for article in articles]
    titles = [json.loads(article["data-ati-tracking"])["url"] for article in articles]
    articles = [Article(url + link, title) for link, title in zip(links, titles)]
    return articles


def get_body(article):
    """
    Get body text of article when already have url and title

    return: str of body
    """
    soup = get_soup(article.url)
    body = [soup.get_text() for soup in soup.find_all("p")[2:]]
    body = clean_text(body)
    body = "\n\n".join([para for para in body if len(para.split(" ")) > 2])
    return body


def get_article(url):
    """
    Function to scrape title and text of article page

    return: article object containing info
    """
    soup = get_soup(url)
    title = soup.find("title").get_text()
    body = [soup.get_text() for soup in soup.find_all("p")[2:]]
    body = "\n".join([para for para in body if len(para.split(" ")) > 2])
    article = Article(url, title, body)
    return article


def update_articles(page):
    """
    Function to update stored articles for page, remove old ones, highlight new ones

    returns: new_articles: list of new Article objects
    """
    file_name = page.split("/")[-1]
    articles = load(file_name) if exists(file_name) else []
    updated_articles = get_page_articles(page)
    new_articles = list_diff(updated_articles, articles)
    save(file_name, updated_articles)
    return new_articles


def load(name):
    return pickle.load(open(name, "rb"))


def save(name, item):
    pickle.dump(item, open(name, "wb"))


def list_diff(l1, l2):
    """
    l1 - l2
    """
    return [el for el in l1 if el not in l2]

def get_headlines(url = home):
    articles = get_titles(url)
    headlines = ([f"{i+1}. {article.title}\n" for i, article in enumerate(articles[:15])])
    save("articles", articles)
    return headlines

def get_full_article(i):
    headlines = load("articles")
    body = get_body(headlines[i])

    return headlines[i].title.upper() + 2*"\n" + body


def clean_text(body):
    """
    function to do cleaning and editing to downloaded article
    :param body: list of raw paragraphs
    :return: body: list of cleaned paragraphs
    """
    # youtube
    for par in body:
        if "We need your consent" in par or "© RTÉ" in par:
            body.remove(par)

    return body
