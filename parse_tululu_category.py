import argparse
import requests

from bs4 import BeautifulSoup
from urllib.parse import urljoin
from parser import fetch_book_genre, fetch_book_comments
from parser import fetch_book_title, fetch_book_cover_url
from parser import download_image, download_txt
from parser import fetch_book_author


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


def fetch_books_ids(start_page, end_page):
    books_urls = parse_pages(start_page, end_page)
    books_ids = [get_book_id(book_url) for book_url in books_urls]
    return books_ids


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--start_page", type=int)
    parser.add_argument("--end_page", type=int, default=701)
    args = parser.parse_args()
    return args.start_page, args.end_page


def main():
    books_description = []
    start_page, end_page = parse_args()
    books_ids = fetch_books_ids(start_page, end_page)
    for book_id in books_ids[:2]:
        book_txt_url = f'http://tululu.org/txt.php?id={book_id}'
        book_page_url = f"http://tululu.org/b{book_id}/"
        book_soup = fetch_book_soup(book_page_url)
        if book_soup:
            book_genre = fetch_book_genre(book_soup)
            comments = fetch_book_comments(book_soup)
            book_name = fetch_book_title(book_soup)
            book_cover_url = fetch_book_cover_url(book_soup)
            image_filepath = download_image(book_cover_url)
            txt_filepath = download_txt(book_txt_url, book_name)
            author = fetch_book_author(book_soup)
            book_description = {"title": book_name,
                                "author": author,
                                "img_src": image_filepath,
                                "book_path": txt_filepath,
                                "comments": comments,
                                "genre": book_genre,
                                }
            books_description.append(book_description)
    save_books_description(books_description)


if __name__ == "__main__":
    main()
