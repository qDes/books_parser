import os
import json
import requests

from pathvalidate import sanitize_filename
from urllib.parse import urljoin


def fetch_book(url):
    response = requests.get(url)
    response.raise_for_status()
    if url == response.url:
        return response.text
    return None


def save_book_to_folder(book, filepath):
    with open(filepath, 'w') as f:
        f.write(book)


def fetch_book_title(soup):
    header_selector = 'body h1'
    title = soup.select_one(header_selector).text
    title = title.split("::")[0].rstrip()
    return title


def fetch_book_author(soup):
    header_selector = 'body h1'
    author = soup.select_one(header_selector).text
    author = author.split("::")[-1].lstrip()
    return author


def download_txt(url, filename, folder='books'):
    """Функция для скачивания текстовых файлов.
    Args:
        url (str): Cсылка на текст, который хочется скачать.
        filename (str): Имя файла, с которым сохранять.
        folder (str): Папка, куда сохранять.
    Returns:
        str: Путь до файла, куда сохранён текст.
    """
    os.makedirs(folder, exist_ok=True)
    book = fetch_book(url)
    if book:
        filename = sanitize_filename(filename) + '.txt'
        filepath = os.path.join(folder, filename)
        save_book_to_folder(book, filepath)
        return filepath
    return None


def download_image(url, folder='images/'):
    os.makedirs(folder, exist_ok=True)
    filename = os.path.join(folder, url.split('/')[-1])
    response = requests.get(url)
    response.raise_for_status()
    with open(filename, 'wb') as f:
        f.write(response.content)
    return filename


def fetch_book_cover_url(soup, book_url):
    base_url = "http://tululu.org"
    try:
        image_selector = '.bookimage img'
        image_url = soup.select_one(image_selector).get('src')
        if image_url[0] == '/':
            return urljoin(base_url, image_url)
        return urljoin(book_url, image_url)
    except AttributeError:
        return None


def fetch_book_comments(soup):
    comments = []
    try:
        comments_selector = '.texts .black'
        comments = soup.select(comments_selector)
        comments = [comment.text for comment in comments]
    except AttributeError:
        pass
    return comments


def fetch_book_genre(soup):
    genre = []
    try:
        genre_selector = 'span.d_book a'
        genre = [genre.text for genre in soup.select(genre_selector)]
    except AttributeError:
        pass
    return genre


def save_books_description(description, filename):
    description = json.dumps(description)
    with open(filename, 'w') as f:
        f.write(description)

