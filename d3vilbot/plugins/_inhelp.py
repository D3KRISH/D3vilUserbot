from math import ceil
from re import compile
import asyncio
import html
import os
import re
import sys

from telethon import Button, custom, events, functions
from telethon.tl.functions.users import GetFullUserRequest
from telethon.events import InlineQuery, callbackquery
from telethon.sync import custom
from telethon.errors.rpcerrorlist import UserNotParticipantError
from telethon.tl.functions.channels import GetParticipantRequest
from telethon.tl.functions.channels import JoinChannelRequest
from telethon.tl.functions.messages import ExportChatInviteRequest

from . import *

d3vil_row = Config.BUTTONS_IN_HELP
d3vil_emoji = Config.EMOJI_IN_HELP
d3vil_pic = Config.PMPERMIT_PIC or "https://telegra.ph/file/ad8abbfbcb2f93f91b10f.jpg"
cstm_pmp = Config.CUSTOM_PMPERMIT
ALV_PIC = Config.ALIVE_PIC

PM_WARNS = {}
PREV_REPLY_MESSAGE = {}

mybot = Config.BOT_USERNAME
if mybot.startswith("@"):
    botname = mybot
else:
    botname = f"@{mybot}"
LOG_GP = Config.LOGGER_ID
mssge = (
    str(cstm_pmp)
    if cstm_pmp
    else "**๐ธ๐๐ ๐ง๐บ๐๐พ ๐ณ๐๐พ๐๐๐บ๐๐๐พ๐ฝ ๐ณ๐ ๐ฌ๐ ๐ฌ๐บ๐๐๐พ๐'๐ ๐ฏ๐ฌ!\n๐ณ๐๐๐ ๐จ๐ ๐จ๐๐๐พ๐๐บ๐ ๐ ๐๐ฝ ๐ฑ๐พ๐๐บ๐๐ฝ๐พ๐ฝ ๐ ๐ ๐ข๐๐๐๐พ.**"
)

USER_BOT_WARN_ZERO = "๐ธ๐๐ ๐๐พ๐๐พ ๐๐๐บ๐๐๐๐๐ ๐๐ ๐๐๐พ๐พ๐ ๐๐บ๐๐๐พ๐'๐ ๐๐๐ป๐๐, ๐๐พ๐๐ผ๐พ๐ฟ๐๐๐๐ ๐๐๐ ๐๐บ๐๐พ ๐ป๐พ๐พ๐ ๐ป๐๐๐ผ๐๐พ๐ฝ ๐ป๐ ๐๐ ๐๐บ๐๐๐พ๐'๐ ๐ฃ3๐๐๐๐ก๐๐.**\n__๐ญ๐๐ ๐ฆ๐ณ๐ฅ๐ฎ, ๐'๐ ๐ป๐๐๐**"

D3VIL_FIRST = (
    "**Hello, ๐ณ๐๐๐ ๐๐ แช3แแฅแแฐแงแ ๐ด๐๐๐๐บ ๐ฏ๐๐๐๐บ๐๐พ ๐ฒ๐พ๐ผ๐๐๐๐๐ ๐ฏ๐๐๐๐๐ผ๐๐โ ๏ธ **\n ๐ณ๐๐๐ ๐๐ ๐๐ ๐๐๐ฟ๐๐๐ ๐๐๐ ๐๐๐บ๐ "
    "{} ๐๐ ๐ผ๐๐๐๐พ๐๐๐๐ ๐๐๐บ๐๐บ๐๐๐บ๐ป๐๐พ. ๐ณ๐๐๐ ๐๐ ๐บ๐ ๐บ๐๐๐๐๐บ๐๐พ๐ฝ ๐๐พ๐๐๐บ๐๐พ.\n\n"
    "{}\n\n**๐ฏ๐๐พ๐บ๐๐พ ๐ข๐๐๐๐๐พ ๐ถ๐๐ ๐ธ๐๐ ๐ ๐๐พ Inbox ๐!!**".format(d3vil_mention, mssge))

