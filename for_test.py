import requests
import os
from bs4 import BeautifulSoup


def get_all_pages():
    # Creating headers dictionary for headers
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36'
    }

    # Getting response from sneakerhead website
    # r = requests.get(url='https://sneakerhead.ru/shoes/', headers=headers)
    #
    # Check the condition of data path
    # if not os.path.exists('data'):
    #     os.mkdir('data')
    #
    # Writing data to a page_1.html
    # with open(r'data/page_1.html', 'w', encoding='utf-8') as file:
    #     file.write(r.text)

    # Reading data from a page_1.html for create soup object
    with open(r'data/page_1.html', encoding='utf-8') as file:
        src = file.read()

    soup = BeautifulSoup(src, 'lxml')
    # Loop for pagination


def main():
    get_all_pages()


if __name__ == '__main__':
    main()

