from pyrogram import Client
from OOP.dbset import DatabaseManager as DB
from OOP.ClientManager import ClientManager as CM
from OOP.Scraper import Scraper as SC
from OOP.helpers import helpers

DB.create_database()

if __name__ == "__main__":
    api_id = 27356729
    api_hash = "2076532de16fc82d242fcc1a012ce5f1"
    client = Client("666mineTGTGBMAmine", api_id=api_id, api_hash=api_hash)
    client.start()
    client_manager = CM.ClientManager([client], api_id, api_hash)
    
    origin_group_id,destination_group_id = helpers.get_origin_and_dest_chat_id(client)

    scraper = SC.Scraper(client_manager, origin_group_id, destination_group_id)

    scraper.scrape_and_add_members()
