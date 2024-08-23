import sqlite3

def delete_all_data(db_name='paintings.db'):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    cursor.execute('DELETE FROM paintings')

    cursor.execute('DELETE FROM sqlite_sequence WHERE name="paintings"')

    conn.commit()
    conn.close()

    print("deleted")

delete_all_data()