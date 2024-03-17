# Install required libraries using pip:
# pip install pyrogram tgcrypto SQLAlchemy

from pyrogram import Client
from pyrogram.raw import functions
from pyrogram.raw.types import InputPeerUser
from sqlalchemy import create_engine, Column, Integer, String, Sequence
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

# SQLite database connection
engine = create_engine('sqlite:///members.db')
Session = sessionmaker(bind=engine)
session = Session()

# Model for scraped members
class Member(Base):
    __tablename__ = 'members'

    id = Column(Integer, Sequence('member_id_seq'), primary_key=True)
    username = Column(String)
    user_id = Column(String)

# Create table in database
Base.metadata.create_all(engine)
        
# Pyrogram Client instances list
clients = []

   
# Function to scrape and add members to destination group
def scrape_and_add_members(origin_group_id, destination_group_id):
    for client in clients:
        try:
            # Get users from origin group
            members = client.get_chat_members(origin_group_id)
            # Get all users id (in a pythonic way :)
            members_ids = [member.user.id for member in members]
            client.add_chat_members(chat_id=destination_group_id,user_ids=members_ids,forward_limit= 100)
            for member in members:
                user_id = member.user.id
                # Save scraped member to database if not already saved
                existing_member = session.query(Member).filter_by(user_id=user_id).first()
                if not existing_member:
                    new_member = Member(username=member.user.username, user_id=user_id)
                    session.add(new_member)
                    session.commit()
        except Exception as e:
            print(f"Error scraping and adding members: {e}")

def get_group_id(client, group_username):
    group_info = client.get_chat(group_username)
    return group_info.id

# Main method
def main():
    # Add your API ID and Hash in the Client creation
  
    client = Client("killbill", api_id=18464835, api_hash="3742f387f1d2804a5799bbd8e7790deb")
    clients.append(client)
    
    for client in clients:
        client.start()

    origin_group_username = input("origin_group_username please bitch: ")
    destination_group_username = input("destination_group_username please bitch: ")
    origin_group_id = get_group_id(clients[0], origin_group_username)
    destination_group_id = get_group_id(clients[0], destination_group_username)
    
    # Scrapping and adding members to destination group
    scrape_and_add_members(origin_group_id, destination_group_id)

if __name__ == "__main__":
    main()