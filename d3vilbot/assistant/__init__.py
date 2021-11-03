from . import *
from telethon import Button, custom

from d3vilbot import bot

from d3vilbot import *
from pyUltroid import *
from pyUltroid.dB.database import Var
from telethon import Button, custom

OWNER_NAME = bot.me.first_name
OWNER_ID = bot.me.id
d3vil_mention = f"[{OWNER_NAME}](tg://user?id={OWNER_ID})"


async def setit(event, name, value):
    try:
        udB.set(name, value)
    except BaseException:
        return await event.edit("`Something Went Wrong`")
