# @Author: Edmund Lam <edl>
# @Date:   06:50:24, 02-May-2018
# @Filename: handlers.py
# @Last modified by:   edl
# @Last modified time: 22:11:06, 09-Oct-2019

bot_data = {}
bot_prefix = '.'
message_handlers = {}
private_message_handlers = {}

import re
import os
import pickle
from random import randint
from shutil import copyfile
from bot.utils import datautils, msgutils, strutils
import discord

print("Begin Handler Initialization")

print("\tBegin Loading Files")
closing = False

if not os.path.exists("data/backup/"):
    os.makedirs("data/backup/")

bot_data = datautils.load_data_file('data.txt');

print("\tLoaded files")

def add_message_handler(handler, keyword):
    message_handlers[strutils.format_regex(keyword)] = handler

def add_private_message_handler(handler, keyword):
    private_message_handlers[strutils.format_regex(keyword)] = handler

def get_data():
    return [bot_data]

# dict utilities

def nested_set(value, *keys):
    dic = bot_data
    for key in keys[:-1]:
        dic = dic.setdefault(key, {})
    dic[keys[-1]] = value
    print(bot_data);

def nested_pop(*keys):
    nested_get(*keys[:-1]).pop(keys[-1], None)

def alt_pop(key, *keys):
    nested_get(*keys).pop(key)


def nested_get(*keys):
    dic = bot_data
    for key in keys:
        dic=dic.setdefault( key, {} )
    return dic

print("Handler initialized")
print("Begin Command Initialization")
# Add modules here
from commands import *
from bot.utils import cmdutils
print("Command Initialization Finished")

import asyncio

async def on_message(bot, msg):
    #implement mention count later
    if not msg.author.bot:
        c = msg.channel;
        try:
            for a in message_handlers:
                reg = re.compile(a).match(msg.content)
                if reg:
                    commandname = message_handlers[a].__name__;
                    if cmdutils.allowed_command(commandname,c):
                        if isinstance(c, discord.abc.PrivateChannel):
                            await c.send("Commands are not supported for private channels")
                            return
                        await message_handlers[a](bot, msg, reg)
                        break
                    else:
                        await c.send('The {} command is disabled in this channel.'.format(commandname))
        except Exception as e:
            em = discord.Embed(title="Unknown Error",
                               description="An unknown error occurred. Trace:\n%s" % e, colour=0xd32323)
            await msgutils.send_embed(bot, msg, em)
            traceback.print_tb(e.__traceback__)

async def timed_save(Bot):
    while True:
        await asyncio.sleep(60)
        # await message_handlers["save"](Bot, None, overrideperms=True)
        try:
            copyfile('data/data.txt', 'data/backup/data.txt')
        except Exception as e:
            traceback.print_tb(e.__traceback__)
