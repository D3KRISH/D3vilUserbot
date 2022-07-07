import asyncio
import datetime

from telethon import events
from telethon.tl import functions, types

from d3vilbot.sql.gvar_sql import addgvar, gvarstat, delgvar
from . import *


global afk_time_1
global last_afk_message_1
global afk_start_1
global afk_end_1
afk_time_1 = None
last_afk_message_1 = {}
afk_start_1 = {}


global afk_time_2
global last_afk_message_2
global afk_start_2
global afk_end_2
afk_time_2 = None
last_afk_message_2 = {}
afk_start_2 = {}


global afk_time_3
global last_afk_message_3
global afk_start_3
global afk_end_3
afk_time_3 = None
last_afk_message_3 = {}
afk_start_3 = {}


global afk_time_4
global last_afk_message_4
global afk_start_4
global afk_end_4
afk_time_4 = None
last_afk_message_4 = {}
afk_start_4 = {}


global afk_time_5
global last_afk_message_5
global afk_start_5
global afk_end_5
afk_time_5 = None
last_afk_message_5 = {}
afk_start_5 = {}


@D1.on(events.NewMessage(outgoing=True))
async def set_not_afk(event):
    global afk_time_1
    global last_afk_message_1
    global afk_start_1
    global afk_end_1
    came_back = datetime.datetime.now()
    afk_end_1 = came_back.replace(microsecond=0)
    if afk_start_1 != {}:
        total_afk_time = str((afk_end_1 - afk_start_1))
    current_message = event.message.message
    if "#" not in current_message and gvarstat("AFK") == "YES":
        d3vilbot = await event.client.send_message(
            event.chat_id,
            "__**Back to Virtual World!**__\nNo Longer AFK.\n⏱️ Was afk for: `"
            + total_afk_time
            + "`", file=d3vilpic_1
        )
        try:
            await unsave_gif(event, d3vilbot)
            delgvar("AFK")
            await event.client.send_message(
                Config.LOGGER_ID,
                f"#AFKFALSE \n\n**AFK mode** = `False`\n**AFK Timer :** `{total_afk_time}`"
            )
        except Exception as e:
            await event.client.send_message(
                event.chat_id,
                "Please set `LOGGER_ID` "
                + "for the proper functioning of afk."
                + f" Ask in {d3vil_grp} to get help!",
                reply_to=event.message.id,
                link_preview=False,
                silent=True,
            )
        await asyncio.sleep(5)
        await d3vilbot.delete()
        afk_time_1 = None


@D1.on(events.NewMessage(incoming=True, func=lambda e: bool(e.mentioned or e.is_private)))
async def on_afk(event):
    global afk_time_1
    global last_afk_message_1
    global afk_start_1
    global afk_end_1
    cum_back = datetime.datetime.now()
    afk_end_1 = cum_back.replace(microsecond=0)
    if afk_start_1 != {}:
        total_afk_time = str((afk_end_1 - afk_start_1))
    current_message_text = event.message.message.lower()
    if "afk" in current_message_text:
        return False
    if gvarstat("AFK") == "YES" and not (await event.get_sender()).bot:
        msg = None
        if reason_1 == "":
            message_to_reply = f"**I'm currently AFK!** \n\n**⏰ AFK Since :**  `{total_afk_time}`"
        else:
            message_to_reply = (
                f"**I'm currently AFK!** \n\n**⏰ AFK Since :**  `{total_afk_time}`\n"
                + f"\n**💬 Reason :** {reason_1}"
                )
        msg = await event.reply(message_to_reply, file=d3vilpic_1)
        try:
            await unsave_gif(event, msg)
        except:
            pass
        await asyncio.sleep(2)
        if event.chat_id in last_afk_message_1:
            await last_afk_message_1[event.chat_id].delete()
        last_afk_message_1[event.chat_id] = msg


