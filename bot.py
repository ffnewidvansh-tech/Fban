import os
import json
import time
import random
import requests
from datetime import datetime
from telebot import TeleBot, types
from telebot.types import MessageEntity, InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton

# ============================================================
# ENVIRONMENT VARIABLES
# ============================================================
BOT_TOKEN = os.environ.get("BOT_TOKEN")
OWNER_ID = int(os.environ.get("OWNER_ID", "8471373583"))
ADMIN_IDS = [OWNER_ID]

if not BOT_TOKEN:
    print("❌ ERROR: BOT_TOKEN not set!")
    exit(1)

bot = TeleBot(BOT_TOKEN)

# ============================================================
# FILES & DATA
# ============================================================
USERS_FILE = "users.json"
ORDERS_FILE = "orders.json"
PENDING_FILE = "pending.json"
SETTINGS_FILE = "settings.json"
BUTTONS_FILE = "buttons.json"

# ============================================================
# STYLISH FONT - ᴀ ʙ ᴄ ᴅ ᴇ...
# ============================================================
def stylish_text(text: str) -> str:
    stylish_chars = {
        'A': 'ᴀ', 'B': 'ʙ', 'C': 'ᴄ', 'D': 'ᴅ', 'E': 'ᴇ', 'F': 'ꜰ', 'G': 'ɢ',
        'H': 'ʜ', 'I': 'ɪ', 'J': 'ᴊ', 'K': 'ᴋ', 'L': 'ʟ', 'M': 'ᴍ', 'N': 'ɴ',
        'O': 'ᴏ', 'P': 'ᴘ', 'Q': 'ǫ', 'R': 'ʀ', 'S': 'ꜱ', 'T': 'ᴛ', 'U': 'ᴜ',
        'V': 'ᴠ', 'W': 'ᴡ', 'X': 'x', 'Y': 'ʏ', 'Z': 'ᴢ',
        'a': 'ᴀ', 'b': 'ʙ', 'c': 'ᴄ', 'd': 'ᴅ', 'e': 'ᴇ', 'f': 'ꜰ', 'g': 'ɢ',
        'h': 'ʜ', 'i': 'ɪ', 'j': 'ᴊ', 'k': 'ᴋ', 'l': 'ʟ', 'm': 'ᴍ', 'n': 'ɴ',
        'o': 'ᴏ', 'p': 'ᴘ', 'q': 'ǫ', 'r': 'ʀ', 's': 'ꜱ', 't': 'ᴛ', 'u': 'ᴜ',
        'v': 'ᴠ', 'w': 'ᴡ', 'x': 'x', 'y': 'ʏ', 'z': 'ᴢ',
        '0': '₀', '1': '₁', '2': '₂', '3': '₃', '4': '₄',
        '5': '₅', '6': '₆', '7': '₇', '8': '₈', '9': '₉'
    }
    result = ""
    for char in text:
        result += stylish_chars.get(char, char)
    return result

# ============================================================
# PREMIUM EMOJIS - MIXTURE
# ============================================================
PREMIUM_EMOJIS = {
    "✅": "6147565374289220368",
    "💎": "6147524086768604985",
    "⭐": "6235403472741603087",
    "🔥": "6032673796530377389",
    "❤️": "6147617184479711380",
    "👍": "6274007313107915274",
    "🌟": "6035338338406242050",
    "✨": "6010338729640596556",
    "🔫": "6035243995154616907",
    "🆓": "6035060329468137931",
    "📞": "6035072209347678547",
    "👑": "5794422335599546668",
    "💰": "6089104607328342288",
    "💳": "6089140105233044310",
    "🏦": "6086664791026307819",
    "📊": "6035085583875837709",
    "👥": "6035081585261287115",
    "📥": "6035210301136182368",
    "📋": "6035317340311129897",
    "➕": "6035372904303038740",
    "❌": "6034843326245508065",
    "⚠️": "6035355642829475999",
    "⏳": "6035374291577475270",
    "🟢": "6035372401791864953",
    "🔴": "6035355642829475999",
    "👤": "6035051267087143217",
    "🆔": "6034945975963881533",
    "👾": "6035169816774446606",
    "🔢": "6034845323405299835",
    "📌": "6035087164423802534",
    "💬": "6035070298087231243",
    "📱": "6035225389356290238",
    "🔄": "6035173858338672933",
    "🎉": "6034955549445984368",
    "⚡": "5791970059597386804",
    "🔑": "6035137110598492010",
    "📸": "6035225389356290238",
    "🤖": "6035169816774446606",
    "📢": "6035210301136182368",
}

# ============================================================
# GET RANDOM PREMIUM EMOJI
# ============================================================
def get_random_premium_emoji():
    return random.choice(list(PREMIUM_EMOJIS.keys()))

# ============================================================
# USERS DATA
# ============================================================
def load_users():
    if os.path.exists(USERS_FILE):
        try:
            with open(USERS_FILE, "r") as f:
                return json.load(f)
        except:
            pass
    
    users = {
        "8586849798": {"id": 8586849798, "username": "Ffaccsellerx", "name": "FF SELLER", "joined": "2026-07-31T05:18:43.493579", "uses": 1, "unlimited": False, "banned": False},
        "8908882066": {"id": 8908882066, "username": None, "name": "Dice", "joined": "2026-07-31T05:30:04.435718", "uses": 0, "unlimited": False, "banned": False},
        "8471373583": {"id": 8471373583, "username": "iflexzyan", "name": "ZYAN", "joined": "2026-07-31T05:30:31.611686", "uses": 0, "unlimited": False, "banned": False},
        "6729963447": {"id": 6729963447, "username": "ZIXU_NXT", "name": "BUNNY !!! ✨", "joined": "2026-07-31T05:31:09.765285", "uses": 0, "unlimited": False, "banned": False},
        "8955229317": {"id": 8955229317, "username": "LEGENDxFIRE", "name": "LEGEND X FIRE 🔥", "joined": "2026-07-31T05:39:01.873843", "uses": 0, "unlimited": True, "banned": False},
        "7977493987": {"id": 7977493987, "username": "Havkerbabaybaba", "name": "Bhai on top", "joined": "2026-07-31T05:39:30.486969", "uses": 0, "unlimited": False, "banned": False},
        "6415045552": {"id": 6415045552, "username": "FOREXX_XD", "name": "FOREXX !!", "joined": "2026-07-31T06:16:36.698711", "uses": 0, "unlimited": False, "banned": False},
        "5961757687": {"id": 5961757687, "username": "Nexo4a", "name": "NEXO", "joined": "2026-07-31T06:17:15.251743", "uses": 0, "unlimited": False, "banned": False},
        "7710991582": {"id": 7710991582, "username": "VccvNomoreccBOT", "name": "Shsb", "joined": "2026-07-31T06:19:52.133642", "uses": 0, "unlimited": False, "banned": False},
        "8741006842": {"id": 8741006842, "username": "LUXFIRE10", "name": "Hello", "joined": "2026-07-31T06:22:17.941171", "uses": 0, "unlimited": False, "banned": False},
        "7896163877": {"id": 7896163877, "username": "cbwel", "name": "VARDAN !!!", "joined": "2026-07-31T06:23:29.242823", "uses": 0, "unlimited": False, "banned": False},
        "8894084046": {"id": 8894084046, "username": None, "name": "Jatin", "joined": "2026-07-31T06:54:35.530336", "uses": 0, "unlimited": False, "banned": False},
        "8345492643": {"id": 8345492643, "username": None, "name": "Fxiiznnn.1", "joined": "2026-07-31T07:06:34.662687", "uses": 0, "unlimited": True, "banned": False},
        "7222081143": {"id": 7222081143, "username": None, "name": "Autopay Agent", "joined": "2026-07-31T07:33:26.632237", "uses": 0, "unlimited": False, "banned": False},
        "8763036983": {"id": 8763036983, "username": "TGKNOWBIKASH", "name": "BIKASH !!!!", "joined": "2026-07-31T07:34:18.997414", "uses": 0, "unlimited": False, "banned": False},
        "6519679140": {"id": 6519679140, "username": "Errorzlive", "name": "ERROR ERA !!", "joined": "2026-07-31T07:34:51.396062", "uses": 0, "unlimited": False, "banned": False},
        "5506071596": {"id": 5506071596, "username": "Zexyxexe", "name": "ZEXY", "joined": "2026-07-31T07:57:02.898103", "uses": 0, "unlimited": False, "banned": False},
        "5749912145": {"id": 5749912145, "username": "Zetoxexe", "name": "ZETOX", "joined": "2026-07-31T07:59:50.685331", "uses": 0, "unlimited": False, "banned": False},
        "8690459200": {"id": 8690459200, "username": "SAITAMAxFF", "name": "SAITAMA FF...!!!", "joined": "2026-07-31T08:56:45.327673", "uses": 0, "unlimited": False, "banned": False},
        "7178372394": {"id": 7178372394, "username": "Abhi_sama1", "name": "Abhi", "joined": "2026-07-31T12:08:57.178524", "uses": 0, "unlimited": False, "banned": False},
        "6776661878": {"id": 6776661878, "username": "TNSELLERFFID", "name": "ITAN", "joined": "2026-07-31T12:10:03.408531", "uses": 0, "unlimited": False, "banned": False},
        "7796329793": {"id": 7796329793, "username": "Vir4jsharma2069", "name": "VIRAJ SHARMA", "joined": "2026-07-31T12:17:34.926080", "uses": 0, "unlimited": False, "banned": False}
    }
    save_users(users)
    return users

