import requests
from bs4 import BeautifulSoup


if __name__ == "__main__":
    url = 'https://www.franksonnenbergonline.com/blog/are-you-grateful/'
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'lxml')
    title_tag = soup.find('main').find('header').find('h1')
    title_text = title_tag.text
    image = soup.find('img', class_='attachment-post-image').get('src')
    article = soup.find('article').text
