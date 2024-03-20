from pyrogram import Client
import sqlite3

client = Client("asghar", api_id=18464835, api_hash='3742f387f1d2804a5799bbd8e7790deb')

client.add_contact()

conn = sqlite3.connect('telegram_scraper.db')
conn.cursor()
