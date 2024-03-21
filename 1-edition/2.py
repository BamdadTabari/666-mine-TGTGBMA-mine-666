import sqlite3

# -----------------DB PART START-------------------#
# We'll use SQLite for simplicity. 
#This database will store the scraped users to avoid adding them multiple times.
def create_database():
    conn = sqlite3.connect('telegram_scraper.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS scraped_users
    (user_id INTEGER PRIMARY KEY, username TEXT)''')
    conn.commit()
    conn.close()

def is_user_scraped(user_id):
    conn = sqlite3.connect('telegram_scraper.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM scraped_users WHERE user_id=?", (user_id,))
    result = cursor.fetchone()
    conn.close()
    return result is not None

def save_user(user_id, username):
    conn = sqlite3.connect('telegram_scraper.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO scraped_users (user_id, username) VALUES (?, ?)", (user_id, username))
    conn.commit()
    conn.close()
# -----------------DB PART End-------------------#
    
# -----------------ClientManager PART START-------------------#
import os
from pyrogram import Client
CLIENTS_DIR = './clients'
CLIENTS = []
API_ID = 18464835
API_HASH = "3742f387f1d2804a5799bbd8e7790deb"
if not os.path.exists(CLIENTS_DIR):
    os.makedirs(CLIENTS_DIR) # Create the directory if it doesn't exist
       
def prepare_clients():
    for f in os.listdir(CLIENTS_DIR):
        if not f.endswith(".session"):
            continue
    session_name = f.replace('.session', '')
    print(f'\n- Client({session_name})')
    client = Client(session_name, workdir=CLIENTS_DIR)
    client.start()
    print(f'  - Client({session_name}): Started')
    CLIENTS.append(client)

def add_client():
    try:
        session_name = input('Input session name: ')
        with Client(session_name, workdir=CLIENTS_DIR) as new_client:
            print(f'- New Client {new_client.storage.database}')
    except Exception as e:
        print(f"Exception : {e}")
        pass

def start_clients():
    for client in CLIENTS:
        try:
            client.start()
        except Exception as e:
            print(f"Exception : {e}")
            continue

def stop_clients():
    for client in CLIENTS:
        client.stop()

# -----------------ClientManager PART End-------------------#