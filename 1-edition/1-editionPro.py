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


# This class will handle the scraping and adding of members.
class Scraper:
    def __init__(self, client_manager, origin_group_id, destination_group_id):
        self.client_manager = client_manager
        self.origin_group_id = origin_group_id
        self.destination_group_id = destination_group_id

    def scrape_and_add_members(self):
        # Start all clients
        self.client_manager.start_clients()

        # Scrape members from origin group
        for client in self.client_manager.clients:
            for member in client.get_chat_members(self.origin_group_id):
                # Check if user is already scraped
                if not self.is_user_scraped(member.user.id):
                    # Add user to contacts
                    client.add_contact(member.user.id, member.user.username)
                    # Add user to destination group
                    client.add_chat_members(self.destination_group_id, member.user.id)
                    # Save user to database
                    self.save_user(member.user.id, member.user.username)

        # Stop all clients
        self.client_manager.stop_clients()

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
