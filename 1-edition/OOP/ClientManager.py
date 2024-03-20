from pyrogram import Client
import os

# This class will manage multiple Telegram sessions (clients)
class ClientManager:
    CLIENTS_DIR = './clients'
    CLIENTS = []
    def __init__(self, api_id, api_hash):
        self.massage = " Write Clean Code, Or I Will Kill You"

        if not os.path.exists(self.CLIENTS_DIR):
            os.makedirs(self.CLIENTS_DIR) # Create the directory if it doesn't exist
        self.prepare_clients()

        self.clients = self.CLIENTS 
        self.api_id = api_id
        self.api_hash = api_hash
       
    def prepare_clients(self):
        for file in os.listdir(self.CLIENTS_DIR):
            if not file.endswith(".session"):
                continue
            session_name = file.replace('.session', '')
            client = Client(session_name, workdir=self.CLIENTS_DIR)
            self.CLIENTS.append(client)

    async def add_client(self):
        try:
            session_name = input('Input session name: ')
            async with Client(session_name, workdir=self.CLIENTS_DIR) as new_client:
                print(f'- New Client {new_client.storage.database}')
        except Exception as e:
            print(f"Exception : {e}")
            pass

    async def start_clients(self):
        for client in self.clients:
            try:
                client.start()
            except Exception as e:
                print(f"Exception : {e}")
                continue

    async def stop_clients(self):
        for client in self.clients:
            client.stop()