@D1.on(admin_cmd(pattern="afk(?:\s|$)([\s\S]*)"))
async def _(event):
    if event.fwd_from:
        return
    d3vilkrishop = await event.get_reply_message()
    global afk_time_1
    global last_afk_message_1
    global afk_start_1
    global afk_end_1
    global reason_1
    global d3vilpic_1
    afk_time_1 = None
    last_afk_message_1 = {}
    afk_end_1 = {}
    start_1 = datetime.datetime.now()
    afk_start_1 = start_1.replace(microsecond=0)
    owo = event.text[5:]
    reason_1 = owo
    d3vilpic_1 = await event.client.download_media(d3vilkrishop)
    if gvarstat("AFK") != "YES":
        last_seen_status = await event.client(
            functions.account.GetPrivacyRequest(types.InputPrivacyKeyStatusTimestamp())
        )
        if isinstance(last_seen_status.rules, types.PrivacyValueAllowAll):
            afk_time_1 = datetime.datetime.now()
        if owo == "":
            addgvar("AFK", "YES")
            x = await event.client.send_message(
                event.chat_id, f"**I'm going afk🚶**", file=d3vilpic_1)
            try:
                await unsave_gif(event, x)
                xy = await event.client.send_message(
                    Config.LOGGER_ID,
                    f"#AFKTRUE \n**AFK mode** = `True`\n**Reason:** `Not Mentioned`", file=d3vilpic_1
                    )
                try:
                    await unsave_gif(event, xy)
                except:
                    pass
            except Exception as e:
                logger.warn(str(e))
        else:
            addgvar("AFK", "YES")
            x = await event.client.send_message(
                event.chat_id, f"**I'm going afk🚶**\n\n**Because :** `{reason_1}`", file=d3vilpic_1)
            try:
                await unsave_gif(event, x)
                xy = await event.client.send_message(
                    Config.LOGGER_ID,
                    f"#AFKTRUE \n**AFK mode** = `True`\n**Reason:** `{reason_1}`", file=d3vilpic_1
                    )
                try:
                    await unsave_gif(event, xy)
                except:
                    pass
            except Exception as e:
                logger.warn(str(e))


if D2:
    @D2.on(events.NewMessage(outgoing=True))
    async def set_not_afk(event):
        global afk_time_2
        global last_afk_message_2
        global afk_start_2
        global afk_end_2
        came_back = datetime.datetime.now()
        afk_end_2 = came_back.replace(microsecond=0)
        if afk_start_2 != {}:
            total_afk_time = str((afk_end_2 - afk_start_2))
        current_message = event.message.message
        if "#" not in current_message and gvarstat("AFK2") == "YES":
            d3vilbot = await event.client.send_message(
                event.chat_id,
                "__**Back to Virtual World!**__\nNo Longer AFK.\n⏱️ Was afk for: `"
                + total_afk_time
                + "`", file=d3vilpic_2
            )
            try:
                await unsave_gif(event, d3vilbot)
                delgvar("AFK2")
                await event.client.send_message(
                    Config.LOGGER_ID,
                    f"#AFKFALSE \n\n**AFK mode** = `False`\n**AFK Timer :** `{total_afk_time}`"
                )
            except Exception as e:
                await event.client.send_message(
                    event.chat_id,
                    "Please set `LOGGER_ID` "
                    + "for the proper functioning of afk."
                    + f" Ask in {d3vil_grp} to get help!",
                    reply_to=event.message.id,
                    link_preview=False,
                    silent=True,
                )
            await asyncio.sleep(5)
            await d3vilbot.delete()
            afk_time_2 = None


    @D2.on(events.NewMessage(incoming=True, func=lambda e: bool(e.mentioned or e.is_private)))
    async def on_afk(event):
        global afk_time_2
        global last_afk_message_2
        global afk_start_2
        global afk_end_2
        cum_back = datetime.datetime.now()
        afk_end_2 = cum_back.replace(microsecond=0)
        if afk_start_2 != {}:
            total_afk_time = str((afk_end_2 - afk_start_2))
        current_message_text = event.message.message.lower()
        if "afk" in current_message_text:
            return False
        if gvarstat("AFK2") == "YES" and not (await event.get_sender()).bot:
            msg = None
            if reason_2 == "":
                message_to_reply = f"**I'm currently AFK!** \n\n**⏰ AFK Since :**  `{total_afk_time}`"
            else:
                message_to_reply = (
                    f"**I'm currently AFK!** \n\n**⏰ AFK Since :**  `{total_afk_time}`\n"
                    + f"\n**💬 Reason :** {reason_2}"
                    )
            msg = await event.reply(message_to_reply, file=d3vilpic_2)
            try:
                await unsave_gif(event, msg)
            except:
                pass
            await asyncio.sleep(2)
            if event.chat_id in last_afk_message_2:
                await last_afk_message_2[event.chat_id].delete()
            last_afk_message_2[event.chat_id] = msg


    @D2.on(admin_cmd(pattern="afk(?:\s|$)([\s\S]*)"))
    async def _(event):
        if event.fwd_from:
            return
        d3vilkrishop = await event.get_reply_message()
        global afk_time_2
        global last_afk_message_2
        global afk_start_2
        global afk_end_2
        global reason_2
        global d3vilpic_2
        afk_time_2 = None
        last_afk_message_2 = {}
        afk_end_2 = {}
        start_1 = datetime.datetime.now()
        afk_start_2 = start_1.replace(microsecond=0)
        owo = event.text[5:]
        reason_2 = owo
        d3vilpic_2 = await event.client.download_media(d3vilkrishop)
        if not gvarstat("AFK2"):
            last_seen_status = await event.client(
                functions.account.GetPrivacyRequest(types.InputPrivacyKeyStatusTimestamp())
            )
            if isinstance(last_seen_status.rules, types.PrivacyValueAllowAll):
                afk_time_2 = datetime.datetime.now()
            if owo == "":
                addgvar("AFK2", "YES")
                x = await event.client.send_message(
                    event.chat_id, f"**I'm going afk🚶**", file=d3vilpic_2)
                try:
                    await unsave_gif(event, x)
                    xy = await event.client.send_message(
                        Config.LOGGER_ID,
                        f"#AFKTRUE \n**AFK mode** = `True`\n**Reason:** `Not Mentioned`",file=d3vilpic_2
                        )
                    try:
                        await unsave_gif(event, xy)
                    except:
                        pass
                except Exception as e:
                    logger.warn(str(e))
            else:
                addgvar("AFK2", "YES")
                x = await event.client.send_message(
                    event.chat_id, f"**I'm going afk🚶**\n\n**Because :** `{reason_2}`", file=d3vilpic_2)
                try:
                    await unsave_gif(event, x)
                    xy = await event.client.send_message(
                        Config.LOGGER_ID,
                        f"#AFKTRUE \n**AFK mode** = `True`\n**Reason:** `{reason_2}`",file=d3vilpic_2
                        )
                    try:
                        await unsave_gif(event, xy)
                    except:
                        pass
                except Exception as e:
                    logger.warn(str(e))