alive_txt = """
**โ๏ธ ๐3๐๐๐๐๐๐ ๐๐ ๐๐๐๐๐๐ โ๏ธ**
{}
**โผ๐ ๐๐ฆ๐ง๐๐ฅโ   :**     **ใ{}ใ**
**โโโโโโโโโโโโโโโโโโโโ
**โ โณโ  ๐ง๐ฒ๐น๐ฒ๐๐ต๐ผ๐ป :**  `{}`
**โ โณโ  ๐3๐ฉ๐๐๐๐ข๐ง  :**  **{}**
**โ โณโ  ๐จ๐ฝ๐๐ถ๐บ๐ฒ   :**  `{}`
**โ โณโ  ๐๐ฏ๐๐๐ฒ    :**  **{}**
**โ โณโ  ๐ฆ๐๐ฑ๐ผ      :**  **{}**
**โโโโโโโโโโโโโโโโโโโโ
"""

def button(page, modules):
    Row = d3vil_row
    Column = 3

    modules = sorted([modul for modul in modules if not modul.startswith("_")])
    pairs = list(map(list, zip(modules[::3], modules[1::3])))
    if len(modules) % 2 == 1:
        pairs.append([modules[-1]])
    max_pages = ceil(len(pairs) / Row)
    pairs = [pairs[i : i + Row] for i in range(0, len(pairs), Row)]
    buttons = []
    for pairs in pairs[page]:
        buttons.append(
            [
                custom.Button.inline(f"{d3vil_emoji} " + pair + f" {d3vil_emoji}", data=f"Information[{page}]({pair})")
                for pair in pairs
            ]
        )

    buttons.append(
        [
            custom.Button.inline(
               f"โ๏ธ๏ธ๏ธ ๐ฑ๐ฐ๐ฒ๐บเผ {d3vil_emoji}", data=f"page({(max_pages - 1) if page == 0 else (page - 1)})"
            ),
            custom.Button.inline(
               f"โข โ โข", data="close"
            ),
            custom.Button.inline(
               f"{d3vil_emoji} เผ๐ฝ๐ด๐๐ โ๏ธ๏ธ๏ธ", data=f"page({0 if page == (max_pages - 1) else page + 1})"
            ),
        ]
    )
    return [max_pages, buttons]


    modules = CMD_HELP
