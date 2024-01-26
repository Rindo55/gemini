from pyrogram import filters, Client
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message
from dotenv import load_dotenv
import os
import google.generativeai as genai
import PIL.Image
import random
import time

from stickers import stickers

load_dotenv()

API_HASH = "95937bcf6bc0938f263fc7ad96959c6d"
API_ID = 3845818
BOT_TOKEN = "6358924089:AAF9ruOPppIC-F3z2LwAym-SGqOFsf-cxuM"
GOOGLE_API_KEY = "AIzaSyA5X_AHEvif0EyIP8_Kx4jCg7lVEsArctQ"



app = Client(
    "VisionScriptBot", api_hash=API_HASH, api_id=int(API_ID), bot_token=BOT_TOKEN
)

genai.configure(api_key=GOOGLE_API_KEY)


@app.on_message(filters.command("start") & filters.private)
async def start(_, message: Message):
    welcome_message = (
        f"👋 Hey @{message.chat.username}!\n\n"
        "I'm here to help. Just send me an image, and I'll do the rest.\n\n"
        "Feel free to explore and use my features. If you have any questions or need assistance, "
        "you can use the /help command.\n\n"
    )
    await message.reply(welcome_message, quote=True)


@app.on_message(filters.command("help") & filters.private)
async def help_command(_, message: Message):
    help_message = (
        "🤖 **How to use this bot?**\n\n"
        "1. **Send an Image:** Simply send me an image containing text that you want transcribed.\nGot any question regarding the image? add it the image caption before uploading."
        "2. **Wait for Transcription:** I'll process the image and provide you with the transcribed text.\n\n"
        "Currently in beta stage.\n"
    )
    await message.reply(help_message, quote=True)


@app.on_message(filters.photo & filters.private)
async def vision(bot, message: Message):
    try:
        model_name = "gemini-pro-vision"
        sticker_id = random.choice(stickers)
        sticker = await message.reply_sticker(sticker_id)
        txt = await message.reply(f"Loading {model_name} ...")
        model = genai.GenerativeModel(model_name)
        await txt.edit("Downloading Photo ....")
        file_path = await message.download()
        caption = message.caption
        img = PIL.Image.open(file_path)
        await txt.edit("Shhh 🤫 , **Gemini Vision Pro** is At Work ⚠️.\n Pls Wait..")
        response = (
            model.generate_content([caption, img])
            if caption
            else model.generate_content(img)
        )
        os.remove(file_path)
        await txt.edit('Formating the Result...')
        await sticker.delete()
        await txt.delete()
        if response.text:
            print("response: ", response.text)
            await message.reply(response.text)
        elif response.parts: # handle multiline resps
           for part in response.parts:
            print("part: ", part)
            await message.reply(part)
            time.sleep(2)
        else:
            await message.reply(
                "Couldn't figure out what's in the Image. Contact @pirate_user for help."
            )
    except Exception as e:
        await message.reply("Something Bad occured, Contact @pirate_user")
        raise e


@app.on_message(filters.document & filters.private)
async def document(bot, message: Message):
    await message.reply(
        "Documents are not supported, Please send the File as Image !!!"
    )


@app.on_message(filters.command("source") & filters.private)
async def source(bot, message: Message):
    msg = (
        "It's currently closed source project."
    )
    await message.reply(msg)


app.run(print("Bot Started..."))
