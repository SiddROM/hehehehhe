import string
from pyrogram import filters, enums
from GodOfDeath import app, BOT_USERNAME

puncs = string.punctuation

@app.on_message(filters.command("write"))
async def handwriting(_, message):
    if len(message.command) < 2:
        return await message.reply_text("Gɪᴠᴇ Sᴏᴍᴇ Tᴇxᴛ Tᴏ Wʀɪᴛᴇ Iᴛ Oɴ Mʏ Cᴏᴩʏ...")
    m = await message.reply_text("Wᴀɪᴛ A Sᴇᴄ, Lᴇᴛ Mᴇ Wʀɪᴛᴇ Tʜᴀᴛ Tᴇxᴛ...")
    name = (
        message.text.split(None, 1)[1]
        if len(message.command) < 3
        else message.text.split(None, 1)[1].replace(" ", "%20")
    )
    text = ''
    for i in name:
        if i in puncs:
            text += name.replace(i, ' ')
    hand = "https://apis.xditya.me/write?text=" + text
    await m.edit("Uploading...")
    await app.send_chat_action(message.chat.id, enums.ChatAction.UPLOAD_PHOTO)
    await message.reply_photo(hand, caption=f"Written with 🖊 by [GodOfDeath](t.me/{BOT_USERNAME})")

__mod_name__ = 'Write'
__help__ = 'Writes given text onto a paper'