if Config.BOT_USERNAME is not None and tgbot is not None:
    @tgbot.on(InlineQuery)  # pylint:disable=E0602
    async def inline_handler(event):
        builder = event.builder
        result = None
        query = event.text
        if event.query.user_id == bot.uid and query == "d3vilbot_d3vlp":
            rev_text = query[::-1]
            veriler = button(0, sorted(CMD_HELP))
            apn = []
            for x in CMD_LIST.values():
                for y in x:
                    apn.append(y)
            result = await builder.article(
                f"Hey! Only use .help please",
                text=f"**ใ{d3vil_mention}ใ**\n\n๐**๐๐๐๐๐ ๐ผ๐๐๐๐๐๐ ๐ธ๐๐๐๐๐๐๐๐** โญ `{len(CMD_HELP)}` \n๐**Tฮฟฯฮฑโ Cฮฟะผะผฮฑะธโั** โญ `{len(apn)}`\n**๐Pฮฑึาฝโญ** 1/{veriler[0]}",
                buttons=veriler[1],
                link_preview=False,
            )
        elif event.query.user_id == bot.uid and query.startswith("fsub"):
            hunter = event.pattern_match.group(1)
            d3vil = hunter.split("+")
            user = await bot.get_entity(int(d3vil[0]))
            channel = await bot.get_entity(int(d3vil[1]))
            msg = f"**๐ ๐๐พ๐๐ผ๐๐๐พ** [{user.first_name}](tg://user?id={user.id}), \n\n** ๐ธ๐๐ ๐๐พ๐พ๐ฝ ๐๐ ๐ฉ๐๐๐** {channel.title} **๐๐ ๐ผ๐๐บ๐ ๐๐ ๐๐๐๐ ๐๐๐๐๐.**"
            if not channel.username:
                link = (await bot(ExportChatInviteRequest(channel))).link
            else:
                link = "https://t.me/" + channel.username
            result = [
                await builder.article(
                    title="force_sub",
                    text = msg,
                    buttons=[
                        [Button.url(text="Channel", url=link)],
                        [custom.Button.inline("๐ ๐ด๐๐๐๐๐พ ๐ฌ๐พ", data=unmute)],
                    ],
                )
            ]

        elif event.query.user_id == bot.uid and query == "alive":
            kr_ish = alive_txt.format(Config.ALIVE_MSG, d3vil_mention, tel_ver, d3vil_ver, uptime, abuse_m, is_sudo)
            alv_btn = [
                [Button.url(f"{D3VIL_USER}", f"tg://openmessage?user_id={d3krish}")],
                [Button.url("๐ฌ๐ ๐ข๐๐บ๐๐๐พ๐", f"https://t.me/{my_channel}"), 
                Button.url("๐ฌ๐ ๐ฆ๐๐๐๐", f"https://t.me/{my_group}")],
            ]
            if ALV_PIC and ALV_PIC.endswith((".jpg", ".png")):
                result = builder.photo(
                    ALV_PIC,
                    text=kr_ish,
                    buttons=alv_btn,
                    link_preview=False,
                )
            elif ALV_PIC:
                result = builder.document(
                    ALV_PIC,
                    text=kr_ish,
                    title="D3vilBot Alive",
                    buttons=alv_btn,
                    link_preview=False,
                )
            else:
                result = builder.article(
                    text=kr_ish,
                    title="D3vilBot Alive",
                    buttons=alv_btn,
                    link_preview=False,
                )

        elif event.query.user_id == bot.uid and query == "pm_warn":
            d3vl_l = D3VIL_FIRST.format(d3vil_mention, mssge)
            result = builder.photo(
                file=d3vil_pic,
                text=d3vl_l,
                buttons=[
                    [
                        custom.Button.inline("๐ซ ๐ฒ๐๐บ๐/๐ฒ๐ผ๐บ๐ ๐ซ", data="teamd3"),
                        custom.Button.inline("๐ฌ ๐ข๐๐บ๐ ๐ฌ", data="chat"),
                    ],
                    [custom.Button.inline("๐ ๐ฑ๐พ๐๐๐พ๐๐ ๐", data="req")],
                    [custom.Button.inline("๐ข๐๐๐๐๐๐ โ", data="pmclick")],
                ],
            )

        elif event.query.user_id == bot.uid and query == "repo":
            result = builder.article(
                title="Repository",
                text=f"**[โ๏ธ ๐ป๐ด๐ถ๐ด๐ฝ๐ณ๐ฐ๐๐ ๐ฐ๐ต ๐๐ด๐ฐ๐ผ ๐ณ3๐๐ธ๐ป โ๏ธ](https://t.me/D3VIL_BOT_OFFICIAL)**",
                buttons=[
                    [Button.url("๐ ๐ฑ๐พ๐๐ ๐", "https://github.com/TEAM-D3VIL/D3vilBot")],
                    [Button.url("๐ ๐ฃ๐พ๐๐๐๐ ๐", "https://dashboard.heroku.com/new?button-url=https%3A%2F%2Fgithub.com%2FTEAM-D3VIL%2FD3vilBot&template=https%3A%2F%2Fgithub.com%2FTEAM-D3VIL%2FD3vilBot")],
                    [Button.url("โต ๐ฎ๐๐๐พ๐ โต", "https://t.me/D3_krish")],
                ],
            )

        elif query.startswith("http"):
            part = query.split(" ")
            result = builder.article(
                "File uploaded",
                text=f"**๐ฅ๐๐๐พ ๐๐๐๐๐บ๐ฝ๐พ๐ฝ ๐๐๐ผ๐ผ๐พ๐๐๐ฟ๐๐๐๐ ๐๐ {part[2]} site.\๐๐ด๐๐๐๐ฝ๐พ๐ฝ ๐ณ๐๐๐พ : {part[1][:3]} ๐๐พ๐ผ๐๐๐ฝ\n[โโโ โ]({part[0]})",
                buttons=[[custom.Button.url("URL", part[0])]],
                link_preview=True,
            )

        else:
            result = builder.article(
                "D3VIL_BOT_OFFICIAL",
                text="""**๐ง๐พ๐! ๐ณ๐๐๐ ๐๐ [โโข๐ณ3๐๐ธ๐ป๐ฑ๐พ๐โขโ](https://t.me/D3VIL_OP_BOLTE) \n ๐ธo๐ ๐ผ๐บ๐ ๐๐๐๐ ๐๐๐๐พ ๐บ๐ป๐๐๐ ๐๐พ ๐ฟ๐๐๐ ๐๐๐พ ๐๐๐๐๐ ๐๐๐๐พ๐ ๐ป๐พ๐๐๐ ๐**""",
                buttons=[
                    [
                        custom.Button.url("๐ฅ ๐ฒ๐ท๐ฐ๐ฝ๐ฝ๐ด๐ป ๐ฅ", "https://t.me/D3VIL_BOT_OFFICIAL"),
                        custom.Button.url(
                            "โก ๐ถ๐๐พ๐๐ฟ โก", "https://t.me/D3VIL_BOT_SUPPORT"
                        ),
                    ],
                    [
                        custom.Button.url(
                            "โจ ๐๐ด๐ฟ๐พ โจ", "https://github.com/D3KRISH/D3vilBot"),
                        custom.Button.url
                    (
                            "๐ฐ ๐๐๐๐พ๐๐ธ๐ฐ๐ป ๐ฐ", "https://youtu.be/PHJ3O34Pvc0"
                    )
                    ],
                ],
                link_preview=False,
            )
        await event.answer([result] if result else None)


    @tgbot.on(callbackquery.CallbackQuery(data=compile(b"pmclick")))
    async def on_pm_click(event):
        if event.query.user_id == bot.uid:
            reply_pop_up_alert = "๐ณ๐๐๐ ๐๐ ๐ฟ๐๐ ๐ฎ๐๐๐พ๐ ๐ด๐๐พ๐๐..."
            await event.answer(reply_pop_up_alert, cache_time=0, alert=True)
        else:
            await event.edit(
                f" ๐ณ๐๐๐ ๐๐ แช3แแฅแแฐแงแ๐ฏ๐ ๐ฒ๐พ๐ผ๐๐๐๐๐ ๐ฟ๐๐ {d3vil_mention} ๐๐ ๐๐พ๐พ๐ ๐บ๐๐บ๐ ๐๐๐๐บ๐๐๐พ๐ฝ ๐๐พ๐๐บ๐๐ฝ๐ ๐ฟ๐๐๐ ๐๐๐บ๐๐๐๐๐ ๐ฏ๐ฌ..."
            )

    @tgbot.on(callbackquery.CallbackQuery(data=compile(b"req")))
    async def on_pm_click(event):
        if event.query.user_id == bot.uid:
            reply_pop_up_alert = "๐ณ๐๐๐ ๐๐ ๐ฟ๐๐ ๐๐๐๐พ๐ ๐๐๐พ๐๐!"
            await event.answer(reply_pop_up_alert, cache_time=0, alert=True)
        else:
            await event.edit(
                f"โ **๐ฑ๐พ๐๐๐พ๐๐ ๐ฑ๐พ๐๐๐๐๐พ๐๐พ๐ฝ** \n\n{d3vil_mention} ๐๐๐๐ ๐๐๐ ๐ฝ๐พ๐ผ๐๐ฝ๐พ ๐๐ ๐๐๐๐ ๐ฟ๐๐ ๐๐๐๐ ๐๐พ๐๐๐พ๐๐ ๐๐ ๐๐๐.\n๐ ๐ณ๐๐๐ ๐๐๐พ๐ ๐๐บ๐๐ ๐บ๐๐ฝ ๐ฝ๐๐'๐ ๐๐๐บ๐!!"
            )
            target = await event.client(GetFullUserRequest(event.query.user_id))
            first_name = html.escape(target.user.first_name)
            ok = event.query.user_id
            if first_name is not None:
                first_name = first_name.replace("\u2060", "")
            tosend = f"**๐ ๐ง๐พ๐ {d3vil_mention} !!** \n\nโ๏ธ ๐ธ๐๐ ๐ฆ๐๐ ๐  ๐ฑ๐พ๐๐๐พ๐๐ ๐ฅ๐๐๐ [{first_name}](tg://user?id={ok}) ๐จ๐ ๐ฏ๐!!"
            await bot.send_message(LOG_GP, tosend)


    @tgbot.on(callbackquery.CallbackQuery(data=compile(b"chat")))
    async def on_pm_click(event):
        event.query.user_id
        if event.query.user_id == bot.uid:
            reply_pop_up_alert = "๐ณ๐๐๐ ๐๐ ๐ฟ๐๐ ๐๐๐๐พ๐ ๐๐๐พ๐๐!"
            await event.answer(reply_pop_up_alert, cache_time=0, alert=True)
        else:
            await event.edit(
                f"๐ ๐๐!! ๐ธ๐๐ ๐๐พ๐๐พ ๐๐ ๐ฝ๐ chat!!\n ๐ฏ๐๐พ๐บ๐๐พ ๐๐บ๐๐ ๐ฟ๐๐ {d3vil_mention} ๐๐ ๐ผ๐๐๐พ. ๐ณ๐๐๐ ๐๐๐พ๐ ๐๐พ๐พ๐ ๐๐บ๐๐๐พ๐๐ผ๐พ ๐บ๐๐ฝ ๐ฝ๐๐'๐ ๐๐๐บ๐."
            )
            target = await event.client(GetFullUserRequest(event.query.user_id))
            ok = event.query.user_id
            first_name = html.escape(target.user.first_name)
            if first_name is not None:
                first_name = first_name.replace("\u2060", "")
            tosend = f"**๐ ๐ง๐พ๐ {d3vil_mention} !!** \n\n โ๏ธ ๐ธ๐๐ ๐ฆ๐๐ ๐  ๐ฏ๐ฌ ๐ฟ๐๐๐  [{first_name}](tg://user?id={ok})  ๐ฟ๐๐ ๐๐บ๐๐ฝ๐๐ ๐ผ๐๐บ๐๐!!"
            await bot.send_message(LOG_GP, tosend)


    @tgbot.on(callbackquery.CallbackQuery(data=compile(b"teamd3")))
    async def on_pm_click(event):
        if event.query.user_id == bot.uid:
            reply_pop_up_alert = "๐ณ๐๐๐ ๐๐ ๐ฟ๐๐ ๐๐๐๐พ๐ ๐๐๐พ๐๐!"
            await event.answer(reply_pop_up_alert, cache_time=0, alert=True)
        else:
            await event.edit(
                f"๐ฅด **๐ญ๐๐๐บ๐ ๐๐บ๐ฝ๐พ๐๐ผ๐๐๐ฝ\n ๐ฏ๐พ๐๐๐ ๐ฟ๐๐๐๐บ๐ ๐๐พ ๐๐๐๐บ๐**"
            )
            await bot(functions.contacts.BlockRequest(event.query.user_id))
            target = await event.client(GetFullUserRequest(event.query.user_id))
            ok = event.query.user_id
            first_name = html.escape(target.user.first_name)
            if first_name is not None:
                first_name = first_name.replace("\u2060", "")
            first_name = html.escape(target.user.first_name)
            await bot.send_message(
                LOG_GP,
                f"**๐ก๐๐๐ผ๐๐พ๐ฝ**  [{first_name}](tg://user?id={ok}) \n\๐๐ฑ๐พ๐บ๐๐๐:- ๐ฒ๐๐บ๐",
            )


    @tgbot.on(callbackquery.CallbackQuery(data=compile(b"unmute")))
    async def on_pm_click(event):
        hunter = (event.data_match.group(1)).decode("UTF-8")
        d3vil = hunter.split("+")
        if not event.sender_id == int(d3vil[0]):
            return await event.answer("๐ณ๐๐๐ ๐ ๐๐'๐ ๐ฅ๐๐ ๐ธ๐๐!!", alert=True)
        try:
            await bot(GetParticipantRequest(int(d3vil[1]), int(d3vil[0])))
        except UserNotParticipantError:
            return await event.answer(
                "You need to join the channel first.", alert=True
            )
        await bot.edit_permissions(
            event.chat_id, int(d3vil[0]), send_message=True, until_date=None
        )
        await event.edit("๐ธ๐บ๐! ๐ธ๐๐ ๐ผ๐บ๐ ๐ผ๐๐บ๐ ๐๐๐ !!")


    @tgbot.on(callbackquery.CallbackQuery(data=compile(b"reopen")))
    async def reopn(event):
            if event.query.user_id == bot.uid or event.query.user_id in Config.SUDO_USERS:
                current_page_number=0
                simp = button(current_page_number, CMD_HELP)
                veriler = button(0, sorted(CMD_HELP))
                apn = []
                for x in CMD_LIST.values():
                    for y in x:
                        apn.append(y)
                await event.edit(
                    f"**ใ{d3vil_mention}ใ**\n\n๐ **๐๐๐๐๐ ๐ผ๐๐๐๐๐๐ ๐ธ๐๐๐๐๐๐๐๐** โญ `{len(CMD_HELP)}` \n๐ **Tฮฟฯฮฑโ Cฮฟะผะผฮฑะธโั** โญ `{len(apn)}`\n๐ **Pฮฑึาฝ** โญ 1/{veriler[0]}",
                    buttons=simp[1],
                    link_preview=False,
                )
            else:
                reply_pop_up_alert = "๐ง๐๐ ๐๐๐บ ๐บ๐๐๐บ. ๐ช๐บ๐ป๐๐พ ๐๐บ๐๐บ๐ ๐๐บ๐๐บ๐ ๐ฝ๐บ๐ป๐บ๐พ ๐๐บ๐บ ๐๐๐พ ๐. ๐๐๐๐ฝ๐๐บ ๐ป๐๐บ ๐๐ ๐๐บ ๐บ๐๐ ๐ผ๐๐๐๐พ ๐๐. ยฉ แช3แแฅแแฐแงแโข"
                await event.answer(reply_pop_up_alert, cache_time=0, alert=True)
        

    @tgbot.on(callbackquery.CallbackQuery(data=compile(b"close")))
    async def on_plug_in_callback_query_handler(event):
        if event.query.user_id == bot.uid or event.query.user_id in Config.SUDO_USERS:
            veriler = custom.Button.inline(f"{d3vil_emoji} Re-Open Menu {d3vil_emoji}", data="reopen")
            await event.edit(f"**โ๏ธ แช3vฮนโะฒฯั ๐ฌรชรฑรป ๐ฏ๐รต๐รฎ๐ฝรช๐ รฌ๐ รฑรด๐ ร๐รถ๐รซ๐ฝ โ๏ธ**\n\n**๐ฌ๐บ๐๐๐พ๐ :**  {d3vil_mention}\n\n        [ยฉ๏ธ แช3แแฅแแฐแงแโข๏ธ]({chnl_link})", buttons=veriler, link_preview=False)
        else:
            reply_pop_up_alert = "๐ง๐พ๐๐๐ ๐๐๐พ๐๐พ ๐ฃ๐พ๐๐๐๐ ๐๐๐๐ ๐๐๐ ๐ฃ3๐ต๐จ๐ซ๐ก๐ฎ๐ณ ๐บ๐๐ฝ ๐๐๐พ. ยฉ แช3แแฅแแฐแงแโข"
            await event.answer(reply_pop_up_alert, cache_time=0, alert=True)
   

    @tgbot.on(callbackquery.CallbackQuery(data=compile(b"page\((.+?)\)")))
    async def page(event):
        page = int(event.data_match.group(1).decode("UTF-8"))
        veriler = button(page, CMD_HELP)
        apn = []
        for x in CMD_LIST.values():
            for y in x:
                apn.append(y)
        if event.query.user_id == bot.uid or event.query.user_id in Config.SUDO_USERS:
            await event.edit(
                f" **ใ{d3vil_mention}ใ**\n\n๐**๐๐๐๐๐ ๐ผ๐๐๐๐๐๐ ๐ธ๐๐๐๐๐๐๐๐** โญ  `{len(CMD_HELP)}` \n๐ **Tฮฟฯฮฑโ Cฮฟะผะผฮฑะธโั** โญ `{len(apn)}`\n๐ **Pฮฑึาฝ** โญ 1/{veriler[0]}",
                buttons=veriler[1],
                link_preview=False,
            )
        else:
            return await event.answer(
                "๐ง๐พ๐๐๐ ๐๐๐พ๐๐พ ๐ฃ๐พ๐๐๐๐ ๐๐๐๐ ๐๐๐ ๐ฃ3๐ต๐จ๐ซ๐ก๐ฎ๐ณ ๐บ๐๐ฝ ๐๐๐พ. ยฉ แช3แแฅแแฐแงแโข",
                cache_time=0,
                alert=True,
            )


    @tgbot.on(
        callbackquery.CallbackQuery(data=compile(b"Information\[(\d*)\]\((.*)\)"))
    )
    async def Information(event):
        page = int(event.data_match.group(1).decode("UTF-8"))
        commands = event.data_match.group(2).decode("UTF-8")
        try:
            buttons = [
                custom.Button.inline(
                    "โ " + cmd[0] + " โ", data=f"commands[{commands}[{page}]]({cmd[0]})"
                )
                for cmd in CMD_HELP_BOT[commands]["commands"].items()
            ]
        except KeyError:
            return await event.answer(
                "๐ญ๐ ๐ฃ๐พ๐๐ผ๐๐๐๐๐๐๐ ๐๐ ๐๐๐๐๐๐พ๐ ๐ฟ๐๐ ๐๐๐๐ ๐๐๐๐๐๐", cache_time=0, alert=True
            )

        buttons = [buttons[i : i + 2] for i in range(0, len(buttons), 2)]
        buttons.append([custom.Button.inline(f"{d3vil_emoji} Main Menu {d3vil_emoji}", data=f"page({page})")])
        if event.query.user_id == bot.uid or event.query.user_id in Config.SUDO_USERS:
            await event.edit(
                f"**๐ ๐ฅ๐๐๐พ :**  `{commands}`\n**๐ข ๐ญ๐๐๐ป๐พ๐ ๐๐ฟ ๐ผ๐๐๐๐บ๐๐ฝ๐ :**  `{len(CMD_HELP_BOT[commands]['commands'])}`",
                buttons=buttons,
                link_preview=False,
            )
        else:
            return await event.answer(
                "๐ง๐พ๐๐๐ ๐๐๐พ๐๐พ ๐ฃ๐พ๐๐๐๐ ๐๐๐๐ ๐๐๐ ๐ฃ3๐ต๐จ๐ซ๐ก๐ฎ๐ณ ๐บ๐๐ฝ ๐๐๐พ. ยฉ แช3แแฅแแฐแงแโข",
                cache_time=0,
                alert=True,
            )


    @tgbot.on(
        callbackquery.CallbackQuery(data=compile(b"commands\[(.*)\[(\d*)\]\]\((.*)\)"))
    )
    async def commands(event):
        cmd = event.data_match.group(1).decode("UTF-8")
        page = int(event.data_match.group(2).decode("UTF-8"))
        commands = event.data_match.group(3).decode("UTF-8")
        result = f"**๐ ๐ฅ๐๐๐พ :**  `{cmd}`\n"
        if CMD_HELP_BOT[cmd]["info"]["info"] == "":
            if not CMD_HELP_BOT[cmd]["info"]["warning"] == "":
                result += f"**โ ๏ธ ๐ถ๐บ๐๐๐๐๐ :**  {CMD_HELP_BOT[cmd]['info']['warning']}\n\n"
        else:
            if not CMD_HELP_BOT[cmd]["info"]["warning"] == "":
                result += f"**โ ๏ธ ๐ถ๐บ๐๐๐๐๐ :**  {CMD_HELP_BOT[cmd]['info']['warning']}\n"
            result += f"**โน๏ธ ๐จ๐๐ฟ๐ :**  {CMD_HELP_BOT[cmd]['info']['info']}\n\n"
        command = CMD_HELP_BOT[cmd]["commands"][commands]
        if command["params"] is None:
            result += f"**๐  ๐ข๐๐๐๐บ๐๐ฝ๐ :**  `{HANDLER[:1]}{command['command']}`\n"
        else:
            result += f"**๐  ๐ข๐๐๐๐บ๐๐ฝ๐ :**  `{HANDLER[:1]}{command['command']} {command['params']}`\n"
        if command["example"] is None:
            result += f"**๐ฌ ๐ค๐๐๐๐บ๐๐บ๐๐๐๐ :**  `{command['usage']}`\n\n"
        else:
            result += f"**๐ฌ ๐ค๐๐๐๐บ๐๐บ๐๐๐๐ :**  `{command['usage']}`\n"
            result += f"**โจ๏ธ ๐ฅ๐๐ ๐ค๐๐บ๐๐๐๐พ :**  `{HANDLER[:1]}{command['example']}`\n\n"
        if event.query.user_id == bot.uid or event.query.user_id in Config.SUDO_USERS:
            await event.edit(
                result,
                buttons=[
                    custom.Button.inline(f"{d3vil_emoji} Return {d3vil_emoji}", data=f"Information[{page}]({cmd})")
                ],
                link_preview=False,
            )
        else:
            return await event.answer(
                "๐ง๐พ๐๐๐ ๐๐๐พ๐๐พ ๐ฃ๐พ๐๐๐๐ ๐๐๐๐ ๐๐๐ ๐ฃ3๐ต๐จ๐ซ๐ก๐ฎ๐ณ ๐บ๐๐ฝ ๐๐๐พ. ยฉ แช3แแฅแแฐแงแโข",
                cache_time=0,
                alert=True,
            )



