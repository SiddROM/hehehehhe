from pyrogram import idle
from GodOfDeath import VIRUS, app
from GodOfDeath.modules.helper_funcs.gods import is_bot_admin

async def ban_virus(bot, m):
    if not is_bot_admin(m.chat, bot.id):
        return
    for i in VIRUS:
        await app.ban_chat_member(m.chat.id, int(i))

app.run(ban_virus())
idle()