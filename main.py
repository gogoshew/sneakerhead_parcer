import requests
import json
import os
import time
from bs4 import BeautifulSoup
from datetime import datetime


def get_all_pages():
    # Creating headers dictionary for headers
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36'
    }

    # Getting response from sneakerhead website
    r = requests.get(url='https://sneakerhead.ru/shoes/', headers=headers)

    # Check the condition of data path
    if not os.path.exists('data'):
        os.mkdir('data')

    # Writing data to a page_1.html
    with open(r'data/page_1.html', 'w', encoding='utf-8') as file:
        file.write(r.text)

    # Reading data from a page_1.html for create soup object
    with open(r'data/page_1.html', encoding='utf-8') as file:
        src = file.read()

    soup = BeautifulSoup(src, 'lxml')

    # Checking current last page
    pages_count = int(soup.find(class_='results').text.strip()[-3:].rstrip(')'))

    for i in range(1, pages_count + 1):
        url = f'https://sneakerhead.ru/shoes/?PAGEN_1={i}'

        # Getting requests for each page
        r = requests.get(url=url, headers=headers)

        # Writing file for each page
        with open(fr'data/page_{i}.html', 'w', encoding='utf-8') as file:
            file.write(r.text)

        # Creating little pause for requests
        time.sleep(2)

    return pages_count + 1

# Creating function for collect data
def collect_data(pages_count):

    # Creating variable for checking date
    current_date = datetime.now().strftime('%d_%m_%Y')

    # Creating data list for collect
    data = []

    for page in range(1, pages_count):
        with open(fr'data/page_{page}.html', encoding='utf-8') as file:
            src = file.read()

        soup = BeautifulSoup(src, 'lxml')
        item_cards = soup.find_all('div', class_='product-card')

        for card in item_cards:
            product_description = card.find('a', class_='product-card__link').text.strip()
            product_sizes = card.find('dl', class_='product-card__sizes').text.strip().split('\n')
            product_price = card.find('div', class_='product-card__price').find('meta').get('content')
            if card.find('span', class_='product-label product-label--discount'):
                product_discount = card.find('span', class_='product-label product-label--discount').text.lstrip('-')
            else:
                product_discount = False
            product_url = 'https://sneakerhead.ru/' + card.find('a', class_='product-card__link').get('href')

            if product_discount:
                data.append(
                    {
                        'Описание': product_description,
                        'Размеры': product_sizes,
                        'Цена': product_price,
                        'Скидка': product_discount,
                        'URL': product_url
                    }
                )
            else:
                data.append(
                    {
                        'Описание': product_description,
                        'Размеры': product_sizes,
                        'Цена': product_price,
                        'URL': product_url
                    }
                )

        print(f"[INFO] Обработана {page}/{pages_count - 1}")

    with open(f'data({current_date}).json', 'a', encoding='utf-8') as file:
        json.dump(data, file, indent=4, ensure_ascii=False)


def main():
    pages_count = get_all_pages()
    collect_data(pages_count=pages_count)

if __name__ == '__main__':
    main()

