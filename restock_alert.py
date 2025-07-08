import os
import discord
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv

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

async def check_stock_once():
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
    await check_stock_once()
    await client.close()  # Optionally shut down bot after one run

client.run(TOKEN)
