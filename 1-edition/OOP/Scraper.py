import sqlite3
from pyrogram import errors
import time

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

