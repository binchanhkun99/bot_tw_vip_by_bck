from deep_translator import GoogleTranslator
from pyrogram import Client
from .tweet import Tweet
import json
import asyncio

class SendMessage:
    def __init__(self, tweet: Tweet, username: str):
        self.tweet = tweet
        self.username = username
        self.prepare()
        self.translate()
        self.send()

    def send(self):
        bot_conf = json.load(open("./files/bot.json"))

        async def asyncfunc():
            telegram = Client("Bot", api_id=bot_conf.get("api_id"), api_hash=bot_conf.get("api_hash"), bot_token=bot_conf.get("bot_token"), workdir="./files")
            async with telegram:
                await telegram.send_message(bot_conf.get("username"), self.message)
        
        asyncio.run(asyncfunc())

    def prepare(self):
        self.message = f"{self.username} "

        if self.tweet.is_retweet():
            self.message += "reposted: \n"
        else:
            self.message += "Posted: \n"

        self.message += self.tweet.get_text()
        self.message += f"\n{self.tweet.get_url()}"

    def translate(self):
        self.message = GoogleTranslator(source='auto', target='vi').translate(self.message)
