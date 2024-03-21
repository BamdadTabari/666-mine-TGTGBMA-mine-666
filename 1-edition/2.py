RETRY_COUNT = 2
#-------------------------------------------------------
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

# -----------------Helper PART Start-------------------#
from time import sleep
        
def get_group_id( client, group_username):
    retry = 0
    try:
        group_info =  client.get_chat(group_username)
        return group_info.id
    except Exception as e:
        print(f"Exception: {e}")
        sleep_bitch(1)
        if retry <= RETRY_COUNT:
            retry += 1
            get_group_id()
        else:
                print("fix the fucking bug first. then come back")
                exit()


def get_origin_and_dest_chat_id():
    retry = 0
    try:
        # start client just for get chats ids
        client = start_helper_client()
        # get data from user and pass the chats ids
        origin_group_username = input("origin_group_username please bitch: ")
        destination_group_username = input("destination_group_username please bitch: ")
        origin_group_id = get_group_id(client, origin_group_username)
        destination_group_id = get_group_id(client, destination_group_username)
        # stop the client
        stop_helper_client(client)
        return origin_group_id,destination_group_id
    except Exception as e:
            print(f"Exception: {e}")
            sleep_bitch(1)
            if retry <= RETRY_COUNT:
                retry += 1
                get_origin_and_dest_chat_id()
            else:
                print("fix the fucking bug first. then come back")
                exit()
    
def start_helper_client():
    retry = 0
    try:
        api_id = 27356729
        api_hash = "2076532de16fc82d242fcc1a012ce5f1"
        client = Client("666mineTGTGBMAmine", api_id=api_id, api_hash=api_hash)
        client.start()
        return client
    except Exception as e:
        print(f"Exception: {e}")
        sleep_bitch(1)
        if retry <= RETRY_COUNT:
            retry += 1
            start_helper_client()
        else:
            print("fix the fucking bug first. then come back")
            exit()
        
    
def stop_helper_client(client):
    retry = 0
    try:
        client.stop()
        client.disconnect()
    except Exception as e:
        print(f"Exception: {e}")
        sleep_bitch(1)
        if retry <= RETRY_COUNT:
            retry += 1
        stop_helper_client()
    else:
        print("fix the fucking bug first. then come back")
        exit()

def sleep_bitch(second):
        sleep(second)
# -----------------Helper PART End-------------------#
        
# -----------------Scraper PART Start-------------------#
from pyrogram import errors

def scrape_and_add_members(origin_group_id,destination_group_id):
    # Start all clients
    start_clients()

    # Scrape members from origin group
    for client in CLIENTS:
        for member in client.get_chat_members(origin_group_id):
            # Check if user is already scraped
            if not is_user_scraped(member.user.id):
                try:
                    # Add user to contacts
                    client.add_contact(member.user.id, member.user.username)
                    # Add user to destination group
                    client.add_chat_members(destination_group_id, member.user.id)
                except errors.PeerFloodError:
                    print(f"""PEER_FLOOD error encountered. Probably this client is limited , check it,\n
                        client data: {client.get_me()}\n
                        Waiting for 5 seconds before changing client.""")
                    sleep(5) # Wait for 60 seconds before retrying
                    break                        
                finally:
                    # Save user to database
                    save_user(member.user.id, member.user.username)
    # Stop all clients
    stop_clients()

# -----------------Scraper PART End-------------------#

def main():
    retry = 0
    try:
        create_database()
        handle_user_actions()
    except Exception as e:
        print(f"Exception: {e}")
        sleep_bitch(2)
        if retry <= RETRY_COUNT:
            retry += 1
            main()
        else:
            print("fix the fucking bug first. then come back")
            exit()
    
def handle_user_actions():
    print("""
            \n welcome to my app \n I am Uncle Bamdad \n What You Want to do?
            [1] Add new client \n [2] Add members to your group \n [3] Exit
    """)

    origin_group_id,destination_group_id = get_origin_and_dest_chat_id()

    try:
        user_choice = input("Just write the number and press enter: ")
        if user_choice == str(1):
            add_client()
        elif user_choice == str(2):
            scrape_and_add_members(origin_group_id, destination_group_id)
        elif user_choice == str(3):
            exit()
    except Exception as e:
        print(f"Exception: {e}")
        handle_user_actions()
        
# start poit
if __name__ == "__main__":
    main()