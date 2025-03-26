import os
import asyncio
import re
from telethon import TelegramClient, events
from telethon.tl.types import DocumentAttributeFilename
from tqdm import tqdm
from loguru import logger
from concurrent.futures import ThreadPoolExecutor
from retrying import retry
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# API credentials from .env file
api_id = os.getenv('API_ID')
api_hash = os.getenv('API_HASH')
phone_number = os.getenv('PHONE_NUMBER')
target_group_username = os.getenv('TARGET_GROUP')

# Ensure that required environment variables are available
if not api_id or not api_hash or not phone_number:
    logger.error("Environment variables for API credentials are missing.")
    exit(1)

if not target_group_username:
    logger.error("Environment variable TARGET_GROUP is missing.")
    exit(1)

# Define the download directory
DOWNLOAD_DIR = 'downloads/telegram'
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

# Setup logging
logger.add("telegram_bot.log", rotation="10 MB", retention="10 days")

# Create the Telegram client
client = TelegramClient('session_name', api_id, api_hash)
executor = ThreadPoolExecutor(max_workers=5)

def sanitize_filename(name):
    """Sanitize file name to avoid unsafe characters."""
    return re.sub(r'[^a-zA-Z0-9_\-.]', '_', name)

@retry(stop_max_attempt_number=5, wait_fixed=2000)
async def download_file(file, file_path, progress_callback):
    await client.download_media(file, file_path, progress_callback=progress_callback)

async def start_download(event, file, file_path):
    """Download the file with a progress bar."""
    logger.info(f"Started Downloading: {file_path}")
    try:
        with tqdm(total=file.size, unit='B', unit_scale=True, desc=file_path, ascii=True) as pbar:
            def progress_callback(current, total):
                pbar.update(current - pbar.n)

            await download_file(file, file_path, progress_callback)
            await event.reply(f'File downloaded and saved to {file_path}')
            logger.info(f'File downloaded and saved to {file_path}')
    except Exception as e:
        logger.error(f"Failed to download {file_path}: {e}")
        await event.reply(f'Failed to download {file_path}: {e}')

    # Fix permissions if inside Docker
    if os.getenv("INSIDE_DOCKER") == "1":
        os.system("chown -R 1000:1000 /app/downloads")

async def handle_event(event):
    if event.message.media:
        file = event.message.media.document
        if file:
            # Get the file name
            file_name = 'unknown_file'
            for attr in file.attributes:
                if isinstance(attr, DocumentAttributeFilename):
                    file_name = sanitize_filename(attr.file_name)
                    logger.info(f"File Name is {file_name}")

            # Define the path to save the file
            file_path = os.path.join(DOWNLOAD_DIR, file_name)

            # Start the download with progress
            await start_download(event, file, file_path)
        else:
            await event.reply('No file found in the message.')
            logger.info("No file found in the message.")
    else:
        await event.reply('No media found in the message.')
        logger.info("No media found in the message.")
        if event.message.text:
            logger.info(f"Text message received: {event.message.text}")
        else:
            logger.info("Non-media message received.")

async def main():
    # Connect to Telegram
    await client.start()

    group = await client.get_entity(target_group_username)
    logger.info(f'Group ID: {group.id}')

    @client.on(events.NewMessage(chats=group))
    async def handler(event):
        await handle_event(event)

    logger.info('Client is running...')
    await client.run_until_disconnected()

# Run the script
with client:
    client.loop.run_until_complete(main())
