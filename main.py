from bs4 import BeautifulSoup
import requests
from concurrent.futures import ThreadPoolExecutor
import sqlite3


data = []
page_count = 1
wanted_paintings = 5000
session = requests.Session()

def page_scrap(paintings):
    for painting in paintings:
        # CATEGORY
        category = painting.find('div', class_='woodmart-product-cats').find('a').get_text()
        if category == 'Posters':
            continue

        # AUTHOR AND COUNTRY
        author_and_country = painting.find('div', class_='woodmart-product-brands-links')
        author = author_and_country.find('a').get_text()

        country = 'N/A'  # Default value
        if '(' in author_and_country.get_text():
            country = author_and_country.get_text().split('(')[1].split(',')[0]

        # NAME AND YEAR
        name_and_year = painting.find('h3', class_='product-title').get_text()
        name = name_and_year
        year = 'N/A'  # Default value
        if '(' in name_and_year and ')' in name_and_year:
            name = name_and_year[:name_and_year.index('(') - 1]
            year = name_and_year[name_and_year.index('(') + 1:name_and_year.index(')')]

        # IMG
        img_tag = painting.find('img')
        img_src = img_tag.get('data-src')

        data.append({
            'author': author,
            'country': country,
            'name': name,
            'year': year,
            'category': category,
            'img_url': img_src
        })

        if len(data) >= wanted_paintings:
            break
        progress_bar(len(data), wanted_paintings)

def save_to_db(data, db_name='paintings.db'):
    # Connect to the SQLite database (or create it if it doesn't exist)
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    # Create a table if it doesn't exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS paintings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            author TEXT,
            country TEXT,
            name TEXT,
            year TEXT,
            category TEXT,
            img_url TEXT
        )
    ''')

    # Insert data into the table
    for painting in data:
        cursor.execute('''
            INSERT INTO paintings (author, country, name, year, category, img_url)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (painting['author'], painting['country'], painting['name'], painting['year'], painting['category'], painting['img_url']))

    # Commit the transaction and close the connection
    conn.commit()
    conn.close()

def progress_bar(progress, total):
    percent = 100 * (progress / float(total))
    bar = '█' * int(percent) + '-' * (100 - int(percent))
    print(f'\r|{bar}| {percent:.2f}%', end='\r')

def fetch_page(page_count):
    artvee = session.get(f'https://artvee.com/page/{page_count}/')
    soup = BeautifulSoup(artvee.text, 'lxml')
    paintings = soup.find_all('div', class_='unsnax snax-collection-item')
    page_scrap(paintings)

while len(data) < wanted_paintings:
    with ThreadPoolExecutor(max_workers=5) as executor:
        executor.map(fetch_page, range(page_count, page_count + 5))
        page_count += 5

save_to_db(data)
print('saved')