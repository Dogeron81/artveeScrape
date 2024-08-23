import sqlite3

def extract_from_db(db_name='paintings.db'):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    cursor.execute('SELECT author, country, name, year, category, img_url FROM paintings')
    
    rows = cursor.fetchall()

    data = []
    for row in rows:
        data.append({
            'author': row[0],
            'country': row[1],
            'name': row[2],
            'year': row[3],
            'category': row[4],
            'img_url': row[5]
        })

    conn.close()

    return data

data = extract_from_db()
print(data)