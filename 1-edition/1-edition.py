import sqlite3
from pyrogram import Client

# We'll use SQLite for simplicity. Create a database and a table to store scraped users
def create_database():
    conn = sqlite3.connect('telegram_scraper.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS scraped_users
                 (user_id INTEGER PRIMARY KEY, username TEXT)''')
    conn.commit()
    conn.close()

create_database()

#For handling multiple sessions, you can use Pyrogram's Client class with different session names.
def create_client(session_name):
    return Client(session_name, api_id=18464835, api_hash='3742f387f1d2804a5799bbd8e7790deb')

#To scrape members from an origin group, join the group, and add members to contacts
async def scrape_members(client, origin_group_id):
    await client.start()
    members = await client.get_chat_members(origin_group_id)
    for member in members:
        if member.user.is_bot:
            continue
        # Add member to contacts
        await client.add_contact(member.user.id, member.user.username)
        # Save to database
        conn = sqlite3.connect('telegram_scraper.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO scraped_users (user_id, username) VALUES (?, ?)",
                 (member.user.id, member.user.username))
        conn.commit()
        conn.close()
    await client.stop()

# After scraping, join the destination group and add the scraped members
async def add_members_to_destination(client, destination_group_id):
    await client.start()
    conn = sqlite3.connect('telegram_scraper.db')
    cursor = conn.cursor()
    cursor.execute("SELECT user_id FROM scraped_users")
    user_ids = [row[0] for row in cursor.fetchall()]
    for user_id in user_ids:
        await client.add_chat_members(destination_group_id, user_id)
    conn.close()
    await client.stop()

# After adding members to the destination group, delete the contacts
async def delete_contacts(client, user_ids):
    await client.start()
    for user_id in user_ids:
        await client.delete_contacts(user_id)
    await client.stop()

# Before adding new members, check if they were added before
def check_and_add_new_members(user_id,username):
    conn = sqlite3.connect('telegram_scraper.db')
    cursor = conn.cursor()
    cursor.execute("SELECT user_id FROM scraped_users WHERE user_id=?", (user_id,))
    if cursor.fetchone() is None:
        # Add new member to database
        cursor.execute("INSERT INTO scraped_users (user_id, username) VALUES (?, ?)",
                 (user_id, username))
        conn.commit()
    conn.close()


