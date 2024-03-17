import sqlite3

class DatabaseManager:
    def __init__(self):
        self.massage = " Be Clean Or I Will Kill You"

    # We'll use SQLite for simplicity. 
    #This database will store the scraped users to avoid adding them multiple times.
    def create_database(self):
        conn = sqlite3.connect('telegram_scraper.db')
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS scraped_users
                    (user_id INTEGER PRIMARY KEY, username TEXT)''')
        conn.commit()
        conn.close()

    def is_user_scraped(self, user_id):
        conn = sqlite3.connect('telegram_scraper.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM scraped_users WHERE user_id=?", (user_id,))
        result = cursor.fetchone()
        conn.close()
        return result is not None

    def save_user(self, user_id, username):
        conn = sqlite3.connect('telegram_scraper.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO scraped_users (user_id, username) VALUES (?, ?)", (user_id, username))
        conn.commit()
        conn.close()