if D3:
    @D3.on(events.NewMessage(outgoing=True))
    async def set_not_afk(event):
        global afk_time_3
        global last_afk_message_3
        global afk_start_3
        global afk_end_3
        came_back = datetime.datetime.now()
        afk_end_3 = came_back.replace(microsecond=0)
        if afk_start_3 != {}:
            total_afk_time = str((afk_end_3 - afk_start_3))
        current_message = event.message.message
        if "#" not in current_message and gvarstat("AFK3") == "YES":
            d3vilbot = await event.client.send_message(
                event.chat_id,
                "__**Back to Virtual World!**__\nNo Longer AFK.\n⏱️ Was afk for: `"
                + total_afk_time
                + "`", file=d3vilpic_3
            )
            try:
                await unsave_gif(event, d3vilbot)
                delgvar("AFK3")
                await event.client.send_message(
                    Config.LOGGER_ID,
                    f"#AFKFALSE \n\n**AFK mode** = `False`\n**AFK Timer :** `{total_afk_time}`"
                )
            except Exception as e:
                await event.client.send_message(
                    event.chat_id,
                    "Please set `LOGGER_ID` "
                    + "for the proper functioning of afk."
                    + f" Ask in {d3vil_grp} to get help!",
                    reply_to=event.message.id,
                    link_preview=False,
                    silent=True,
                )
            await asyncio.sleep(5)
            await d3vilbot.delete()
            afk_time_3 = None


    @D3.on(events.NewMessage(incoming=True, func=lambda e: bool(e.mentioned or e.is_private)))
    async def on_afk(event):
        global afk_time_3
        global last_afk_message_3
        global afk_start_3
        global afk_end_3
        cum_back = datetime.datetime.now()
        afk_end_3 = cum_back.replace(microsecond=0)
        if afk_start_3 != {}:
            total_afk_time = str((afk_end_3 - afk_start_3))
        current_message_text = event.message.message.lower()
        if "afk" in current_message_text:
            return False
        if gvarstat("AFK3") == "YES" and not (await event.get_sender()).bot:
            msg = None
            if reason == "":
                message_to_reply = f"**I'm currently AFK!** \n\n**⏰ AFK Since :**  `{total_afk_time}`"
            else:
                message_to_reply = (
                    f"**I'm currently AFK!** \n\n**⏰ AFK Since :**  `{total_afk_time}`\n"
                    + f"\n**💬 Reason :** {reason_3}"
                    )
            msg = await event.reply(message_to_reply, file=d3vilpic_3)
            try:
                await unsave_gif(event, msg)
            except:
                pass
            await asyncio.sleep(2)
            if event.chat_id in last_afk_message_3:
                await last_afk_message_3[event.chat_id].delete()
            last_afk_message_3[event.chat_id] = msg


    @D3.on(admin_cmd(pattern="afk(?:\s|$)([\s\S]*)"))
    async def _(event):
        if event.fwd_from:
            return
        d3vilkrishop = await event.get_reply_message()
        global afk_time_3
        global last_afk_message_3
        global afk_start_3
        global afk_end_3
        global reason_3
        global d3vilpic_3
        afk_time_3 = None
        last_afk_message_3 = {}
        afk_end_3 = {}
        start_1 = datetime.datetime.now()
        afk_start_3 = start_1.replace(microsecond=0)
        owo = event.text[5:]
        reason_3 = owo
        d3vilpic_3 = await event.client.download_media(d3vilkrishop)
        if not gvarstat("AFK3"):
            last_seen_status = await event.client(
                functions.account.GetPrivacyRequest(types.InputPrivacyKeyStatusTimestamp())
            )
            if isinstance(last_seen_status.rules, types.PrivacyValueAllowAll):
                afk_time_3 = datetime.datetime.now()
            if owo == "":
                addgvar("AFK3", "YES")
                x = await event.client.send_message(
                    event.chat_id, f"**I'm going afk🚶**", file=d3vilpic_3)
                try:
                    await unsave_gif(event, x)
                    xy = await event.client.send_message(
                        Config.LOGGER_ID,
                        f"#AFKTRUE \n**AFK mode** = `True`\n**Reason:** `Not Mentioned`",file=d3vilpic_3
                        )
                    try:
                        await unsave_gif(event, xy)
                    except:
                        pass
                except Exception as e:
                    logger.warn(str(e))
            else:
                addgvar("AFK3", "YES")
                x = await event.client.send_message(
                    event.chat_id, f"**I'm going afk🚶**\n\n**Because :** `{reason_3}`", file=d3vilpic_3)
                try:
                    await unsave_gif(event, x)
                    xy = await event.client.send_message(
                        Config.LOGGER_ID,
                        f"#AFKTRUE \n**AFK mode** = `True`\n**Reason:** `{reason_3}`",file=d3vilpic_3
                        )
                    try:
                        await unsave_gif(event, xy)
                    except:
                        pass
                except Exception as e:
                    logger.warn(str(e))


