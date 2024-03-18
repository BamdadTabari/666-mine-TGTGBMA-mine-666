from pyrogram import Client
import os

# This class will manage multiple Telegram sessions (clients)
class ClientManager:
    CLIENTS_DIR = './clients'

    def __init__(self, api_id, api_hash):
        self.massage = " Write Clean Code, Or I Will Kill You"
        self.clients = os.listdir(self.CLIENTS_DIR) # add all clients to the list
        self.api_id = api_id
        self.api_hash = api_hash
       

    async def add_client(self, session_name):
        try:
            session_name = input('Input session name: ')
            async with Client(session_name, workdir=self.CLIENTS_DIR) as new_client:
                print(f'- New Client {new_client.storage.database}')
        except Exception as e:
            print(f"Exception : {e}")
            pass

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
