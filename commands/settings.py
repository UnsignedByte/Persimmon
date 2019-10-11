# @Author: Edmund Lam <edl>
# @Date:   11:04:49, 05-Apr-2018
# @Filename: settings.py
# @Last modified by:   edl
# @Last modified time: 11:09:22, 10-Oct-2019


import asyncio
from bot.utils import msgutils, strutils, cmdutils, datautils
from bot.handlers import add_message_handler
import discord
from discord import Embed, ChannelType

async def settings(bot, msg, reg):
    command = reg.group('command');
    perms = msg.channel.permissions_for(msg.author)
    #make sure user is authorized to edit bot preferences
    #and that command exists
    if perms.manage_guild and cmdutils.is_command(command):
        sub = reg.group('sub');
        channels = reg.group('channels')
        if channels == 'all':
            channels = list(n for n in msg.guild.channels if isinstance(n, discord.TextChannel))
        else:
            channels = msg.channel_mentions
        for channel in channels:
            datautils.nested_set(sub == 'disable', 'guilds', msg.guild.id, 'channels', channel.id, 'commands', command)
        await msg.channel.send('Command `{}` has been {}d in {}'.format(command, sub, ', '.join(map(lambda x:x.mention,  channels))))

add_message_handler(settings, r'settings (?P<sub>enable|disable) (?P<command>.+?) (?P<channels>all|(?:channel_mention )+)')
