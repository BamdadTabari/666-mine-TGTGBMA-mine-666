import sqlite3
from pyrogram import Client

# We'll use SQLite for simplicity. 
#This database will store the scraped users to avoid adding them multiple times.
def create_database():
    conn = sqlite3.connect('telegram_scraper.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS scraped_users
                 (user_id INTEGER PRIMARY KEY, username TEXT)''')
    conn.commit()
    conn.close()

create_database()

# This class will manage multiple Telegram sessions (clients)
class ClientManager:
    def __init__(self, api_id, api_hash):
        self.clients = []
        self.api_id = api_id
        self.api_hash = api_hash

    def add_client(self, session_name):
        client = Client(session_name, self.api_id, self.api_hash)
        self.clients.append(client)
        return client

    def start_clients(self):
        for client in self.clients:
            client.start()

    def stop_clients(self):
        for client in self.clients:
            client.stop()
