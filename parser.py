import os
import requests

from bs4 import BeautifulSoup
from pathvalidate import sanitize_filename


def fetch_book(url):
    # url = f'http://tululu.org/txt.php?id={id_}'
    response = requests.get(url)
    response.raise_for_status()
    if url == response.url:
        return response.text
    return None


def save_book_to_folder(book, filepath):
   with open(filepath, 'w') as f:
        f.write(book)


def fetch_book_title(url):
    #url = f"http://tululu.org/b{id_}/"
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'lxml')
    title = soup.find('body').find('h1').text
    title = title.split("::")[0].rstrip()
    return title


def download_txt(url, filename, folder='books/'):
    """Функция для скачивания текстовых файлов.
    Args:
        url (str): Cсылка на текст, который хочется скачать.
        filename (str): Имя файла, с которым сохранять.
        folder (str): Папка, куда сохранять.
    Returns:
        str: Путь до файла, куда сохранён текст.
    """
    if not os.path.exists(folder):
        os.makedirs(folder)
    book = fetch_book(url)
    if book:
        filename = sanitize_filename(filename) + '.txt'
        filepath = os.path.join(folder, filename)
        save_book_to_folder(book, filepath)
        return filepath
    return None


def main():
    for id_ in range(1,11):
        download_url = f'http://tululu.org/txt.php?id={id_}'
        book_page_url = f"http://tululu.org/b{id_}/"
        book_name = fetch_book_title(book_page_url)
        filepath = download_txt(download_url, book_name)
        print(filepath)


if __name__ == "__main__":
    main()