if D4:
    @D4.on(events.NewMessage(outgoing=True))
    async def set_not_afk(event):
        global afk_time_4
        global last_afk_message_4
        global afk_start_4
        global afk_end_4
        came_back = datetime.datetime.now()
        afk_end_4 = came_back.replace(microsecond=0)
        if afk_start_4 != {}:
            total_afk_time = str((afk_end_4 - afk_start_4))
        current_message = event.message.message
        if "#" not in current_message and gvarstat("AFK4") == "YES":
            d3vilbot = await event.client.send_message(
                event.chat_id,
                "__**Back to Virtual World!**__\nNo Longer AFK.\n⏱️ Was afk for: `"
                + total_afk_time
                + "`", file=d3vilpic_4
            )
            try:
                await unsave_gif(event, d3vilbot)
                delgvar("AFK4")
                await event.client.send_message(
                    Config.LOGGER_ID,
                    f"#AFKFALSE \n\n**AFK mode** = `False`\n**AFK Timer :** `{total_afk_time}`"
                )
            except Exception as e:
                await event.client.send_message(
                    event.chat_id,
                    "Please set `LOGGER_ID` "
                    + "for the proper functioning of afk."
                    + f" Ask in {d3vil_grp} to get help!",
                    reply_to=event.message.id,
                    link_preview=False,
                    silent=True,
                )
            await asyncio.sleep(5)
            await d3vilbot.delete()
            afk_time_4 = None


    @D4.on(events.NewMessage(incoming=True, func=lambda e: bool(e.mentioned or e.is_private)))
    async def on_afk(event):
        global afk_time_4
        global last_afk_message_4
        global afk_start_4
        global afk_end_4
        cum_back = datetime.datetime.now()
        afk_end_4 = cum_back.replace(microsecond=0)
        if afk_start_4 != {}:
            total_afk_time = str((afk_end_4 - afk_start_4))
        current_message_text = event.message.message.lower()
        if "afk" in current_message_text:
            return False
        if gvarstat("AFK4") == "YES" and not (await event.get_sender()).bot:
            msg = None
            if reason_4 == "":
                message_to_reply = f"**I'm currently AFK!** \n\n**⏰ AFK Since :**  `{total_afk_time}`"
            else:
                message_to_reply = (
                    f"**I'm currently AFK!** \n\n**⏰ AFK Since :**  `{total_afk_time}`\n"
                    + f"\n**💬 Reason :** {reason_4}"
                    )
            msg = await event.reply(message_to_reply, file=d3vilpic_4)
            try:
                await unsave_gif(event, msg)
            except:
                pass
            await asyncio.sleep(2)
            if event.chat_id in last_afk_message_4:
                await last_afk_message_4[event.chat_id].delete()
            last_afk_message_4[event.chat_id] = msg


    @D4.on(admin_cmd(pattern="afk(?:\s|$)([\s\S]*)"))
    async def _(event):
        if event.fwd_from:
            return
        d3vilkrishop = await event.get_reply_message()
        global afk_time_4
        global last_afk_message_4
        global afk_start_4
        global afk_end_4
        global reason_4
        global d3vilpic_4
        afk_time_4 = None
        last_afk_message_4 = {}
        afk_end_4 = {}
        start_1 = datetime.datetime.now()
        afk_start_4 = start_1.replace(microsecond=0)
        owo = event.text[5:]
        reason_4 = owo
        d3vilpic_4 = await event.client.download_media(d3vilkrishop)
        if not gvarstat("AFK4"):
            last_seen_status = await event.client(
                functions.account.GetPrivacyRequest(types.InputPrivacyKeyStatusTimestamp())
            )
            if isinstance(last_seen_status.rules, types.PrivacyValueAllowAll):
                afk_time_4 = datetime.datetime.now()
            if owo == "":
                addgvar("AFK4", "YES")
                x = await event.client.send_message(
                    event.chat_id, f"**I'm going afk🚶**", file=d3vilpic_4)
                try:
                    await unsave_gif(event, x)
                    xy = await event.client.send_message(
                        Config.LOGGER_ID,
                        f"#AFKTRUE \n**AFK mode** = `True`\n**Reason:** `Not Mentioned`",file=d3vilpic_4
                        )
                    try:
                        await unsave_gif(event, xy)
                    except:
                        pass
                except Exception as e:
                    logger.warn(str(e))
            else:
                addgvar("AFK4", "YES")
                x = await event.client.send_message(
                    event.chat_id, f"**I'm going afk🚶**\n\n**Because :** `{reason_4}`", file=d3vilpic_4)
                try:
                    await unsave_gif(event, x)
                    xy = await event.client.send_message(
                        Config.LOGGER_ID,
                        f"#AFKTRUE \n**AFK mode** = `True`\n**Reason:** `{reason_4}`",file=d3vilpic_4
                        )
                    try:
                        await unsave_gif(event, xy)
                    except:
                        pass
                except Exception as e:
                    logger.warn(str(e))


