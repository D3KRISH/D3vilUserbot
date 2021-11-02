import asyncio
import datetime
import importlib
import inspect
import logging
import math
import os
import re
import sys
import time
import traceback
from pathlib import Path
from time import gmtime, strftime

from telethon import events
from telethon.tl.functions.channels import GetParticipantRequest
from telethon.tl.types import ChannelParticipantAdmin, ChannelParticipantCreator

from d3vilbot import *
from d3vilbot.helpers import *
from d3vilbot.config import Config


# this shit handles errors
def errors_handler(func):
    async def wrapper(errors):
        try:
            await func(errors)
        except BaseException:

            date = strftime("%Y-%m-%d %H:%M:%S", gmtime())
            new = {
                'error': str(sys.exc_info()[1]),
                'date': datetime.datetime.now()
            }

            text = "**𝓓3𝓿𝓲𝓵𝓫𝓸𝓽 𝓒𝓡𝓐𝓢𝓗 𝓡𝓔𝓟𝓞𝓡𝓣**\n\n"

            link = "[here](https://t.me/D3VIL_BOT_SUPPORT)"
            text += "If you wanna you can report it"
            text += f"- just forward this message {link}.\n"
            text += "Nothing is logged except the fact of error and date\n"

            ftext = "\nDisclaimer:\nThis file is uploaded ONLY here,"
            ftext += "\nwe logged only fact of error and date,"
            ftext += "\nwe respect your privacy,"
            ftext += "\nyou may not report this error if you've"
            ftext += "\nany confidential data here, no one will see your data\n\n"

            ftext += "--------BEGIN D3VILBOT TRACEBACK LOG--------"
            ftext += "\nDate: " + date
            ftext += "\nGroup ID: " + str(errors.chat_id)
            ftext += "\nSender ID: " + str(errors.sender_id)
            ftext += "\n\nEvent Trigger:\n"
            ftext += str(errors.text)
            ftext += "\n\nTraceback info:\n"
            ftext += str(traceback.format_exc())
            ftext += "\n\nError text:\n"
            ftext += str(sys.exc_info()[1])
            ftext += "\n\n--------𝓔𝓝𝓓 𝓓3𝓥𝓘𝓛𝓑𝓞𝓣 𝓣𝓡𝓐𝓒𝓔𝓑𝓐𝓒𝓚 𝓛𝓞𝓖--------"

            command = "git log --pretty=format:\"%an: %s\" -5"

            ftext += "\n\n\nLast 5 commits:\n"

            process = await asyncio.create_subprocess_sd3vil(
                command,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE)
            stdout, stderr = await process.communicate()
            result = str(stdout.decode().strip()) \
                + str(stderr.decode().strip())

            ftext += result

    return wrapper

#Assistant
def start_assistant(shortname):
    if shortname.startswith("__"):
        pass
    elif shortname.endswith("_"):
        import importlib
        import sys
        from pathlib import Path

        path = Path(f"d3vilbot/assistant/{shortname}.py")
        name = "d3vilbot.assistant.{}".format(shortname)
        spec = importlib.util.spec_from_file_location(name, path)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        print("Starting Your Assistant Bot.")
        print("Assistant Sucessfully imported " + shortname)
    else:
        import importlib
        import sys
        from pathlib import Path

        path = Path(f"d3vilbot/assistant/{shortname}.py")
        name = "d3vilbot.assistant.{}".format(shortname)
        spec = importlib.util.spec_from_file_location(name, path)
        mod = importlib.util.module_from_spec(spec)
        mod.tgbot = bot.tgbot
        spec.loader.exec_module(mod)
        sys.modules["d3vilbot.assistant" + shortname] = mod
        print("Assistant Has imported " + shortname) 

#Assistant
def start_assistant(shortname):
    if shortname.startswith("__"):
        pass
    elif shortname.endswith("_"):
        import importlib
        import sys
        from pathlib import Path

        path = Path(f"d3vilbot/assistant/{shortname}.py")
        name = "d3vilbot.assistant.{}".format(shortname)
        spec = importlib.util.spec_from_file_location(name, path)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        print("Starting Your Assistant Bot.")
        print("Assistant Sucessfully imported " + shortname)
    else:
        import importlib
        import sys
        from pathlib import Path

        path = Path(f"d3vilbot/assistant/{shortname}.py")
        name = "d3vilbot.assistant.{}".format(shortname)
        spec = importlib.util.spec_from_file_location(name, path)
        mod = importlib.util.module_from_spec(spec)
        mod.tgbot = bot.tgbot
        spec.loader.exec_module(mod)
        sys.modules["d3vilbot.assistant" + shortname] = mod
        print("[⚡Assistant⚡ 2.0] ~ HAS ~ •Installed۝۝" + shortname)  

#Addons...

def load_addons(shortname):
    if shortname.startswith("__"):
        pass
    elif shortname.endswith("_"):
        import userbot.utils
        import sys
        import importlib
        from pathlib import Path
        path = Path(f"D3VILADDONS/{shortname}.py")
        name = "D3VILADDONS.{}".format(shortname)
        spec = importlib.util.spec_from_file_location(name, path)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        LOGS.info("♦️Extra Plugin♦️ ~ " + shortname)
    else:
        import userbot.utils
        import sys
        import importlib
        from pathlib import Path
        path = Path(f"D3VILADDONS/{shortname}.py")
        name = "D3VILADDONS.{}".format(shortname)
        spec = importlib.util.spec_from_file_location(name, path)
        mod = importlib.util.module_from_spec(spec)
#        mod.d3vil = d3vil
        mod.bot = bot
        mod.bot = bot
#        mod.command = command
        mod.borg = bot
        mod.d3vilbot = bot
        mod.tgbot = bot.tgbot
        mod.Var = Config
        mod.Config = Config
#        mod.edit_or_reply = edit_or_reply
        mod.delete_d3vil = delete_d3vil
        mod.eod = delete_d3vil
        mod.admin_cmd = d3vil_cmd
        mod.logger = logging.getLogger(shortname)
        # support for D3VILBOT originals
        sys.modules["userbot.utils"] = d3vilbot.utils
        sys.modules["userbot"] = d3vilbot
        # support for paperplaneextended
        sys.modules["userbot.events"] = d3vilbot
        spec.loader.exec_module(mod)
        # for imports
        sys.modules["D3VILADDONS." + shortname] = mod
        LOGS.info("🔱Extra Plugin🔱 ~ " + shortname)
#d3vilbot
