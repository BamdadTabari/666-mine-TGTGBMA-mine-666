#--------------- signal handler part start---------------------
# this will use in case of app crash or user closed app
    
# import signal
# import sys
# import traceback

# def signal_handler(sig, frame):
#     """
#     This function will be called when the application receives a SIGINT or SIGTERM signal.
#     """
#     print("Caught signal:", sig)
#     print("Performing cleanup...")
#     try:
#         stop_helper_client(HELPER_CLIENT)
#     except:
#         pass
#     # Print a stack trace to help with debugging
#     traceback.print_stack(frame)
#     print("Cleanup complete. Exiting.")
#     sys.exit(0)

# # Register the signal handler for SIGINT, SIGTERM, CTRL_BREAK_EVENT, CTRL_C_EVENT
# signal.signal(signal.SIGINT, signal_handler)
# signal.signal(signal.SIGTERM, signal_handler)

#--------------- signal handler part end---------------------

# -----------------DB PART START-------------------#

import sqlite3
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
CLIENTS_DIR = os.getcwd() + '\\1-edition\\clients'
CLIENTS = []
API_ID = 18464835
API_HASH = "3742f387f1d2804a5799bbd8e7790deb"
if not os.path.exists(CLIENTS_DIR):
    os.makedirs(CLIENTS_DIR) # Create the directory if it doesn't exist
       
def prepare_clients():
    files = os.listdir(CLIENTS_DIR)
    for file in files:
        if not file.endswith(".session"):
            continue
        session_name = file.replace('.session', '')
        print(f'\n- Client({session_name})')
        client = Client(session_name, workdir=CLIENTS_DIR)
        CLIENTS.append(client)

def add_client():
    """
    Creates a new Telegram client session using the Pyrogram library.
    The session is stored in the CLIENTS_DIR with a filename based on the session name provided by the user.
    """
    try:
        # Prompt the user to input a session name
        session_name = input('Input session name: ')
        # Create a new client session with the specified session name and working directory
        with Client(f"{session_name}", api_id = API_ID, api_hash = API_HASH , workdir=CLIENTS_DIR) as new_client:
            # Print a message indicating the creation of a new client, including the database associated with the new client
            print(f'- New Client {new_client.storage.database}')
            want_add_another = input("do you want to add another client? (y/n)")
            if want_add_another == "y":
                add_client()
            elif want_add_another == "n":
                main()
            else:
                print("wrong character. Redirecting to main menu..." )
                main()
    except Exception as e:
        # Catch and print any exceptions that occur during the client creation and initialization process
        print(f"Exception : {e}")

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
    try:
        group_info =  client.get_chat(group_username)
        return group_info.id
    except Exception as e:
        print(f"Exception: {e}")
        print("fix the fucking bug first. then come back")
        exit()


def get_origin_and_dest_chat_id():
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
        print("fix the fucking bug first. then come back")
        exit()
    
def start_helper_client():
    try:
        # api_id = 27356729
        # api_hash = "2076532de16fc82d242fcc1a012ce5f1"
        client = Client("666mineTGTGBMAmine", api_id=API_ID, api_hash=API_HASH)
        client.start()
        return client
    except Exception as e:
        print(f"Exception: {e}")
        print("fix the fucking bug first. then come back")
        exit(0) 
        
    
def stop_helper_client(client):
    try:
        client.stop()
    except Exception as e:
        print(f"Exception: {e}")
        print("fix the fucking bug first. then come back")
        exit(0) 

def sleep_bitch(second):
        sleep(second)
# -----------------Helper PART End-------------------#
        
# -----------------Scraper PART Start-------------------#
from pyrogram.errors import PeerFlood

def scrape_and_add_members():
    # get org and dest chat id using helper client
    origin_group_id,destination_group_id = get_origin_and_dest_chat_id()

    # prepare all clients
    prepare_clients()
    
    # Start all clients
    start_clients()

    # Scrape members from origin group
    for client in CLIENTS:
        members = client.get_chat_members(origin_group_id)
        for member in members:
            # Check if user is already scraped
            if not is_user_scraped(member.user.id):
                try:
                    # Add user to contacts
                    client.add_contact(member.user.id, member.user.username)
                    # Add user to destination group
                    client.add_chat_members(destination_group_id, member.user.id)
                except PeerFlood as pe:
                    print(f"Exception:  {pe}")
                    print(f"""PEER_FLOOD error encountered. Probably this client is limited , check it,\n
                        client data: {client.get_me()}\n
                        Waiting for 5 seconds before changing client.""")
                    sleep(5) # Wait for 60 seconds before retrying
                    break 
                except Exception as ex:
                    print(f"Exception: {ex}")
                    break                       
                finally:
                    # Save user to database
                    save_user(member.user.id, member.user.username)
    # Stop all clients
    stop_clients()

# -----------------Scraper PART End-------------------#

def main():
    
    try:
        create_database()
        handle_user_actions()
    except Exception as e:
        print(f"Exception: {e}")
        print("fix the fucking bug first. then come back")
        exit()

def handle_user_actions():
    print("""
            \n welcome to my app \n I am Uncle Bamdad \n What You Want to do?
            \n [1] Add new client \n [2] Add members to your group \n [3] Exit
    """)

    try:
        user_choice = input("Just write the number and press enter: ")
        if user_choice == str(1):
            add_client()
        elif user_choice == str(2):
            scrape_and_add_members()
        elif user_choice == str(3):
            exit()
    except Exception as e:
        print(f"Exception: {e}")
        handle_user_actions()
        
# start point
if __name__ == "__main__":
    main()
  

