import sqlite3
from pyrogram import Client, errors
import time

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
    def __init__(self,clients, api_id, api_hash):
        self.clients = clients
        self.api_id = api_id
        self.api_hash = api_hash

    def add_client(self, session_name):
        client = Client(session_name, self.api_id, self.api_hash)
        self.clients.append(client)
        return client

    def start_clients(self):
        for client in self.clients:
            try:
                client.start()
            except Exception as e:
                print(f"Exception : {e}")
                continue

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
                    try:
                        # Add user to contacts
                        client.add_contact(member.user.id, member.user.username)
                        # Add user to destination group
                        client.add_chat_members(self.destination_group_id, member.user.id)
                    except errors.PeerFloodError:
                        print(f"""PEER_FLOOD error encountered. Probably this client is limited , check it,\n
                              client data: {client.get_me()}
                              \n
                              Waiting for 5 seconds before changing client.""")
                        time.sleep(5) # Wait for 60 seconds before retrying
                        break                        

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


def get_group_id(client, group_username):
    group_info = client.get_chat(group_username)
    return group_info.id

if __name__ == "__main__":
    api_id = 27356729
    api_hash = "2076532de16fc82d242fcc1a012ce5f1"
    client = Client("666mineTGTGBMAmine", api_id=api_id, api_hash=api_hash)
    client.start()
    client_manager = ClientManager([client], api_id, api_hash)
    
    origin_group_username = input("origin_group_username please bitch: ")
    destination_group_username = input("destination_group_username please bitch: ")
    origin_group_id = get_group_id(client, origin_group_username)
    destination_group_id = get_group_id(client, destination_group_username)

    scraper = Scraper(client_manager, origin_group_id, destination_group_id)

    scraper.scrape_and_add_members()
