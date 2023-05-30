from time import perf_counter
from functools import wraps
from cachetools import TTLCache
from threading import RLock
from GodOfDeath import (
    INFINITY_GODS,
    ULTIMATE_GODS,
    SUPERIORS,
    LEGENDS,
    MEN,
    SUPPORT,
    app,
)

DEL_CMDS = True

from pyrogram.enums import ParseMode, ChatType, ChatMembersFilter, ChatMemberStatus
from pyrogram.types import Chat, ChatMember

# stores admemes in memory for 10 min.
ADMIN_CACHE = TTLCache(maxsize=512, ttl=60 * 10, timer=perf_counter)
THREAD_LOCK = RLock()


def is_whitelist_plus(chat: Chat, user_id: int, member: ChatMember = None) -> bool:
    return any(user_id in user for user in [INFINITY_GODS, ULTIMATE_GODS, SUPERIORS, LEGENDS, MEN])


def is_support_plus(chat: Chat, user_id: int, member: ChatMember = None) -> bool:
    return user_id in SUPERIORS or user_id in ULTIMATE_GODS or user_id in INFINITY_GODS


def is_sudo_plus(chat: Chat, user_id: int, member: ChatMember = None) -> bool:
    return user_id in ULTIMATE_GODS or user_id in INFINITY_GODS


def is_user_admin(chat: Chat, user_id: int, member: ChatMember = None) -> bool:
    if (
        chat.type == ChatType.PRIVATE
        or user_id in ULTIMATE_GODS
        or user_id in INFINITY_GODS
        or user_id in [777000, 1218405248]
    ):  # Count telegram and Group Anonymous as admin
        return True
    if not member:
        with THREAD_LOCK:
            # try to fetch from cache first.
            try:
                return user_id in ADMIN_CACHE[chat.id]
            except KeyError:
                # keyerror happend means cache is deleted,
                # so query bot api again and return user status
                # while saving it in cache for future useage...
                chat_admins = chat.get_members(filter=ChatMembersFilter.ADMINISTRATORS)
                admin_list = [x.user.id for x in chat_admins]
                ADMIN_CACHE[chat.id] = admin_list

                return user_id in admin_list
    else:
        return member.status in [ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER]


def is_bot_admin(chat: Chat, bot_id: int, bot_member: ChatMember = None) -> bool:
    if chat.type == ChatType.PRIVATE:
        return True

    if not bot_member:
        bot_member = chat.get_member(bot_id)

    return bot_member.status == ChatMemberStatus.ADMINISTRATOR


def can_delete(chat: Chat, bot_id: int) -> bool:
    return chat.get_member(bot_id).privileges.can_delete_messages


def is_user_ban_protected(chat: Chat, user_id: int, member: ChatMember = None) -> bool:
    if (
        chat.type == ChatType.PRIVATE
        or user_id in ULTIMATE_GODS
        or user_id in INFINITY_GODS
        or user_id in SUPERIORS
        or user_id in LEGENDS
        or user_id in [777000, 1218405248]
    ):  # Count telegram and Group Anonymous as admin
        return True

    if not member:
        member = chat.get_member(user_id)

    return member.status in [ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER]


def is_user_in_chat(chat: Chat, user_id: int) -> bool:
    member = chat.get_member(user_id)
    return member.status not in [ChatMembersStatus.LEFT, ChatMemberStatus.BANNED]


def dev_plus(func):
    @wraps(func)
    async def is_dev_plus_func(bot, message, *args, **kwargs):
        user = message.from_user
        if user.id in INFINITY_GODS:
            return func(bot, message, *args, **kwargs)
        elif not user:
            pass
        elif DEL_CMDS and " " not in message.text:
            try:
                await message.delete()
            except:
                pass
        else:
            await message.reply_text(
                "This is a developer restricted command.\nYou do not have permissions to run this."
            )

    return is_dev_plus_func


def sudo_plus(func):
    @wraps(func)
    async def is_sudo_plus_func(bot, message, *args, **kwargs):
        
        user = message.from_user
        chat = message.chat

        if user and is_sudo_plus(chat, user.id):
            return func(bot, message, *args, **kwargs)
        elif not user:
            pass
        elif DEL_CMDS and " " not in message.text:
            try:
                await message.delete()
            except:
                pass
        else:
            await message.reply_text(
                "Who dis non-admin telling me what to do? You want a punch?"
            )

    return is_sudo_plus_func


def support_plus(func):
    @wraps(func)
    async def is_support_plus_func(bot, message, *args, **kwargs):
        
        user = message.from_user
        chat = message.chat

        if user and is_support_plus(chat, user.id):
            return func(bot, message, *args, **kwargs)
        elif DEL_CMDS and " " not in message.text:
            try:
                await message.delete()
            except:
                pass

    return is_support_plus_func


