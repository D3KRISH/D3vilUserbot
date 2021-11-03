import os

from telegraph import Telegraph, upload_file

from . import *

# --------------------------------------------------------------------#
telegraph = Telegraph()
r = telegraph.create_account(short_name="D3vil")
auth_url = r["auth_url"]
# --------------------------------------------------------------------#


@callback("alvcstm")
@owner
async def alvcs(event):
    await event.edit(
        "Customise your {}alive. Choose from the below options -".format(HNDLR),
        buttons=[
            [Button.inline("Aʟɪᴠᴇ Tᴇxᴛ", data="alvtx")],
            [Button.inline("Aʟɪᴠᴇ ᴍᴇᴅɪᴀ", data="alvmed")],
            [Button.inline("Dᴇʟᴇᴛᴇ Aʟɪᴠᴇ Mᴇᴅɪᴀ", data="delmed")],
            [Button.inline("« Bᴀᴄᴋ", data="setter")],
        ],
    )


@callback("alvtx")
@owner
async def name(event):
    await event.delete()
    pru = event.sender_id
    var = "ALIVE_MSG"
    name = "Alive Text"
    async with event.client.conversation(pru) as conv:
        await conv.send_message(
            "**Alive Text**\nEnter the new alive text.\n\nUse /cancel to terminate the operation."
        )
        response = conv.wait_event(events.NewMessage(chats=pru))
        response = await response
        themssg = response.message.message
        if themssg == "/cancel":
            return await conv.send_message("Cancelled!!")
        else:
            await setit(event, var, themssg)
            await conv.send_message(
                "{} changed to {}\n\nAfter Setting All Things Do restart".format(
                    name, themssg
                )
            )


@callback("alvmed")
@owner
async def media(event):
    await event.delete()
    pru = event.sender_id
    var = "ALIVE_PIC"
    name = "Alive Media"
    async with event.client.conversation(pru) as conv:
        await conv.send_message(
            "**Alive Media**\nSend me a pic/gif/bot api id of sticker to set as alive media.\n\nUse /cancel to terminate the operation."
        )
        response = await conv.get_response()
        try:
            themssg = response.message.message
            if themssg == "/cancel":
                return await conv.send_message("Operation cancelled!!")
        except BaseException:
            pass
        media = await event.client.download_media(response, "alvpc")
        if not (response.text).startswith("/") and not response.text == "":
            url = response.text
        else:
            try:
                x = upload_file(media)
                url = f"https://telegra.ph/{x[0]}"
                os.remove(media)
            except BaseException:
                return await conv.send_message("Terminated.")
        await setit(event, var, url)
        await conv.send_message("{} has been set.".format(name))


@callback("delmed")
@owner
async def dell(event):
    try:
        udB.delete("ALIVE_PIC")
        return await event.edit("Done!")
    except BaseException:
        return await event.edit("Something went wrong...")


@callback("pmcstm")
@owner
async def alvcs(event):
    await event.edit(
        "Customise your PMPERMIT Settings -",
        buttons=[
            [Button.inline("Pᴍ Mᴇᴅɪᴀ", data="pmmed")],
            [Button.inline("Dᴇʟᴇᴛᴇ Pᴍ Mᴇᴅɪᴀ", data="delpmmed")],
            [Button.inline("« Bᴀᴄᴋ", data="pmset")],
        ],
    )



@callback("pmmed")
@owner
async def media(event):
    await event.delete()
    pru = event.sender_id
    var = "PMPERMIT_PIC"
    name = "PM Media"
    async with event.client.conversation(pru) as conv:
        await conv.send_message(
            "**PM Media**\nSend me a pic/gif/bot api id of sticker to set as pmpermit media.\n\nUse /cancel to terminate the operation."
        )
        response = await conv.get_response()
        try:
            themssg = response.message.message
            if themssg == "/cancel":
                return await conv.send_message("Operation cancelled!!")
        except BaseException:
            pass
        media = await event.client.download_media(response, "pmpcc")
        if not (response.text).startswith("/") and not response.text == "":
            url = response.text
        else:
            try:
                x = upload_file(media)
                url = f"https://telegra.ph/{x[0]}"
                os.remove(media)
            except BaseException:
                return await conv.send_message("Terminated.")
        await setit(event, var, url)
        await conv.send_message("{} has been set.".format(name))


@callback("delpmmed")
@owner
async def dell(event):
    try:
        udB.delete("PMPERMIT_PIC")
        return await event.edit("Done!")
    except BaseException:
        return await event.edit("Something went wrong...")



@callback("pmset")
@owner
async def pmset(event):
    await event.edit(
        "PMPermit Settings:",
        buttons=[
            [Button.inline("Tᴜʀɴ PMPᴇʀᴍɪᴛ Oɴ", data="pmon")],
            [Button.inline("Tᴜʀɴ PMPᴇʀᴍɪᴛ Oғғ", data="pmoff")],
            [Button.inline("Cᴜsᴛᴏᴍɪᴢᴇ PMPᴇʀᴍɪᴛ", data="pmcstm")],
            [Button.inline("« Bᴀᴄᴋ", data="setter")],
        ],
    )


@callback("pmon")
@owner
async def pmonn(event):
    var = "PM_PERMIT"
    await setit(event, var, "ENABLE")
    await event.edit(f"Done! PMPermit has been turned on!!")


@callback("pmoff")
@owner
async def pmofff(event):
    var = "PMSETTING"
    await setit(event, var, "DISABLE")
    await event.edit(f"Done! PMPermit has been turned off!!")