def save_users(users):
    with open(USERS_FILE, "w") as f:
        json.dump(users, f, indent=2)

def load_buttons():
    if os.path.exists(BUTTONS_FILE):
        try:
            with open(BUTTONS_FILE, "r") as f:
                return json.load(f)
        except:
            return {}
    return {}

def save_buttons(buttons):
    with open(BUTTONS_FILE, "w") as f:
        json.dump(buttons, f, indent=2)

def load_data(file):
    if os.path.exists(file):
        try:
            with open(file, "r") as f:
                return json.load(f)
        except:
            return {}
    return {}

def save_data(file, data):
    with open(file, "w") as f:
        json.dump(data, f, indent=2)

def load_orders():
    return load_data(ORDERS_FILE)

def save_orders(orders):
    save_data(ORDERS_FILE, orders)

def load_pending():
    return load_data(PENDING_FILE)

def save_pending(pending):
    save_data(PENDING_FILE, pending)

def load_settings():
    default = {
        "price": 99,
        "upi": "vanshx111@naviaxis",
        "free_trial": True,
        "bot_name": "FF BAN BOT",
        "developer": "@iflexzyan",
        "support": "@iflexzyan",
        "welcome_image": "https://iili.io/C8DNTyQ.jpg",
        "token_text": "1️⃣ Open Free Fire Game\n2️⃣ Go to Settings ⚙️\n3️⃣ Click on Account\n4️⃣ Find Data Access\n5️⃣ Copy Access Token"
    }
    data = load_data(SETTINGS_FILE)
    for key, val in default.items():
        if key not in data:
            data[key] = val
    return data

def save_settings(settings):
    save_data(SETTINGS_FILE, settings)

# ============================================================
# EMOJI HELPERS
# ============================================================
def get_emoji_id(emoji: str) -> int:
    return int(PREMIUM_EMOJIS.get(emoji, "6147565374289220368"))

def _utf16_len(ch: str) -> int:
    return len(ch.encode("utf-16-le")) // 2

def _utf16_len_str(s: str) -> int:
    return len(s.encode("utf-16-le")) // 2

def _build_pe_entities(text: str):
    entities = []
    utf16_offset = 0
    total_utf16 = _utf16_len_str(text)
    
    if total_utf16 > 0:
        entities.append(MessageEntity(type="bold", offset=0, length=total_utf16))
    
    i = 0
    while i < len(text):
        ch = text[i]
        ch_len = _utf16_len(ch)
        
        if ch in PREMIUM_EMOJIS:
            eid = int(PREMIUM_EMOJIS[ch])
            entities.append(MessageEntity(
                type="custom_emoji",
                offset=utf16_offset,
                length=ch_len,
                custom_emoji_id=eid
            ))
        utf16_offset += ch_len
        i += 1
    
    return entities

def _send_pe(chat_id, text: str, reply_markup=None):
    entities = _build_pe_entities(text)
    try:
        return bot.send_message(chat_id, text, entities=entities, reply_markup=reply_markup, parse_mode=None)
    except:
        return bot.send_message(chat_id, text, reply_markup=reply_markup)

def _send_pe_return(chat_id, text: str, reply_markup=None):
    entities = _build_pe_entities(text)
    try:
        return bot.send_message(chat_id, text, entities=entities, reply_markup=reply_markup, parse_mode=None)
    except:
        return bot.send_message(chat_id, text, reply_markup=reply_markup)

# ============================================================
# MAKE COLORED BUTTONS
# ============================================================
def make_colored_button(text: str, style: str = None, callback: str = None, url: str = None):
    stylish_text_result = stylish_text(text)
    left_emoji = get_random_premium_emoji()
    right_emoji = get_random_premium_emoji()
    final_text = f"{left_emoji} {stylish_text_result} {right_emoji}"
    
    try:
        if callback:
            return InlineKeyboardButton(text=final_text, style=style, callback_data=callback)
        elif url:
            return InlineKeyboardButton(text=final_text, style=style, url=url)
        else:
            return InlineKeyboardButton(text=final_text, style=style)
    except:
        if callback:
            return InlineKeyboardButton(text=final_text, callback_data=callback)
        elif url:
            return InlineKeyboardButton(text=final_text, url=url)
        else:
            return InlineKeyboardButton(text=final_text)

def make_green_button(text: str, callback: str = None, url: str = None):
    return make_colored_button(text, style="success", callback=callback, url=url)

def make_red_button(text: str, callback: str = None, url: str = None):
    return make_colored_button(text, style="danger", callback=callback, url=url)

def make_blue_button(text: str, callback: str = None, url: str = None):
    return make_colored_button(text, style="primary", callback=callback, url=url)

# ============================================================
# HELPERS
# ============================================================
def is_admin(user_id):
    return user_id in ADMIN_IDS

def register_user(user_id, username=None, first_name=None):
    users = load_users()
    if str(user_id) not in users:
        users[str(user_id)] = {
            "id": user_id,
            "username": username,
            "name": first_name or "Unknown",
            "joined": datetime.now().isoformat(),
            "uses": 0,
            "unlimited": False,
            "banned": False
        }
        save_users(users)
        notify_owner(f"✅ ɴᴇᴡ ᴜsᴇʀ ᴊᴏɪɴᴇᴅ!\n👤 ɪᴅ: {user_id}\n👾 @{username or 'N/A'}")
    return users[str(user_id)]

def get_user(user_id):
    users = load_users()
    return users.get(str(user_id))

def update_user(user_id, key, value):
    users = load_users()
    if str(user_id) in users:
        users[str(user_id)][key] = value
        save_users(users)

def notify_owner(msg):
    try:
        bot.send_message(OWNER_ID, msg)
    except:
        pass

# ============================================================
# GET USER MENU
# ============================================================
def get_user_menu(user_id):
    markup = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    
    markup.row(KeyboardButton(f"🔫 {stylish_text('BAN ACCOUNT')}"))
    markup.row(
        KeyboardButton(f"🆓 {stylish_text('FREE TRIAL')}"),
        KeyboardButton(f"💎 {stylish_text('UNLIMITED')}")
    )
    markup.row(
        KeyboardButton(f"❓ {stylish_text('HOW TO GET TOKEN')}"),
        KeyboardButton(f"📞 {stylish_text('SUPPORT')}")
    )
    markup.row(
        KeyboardButton(f"❓ {stylish_text('HELP')}"),
        KeyboardButton(f"ℹ️ {stylish_text('ABOUT')}")
    )
    
    return markup

