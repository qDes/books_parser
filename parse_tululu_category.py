import argparse
import requests

from bs4 import BeautifulSoup
from configargparse import ArgParser
from parser import fetch_book_genre, fetch_book_comments
from parser import fetch_book_title, fetch_book_cover_url
from parser import download_image, download_txt
from parser import fetch_book_author, save_books_description
from urllib.parse import urljoin


def fetch_book_soup(url):
    response = requests.get(url)
    response.raise_for_status()
    if url == response.url:
        soup = BeautifulSoup(response.text, "lxml")
        return soup
    return None


def fetch_books_urls(url):
    books_urls = []
    base_url = "http://tululu.org/"
    book_soup = fetch_book_soup(url)
    book_cards = book_soup.select(".d_book")
    books_urls = [
        urljoin(base_url, book_card.select_one("a").get("href"))
        for book_card in book_cards
    ]
    return books_urls


def parse_pages(start_page, end_page):
    books_urls = []
    for page in range(start_page, end_page + 1):
        url = f"http://tululu.org/l55/{page}/"
        books_urls += fetch_books_urls(url)
    return books_urls


def get_book_id(book_url):
    return book_url.split("/")[-2][1:]


def fetch_books_ids(start_page, end_page):
    books_urls = parse_pages(start_page, end_page)
    books_ids = [get_book_id(book_url) for book_url in books_urls]
    return books_ids


def parse_args():
    parser = ArgParser(default_config_files=[".env"])
    parser.add("--start_page", required=True, type=int)
    parser.add("--end_page", type=int, default=701)
    parser.add("--file", required=True, help="books description file")
    args = parser.parse_args()
    return args


def main():
    books_description = []
    args = parse_args()
    start_page, end_page, description_file = args.start_page, args.end_page, args.file
    books_ids = fetch_books_ids(start_page, end_page)
    for book_id in books_ids:
        book_txt_url = f"http://tululu.org/txt.php?id={book_id}"
        book_page_url = f"http://tululu.org/b{book_id}/"
        book_soup = fetch_book_soup(book_page_url)
        if not book_soup:
            continue
        book_name = fetch_book_title(book_soup)
        book_cover_url = fetch_book_cover_url(book_soup, book_page_url)
        book_description = {
            "title": fetch_book_title(book_soup),
            "author": fetch_book_author(book_soup),
            "img_src": download_image(book_cover_url),
            "book_path": download_txt(book_txt_url, book_name),
            "comments": fetch_book_comments(book_soup),
            "genre": fetch_book_genre(book_soup),
        }
        books_description.append(book_description)
    save_books_description(books_description, description_file)


if __name__ == "__main__":
    main()
