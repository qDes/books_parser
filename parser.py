import os
import requests


def fetch_book(id_):
    url = f'http://tululu.org/txt.php?id={id_}'
    response = requests.get(url)
    response.raise_for_status()
    if url == response.url:
        return response.text
    return None


def save_book_to_folder(book, folder, id_):
    if not os.path.exists(folder):
        os.makedirs(folder)
    with open(f'{folder}/id{id_}.txt','w') as f:
        f.write(book)


if __name__ == "__main__":
    for num in range(1,11):
        book = fetch_book(num)
        if book:
            save_book_to_folder(book, 'books', num)
