import os
from GodOfDeath import app
from pyrogram import filters
try:
	from phlogo import generate
except ModuleNotFoundError:
	os.system("pip install phlogo")
	from phlogo import generate

@app.on_message(filters.command("phlogo", prefixes=['!', '']) | filters.command("phst", prefixes=['!', '']))
async def ph(bot, m):
	msg = m.text.split(" ", 1)
	cmd = msg[0]
	query = str(msg[1])

	if query == "":
		return await m.reply_text("Give some text bruh")

	try:
		q = query.split(' ', 1)
		p = q[0]
		h = q[1]
	except:
		return await m.reply_text("Something went wrong, try giving two words.")
		
	result = generate(f"{p}",f"{h}")

	if cmd == 'phlogo':
		pic = "ph.png"
		result.save(pic, "png")
		await m.reply_photo(pic)

	if cmd == 'phst':
		pic = "ph.webp"
		result.save(pic, "webp")
		await m.reply_sticker(pic)

	os.remove(pic)

__mod_name__ = "Phub Logo"
__help__ = """PHub Style Logo
Usage:
⋗ /phlogo <word1> <word2>
⋗ /phst <word1> <word2>
"""