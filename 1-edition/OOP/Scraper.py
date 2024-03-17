import sqlite3
from pyrogram import errors
import time
import dbset as DB

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
                if not DB.is_user_scraped(member.user.id):
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
                    DB.save_user(member.user.id, member.user.username)
        # Stop all clients
        self.client_manager.stop_clients()