# ============================================================
# GET ADMIN MENU
# ============================================================
def get_admin_menu(user_id):
    markup = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    
    markup.row(
        KeyboardButton(f"🔴 {stylish_text('BOT OFF')}"),
        KeyboardButton(f"🟢 {stylish_text('BOT ON')}")
    )
    markup.row(
        KeyboardButton(f"👑 {stylish_text('ADMIN PANEL')}"),
        KeyboardButton(f"📊 {stylish_text('STATS')}")
    )
    markup.row(
        KeyboardButton(f"👥 {stylish_text('USERS')}"),
        KeyboardButton(f"📥 {stylish_text('DATA')}")
    )
    markup.row(
        KeyboardButton(f"💳 {stylish_text('PRICE')}"),
        KeyboardButton(f"🏦 {stylish_text('UPI')}")
    )
    markup.row(
        KeyboardButton(f"➕ {stylish_text('ADD ADMIN')}"),
        KeyboardButton(f"📋 {stylish_text('ALL COMMANDS')}")
    )
    markup.row(
        KeyboardButton(f"❓ {stylish_text('HOW TO GET TOKEN')}"),
        KeyboardButton(f"📢 {stylish_text('BROADCAST')}")
    )
    markup.row(
        KeyboardButton(f"📢 {stylish_text('ALL BROADCAST')}"),
        KeyboardButton(f"🖼️ {stylish_text('SET WELCOME IMAGE')}")
    )
    markup.row(
        KeyboardButton(f"📝 {stylish_text('SET TOKEN TEXT')}"),
        KeyboardButton(f"")
    )
    
    return markup

# ============================================================
# ALL COMMANDS
# ============================================================
@bot.message_handler(commands=['allcommands'])
def all_commands_cmd(message):
    if not is_admin(message.from_user.id):
        _send_pe(message.chat.id, f"❌ ᴜɴᴀᴜᴛʜᴏʀɪᴢᴇᴅ!")
        return
    
    text = f"""
✅ ═══《 📋 ᴀʟʟ ᴄᴏᴍᴍᴀɴᴅs 》═══ ✅

✅ ᴜsᴇʀ ᴄᴏᴍᴍᴀɴᴅs:
✅ /start - sᴛᴀʀᴛ ʙᴏᴛ
✅ /help - ʜᴇʟᴘ ɢᴜɪᴅᴇ

✅ ═══════════════════════ ✅

✅ ᴀᴅᴍɪɴ ᴄᴏᴍᴍᴀɴᴅs:
✅ /approve ɪᴅ - ᴀᴘᴘʀᴏᴠᴇ ᴘᴀʏᴍᴇɴᴛ
✅ /disapprove ɪᴅ - ʀᴇᴊᴇᴄᴛ ᴘᴀʏᴍᴇɴᴛ
✅ /ban ɪᴅ - ʙᴀɴ ᴜsᴇʀ
✅ /unban ɪᴅ - ᴜɴʙᴀɴ ᴜsᴇʀ
✅ /users - sʜᴏᴡ ᴀʟʟ ᴜsᴇʀs
✅ /data - ᴅᴏᴡɴʟᴏᴀᴅ ᴅᴀᴛᴀ
✅ /price <ᴀᴍᴛ> - ᴄʜᴀɴɢᴇ ᴘʀɪᴄᴇ
✅ /upi <ᴜᴘɪ> - ᴄʜᴀɴɢᴇ ᴜᴘɪ
✅ /developer <@> - ᴄʜᴀɴɢᴇ ᴅᴇᴠᴇʟᴏᴘᴇʀ
✅ /addadmin ɪᴅ - ᴀᴅᴅ ᴀᴅᴍɪɴ
✅ /broadcastuser ɪᴅ ᴍsɢ - sᴇɴᴅ ᴛᴏ ᴜsᴇʀ
✅ /allbroadcast ᴍsɢ - sᴇɴᴅ ᴛᴏ ᴀʟʟ
✅ /addtokenvideo - ᴀᴅᴅ ᴛᴏᴋᴇɴ ᴠɪᴅᴇᴏ
✅ /settokentext - sᴇᴛ ᴛᴏᴋᴇɴ ᴛᴇxᴛ
✅ /setwelcomeimage - sᴇᴛ ᴡᴇʟᴄᴏᴍᴇ ɪᴍᴀɢᴇ
✅ /allcommands - ᴛʜɪs ᴍᴇɴᴜ

✅ ═══════════════════════ ✅
"""
    _send_pe(message.chat.id, text)

# ============================================================
# SET TOKEN TEXT
# ============================================================
@bot.message_handler(commands=['settokentext'])
def set_token_text_cmd(message):
    if not is_admin(message.from_user.id):
        _send_pe(message.chat.id, f"❌ ᴜɴᴀᴜᴛʜᴏʀɪᴢᴇᴅ!")
        return
    
    _send_pe(message.chat.id, f"""
✅ ═══《 📝 sᴇᴛ ᴛᴏᴋᴇɴ ᴛᴇxᴛ 》═══ ✅

✅ sᴇɴᴅ ᴍᴇ ᴛʜᴇ ɴᴇᴡ ᴛᴇxᴛ ғᴏʀ 'ʜᴏᴡ ᴛᴏ ɢᴇᴛ ᴛᴏᴋᴇɴ'

✅ ᴇxᴀᴍᴘʟᴇ:
✅ 𝟷️⃣ ᴏᴘᴇɴ ғʀᴇᴇ ғɪʀᴇ
✅ 𝟸️⃣ ɢᴏ ᴛᴏ sᴇᴛᴛɪɴɢs
✅ 𝟹️⃣ ᴄʟɪᴄᴋ ᴀᴄᴄᴏᴜɴᴛ
✅ 𝟺️⃣ ғɪɴᴅ ᴅᴀᴛᴀ ᴀᴄᴄᴇss
✅ 𝟻️⃣ ᴄᴏᴘʏ ᴀᴄᴄᴇss ᴛᴏᴋᴇɴ

✅ ═══════════════════════ ✅
""")
    bot.register_next_step_handler(message, save_token_text)

def save_token_text(message):
    if not is_admin(message.from_user.id):
        return
    
    settings = load_settings()
    settings["token_text"] = message.text.strip()
    save_settings(settings)
    _send_pe(message.chat.id, f"✅ ᴛᴏᴋᴇɴ ᴛᴇxᴛ ᴜᴘᴅᴀᴛᴇᴅ!")

# ============================================================
# ADD TOKEN VIDEO
# ============================================================
@bot.message_handler(commands=['addtokenvideo'])
def add_token_video(message):
    if not is_admin(message.from_user.id):
        _send_pe(message.chat.id, f"❌ ᴜɴᴀᴜᴛʜᴏʀɪᴢᴇᴅ!")
        return
    
    _send_pe(message.chat.id, f"📤 sᴇɴᴅ ᴠɪᴅᴇᴏ ғᴏʀ 'ʜᴏᴡ ᴛᴏ ɢᴇᴛ ᴛᴏᴋᴇɴ'")
    bot.register_next_step_handler(message, save_token_video)