if D5:
    @D5.on(events.NewMessage(outgoing=True))
    async def set_not_afk(event):
        global afk_time_5
        global last_afk_message_5
        global afk_start_5
        global afk_end_5
        came_back = datetime.datetime.now()
        afk_end_5 = came_back.replace(microsecond=0)
        if afk_start_5 != {}:
            total_afk_time = str((afk_end_5 - afk_start_5))
        current_message = event.message.message
        if "#" not in current_message and gvarstat("AFK5") == "YES":
            d3vilbot = await event.client.send_message(
                event.chat_id,
                "__**Back to Virtual World!**__\nNo Longer AFK.\n⏱️ Was afk for: `"
                + total_afk_time
                + "`", file=d3vilpic_5
            )
            try:
                await unsave_gif(event, d3vilbot)
                delgvar("AFK5")
                await event.client.send_message(
                    Config.LOGGER_ID,
                    f"#AFKFALSE \n\n**AFK mode** = `False`\n**AFK Timer :** `{total_afk_time}`"
                )
            except Exception as e:
                await event.client.send_message(
                    event.chat_id,
                    "Please set `LOGGER_ID` "
                    + "for the proper functioning of afk."
                    + f" Ask in {d3vil_grp} to get help!",
                    reply_to=event.message.id,
                    link_preview=False,
                    silent=True,
                )
            await asyncio.sleep(5)
            await d3vilbot.delete()
            afk_time_5 = None


    @D5.on(events.NewMessage(incoming=True, func=lambda e: bool(e.mentioned or e.is_private)))
    async def on_afk(event):
        global afk_time_5
        global last_afk_message_5
        global afk_start_5
        global afk_end_5
        cum_back = datetime.datetime.now()
        afk_end_5 = cum_back.replace(microsecond=0)
        if afk_start_5 != {}:
            total_afk_time = str((afk_end_5 - afk_start_5))
        current_message_text = event.message.message.lower()
        if "afk" in current_message_text:
            return False
        if gvarstat("AFK5") == "YES" and not (await event.get_sender()).bot:
            msg = None
            if reason_5 == "":
                message_to_reply = f"**I'm currently AFK!** \n\n**⏰ AFK Since :**  `{total_afk_time}`"
            else:
                message_to_reply = (
                    f"**I'm currently AFK!** \n\n**⏰ AFK Since :**  `{total_afk_time}`\n"
                    + f"\n**💬 Reason :** {reason_5}"
                    )
            msg = await event.reply(message_to_reply, file=d3vilpic_5)
            try:
                await unsave_gif(event, msg)
            except:
                pass
            await asyncio.sleep(2)
            if event.chat_id in last_afk_message_5:
                await last_afk_message_5[event.chat_id].delete()
            last_afk_message_5[event.chat_id] = msg


    @D5.on(admin_cmd(pattern="afk(?:\s|$)([\s\S]*)"))
    async def _(event):
        if event.fwd_from:
            return
        d3vilkrishop = await event.get_reply_message()
        global afk_time_5
        global last_afk_message_5
        global afk_start_5
        global afk_end_5
        global reason_5
        global d3vilpic_5
        afk_time_5 = None
        last_afk_message_5 = {}
        afk_end_5 = {}
        start_1 = datetime.datetime.now()
        afk_start_5 = start_1.replace(microsecond=0)
        owo = event.text[5:]
        reason_5 = owo
        d3vilpic_5 = await event.client.download_media(d3vilkrishop)
        if not gvarstat("AFK5"):
            last_seen_status = await event.client(
                functions.account.GetPrivacyRequest(types.InputPrivacyKeyStatusTimestamp())
            )
            if isinstance(last_seen_status.rules, types.PrivacyValueAllowAll):
                afk_time_5 = datetime.datetime.now()
            if owo == "":
                addgvar("AFK5", "YES")
                x = await event.client.send_message(
                    event.chat_id, f"**I'm going afk🚶**", file=d3vilpic_5)
                try:
                    await unsave_gif(event, x)
                    xy = await event.client.send_message(
                        Config.LOGGER_ID,
                        f"#AFKTRUE \n**AFK mode** = `True`\n**Reason:** `Not Mentioned`",file=d3vilpic_5
                        )
                    try:
                        await unsave_gif(event, xy)
                    except:
                        pass
                except Exception as e:
                    logger.warn(str(e))
            else:
                addgvar("AFK5", "YES")
                x = await event.client.send_message(
                    event.chat_id, f"**I'm going afk🚶**\n\n**Because :** `{reason_5}`", file=d3vilpic_5)
                try:
                    await unsave_gif(event, x)
                    xy = await event.client.send_message(
                        Config.LOGGER_ID,
                        f"#AFKTRUE \n**AFK mode** = `True`\n**Reason:** `{reason_5}`",file=d3vilpic_5
                        )
                    try:
                        await unsave_gif(event, xy)
                    except:
                        pass
                except Exception as e:
                    logger.warn(str(e))


CmdHelp("afk").add_command(
  'afk', '<reply to media>/<reason>', 'Marks you AFK with reason also shows afk time. Media also supported.', "afk <reason>`"
).add_extra(
  "📌 Exception", "Use # in a msg to stay in afk mode while chatting."
).add_info(
  "Away From Keyboard"
).add_warning(
  "✅ Harmless Module."
).add()
