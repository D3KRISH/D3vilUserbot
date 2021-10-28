import os
from . import *
from multiutility import EmojiCreator

Emoji = EmojiCreator()

@borg.on(d3vil_cmd(pattern="randomoji", outgoing=True))  # pylint:disable=E0602
@borg.on(sudo_cmd(pattern="randomoji"))
async def _(event):
    mmmm = await edit_or_reply(event, "**Generating Your Random Emoji ⏰✍️**")
    emoji = Emoji.get_random()
    await event.respond("**--- Random Emoji For You ---**", file=emoji)
    os.remove(emoji)
    await mmmm.delete()
 
 
CmdHelp("randomemoji").add_command(
  "randomoji", None, "Get Random Emoji as Image."
).add()
