from telethon import events
from telethon.utils import pack_bot_file_id

from . import *

# outgoing


@tgbot.on(events.NewMessage(func=lambda e: e.is_private))
async def on_out_mssg(event):
    x = await event.get_reply_message()
    if x is None:
        return
    to_send = event.raw_text
    who = event.sender_id
    if x.fwd_from:
        to_user = x.fwd_from.sender_id.user_id
    else:
        # this is a weird way of doing it
        return
    if who == OWNER_ID:
        if to_send.startswith("/"):
            return
        if event.text is not None and event.media:
            # if sending media
            bot_api_file_id = pack_bot_file_id(event.media)
            await tgbot.send_file(
                to_user,
                file=bot_api_file_id,
                caption=event.text,
                reply_to=x.reply_to_msg_id,
            )
        else:
            await tgbot.send_message(to_user, to_send, reply_to=x.reply_to_msg_id)
