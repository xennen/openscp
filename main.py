from bs4 import BeautifulSoup
import requests
import csv

with open('moscow_books.csv', 'w', encoding='utf-8-sig', newline='') as file:
    writer = csv.writer(file, delimiter=';')
    writer.writerow([
        'Автор', 'Книга', 'Цена'])

for j in range(1, 358):
    url = f'https://www.moscowbooks.ru/books/fiction/?page={j}'
    response = requests.get(url=url)
    response.encoding = 'utf-8'
    soup = BeautifulSoup(response.text, 'lxml')

    price = [name.text.strip() for name in soup.find_all('div', class_='book-preview__price')]
    author = [name.text for name in soup.find_all('a', class_='author-name')]
    title = [name.text for name in soup.find_all('a', class_='book-preview__title-link')]

    for title_name, author_name, book_price in zip(title, author, price):
        flatten = author_name, title_name, book_price
        with open('moscow_books.csv', 'a', newline='', encoding='utf-8-sig') as file:
            writer = csv.writer(file, delimiter=';')
            writer.writerow(flatten)
    file.close()
    print(f'Страница {j} готова')


