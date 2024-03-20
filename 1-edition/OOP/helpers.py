from pyrogram import Client
from time import sleep

class helpers:
    RETRY_COUNT = 2
    def __init__(self):
        self.massage = " Write Clean Code, Or I Will Kill You"
        
    def get_group_id(self, client, group_username):
        retry = 0
        try:
            group_info = client.get_chat(group_username)
            return group_info.id
        except Exception as e:
            print(f"Exception: {e}")
            sleep(1)
            if retry <= self.RETRY_COUNT:
                retry += 1
                self.get_group_id()
            else:
                print("fix the fucking bug first. then come back")
                exit()


    def get_origin_and_dest_chat_id(self):
        retry = 0
        try:
             # start client just for get chats ids
            client = self.start_helper_client()
            # get data from user and pass the chats ids
            origin_group_username = input("origin_group_username please bitch: ")
            destination_group_username = input("destination_group_username please bitch: ")
            origin_group_id = self.get_group_id(client, origin_group_username)
            destination_group_id = self.get_group_id(client, destination_group_username)
            # stop the client
            self.stop_helper_client(client)
            return origin_group_id,destination_group_id
        except Exception as e:
            print(f"Exception: {e}")
            sleep(1)
            if retry <= self.RETRY_COUNT:
                retry += 1
                self.get_origin_and_dest_chat_id()
            else:
                print("fix the fucking bug first. then come back")
                exit()
    
    def start_helper_client(self):
        retry = 0
        try:
            api_id = 27356729
            api_hash = "2076532de16fc82d242fcc1a012ce5f1"
            client = Client("666mineTGTGBMAmine", api_id=api_id, api_hash=api_hash)
            client.start()
            return client
        except Exception as e:
            print(f"Exception: {e}")
            sleep(1)
            if retry <= self.RETRY_COUNT:
                retry += 1
                self.start_helper_client()
            else:
                print("fix the fucking bug first. then come back")
                exit()
        
    
    def stop_helper_client(self, client):
        retry = 0
        try:
            client.stop()
            client.disconnect()
        except Exception as e:
            print(f"Exception: {e}")
            sleep(1)
            if retry <= self.RETRY_COUNT:
                retry += 1
                self.stop_helper_client()
            else:
                print("fix the fucking bug first. then come back")
                exit()

    def sleep_bitch(second):
        sleep(second)