def save_token_video(message):
    if message.video:
        file_info = bot.get_file(message.video.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        with open("token_video.mp4", "wb") as f:
            f.write(downloaded_file)
        _send_pe(message.chat.id, f"✅ ᴠɪᴅᴇᴏ sᴀᴠᴇᴅ!")
    else:
        _send_pe(message.chat.id, f"❌ sᴇɴᴅ ᴀ ᴠɪᴅᴇᴏ!")

# ============================================================
# SET WELCOME IMAGE
# ============================================================
@bot.message_handler(commands=['setwelcomeimage'])
def set_welcome_image_cmd(message):
    if not is_admin(message.from_user.id):
        _send_pe(message.chat.id, f"❌ ᴜɴᴀᴜᴛʜᴏʀɪᴢᴇᴅ!")
        return
    
    _send_pe(message.chat.id, f"""
✅ ═══《 🖼️ sᴇᴛ ᴡᴇʟᴄᴏᴍᴇ ɪᴍᴀɢᴇ 》═══ ✅

✅ sᴇɴᴅ ᴀ ᴘʜᴏᴛᴏ ᴏʀ ɪᴍᴀɢᴇ ᴜʀʟ

✅ ═══════════════════════ ✅
""")
    bot.register_next_step_handler(message, save_welcome_image)

def save_welcome_image(message):
    if not is_admin(message.from_user.id):
        return
    
    settings = load_settings()
    
    if message.photo:
        file_id = message.photo[-1].file_id
        settings["welcome_image"] = file_id
        save_settings(settings)
        _send_pe(message.chat.id, f"✅ ᴡᴇʟᴄᴏᴍᴇ ɪᴍᴀɢᴇ ᴜᴘᴅᴀᴛᴇᴅ!")
    elif message.text and message.text.startswith("http"):
        settings["welcome_image"] = message.text.strip()
        save_settings(settings)
        _send_pe(message.chat.id, f"✅ ᴡᴇʟᴄᴏᴍᴇ ɪᴍᴀɢᴇ ᴜʀʟ ᴜᴘᴅᴀᴛᴇᴅ!")
    else:
        _send_pe(message.chat.id, f"❌ sᴇɴᴅ ᴀ ᴘʜᴏᴛᴏ ᴏʀ ᴠᴀʟɪᴅ ᴜʀʟ!")

# ============================================================
# BOT COMMANDS
# ============================================================

@bot.message_handler(commands=['start'])
def start_cmd(message):
    user_id = message.from_user.id
    username = message.from_user.username
    first_name = message.from_user.first_name
    
    settings = load_settings()
    price = settings.get("price", 99)
    developer = settings.get("developer", "@iflexzyan")
    welcome_image = settings.get("welcome_image", "https://iili.io/C8DNTyQ.jpg")
    
    user = register_user(user_id, username, first_name)
    
    if user.get("banned", False):
        _send_pe(message.chat.id, f"❌ ʏᴏᴜ ᴀʀᴇ ʙᴀɴɴᴇᴅ!")
        return
    
    try:
        if welcome_image.startswith("http"):
            bot.send_photo(message.chat.id, photo=welcome_image)
        else:
            bot.send_photo(message.chat.id, photo=welcome_image)
    except:
        try:
            bot.send_photo(message.chat.id, photo="https://iili.io/C8DNTyQ.jpg")
        except:
            pass
    
    welcome_text = f"""
✅ ═══《 🔥 ᴡᴇʟᴄᴏᴍᴇ ᴛᴏ ғғ ʙᴀɴ ʙᴏᴛ 》═══ ✅

✅ 👤 ᴜsᴇʀ: {first_name}
✅ 🆔 ɪᴅ: {user_id}
✅ 👾 ᴜsᴇʀɴᴀᴍᴇ: @{username or 'N/A'}

✅ ═══════════════════════ ✅

✅ 🎯 𝟷 ғʀᴇᴇ ᴛʀɪᴀʟ - ʙᴀɴ 𝟷 ᴀᴄᴄᴏᴜɴᴛ
✅ 💰 ᴜɴʟɪᴍɪᴛᴇᴅ ᴀᴄᴄᴇss - ʀs.{price}

✅ ═══════════════════════ ✅

✅ 👨‍💻 ᴅᴇᴠᴇʟᴏᴘᴇʀ: {developer}

✅ ═══════════════════════ ✅
"""
    
    if is_admin(user_id):
        markup = get_admin_menu(user_id)
    else:
        markup = get_user_menu(user_id)
    
    _send_pe(message.chat.id, welcome_text, reply_markup=markup)

@bot.message_handler(commands=['help'])
def help_cmd(message):
    user_id = message.from_user.id
    
    if is_admin(user_id):
        markup = get_admin_menu(user_id)
    else:
        markup = get_user_menu(user_id)
    
    help_text = f"""
✅ ═══《 ❓ ʜᴇʟᴘ 》═══ ✅

✅ ʜᴏᴡ ᴛᴏ ᴜsᴇ:

✅ 𝟷️⃣ ᴄʟɪᴄᴋ ʙᴀɴ ᴀᴄᴄᴏᴜɴᴛ
✅ 𝟸️⃣ sᴇɴᴅ ᴀᴄᴄᴇss ᴛᴏᴋᴇɴ
✅ 𝟹️⃣ ᴄᴏɴғɪʀᴍ ʏᴇs
✅ 𝟺️⃣ ᴀᴄᴄᴏᴜɴᴛ ɢᴇᴛs ʙᴀɴɴᴇᴅ!

✅ ═══════════════════ ✅

✅ 🆓 ғʀᴇᴇ ᴛʀɪᴀʟ: 𝟷 ʙᴀɴ✅ 💰 ᴜɴʟɪᴍɪᴛᴇᴅ: ᴘᴀʏ & ɢᴇᴛ

✅ ═══════════════════ ✅

✅ 👨‍💻 ᴅᴇᴠᴇʟᴏᴘᴇʀ: @iflexzyan
"""
    _send_pe(message.chat.id, help_text, reply_markup=markup)

# ============================================================
# BAN ACCOUNT - WITH CONFIRMATION
# ============================================================

user_tokens = {}

@bot.message_handler(func=lambda m: m.text and "ʙᴀɴ ᴀᴄᴄᴏᴜɴᴛ" in m.text.lower())
def ban_account_start(message):
    user_id = message.from_user.id
    user = get_user(user_id)
    
    if not user or user.get("banned", False):
        _send_pe(message.chat.id, f"❌ ʏᴏᴜ ᴀʀᴇ ʙᴀɴɴᴇᴅ!")
        return
    
    if not user.get("unlimited", False):
        uses = user.get("uses", 0)
        if uses >= 1:
            _send_pe(message.chat.id, f"⚠️ ғʀᴇᴇ ᴛʀɪᴀʟ ᴜsᴇᴅ!\n💰 ᴘᴀʏ ʀs.{load_settings().get('price', 99)} ғᴏʀ ᴜɴʟɪᴍɪᴛᴇᴅ")
            send_payment_qr(message.chat.id)
            return
    
    _send_pe(message.chat.id, f"🔑 sᴇɴᴅ ᴛʜᴇ ᴀᴄᴄᴇss ᴛᴏᴋᴇɴ:")
    bot.register_next_step_handler(message, get_ban_token)

def get_ban_token(message):
    user_id = message.from_user.id
    token = message.text.strip()
    
    if len(token) < 30:
        _send_pe(message.chat.id, f"❌ ɪɴᴠᴀʟɪᴅ ᴛᴏᴋᴇɴ!")
        return
    
    user_tokens[user_id] = token
    
    keyboard = [
        [make_green_button("ʏᴇs, ɪ ᴀᴍ 𝟷𝟶𝟶% sᴜʀᴇ", callback=f"confirm_ban_{user_id}")],
        [make_red_button("ɴᴏ, ᴄᴀɴᴄᴇʟ", callback="cancel_ban")]
    ]
    markup = InlineKeyboardMarkup(keyboard)
    
    _send_pe(message.chat.id, f"""
⚠️ ═══《 ⚠️ ᴄᴏɴғɪʀᴍᴀᴛɪᴏɴ 》═══ ⚠️

⚠️ ᴀʀᴇ ʏᴏᴜ 𝟷𝟶𝟶% sᴜʀᴇ?

⚠️ ᴛʜɪs ᴀᴄᴛɪᴏɴ ᴄᴀɴɴᴏᴛ ʙᴇ ᴜɴᴅᴏɴᴇ!

⚠️ ═══════════════════════ ⚠️
""", reply_markup=markup)

@bot.callback_query_handler(func=lambda c: c.data and c.data.startswith("confirm_ban_"))
def confirm_ban_callback(call):
    user_id = int(call.data.split("_")[2])
    
    if call.from_user.id != user_id:
        _send_pe(call.message.chat.id, f"❌ ɴᴏᴛ ʏᴏᴜʀ ʀᴇǫᴜᴇsᴛ!")
        bot.answer_callback_query(call.id)
        return
    
    token = user_tokens.get(user_id)
    if not token:
        _send_pe(call.message.chat.id, f"❌ sᴇssɪᴏɴ ᴇxᴘɪʀᴇᴅ!")
        bot.answer_callback_query(call.id)
        return
    
    try:
        bot.delete_message(call.message.chat.id, call.message.message_id)
    except:
        pass
    
    msg = _send_pe_return(call.message.chat.id, f"⏳ ʙᴀɴɴɪɴɢ...")
    
    try:
        url = f"https://ffidbanapi.vercel.app/ban-account?access-token={token}&key=ANIXH"
        response = requests.get(url, timeout=30)
        data = response.json()
        
        account_id = data.get('id', 'N/A')
        account_name = data.get('name', 'N/A')
        account_uid = data.get('uid', 'N/A')
        status = data.get('status', 'UNKNOWN')
        
        is_banned = "BANNED" in str(status).upper()
        
        bot.delete_message(call.message.chat.id, msg.message_id)
        
        if is_banned:
            user = get_user(user_id)
            if user:
                uses = user.get("uses", 0) + 1
                update_user(user_id, "uses", uses)
            
            result_text = f"""
✅ ═══《 ✅ ᴀᴄᴄᴏᴜɴᴛ ʙᴀɴɴᴇᴅ 》═══ ✅

✅ 🎯 ʙᴀɴ sᴜᴄᴄᴇssғᴜʟ!

✅ ═══════════════════════ ✅

✅ 🆔 ɪᴅ: {account_id}
✅ 👤 ɴᴀᴍᴇ: {account_name}
✅ 🔢 ᴜɪᴅ: {account_uid}

✅ ═══════════════════════ ✅

✅ 👨‍💻 @iflexzyan
"""
            keyboard = [
                [make_green_button("ʙᴀɴ ᴀɴᴏᴛʜᴇʀ", callback="ban_another")],
                [make_blue_button("ɢᴇᴛ ᴜɴʟɪᴍɪᴛᴇᴅ", callback="get_unlimited")]
            ]
            markup = InlineKeyboardMarkup(keyboard)
            _send_pe(call.message.chat.id, result_text, reply_markup=markup)
            
            notify_owner(f"✅ ʙᴀɴɴᴇᴅ!\n👤 {user_id}\n🔢 {account_uid}")
            
        else:
            result_text = f"""
❌ ═══《 ❌ ʙᴀɴ ғᴀɪʟᴇᴅ 》═══ ❌

❌ ɴᴏᴛ ʙᴀɴɴᴇᴅ!

❌ 🆔 ɪᴅ: {account_id}
❌ 👤 ɴᴀᴍᴇ: {account_name}
❌ 🔢 ᴜɪᴅ: {account_uid}
❌ 📌 sᴛᴀᴛᴜs: {status}

❌ ═══════════════════════ ❌

❌ 👨‍💻 @iflexzyan
"""
            _send_pe(call.message.chat.id, result_text)
            
    except Exception as e:
        bot.delete_message(call.message.chat.id, msg.message_id)
        _send_pe(call.message.chat.id, f"❌ ᴇʀʀᴏʀ: {str(e)}")
    
    user_tokens.pop(user_id, None)
    bot.answer_callback_query(call.id)

@bot.callback_query_handler(func=lambda c: c.data == "cancel_ban")
def cancel_ban_callback(call):
    try:
        bot.delete_message(call.message.chat.id, call.message.message_id)
    except:
        pass
    _send_pe(call.message.chat.id, f"✅ ᴄᴀɴᴄᴇʟʟᴇᴅ!")
    user_tokens.pop(call.from_user.id, None)
    bot.answer_callback_query(call.id)

# ============================================================
# PAYMENT SYSTEM
# ============================================================

def send_payment_qr(chat_id):
    settings = load_settings()
    upi = settings.get("upi", "vanshx111@naviaxis")
    price = settings.get("price", 99)
    
    qr_url = f"https://api.qrserver.com/v1/create-qr-code/?size=300x300&data=upi://pay?pa={upi}&am={price}&cu=INR"
    
    text = f"""
✅ ═══《 💰 ᴘᴀʏᴍᴇɴᴛ 》═══ ✅

✅ 💳 ᴜᴘɪ: {upi}
✅ 💰 ᴀᴍᴏᴜɴᴛ: ʀs.{price}

✅ ═══════════════════════ ✅

✅ 📱 sᴄᴀɴ ǫʀ ᴛᴏ ᴘᴀʏ

✅ ═══════════════════════ ✅
"""
    
    keyboard = [
        [make_green_button("ɪ ʜᴀᴠᴇ ᴘᴀɪᴅ", callback=f"paid_{chat_id}")],
        [make_red_button("ᴄᴀɴᴄᴇʟ", callback="cancel_payment")]
    ]
    markup = InlineKeyboardMarkup(keyboard)
    
    try:
        bot.send_photo(chat_id, photo=qr_url, caption=text, reply_markup=markup)
    except:
        _send_pe(chat_id, text, reply_markup=markup)

@bot.callback_query_handler(func=lambda c: c.data and c.data.startswith("paid_"))
def handle_paid(call):
    user_id = call.from_user.id
    chat_id = call.message.chat.id
    
    try:
        bot.delete_message(chat_id, call.message.message_id)
    except:
        pass
    
    pending = load_pending()
    pending[str(user_id)] = {
        "user_id": user_id,
        "username": call.from_user.username,
        "name": call.from_user.first_name,
        "status": "pending",
        "requested": datetime.now().isoformat()
    }
    save_pending(pending)
    
    _send_pe(chat_id, f"📸 sᴇɴᴅ sᴄʀᴇᴇɴsʜᴏᴛ!")
    bot.register_next_step_handler(call.message, receive_payment_screenshot)
    bot.answer_callback_query(call.id)

def receive_payment_screenshot(message):
    user_id = message.from_user.id
    
    if message.photo:
        file_id = message.photo[-1].file_id
        pending = load_pending()
        if str(user_id) in pending:
            pending[str(user_id)]["screenshot"] = file_id
            pending[str(user_id)]["status"] = "pending"
            save_pending(pending)
        
        _send_pe(message.chat.id, f"✅ ʀᴇᴄᴇɪᴠᴇᴅ!\n⏳ ᴡᴀɪᴛ ғᴏʀ ᴀᴅᴍɪɴ")
        
        admin_text = f"""
✅ ═══《 💰 ɴᴇᴡ ᴘᴀʏᴍᴇɴᴛ 》═══ ✅

✅ 👤 {message.from_user.first_name}
✅ 🆔 {user_id}
✅ 👾 @{message.from_user.username or 'N/A'}

✅ 📌 /approve {user_id}
✅ 📌 /disapprove {user_id}
"""
        for admin in ADMIN_IDS:
            try:
                bot.send_photo(admin, photo=file_id, caption=admin_text)
            except:
                bot.send_message(admin, admin_text)
    else:
        _send_pe(message.chat.id, f"❌ sᴇɴᴅ ᴀ ᴘʜᴏᴛᴏ!")

@bot.callback_query_handler(func=lambda c: c.data == "cancel_payment")
def cancel_payment_callback(call):
    try:
        bot.delete_message(call.message.chat.id, call.message.message_id)
    except:
        pass
    _send_pe(call.message.chat.id, f"✅ ᴄᴀɴᴄᴇʟʟᴇᴅ!")
    bot.answer_callback_query(call.id)

# ============================================================
# FREE TRIAL, UNLIMITED, SUPPORT, ABOUT, HOW TO GET TOKEN
# ============================================================

@bot.message_handler(func=lambda m: m.text and "ғʀᴇᴇ ᴛʀɪᴀʟ" in m.text.lower())
def free_trial_cmd(message):
    user_id = message.from_user.id
    user = get_user(user_id)
    
    if not user:
        _send_pe(message.chat.id, f"❌ /start ғɪʀsᴛ!")
        return
    
    if user.get("unlimited", False):
        _send_pe(message.chat.id, f"✅ ᴀʟʀᴇᴀᴅʏ ᴜɴʟɪᴍɪᴛᴇᴅ!")
        return
    
    uses = user.get("uses", 0)
    if uses >= 1:
        _send_pe(message.chat.id, f"⚠️ ᴜsᴇᴅ!\n💰 ᴘᴀʏ ʀs.{load_settings().get('price', 99)}")
        send_payment_qr(message.chat.id)
        return
    
    _send_pe(message.chat.id, f"🆓 ᴀᴄᴛɪᴠᴀᴛᴇᴅ!\n🔫 sᴇɴᴅ ᴛᴏᴋᴇɴ!")

@bot.message_handler(func=lambda m: m.text and "ᴜɴʟɪᴍɪᴛᴇᴅ" in m.text.lower())
def unlimited_cmd(message):
    user_id = message.from_user.id
    user = get_user(user_id)
    
    if user and user.get("unlimited", False):
        _send_pe(message.chat.id, f"✅ ᴀʟʀᴇᴀᴅʏ ᴜɴʟɪᴍɪᴛᴇᴅ!")
        return
    
    send_payment_qr(message.chat.id)

@bot.message_handler(func=lambda m: m.text and "sᴜᴘᴘᴏʀᴛ" in m.text.lower())
def support_cmd(message):
    settings = load_settings()
    support = settings.get("support", "@iflexzyan")
    developer = settings.get("developer", "@iflexzyan")
    
    text = f"""
✅ ═══《 📞 sᴜᴘᴘᴏʀᴛ 》═══ ✅

✅ 👨‍💻 {developer}

✅ ғᴏʀ ᴀɴʏ ɪssᴜᴇ:
✅ 📱 {support}

✅ ═══════════════════════ ✅
"""
    markup = InlineKeyboardMarkup([
        [make_blue_button("ᴄᴏɴᴛᴀᴄᴛ", url=f"https://t.me/{support.replace('@', '')}")]
    ])
    _send_pe(message.chat.id, text, reply_markup=markup)

@bot.message_handler(func=lambda m: m.text and "ᴀʙᴏᴜᴛ" in m.text.lower())
def about_cmd(message):
    settings = load_settings()
    developer = settings.get("developer", "@iflexzyan")
    
    text = f"""
✅ ═══《 ℹ️ ᴀʙᴏᴜᴛ 》═══ ✅

✅ 🤖 ғғ ʙᴀɴ ʙᴏᴛ

✅ 🔫 ʙᴀɴ ғʀᴇᴇ ғɪʀᴇ ᴀᴄᴄᴏᴜɴᴛs
✅ 💰 ᴘᴀʏ & ɢᴇᴛ ᴜɴʟɪᴍɪᴛᴇᴅ
✅ 🆓 𝟷 ғʀᴇᴇ ᴛʀɪᴀʟ

✅ 👨‍💻 {developer}
"""
    _send_pe(message.chat.id, text)

@bot.message_handler(func=lambda m: m.text and "ʜᴏᴡ ᴛᴏ ɢᴇᴛ ᴛᴏᴋᴇɴ" in m.text.lower())
def how_to_get_token(message):
    settings = load_settings()
    token_text = settings.get("token_text", "1️⃣ Open Free Fire\n2️⃣ Go to Settings\n3️⃣ Click Account\n4️⃣ Find Data Access\n5️⃣ Copy Token")
    
    # Send text first
    _send_pe(message.chat.id, f"""
✅ ═══《 🔑 ʜᴏᴡ ᴛᴏ ɢᴇᴛ ᴛᴏᴋᴇɴ 》═══ ✅

✅ {token_text}

✅ ═══════════════════════ ✅
""")
    
    # Then send video if exists
    if os.path.exists("token_video.mp4"):
        with open("token_video.mp4", "rb") as f:
            bot.send_video(message.chat.id, f, caption=f"✅ ᴠɪᴅᴇᴏ ɢᴜɪᴅᴇ")

# ============================================================
# BROADCAST COMMANDS
# ============================================================

@bot.message_handler(func=lambda m: m.text and "ʙʀᴏᴀᴅᴄᴀsᴛ" in m.text.lower() and "ᴀʟʟ" not in m.text.lower())
def broadcast_btn(message):
    if not is_admin(message.from_user.id):
        _send_pe(message.chat.id, f"❌ ᴜɴᴀᴜᴛʜᴏʀɪᴢᴇᴅ!")
        return
    
    _send_pe(message.chat.id, f"""
✅ ═══《 📢 ʙʀᴏᴀᴅᴄᴀsᴛ 》═══ ✅

✅ /broadcastuser ɪᴅ ᴍsɢ

✅ ᴇxᴀᴍᴘʟᴇ:
✅ /broadcastuser 8471373583 ʜᴇʟʟᴏ

✅ ═══════════════════════ ✅
""")

@bot.message_handler(func=lambda m: m.text and "ᴀʟʟ ʙʀᴏᴀᴅᴄᴀsᴛ" in m.text.lower())
def all_broadcast_btn(message):
    if not is_admin(message.from_user.id):
        _send_pe(message.chat.id, f"❌ ᴜɴᴀᴜᴛʜᴏʀɪᴢᴇᴅ!")
        return
    
    _send_pe(message.chat.id, f"""
✅ ═══《 📢 ᴀʟʟ ʙʀᴏᴀᴅᴄᴀsᴛ 》═══ ✅

✅ /allbroadcast ᴍsɢ

✅ ᴇxᴀᴍᴘʟᴇ:
✅ /allbroadcast ʜᴇʟʟᴏ ᴇᴠᴇʀʏᴏɴᴇ!

✅ ═══════════════════════ ✅
""")

@bot.message_handler(commands=['broadcastuser'])
def broadcast_user(message):
    if not is_admin(message.from_user.id):
        _send_pe(message.chat.id, f"❌ ᴜɴᴀᴜᴛʜᴏʀɪᴢᴇᴅ!")
        return
    
    parts = message.text.split(maxsplit=2)
    if len(parts) < 3:
        _send_pe(message.chat.id, f"❌ /broadcastuser ɪᴅ ᴍsɢ")
        return
    
    try:
        user_id = int(parts[1])
        msg = parts[2]
    except:
        _send_pe(message.chat.id, f"❌ ɪɴᴠᴀʟɪᴅ ɪᴅ!")
        return
    
    try:
        bot.send_message(user_id, f"📢 {msg}")
        _send_pe(message.chat.id, f"✅ sᴇɴᴛ ᴛᴏ {user_id}!")
    except Exception as e:
        _send_pe(message.chat.id, f"❌ ғᴀɪʟᴇᴅ: {str(e)}")

@bot.message_handler(commands=['allbroadcast'])
def all_broadcast(message):
    if not is_admin(message.from_user.id):
        _send_pe(message.chat.id, f"❌ ᴜɴᴀᴜᴛʜᴏʀɪᴢᴇᴅ!")
        return
    
    parts = message.text.split(maxsplit=1)
    if len(parts) < 2:
        _send_pe(message.chat.id, f"❌ /allbroadcast ᴍsɢ")
        return
    
    msg = parts[1]
    users = load_users()
    
    if not users:
        _send_pe(message.chat.id, f"❌ ɴᴏ ᴜsᴇʀs!")
        return
    
    sent = 0
    failed = 0
    
    _send_pe(message.chat.id, f"⏳ sᴇɴᴅɪɴɢ ᴛᴏ {len(users)} ᴜsᴇʀs...")
    
    for user_id in users.keys():
        try:
            bot.send_message(int(user_id), f"📢 {msg}")
            sent += 1
            time.sleep(0.05)
        except:
            failed += 1
    
    _send_pe(message.chat.id, f"""
✅ ᴄᴏᴍᴘʟᴇᴛᴇ!

✅ ᴛᴏᴛᴀʟ: {len(users)}
✅ sᴇɴᴛ: {sent}
✅ ғᴀɪʟᴇᴅ: {failed}
""")

# ============================================================
# ADMIN COMMANDS
# ============================================================

@bot.message_handler(commands=['approve'])
def approve_user(message):
    if not is_admin(message.from_user.id):
        _send_pe(message.chat.id, f"❌ ᴜɴᴀᴜᴛʜᴏʀɪᴢᴇᴅ!")
        return
    
    parts = message.text.split()
    if len(parts) < 2:
        _send_pe(message.chat.id, f"❌ /approve ɪᴅ")
        return
    
    try:
        user_id = int(parts[1])
    except:
        _send_pe(message.chat.id, f"❌ ɪɴᴠᴀʟɪᴅ ɪᴅ!")
        return
    
    update_user(user_id, "unlimited", True)
    update_user(user_id, "uses", 0)
    
    pending = load_pending()
    if str(user_id) in pending:
        del pending[str(user_id)]
        save_pending(pending)
    
    _send_pe(message.chat.id, f"✅ ᴜsᴇʀ {user_id} ᴀᴘᴘʀᴏᴠᴇᴅ!")
    
    try:
        bot.send_message(user_id, f"✅ ᴄᴏɴɢʀᴀᴛs! ᴜɴʟɪᴍɪᴛᴇᴅ ᴀᴄᴄᴇss! 🎉")
    except:
        pass

@bot.message_handler(commands=['disapprove'])
def disapprove_user(message):
    if not is_admin(message.from_user.id):
        _send_pe(message.chat.id, f"❌ ᴜɴᴀᴜᴛʜᴏʀɪᴢᴇᴅ!")
        return
    
    parts = message.text.split()
    if len(parts) < 2:
        _send_pe(message.chat.id, f"❌ /disapprove ɪᴅ")
        return
    
    try:
        user_id = int(parts[1])
    except:
        _send_pe(message.chat.id, f"❌ ɪɴᴠᴀʟɪᴅ ɪᴅ!")
        return
    
    pending = load_pending()
    if str(user_id) in pending:
        del pending[str(user_id)]
        save_pending(pending)
    
    _send_pe(message.chat.id, f"❌ ᴜsᴇʀ {user_id} ʀᴇᴊᴇᴄᴛᴇᴅ!")
    
    try:
        bot.send_message(user_id, f"❌ ᴘᴀʏᴍᴇɴᴛ ɴᴏᴛ ᴀᴘᴘʀᴏᴠᴇᴅ.")
    except:
        pass

@bot.message_handler(commands=['ban'])
def ban_user_cmd(message):
    if not is_admin(message.from_user.id):
        _send_pe(message.chat.id, f"❌ ᴜɴᴀᴜᴛʜᴏʀɪᴢᴇᴅ!")
        return
    
    parts = message.text.split()
    if len(parts) < 2:
        _send_pe(message.chat.id, f"❌ /ban ɪᴅ")
        return
    
    try:
        user_id = int(parts[1])
    except:
        _send_pe(message.chat.id, f"❌ ɪɴᴠᴀʟɪᴅ ɪᴅ!")
        return
    
    update_user(user_id, "banned", True)
    _send_pe(message.chat.id, f"✅ ᴜsᴇʀ {user_id} ʙᴀɴɴᴇᴅ!")

@bot.message_handler(commands=['unban'])
def unban_user_cmd(message):
    if not is_admin(message.from_user.id):
        _send_pe(message.chat.id, f"❌ ᴜɴᴀᴜᴛʜᴏʀɪᴢᴇᴅ!")
        return
    
    parts = message.text.split()
    if len(parts) < 2:
        _send_pe(message.chat.id, f"❌ /unban ɪᴅ")
        return
    
    try:
        user_id = int(parts[1])
    except:
        _send_pe(message.chat.id, f"❌ ɪɴᴠᴀʟɪᴅ ɪᴅ!")
        return
    
    update_user(user_id, "banned", False)
    _send_pe(message.chat.id, f"✅ ᴜsᴇʀ {user_id} ᴜɴʙᴀɴɴᴇᴅ!")

@bot.message_handler(commands=['users'])
def users_cmd(message):
    if not is_admin(message.from_user.id):
        _send_pe(message.chat.id, f"❌ ᴜɴᴀᴜᴛʜᴏʀɪᴢᴇᴅ!")
        return
    
    users = load_users()
    total = len(users)
    unlimited = sum(1 for u in users.values() if u.get("unlimited", False))
    banned = sum(1 for u in users.values() if u.get("banned", False))
    
    text = f"""
✅ ═══《 👥 ᴜsᴇʀs 》═══ ✅

✅ 📊 ᴛᴏᴛᴀʟ: {total}
✅ 💎 ᴜɴʟɪᴍɪᴛᴇᴅ: {unlimited}
✅ 🚫 ʙᴀɴɴᴇᴅ: {banned}

✅ 👥 ʟɪsᴛ:
"""
    
    for uid, data in users.items():
        status = "💎" if data.get("unlimited", False) else "🆓"
        banned_status = "🚫" if data.get("banned", False) else "✅"
        text += f"✅ • {data.get('name', 'Unknown')} (@{data.get('username', 'N/A')}) - {status} {banned_status}\n"
    
    _send_pe(message.chat.id, text)

@bot.message_handler(commands=['data'])
def data_cmd(message):
    if not is_admin(message.from_user.id):
        _send_pe(message.chat.id, f"❌ ᴜɴᴀᴜᴛʜᴏʀɪᴢᴇᴅ!")
        return
    
    users = load_users()
    orders = load_orders()
    pending = load_pending()
    settings = load_settings()
    
    data = {
        "users": users,
        "orders": orders,
        "pending": pending,
        "settings": settings,
        "total_users": len(users),
        "total_bans": len(orders),
        "pending_payments": len(pending),
        "generated": datetime.now().isoformat()
    }
    
    file_path = "bot_data.json"
    with open(file_path, "w") as f:
        json.dump(data, f, indent=2)
    
    with open(file_path, "rb") as f:
        bot.send_document(message.chat.id, f, caption=f"✅ 📥 ᴅᴀᴛᴀ ᴇxᴘᴏʀᴛ")

@bot.message_handler(commands=['price'])
def price_cmd(message):
    if not is_admin(message.from_user.id):
        _send_pe(message.chat.id, f"❌ ᴜɴᴀᴜᴛʜᴏʀɪᴢᴇᴅ!")
        return
    
    parts = message.text.split()
    if len(parts) < 2:
        settings = load_settings()
        _send_pe(message.chat.id, f"✅ 💰 ᴄᴜʀʀᴇɴᴛ: ʀs.{settings.get('price', 99)}\n✅ 📌 /price <ᴀᴍᴛ>")
        return
    
    try:
        price = int(parts[1])
        settings = load_settings()
        settings["price"] = price
        save_settings(settings)
        _send_pe(message.chat.id, f"✅ ᴘʀɪᴄᴇ: ʀs.{price}!")
    except:
        _send_pe(message.chat.id, f"❌ ɪɴᴠᴀʟɪᴅ!")

@bot.message_handler(commands=['upi'])
def upi_cmd(message):
    if not is_admin(message.from_user.id):
        _send_pe(message.chat.id, f"❌ ᴜɴᴀᴜᴛʜᴏʀɪᴢᴇᴅ!")
        return
    
    parts = message.text.split()
    if len(parts) < 2:
        settings = load_settings()
        _send_pe(message.chat.id, f"✅ 🏦 ᴄᴜʀʀᴇɴᴛ: {settings.get('upi', 'vanshx111@naviaxis')}\n✅ 📌 /upi <ɴᴇᴡ>")
        return
    
    upi = parts[1]
    settings = load_settings()
    settings["upi"] = upi
    save_settings(settings)
    _send_pe(message.chat.id, f"✅ ᴜᴘɪ: {upi}!")

@bot.message_handler(commands=['developer'])
def developer_cmd(message):
    if not is_admin(message.from_user.id):
        _send_pe(message.chat.id, f"❌ ᴜɴᴀᴜᴛʜᴏʀɪᴢᴇᴅ!")
        return
    
    parts = message.text.split()
    if len(parts) < 2:
        settings = load_settings()
        _send_pe(message.chat.id, f"✅ 👨‍💻 ᴄᴜʀʀᴇɴᴛ: {settings.get('developer', '@iflexzyan')}\n✅ 📌 /developer <@>")
        return
    
    developer = parts[1]
    settings = load_settings()
    settings["developer"] = developer
    settings["support"] = developer
    save_settings(settings)
    _send_pe(message.chat.id, f"✅ ᴅᴇᴠᴇʟᴏᴘᴇʀ: {developer}!")

@bot.message_handler(commands=['addadmin'])
def add_admin_cmd(message):
    if not is_admin(message.from_user.id):
        _send_pe(message.chat.id, f"❌ ᴜɴᴀᴜᴛʜᴏʀɪᴢᴇᴅ!")
        return
    
    parts = message.text.split()
    if len(parts) < 2:
        _send_pe(message.chat.id, f"❌ /addadmin ɪᴅ")
        return
    
    try:
        user_id = int(parts[1])
        if user_id not in ADMIN_IDS:
            ADMIN_IDS.append(user_id)
            _send_pe(message.chat.id, f"✅ ᴀᴅᴅᴇᴅ!")
        else:
            _send_pe(message.chat.id, f"⚠️ ᴀʟʀᴇᴀᴅʏ ᴀᴅᴍɪɴ!")
    except:
        _send_pe(message.chat.id, f"❌ ɪɴᴠᴀʟɪᴅ!")

# ============================================================
# BOT ON/OFF
# ============================================================

@bot.message_handler(func=lambda m: m.text and "ʙᴏᴛ ᴏɴ" in m.text.lower())
def bot_on_cmd(message):
    if not is_admin(message.from_user.id):
        _send_pe(message.chat.id, f"❌ ᴜɴᴀᴜᴛʜᴏʀɪᴢᴇᴅ!")
        return
    
    global bot_active
    bot_active = True
    _send_pe(message.chat.id, f"✅ 🟢 ᴏɴʟɪɴᴇ!")

@bot.message_handler(func=lambda m: m.text and "ʙᴏᴛ ᴏғғ" in m.text.lower())
def bot_off_cmd(message):
    if not is_admin(message.from_user.id):
        _send_pe(message.chat.id, f"❌ ᴜɴᴀᴜᴛʜᴏʀɪᴢᴇᴅ!")
        return
    
    global bot_active
    bot_active = False
    _send_pe(message.chat.id, f"✅ 🔴 ᴏғғʟɪɴᴇ!")

# ============================================================
# STATS & ADMIN PANEL
# ============================================================

@bot.message_handler(func=lambda m: m.text and "sᴛᴀᴛs" in m.text.lower())
def stats_cmd(message):
    if not is_admin(message.from_user.id):
        _send_pe(message.chat.id, f"❌ ᴜɴᴀᴜᴛʜᴏʀɪᴢᴇᴅ!")
        return
    
    users = load_users()
    orders = load_orders()
    pending = load_pending()
    settings = load_settings()
    
    text = f"""
✅ ═══《 📊 sᴛᴀᴛs 》═══ ✅

✅ 👥 ᴜsᴇʀs: {len(users)}
✅ 🔫 ʙᴀɴs: {len(orders)}
✅ 💰 ᴘᴇɴᴅɪɴɢ: {len(pending)}
✅ 💎 ᴜɴʟɪᴍɪᴛᴇᴅ: {sum(1 for u in users.values() if u.get('unlimited', False))}

✅ 💳 ᴘʀɪᴄᴇ: ʀs.{settings.get('price', 99)}
✅ 🏦 ᴜᴘɪ: {settings.get('upi', 'vanshx111@naviaxis')}
✅ 👨‍💻 {settings.get('developer', '@iflexzyan')}
"""
    _send_pe(message.chat.id, text)

@bot.message_handler(func=lambda m: m.text and "ᴀᴅᴍɪɴ ᴘᴀɴᴇʟ" in m.text.lower())
def admin_panel_cmd(message):
    if not is_admin(message.from_user.id):
        _send_pe(message.chat.id, f"❌ ᴜɴᴀᴜᴛʜᴏʀɪᴢᴇᴅ!")
        return
    
    text = f"""
✅ ═══《 👑 ᴀᴅᴍɪɴ ᴘᴀɴᴇʟ 》═══ ✅

✅ /approve ɪᴅ - ᴀᴘᴘʀᴏᴠᴇ
✅ /disapprove ɪᴅ - ʀᴇᴊᴇᴄᴛ
✅ /ban ɪᴅ - ʙᴀɴ
✅ /unban ɪᴅ - ᴜɴʙᴀɴ
✅ /users - ᴀʟʟ ᴜsᴇʀs
✅ /data - ᴅᴏᴡɴʟᴏᴀᴅ
✅ /price <ᴀᴍᴛ> - ᴄʜᴀɴɢᴇ
✅ /upi <ᴜᴘɪ> - ᴄʜᴀɴɢᴇ
✅ /developer <@> - ᴄʜᴀɴɢᴇ
✅ /addadmin ɪᴅ - ᴀᴅᴅ
✅ /broadcastuser ɪᴅ ᴍsɢ - sᴇɴᴅ
✅ /allbroadcast ᴍsɢ - ᴀʟʟ
✅ /addtokenvideo - ᴀᴅᴅ ᴠɪᴅᴇᴏ
✅ /settokentext - sᴇᴛ ᴛᴇxᴛ
✅ /setwelcomeimage - sᴇᴛ ɪᴍᴀɢᴇ
✅ /allcommands - ᴛʜɪs

✅ ═══════════════════════ ✅
"""
    _send_pe(message.chat.id, text)

# ============================================================
# CALLBACK HANDLERS
# ============================================================

@bot.callback_query_handler(func=lambda c: c.data == "ban_another")
def ban_another_callback(call):
    user_id = call.from_user.id
    user = get_user(user_id)
    
    if not user or user.get("banned", False):
        _send_pe(call.message.chat.id, f"❌ ʙᴀɴɴᴇᴅ!")
        return
    
    if not user.get("unlimited", False):
        uses = user.get("uses", 0)
        if uses >= 1:
            _send_pe(call.message.chat.id, f"⚠️ ᴜsᴇᴅ!\n💰 ᴘᴀʏ ʀs.{load_settings().get('price', 99)}")
            send_payment_qr(call.message.chat.id)
            bot.answer_callback_query(call.id)
            return
    
    _send_pe(call.message.chat.id, f"🔑 sᴇɴᴅ ᴛᴏᴋᴇɴ:")
    bot.register_next_step_handler(call.message, get_ban_token)
    bot.answer_callback_query(call.id)

@bot.callback_query_handler(func=lambda c: c.data == "get_unlimited")
def get_unlimited_callback(call):
    send_payment_qr(call.message.chat.id)
    bot.answer_callback_query(call.id)

# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":
    print("✅ ʙᴏᴛ sᴛᴀʀᴛᴇᴅ!")
    print(f"✅ ᴏᴡɴᴇʀ: {OWNER_ID}")
    print(f"✅ ᴜsᴇʀs: {len(load_users())}")
    
    try:
        bot.remove_webhook()
        print("✅ ᴡᴇʙʜᴏᴏᴋ ʀᴇᴍᴏᴠᴇᴅ!")
    except:
        pass
    
    bot.infinity_polling()