import os
import requests

from bs4 import BeautifulSoup
from pathvalidate import sanitize_filename
from urllib.parse import urljoin


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


def fetch_book_soup(url):
    response = requests.get(url)
    response.raise_for_status()
    if url == response.url:
        soup = BeautifulSoup(response.text, 'lxml')
        return soup
    return None


def fetch_book_title(soup):
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


def download_image(url, folder='covers/'):
    if not os.path.exists(folder):
        os.makedirs(folder)
    filename = os.path.join(folder, url.split('/')[-1])
    response = requests.get(url)
    response.raise_for_status()
    with open(filename, 'wb') as f:
        f.write(response.content)
    return filename


def fetch_book_cover_url(soup):
    base_url = "http://tululu.org"
    try:
        image_relative_url = soup.find('div', class_='bookimage').find('img').get('src')
        book_cover_url = urljoin(base_url, image_relative_url)
        return book_cover_url
    except AttributeError:
        return None


def fetch_book_comments(soup):
    comments = []
    try:
        raw_comments = soup.find_all('div', class_='texts')
        for raw_comment in raw_comments:
            comments.append(raw_comment.find('span').text)
    except AttributeError:
        pass
    return comments


def fetch_book_genre(soup):
    genre = []    
    try:
        raw_genre = soup.find('span', class_='d_book').find_all('a')
        genre = [gen.text for gen in raw_genre]
    except AttributeError:
        pass
    return genre


def main():
    for id_ in range(1,11):
        download_url = f'http://tululu.org/txt.php?id={id_}'
        book_page_url = f"http://tululu.org/b{id_}/"
        book_soup = fetch_book_soup(book_page_url)
        if book_soup:
            book_genre = fetch_book_genre(book_soup)
            print(book_genre)
            #comments = fetch_book_comments(book_soup)
            #book_name = fetch_book_title(book_soup)
            #book_cover_url = fetch_book_cover_url(book_soup)
            #filepath = download_image(book_cover_url) 
            print()
        '''
        filepath = download_txt(download_url, book_name)
        if filepath:
            book_cover_url = fetch_book_cover_url(book_soup)
            print(""filepath)
            print(book_cover_url)
        '''



if __name__ == "__main__":
    main()
