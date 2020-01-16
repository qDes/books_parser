import os
import requests

from bs4 import BeautifulSoup
from urllib.parse import urljoin


def fetch_book_soup(url):
    response = requests.get(url)
    response.raise_for_status()
    if url == response.url:
        soup = BeautifulSoup(response.text, 'lxml')
        return soup
    return None


def fetch_books_urls(url):
    books_urls = []
    base_url = "http://tululu.org/"
    book_soup = fetch_book_soup(url)
    book_cards = book_soup.find_all('table', class_='d_book')
    for book_card in book_cards:
        href = book_card.find('a').get('href')
        book_url = urljoin(base_url, href)
        books_urls.append(book_url)
    return books_urls


def parse_pages(start_page, end_page):
    books_urls = []
    for page in range(start_page, end_page+1):
        url = f"http://tululu.org/l55/{page}/"
        books_urls += fetch_books_urls(url)
    return books_urls


def get_book_id(book_url):
    return book_url.split('/')[-2][1:]


def fetch_books_ids():
    books_urls = parse_pages(1, 10)
    books_ids = [get_book_id(book_url) for book_url in books_urls]
    return books_ids


if __name__ == "__main__":
    books_ids = fetch_books_ids()
