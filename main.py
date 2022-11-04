#!/usr/bin/python3
# (c) yashoswalyo
"""
Transfer messages from 1 channel to another iteratively
Command:: !t <src_id> <dest_id> <start_message_id> <end_message_id>
Usage:
    src_id: Source Channel ID
    dst_id: Destination Channel ID
    start_message_id: Message ID of initial message
    end_message_id: Message ID of final message
"""

from pyrogram import Client,filters,enums
from pyrogram.errors import FloodWait
from pyrogram.types import Message
import time
import os
SESSION_STR = os.getenv("SESSION_STRING")
User = Client(
    name="yashbot",
    session_string=SESSION_STR
)

@User.on_message(filters.command(["t"],prefixes="!"))
async def transfer(c:Client, m:Message):
    print(m.from_user.first_name)
    owner = await c.get_me()
    if m.from_user.id in [owner.id]:
        grp = m.text.split(' ')
        try:
            oldChannel = int(grp[1])
            newChannel = int(grp[2])
            start_message = int(grp[3])
            end_message = int(grp[4])
            total_messages = end_message - start_message + 1
            if total_messages<0:
                await m.reply(text="Message range is not valid")
                return
            statmsg = await m.reply(text=f"**Total: {total_messages}\nDone:0, \nFailed:0**")
            chat = await c.get_chat(chat_id=oldChannel)
            failed = 0
            passed = 0

            for i in range(start_message,end_message+1):
                try:
                    passed+=1
                    await c.copy_message(chat_id=newChannel,from_chat_id=oldChannel,message_id=i)
                    await statmsg.edit(text=f"**Total: {total_messages}\nDone:`{passed}`\nFailed/NF:`{failed}`**")
                except FloodWait as e:
                    time.sleep(e*1.5)
                except Exception as e:
                    print(e)
                    failed += 1
                    pass
                time.sleep(3)
        except:
            await m.reply("**Commad:** `!t <src_id> <dest_id> <start_message_id> <end_message_id>`",parse_mode=enums.ParseMode.MARKDOWN,quote=True)
    else:
        await m.reply("Not valid User")

User.run()