def whitelist_plus(func):
    @wraps(func)
    async def is_whitelist_plus_func(bot, message, *args, **kwargs):
        
        user = message.from_user
        chat = message.chat

        if user and is_whitelist_plus(chat, user.id):
            return func(bot, message, *args, **kwargs)
        else:
            await message.reply_text(
                f"You don't have access to use this.\nVisit @{SUPPORT}"
            )

    return is_whitelist_plus_func


def user_admin(func):
    @wraps(func)
    async def is_admin(bot, message, *args, **kwargs):
        
        user = message.from_user
        chat = message.chat

        if user and is_user_admin(chat, user.id):
            return func(bot, message, *args, **kwargs)
        elif not user:
            pass
        elif DEL_CMDS and " " not in message.text:
            try:
                await message.delete()
            except:
                pass
        else:
            await message.reply_text(
                "Who dis non-admin telling me what to do? You want a punch?"
            )

    return is_admin


def user_admin_no_reply(func):
    @wraps(func)
    async def is_not_admin_no_reply(bot, message, *args, **kwargs):
        
        user = message.from_user
        chat = message.chat

        if user and is_user_admin(chat, user.id):
            return func(bot, message, *args, **kwargs)
        elif not user:
            pass
        elif DEL_CMDS and " " not in await message.text:
            try:
                await message.delete()
            except:
                pass

    return is_not_admin_no_reply


def user_not_admin(func):
    @wraps(func)
    async def is_not_admin(bot, message, *args, **kwargs):
        
        user = message.from_user
        chat = message.chat

        if user and not is_user_admin(chat, user.id):
            return func(bot, message, *args, **kwargs)
        elif not user:
            pass

    return is_not_admin


def bot_admin(func):
    @wraps(func)
    async def is_admin(bot, message, *args, **kwargs):
        
        chat = message.chat
        not_admin = "I'm not admin bruh."
        if is_bot_admin(chat, bot.id):
            return func(bot, message, *args, **kwargs)
        else:
            await message.reply_text(not_admin, parse_mode=ParseMode.HTML)

    return is_admin


def bot_can_delete(func):
    @wraps(func)
    async def delete_rights(bot, message, *args, **kwargs):
        
        chat = message.chat
        cant_delete = "I can't delete messages here!\nMake sure I'm admin and can delete other user's messages."
        
        if can_delete(chat, bot.id):
            return func(bot, message, *args, **kwargs)
        else:
            await message.reply_text(cant_delete, parse_mode=ParseMode.HTML)

    return delete_rights


def can_pin(func):
    @wraps(func)
    async def pin_rights(bot, message, *args, **kwargs):
        
        chat = message.chat
        cant_pin = "I can't pin messages here!\nMake sure I'm admin and can pin messages."

        if chat.get_member(bot.id).privileges.can_pin_messages:
            return func(bot, message, *args, **kwargs)
        else:
            await message.reply_text(cant_pin, parse_mode=ParseMode.HTML)

    return pin_rights


def can_promote(func):
    @wraps(func)
    async def promote_rights(bot, message, *args, **kwargs):
        
        chat = message.chat
        cant_promote = "I can't promote/demote people here!\nMake sure I'm admin and can appoint new admins."
        
        if chat.get_member(bot.id).can_promote_members:
            return func(bot, message, *args, **kwargs)
        else:
            await message.reply_text(cant_promote, parse_mode=ParseMode.HTML)

    return promote_rights


def can_restrict(func):
    @wraps(func)
    async def restrict_rights(bot, message, *args, **kwargs):
        
        chat = message.chat
        cant_restrict = "I can't restrict people here!\nMake sure I'm admin and can restrict users."
        
        if chat.get_member(bot.id).can_restrict_members:
            return func(bot, message, *args, **kwargs)
        else:
            await message.reply_text(cant_restrict, parse_mode=ParseMode.HTML)

    return restrict_rights


def user_can_ban(func):
    @wraps(func)
    async def user_is_banhammer(bot, message, *args, **kwargs):
        user = message.from_user.id
        member = message.chat.get_member(user)
        if (
            not (member.privileges.can_restrict_members or member.status == ChatMemberStatus.OWNER)
            and user not in ULTIMATE_GODS
            and user not in [777000, 1087968824]
        ):
            await message.reply_text(
                "😹 Sorry You can't do that"
            )
            return ""
        return func(bot, message, *args, **kwargs)

    return user_is_banhammer
