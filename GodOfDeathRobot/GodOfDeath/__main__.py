import importlib
import re
import time
from math import ceil
from typing import Dict, List
from uuid import uuid4
from platform import python_version as y
from sys import argv

from pyrogram import __version__ as pyrover, filters, idle
from pyrogram.enums import ParseMode, ChatType
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from GodOfDeath import (
    API_ID,
    API_HASH,
    OWNER_ID,
    OWNER_USERNAME,
    BOT_ID,
    BOT_TOKEN,
    BOT_USERNAME,
    START_IMG,
    LOGGER,
    StartTime,
    app
)
from GodOfDeath.modules import ALL_MODULES


class EqInlineKeyboardButton(InlineKeyboardButton):
    def __eq__(self, other):
        return self.text == other.text

    def __lt__(self, other):
        return self.text < other.text

    def __gt__(self, other):
        return self.text > other.text


def paginate_modules(page_n: int, module_dict: Dict, prefix, chat=None) -> List:
    if not chat:
        modules = sorted(
            [
                EqInlineKeyboardButton(
                    x.__mod_name__,
                    callback_data="{}_module({})".format(
                        prefix, x.__mod_name__.lower()
                    ),
                )
                for x in module_dict.values()
            ]
        )
    else:
        modules = sorted(
            [
                EqInlineKeyboardButton(
                    x.__mod_name__,
                    callback_data="{}_module({},{})".format(
                        prefix, chat, x.__mod_name__.lower()
                    ),
                )
                for x in module_dict.values()
            ]
        )

    pairs = [modules[i * 3 : (i + 1) * 3] for i in range((len(modules) + 3 - 1) // 3)]

    round_num = len(modules) / 3
    calc = len(modules) - round(round_num)
    if calc in [1, 2]:
        pairs.append((modules[-1],))

    max_num_pages = ceil(len(pairs) / 4)
    modulo_page = page_n % max_num_pages

    # can only have a certain amount of buttons side by side
    if len(pairs) > 3:
        pairs = pairs[modulo_page * 4 : 4 * (modulo_page + 1)] + [
            (
                EqInlineKeyboardButton(
                    "⇚", callback_data="{}_prev({})".format(prefix, modulo_page)
                ),
                EqInlineKeyboardButton("Home", callback_data="home"),
                EqInlineKeyboardButton(
                    "⇛", callback_data="{}_next({})".format(prefix, modulo_page)
                ),
            )
        ]

    else:
        pairs += [[EqInlineKeyboardButton("Back", callback_data="home")]]

    return pairs

def get_readable_time(seconds: int) -> str:
    count = 0
    ping_time = ""
    time_list = []
    time_suffix_list = ["s", "m", "h", "days"]
    while count < 4:
        count += 1
        remainder, result = divmod(seconds, 60) if count < 3 else divmod(seconds, 24)
        if seconds == 0 and remainder == 0:
            break
        time_list.append(int(result))
        seconds = int(remainder)
    for x in range(len(time_list)):
        time_list[x] = str(time_list[x]) + time_suffix_list[x]
    if len(time_list) == 4:
        ping_time += time_list.pop() + ", "
    time_list.reverse()
    ping_time += ":".join(time_list)
    return ping_time

ALIVE_TEXT = f"I'm Alive and running [ ]({START_IMG})\n\nPython Version: {y}\nPyrogram Version: {pyrover}"

START_TEXT = '''
Hello {}! [ ]({})
I'm GodOfDeath, An assistant bot to make your life(on telegram) a bit easier.

I'm alive since {}
'''
buttons = [
    [
        InlineKeyboardButton(text='Developer', user_id=OWNER_ID),
        InlineKeyboardButton(text='Support', user_id=OWNER_ID)
    ],
    [
        InlineKeyboardButton(text='Help', callback_data='help_back')
    ],
    [
        InlineKeyboardButton(text='Add me to your Group', url=f'https://t.me/{BOT_USERNAME}?startgroup=true')
    ]
]
HELP_TEXT = "Help Menu for GodOfDeath."

IMPORTED = {}
HELPABLE = {}

for module_name in ALL_MODULES:
    imported_module = importlib.import_module("GodOfDeath.modules." + module_name)
    if not hasattr(imported_module, "__mod_name__"):
        imported_module.__mod_name__ = imported_module.__name__
    if imported_module.__mod_name__.lower() not in IMPORTED:
        IMPORTED[imported_module.__mod_name__.lower()] = imported_module
    else:
        raise Exception("Can't have two modules with the same name! Please change name of one.")

    if hasattr(imported_module, "__help__") and imported_module.__help__:
        HELPABLE[imported_module.__mod_name__.lower()] = imported_module


async def send_help(chat_id, text, keyboard=None):
    if not keyboard:
        keyboard = InlineKeyboardMarkup(paginate_modules(0, HELPABLE, "help"))
    await app.send_message(
        chat_id=chat_id,
        text=text,
        parse_mode=ParseMode.MARKDOWN,
        disable_web_page_preview=True,
        reply_markup=keyboard,
    )


@app.on_message(filters.command('start', prefixes=['!', '']))
async def start(bot, m):
    uptime = get_readable_time((time.time() - StartTime))
    first_name = m.from_user.first_name
    await m.reply_text(
        START_TEXT.format(first_name, START_IMG, uptime),
        reply_markup=InlineKeyboardMarkup(buttons),
        parse_mode=ParseMode.MARKDOWN,
        disable_web_page_preview=False
        )

@app.on_message(filters.command('ping', prefixes=['!', '']))
async def ping(bot, m):
    start_time = time.time()
    message = m.reply_text("Pinging...")
    end_time = time.time()
    telegram_ping = str(round((end_time - start_time) * 1000, 3)) + " ms"
    uptime = get_readable_time((time.time() - StartTime))
    message.edit_text(
        "ᴘᴏɴɢ!!\n"
        "ᴛɪᴍᴇ ᴛᴀᴋᴇɴ: <code>{}</code>\n"
        "sᴇʀᴠɪᴄᴇ ᴜᴘᴛɪᴍᴇ: <code>{}</code>".format(telegram_ping, uptime),
        parse_mode=ParseMode.HTML,
    )

@app.on_callback_query(filters.regex('help'))
async def help_button(bot, query):
    mod_match = re.match(r"help_module\((.+?)\)", query.data)
    prev_match = re.match(r"help_prev\((.+?)\)", query.data)
    next_match = re.match(r"help_next\((.+?)\)", query.data)
    back_match = re.match(r"help_back", query.data)

    try:
        if mod_match:
            module = mod_match.group(1)
            text = (
                "Availabe Help For {} :\n".format(
                    HELPABLE[module].__mod_name__
                )
                + HELPABLE[module].__help__
            )
            await query.message.edit_text(
                text=text,
                parse_mode=ParseMode.MARKDOWN,
                disable_web_page_preview=True,
                reply_markup=InlineKeyboardMarkup(
                    [[InlineKeyboardButton(text="Back", callback_data="help_back")]]
                ),
            )

        elif prev_match:
            curr_page = int(prev_match.group(1))
            await query.message.edit_text(
                text=HELP_TEXT,
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=InlineKeyboardMarkup(
                    paginate_modules(curr_page - 1, HELPABLE, "help")
                ),
            )

        elif next_match:
            curr_page = int(next_match.group(1))
            await query.message.edit_text(
                text=HELP_TEXT,
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=InlineKeyboardMarkup(
                    paginate_modules(curr_page + 1, HELPABLE, "help")
                ),
            )

        elif back_match:
            await query.message.edit_text(
                text=HELP_TEXT,
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=InlineKeyboardMarkup(
                    paginate_modules(0, HELPABLE, "help")
                ),
            )

        await app.answer_callback_query(query.id)

    except Exception as e:
        await m.reply_text(e)

@app.on_callback_query()
async def GodOfDeath_callback(bot, query):
    if query.data == 'home':
        uptime = get_readable_time((time.time() - StartTime))
        first_name = query.from_user.first_name
        await query.message.edit_text(
        START_TEXT.format(first_name, START_IMG, uptime),
        reply_markup=InlineKeyboardMarkup(buttons),
        parse_mode=ParseMode.MARKDOWN,
        disable_web_page_preview=False
        )
    await app.answer_callback_query(query.id)


@app.on_message(filters.command('help', prefixes=['!', '']))
async def get_help(bot, m):
    args = m.text.split(None, 1)
    if m.chat.type != ChatType.PRIVATE:
        await m.reply_text(
            "Choose an option for getting help.",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            text="Open in Private",
                            url=f"https://t.me/{BOT_USERNAME}?start=help"
                        )
                    ],
                    [
                        InlineKeyboardButton(
                            text="Open Here",
                            callback_data="help_back",
                        )
                    ],
                ]
            ),
        )
        return

    elif len(args) >= 2 and any(args[1].lower() == x for x in HELPABLE):
        module = args[1].lower()
        text = (
            "Help for {}:\n".format(
                HELPABLE[module].__mod_name__
            )
            + HELPABLE[module].__help__
        )
        send_help(
            m.chat.id,
            text,
            InlineKeyboardMarkup(
                [[InlineKeyboardButton(text="Back", callback_data="help_back")]]
            ),
        )
    else:
        await send_help(m.chat.id, HELP_TEXT)

@app.on_message(filters.command('alive', prefixes=['!', '']))
async def alive(bot, m):
    await m.reply_text(ALIVE_TEXT, reply_markup=InlineKeyboardMarkup(buttons), disable_web_page_preview=False)


def main():
    app.send_message(OWNER_ID, 'GodOfDeath has successfully started.')
    LOGGER.critical("GodOfDeath has successfully started")


if __name__ == "__main__":
    LOGGER.info(f"Successfully loaded modules: {ALL_MODULES}")
    app.start()
    main()
    idle()