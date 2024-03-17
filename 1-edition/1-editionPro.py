from pyrogram import Client
import OOP.dbset as DB
import OOP.ClientManager as CM
import OOP.Scraper as SC
import OOP.helpers as helper

DB.create_database()

if __name__ == "__main__":
    api_id = 27356729
    api_hash = "2076532de16fc82d242fcc1a012ce5f1"
    client = Client("666mineTGTGBMAmine", api_id=api_id, api_hash=api_hash)
    client.start()
    client_manager = CM.ClientManager([client], api_id, api_hash)
    
    origin_group_id,destination_group_id = helper.get_origin_and_dest_chat_id(client)

    scraper = SC.Scraper(client_manager, origin_group_id, destination_group_id)

    scraper.scrape_and_add_members()
