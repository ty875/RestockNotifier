import os
import discord
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from discord.ext import tasks

load_dotenv()

TOKEN = os.getenv("DISCORD_BOT_TOKEN")
CHANNEL_ID = int(os.getenv("DISCORD_CHANNEL_ID"))
PRODUCT_URL = os.getenv("PRODUCT_URL")

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

def is_product_in_stock():
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(PRODUCT_URL, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    stock_status = soup.find('p', class_='stock single-stock-status out-of-stock')
    return stock_status is None  # If out-of-stock text not found, product is in stock

@tasks.loop(hours=12)
async def check_stock():
    channel = client.get_channel(CHANNEL_ID)
    if channel is None:
        print(f"⚠️ Channel ID {CHANNEL_ID} not found or bot can't access it.")
        return
    if is_product_in_stock():
        await channel.send(f"✅ Product is BACK IN STOCK!\n{PRODUCT_URL}")
    else:
        await channel.send(f"❌ Product is still out of stock.\n{PRODUCT_URL}")

@client.event
async def on_ready():
    print(f"Logged in as {client.user}")
    check_stock.start()

client.run(TOKEN)
