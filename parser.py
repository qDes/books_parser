import requests


def download_book(id_):
    url = f'http://tululu.org/txt.php?id={id_}'
    response = requests.get(url)
    response.raise_for_status()
    if url == response.url:
        with open(f'{id_}.txt','w') as f:
            f.write(response.text)


if __name__ == "__main__":
    for num in range(1,11):
        download_book(num)
