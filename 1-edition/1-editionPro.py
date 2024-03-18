from pyrogram import Client
from OOP.dbset import DatabaseManager as DB
from OOP.ClientManager import ClientManager as CM
from OOP.Scraper import Scraper as SC
from OOP.helpers import helpers

async def main():
    DB.create_database()
    
    
def handle_user_actions():
    print("""
            welcome to my app \n I am Uncle Bamdad \n What You Want to do? \n 
            [1] Add new client \n [2] Add members to your group \n [3] Exit
    """)
    client_manager = CM()
    origin_group_id,destination_group_id = helpers.get_origin_and_dest_chat_id()
    scraper = SC(client_manager,origin_group_id,destination_group_id)
    try:
        user_choice = input("Just write the number and press enter: ")
        if user_choice == str(1):
            CM.add_client()
        elif user_choice == str(2):
            scraper.scrape_and_add_members()
        elif user_choice == str(3):
            exit()
    except Exception as e:
        print(f"Exception: {e}")
        handle_user_actions()
        

if __name__ == "__main__":
    print("""
          6666666666666666666   6666666666666666666   6666666666666666666 
          6666666666666666666   6666666666666666666   6666666666666666666
          6666                  6666                  6666
          6666                  6666                  6666
          6666666666666666666   6666666666666666666   6666666666666666666
          6666666666666666666   6666666666666666666   6666666666666666666
          6666           6666   6666           6666   6666           6666
          6666           6666   6666           6666   6666           6666
          6666666666666666666   6666666666666666666   6666666666666666666
          6666666666666666666   6666666666666666666   6666666666666666666

           author: Bamdad Tabari [Uncle Bamdad]
           star my projects on github: https://github.com/BamdadTabari
           see my articles in medium site: https://medium.com/@bamdadtabari/
    """)
     
    main()

