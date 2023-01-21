from bs4 import BeautifulSoup
import requests
import csv
import os

with open('moscow_books.csv', 'w', encoding='utf-8-sig', newline='') as file:
    writer = csv.writer(file, delimiter=';')
    writer.writerow([
        'Автор', 'Книга', 'Цена'])

for j in range(1, 4):

    url = f'https://www.moscowbooks.ru/books/fiction/?page={j}'
    response = requests.get(url=url)
    response.encoding = 'utf-8'
    soup = BeautifulSoup(response.text, 'lxml')

    price = [name.text.strip() for name in soup.find_all('div', class_='book-preview__price')]
    author = [name.text for name in soup.find_all('a', class_='author-name')]
    title = [name.text.strip('"').replace('"', '') for name in soup.find_all('a', class_='book-preview__title-link')]
    img = [name['src'] for name in soup.find_all('img', class_='book-preview__img')]

    for title_name, author_name, book_price, img_url in zip(title, author, price, img):
        flatten = author_name, title_name, book_price

        if os.path.exists(f'/home/xennen/scratchbooks/books/{author_name}') == False:
            os.mkdir(f'/home/xennen/scratchbooks/books/{author_name}')
        os.mkdir(f'/home/xennen/scratchbooks/books/{author_name}/{title_name}')
        file2 = open(f'/home/xennen/scratchbooks/books/{author_name}/{title_name}/{title_name}, {book_price}.txt', 'x', encoding='utf-8')

        image = requests.get(url=f'https://www.moscowbooks.ru/{img_url}')
        with open(f'/home/xennen/scratchbooks/books/{author_name}/{title_name}/{title_name}.jpeg', 'wb') as file:
            file.write(response.content)

        with open('moscow_books.csv', 'a', newline='', encoding='utf-8-sig') as file:
            writer = csv.writer(file, delimiter=';')
            writer.writerow(flatten)

    file.close()
    print(f'Страница {j} готова')


