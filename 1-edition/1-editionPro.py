import OOP.DatabaseManager as DBM
from OOP.ClientManager import ClientManager as CM
from OOP.Scraper import Scraper as SC
from OOP.helpers import helpers

RETRY_COUNT = 2
DB = DBM.DatabaseManager()
def main():
    retry = 0
    try:
        DB.create_database()
        handle_user_actions()
    except Exception as e:
        print(f"Exception: {e}")
        helpers.sleep_bitch(2)
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

    client_manager = CM(api_id=18464835, api_hash="3742f387f1d2804a5799bbd8e7790deb")
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
        

# start point
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

