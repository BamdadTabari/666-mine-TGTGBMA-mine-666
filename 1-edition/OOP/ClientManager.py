from pyrogram import Client

# This class will manage multiple Telegram sessions (clients)
class ClientManager:
    CLIENTS_DIR = './clients'
    def __init__(self,clients, api_id, api_hash):
        self.massage = " Be Clean Or I Will Kill You"
        self.clients = clients
        self.api_id = api_id
        self.api_hash = api_hash

    def add_client(self, session_name):
        try:
            client = Client(session_name, self.api_id, self.api_hash)
            self.clients.append(client)
            return client
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
