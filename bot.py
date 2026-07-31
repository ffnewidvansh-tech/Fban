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
CHANNEL_ID = os.environ.get("CHANNEL_ID", "-1003360548513")  # Channel ID

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
CLONE_FILE = "clone.json"
BUTTONS_FILE = "buttons.json"

# ============================================================
# STYLISH FONT - 𝘼 𝘽 𝘾...
# ============================================================
def stylish_text(text: str) -> str:
    stylish_chars = {
        'A': '𝘼', 'B': '𝘽', 'C': '𝘾', 'D': '𝘿', 'E': '𝙀', 'F': '𝙁', 'G': '𝙂',
        'H': '𝙃', 'I': '𝙄', 'J': '𝙅', 'K': '𝙆', 'L': '𝙇', 'M': '𝙈', 'N': '𝙉',
        'O': '𝙊', 'P': '𝙋', 'Q': '𝙌', 'R': '𝙍', 'S': '𝙎', 'T': '𝙏', 'U': '𝙐',
        'V': '𝙑', 'W': '𝙒', 'X': '𝙓', 'Y': '𝙔', 'Z': '𝙕',
        'a': '𝙖', 'b': '𝙗', 'c': '𝙘', 'd': '𝙙', 'e': '𝙚', 'f': '𝙛', 'g': '𝙜',
        'h': '𝙝', 'i': '𝙞', 'j': '𝙟', 'k': '𝙠', 'l': '𝙡', 'm': '𝙢', 'n': '𝙣',
        'o': '𝙤', 'p': '𝙥', 'q': '𝙦', 'r': '𝙧', 's': '𝙨', 't': '𝙩', 'u': '𝙪',
        'v': '𝙫', 'w': '𝙬', 'x': '𝙭', 'y': '𝙮', 'z': '𝙯',
        '0': '𝟬', '1': '𝟭', '2': '𝟮', '3': '𝟯', '4': '𝟰',
        '5': '𝟱', '6': '𝟲', '7': '𝟳', '8': '𝟴', '9': '𝟵'
    }
    result = ""
    for char in text:
        result += stylish_chars.get(char, char)
    return result

# ============================================================
# PREMIUM EMOJIS WITH VERIFIED IDS (Numbers)
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
# USERS DATA (JO TUMPE DIYA THA)
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

# ============================================================
# OTHER DATA FUNCTIONS
# ============================================================
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
        "bot_name": "𝙁𝙁 𝘽𝘼𝙉 𝘽𝙊𝙏",
        "developer": "@iflexzyan",
        "support": "@iflexzyan",
        "clone_price": 199
    }
    data = load_data(SETTINGS_FILE)
    for key, val in default.items():
        if key not in data:
            data[key] = val
    return data

def save_settings(settings):
    save_data(SETTINGS_FILE, settings)

def load_clone():
    return load_data(CLONE_FILE)

def save_clone(data):
    save_data(CLONE_FILE, data)

# ============================================================
# PREMIUM EMOJI HELPERS
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
        
        # Check if it's a premium emoji
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
# MAKE COLORED BUTTONS WITH PREMIUM EMOJIS
# ============================================================
def make_colored_button(text: str, style: str = None, callback: str = None, url: str = None):
    """Create button with stylish text + premium emojis + color"""
    stylish_text_result = stylish_text(text)
    left_emoji = random.choice(["✅", "💎", "⭐", "🔥", "❤️", "👍"])
    right_emoji = random.choice(["✅", "💎", "⭐", "🔥", "❤️", "👍"])
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
# JOIN CHANNEL CHECK
# ============================================================
def is_user_in_channel(user_id):
    if not CHANNEL_ID:
        return True
    try:
        member = bot.get_chat_member(CHANNEL_ID, user_id)
        return member.status in ["member", "administrator", "creator"]
    except:
        return False

def send_join_channel_message(chat_id):
    text = f"""
✅ ═══《 🔒 𝙅𝙊𝙄𝙉 𝘾𝙃𝘼𝙉𝙉𝙀𝙇 》═══ ✅

✅ 𝙋𝙡𝙚𝙖𝙨𝙚 𝙟𝙤𝙞𝙣 𝙤𝙪𝙧 𝙘𝙝𝙖𝙣𝙣𝙚𝙡 𝙩𝙤 𝙪𝙨𝙚 𝙩𝙝𝙞𝙨 𝙗𝙤𝙩!

✅ ═══════════════════════ ✅

✅ 𝘾𝙡𝙞𝙘𝙠 𝙩𝙝𝙚 𝙗𝙪𝙩𝙩𝙤𝙣 𝙗𝙚𝙡𝙤𝙬 𝙩𝙤 𝙟𝙤𝙞𝙣:

✅ ═══════════════════════ ✅
"""
    keyboard = [
        [make_green_button("𝙅𝙊𝙄𝙉 𝘾𝙃𝘼𝙉𝙉𝙀𝙇", url="https://t.me/yourchannel")],
        [make_blue_button("✅ 𝙄 𝙃𝘼𝙑𝙀 𝙅𝙊𝙄𝙉𝙀𝘿", callback="check_join")]
    ]
    markup = InlineKeyboardMarkup(keyboard)
    _send_pe(chat_id, text, reply_markup=markup)

@bot.callback_query_handler(func=lambda c: c.data == "check_join")
def check_join_callback(call):
    user_id = call.from_user.id
    if is_user_in_channel(user_id):
        _send_pe(call.message.chat.id, f"✅ 𝙔𝙤𝙪 𝙝𝙖𝙫𝙚 𝙟𝙤𝙞𝙣𝙚𝙙 𝙩𝙝𝙚 𝙘𝙝𝙖𝙣𝙣𝙚𝙡! 𝙔𝙤𝙪 𝙘𝙖𝙣 𝙣𝙤𝙬 𝙪𝙨𝙚 𝙩𝙝𝙚 𝙗𝙤𝙩.")
        try:
            bot.delete_message(call.message.chat.id, call.message.message_id)
        except:
            pass
        start_cmd(call.message)
    else:
        _send_pe(call.message.chat.id, f"❌ 𝙔𝙤𝙪 𝙝𝙖𝙫𝙚 𝙣𝙤𝙩 𝙟𝙤𝙞𝙣𝙚𝙙 𝙮𝙚𝙩! 𝙋𝙡𝙚𝙖𝙨𝙚 𝙟𝙤𝙞𝙣 𝙛𝙞𝙧𝙨𝙩.")
    bot.answer_callback_query(call.id)

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
        notify_owner(f"✅ 𝙉𝙚𝙬 𝙐𝙨𝙚𝙧 𝙅𝙤𝙞𝙣𝙚𝙙!\n👤 𝙄𝘿: {user_id}\n👾 @{username or 'N/A'}\n📛 {first_name or 'Unknown'}")
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
# GET MENU - WITH COLORFUL BUTTONS
# ============================================================
def get_menu(user_id):
    markup = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    is_admin_user = is_admin(user_id)
    
    # Admin buttons
    if is_admin_user:
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
            KeyboardButton(f"📋 {stylish_text('CLONE')}")
        )
        markup.row(
            KeyboardButton(f"❓ {stylish_text('HOW TO GET TOKEN')}"),
            KeyboardButton(f"💎 {stylish_text('CLONE PRICE')}")
        )
        markup.row(
            KeyboardButton(f"📢 {stylish_text('BROADCAST')}"),
            KeyboardButton(f"📢 {stylish_text('ALL BROADCAST')}")
        )
        markup.row(
            KeyboardButton(f"➕ {stylish_text('ADD BUTTON')}"),
            KeyboardButton(f"📋 {stylish_text('LIST BUTTONS')}")
        )
        markup.row(
            KeyboardButton(f"❌ {stylish_text('REMOVE BUTTON')}"),
            KeyboardButton(f"📋 {stylish_text('ALL COMMANDS')}")
        )
    else:
        markup.row(KeyboardButton(f"🔫 {stylish_text('BAN ACCOUNT')}"))
        markup.row(
            KeyboardButton(f"🆓 {stylish_text('FREE TRIAL')}"),
            KeyboardButton(f"💎 {stylish_text('UNLIMITED')}")
        )
        markup.row(
            KeyboardButton(f"❓ {stylish_text('HOW TO GET TOKEN')}"),
            KeyboardButton(f"📋 {stylish_text('CLONE BOT')}")
        )
    
    # Custom buttons
    buttons = load_buttons()
    if buttons:
        row = []
        for key, value in buttons.items():
            row.append(KeyboardButton(value["name"]))
            if len(row) == 2:
                markup.row(*row)
                row = []
        if row:
            markup.row(*row)
    
    markup.row(
        KeyboardButton(f"❓ {stylish_text('HELP')}"),
        KeyboardButton(f"ℹ️ {stylish_text('ABOUT')}")
    )
    markup.row(KeyboardButton(f"📞 {stylish_text('SUPPORT')}"))
    
    return markup

# ============================================================
# ALL COMMANDS
# ============================================================
@bot.message_handler(commands=['allcommands'])
def all_commands_cmd(message):
    if not is_admin(message.from_user.id):
        _send_pe(message.chat.id, f"❌ 𝙐𝙣𝙖𝙪𝙩𝙝𝙤𝙧𝙞𝙯𝙚𝙙!")
        return
    
    text = f"""
✅ ═══《 📋 𝘼𝙇𝙇 𝘾𝙊𝙈𝙈𝘼𝙉𝘿𝙎 》═══ ✅

✅ 𝙐𝙎𝙀𝙍 𝘾𝙊𝙈𝙈𝘼𝙉𝘿𝙎:
✅ /start - 𝙎𝙩𝙖𝙧𝙩 𝙗𝙤𝙩
✅ /help - 𝙃𝙚𝙡𝙥 𝙜𝙪𝙞𝙙𝙚

✅ ═══════════════════════ ✅

✅ 𝘼𝘿𝙈𝙄𝙉 𝘾𝙊𝙈𝙈𝘼𝙉𝘿𝙎:
✅ /approve 𝙪𝙨𝙚𝙧_𝙞𝙙 - 𝘼𝙥𝙥𝙧𝙤𝙫𝙚 𝙥𝙖𝙮𝙢𝙚𝙣𝙩
✅ /disapprove 𝙪𝙨𝙚𝙧_𝙞𝙙 - 𝙍𝙚𝙟𝙚𝙘𝙩 𝙥𝙖𝙮𝙢𝙚𝙣𝙩
✅ /ban 𝙪𝙨𝙚𝙧_𝙞𝙙 - 𝘽𝙖𝙣 𝙪𝙨𝙚𝙧
✅ /unban 𝙪𝙨𝙚𝙧_𝙞𝙙 - 𝙐𝙣𝙗𝙖𝙣 𝙪𝙨𝙚𝙧
✅ /users - 𝙎𝙝𝙤𝙬 𝙖𝙡𝙡 𝙪𝙨𝙚𝙧𝙨
✅ /data - 𝘿𝙤𝙬𝙣𝙡𝙤𝙖𝙙 𝙙𝙖𝙩𝙖
✅ /price <𝙖𝙢𝙤𝙪𝙣𝙩> - 𝘾𝙝𝙖𝙣𝙜𝙚 𝙥𝙧𝙞𝙘𝙚
✅ /upi <𝙪𝙥𝙞> - 𝘾𝙝𝙖𝙣𝙜𝙚 𝙐𝙋𝙄
✅ /developer <@𝙣𝙖𝙢𝙚> - 𝘾𝙝𝙖𝙣𝙜𝙚 𝙙𝙚𝙫𝙚𝙡𝙤𝙥𝙚𝙧
✅ /addadmin 𝙪𝙨𝙚𝙧_𝙞𝙙 - 𝘼𝙙𝙙 𝙖𝙙𝙢𝙞𝙣
✅ /clone - 𝘾𝙡𝙤𝙣𝙚 𝙗𝙤𝙩
✅ /prcclone <𝙖𝙢𝙤𝙪𝙣𝙩> - 𝘾𝙡𝙤𝙣𝙚 𝙥𝙧𝙞𝙘𝙚
✅ /approveclone 𝙪𝙨𝙚𝙧_𝙞𝙙 - 𝘼𝙥𝙥𝙧𝙤𝙫𝙚 𝙘𝙡𝙤𝙣𝙚
✅ /disapproveclone 𝙪𝙨𝙚𝙧_𝙞𝙙 - 𝙍𝙚𝙟𝙚𝙘𝙩 𝙘𝙡𝙤𝙣𝙚
✅ /broadcastuser 𝙪𝙨𝙚𝙧_𝙞𝙙 𝙢𝙨𝙜 - 𝙎𝙚𝙣𝙙 𝙩𝙤 𝙪𝙨𝙚𝙧
✅ /allbroadcast 𝙢𝙨𝙜 - 𝙎𝙚𝙣𝙙 𝙩𝙤 𝙖𝙡𝙡
✅ /addbutton - 𝘼𝙙𝙙 𝙘𝙪𝙨𝙩𝙤𝙢 𝙗𝙪𝙩𝙩𝙤𝙣
✅ /listbuttons - 𝙇𝙞𝙨𝙩 𝙖𝙡𝙡 𝙗𝙪𝙩𝙩𝙤𝙣𝙨
✅ /removebutton - 𝙍𝙚𝙢𝙤𝙫𝙚 𝙗𝙪𝙩𝙩𝙤𝙣
✅ /addtokenvideo - 𝘼𝙙𝙙 𝙩𝙤𝙠𝙚𝙣 𝙫𝙞𝙙𝙚𝙤
✅ /allcommands - 𝙏𝙝𝙞𝙨 𝙢𝙚𝙣𝙪

✅ ═══════════════════════ ✅
"""
    _send_pe(message.chat.id, text)

# ============================================================
# ADD BUTTON COMMAND
# ============================================================
@bot.message_handler(commands=['addbutton'])
def add_button_cmd(message):
    if not is_admin(message.from_user.id):
        _send_pe(message.chat.id, f"❌ 𝙐𝙣𝙖𝙪𝙩𝙝𝙤𝙧𝙞𝙯𝙚𝙙!")
        return
    
    _send_pe(message.chat.id, f"""
✅ ═══《 ➕ 𝘼𝘿𝘿 𝘽𝙐𝙏𝙏𝙊𝙉 》═══ ✅

✅ 𝙎𝙚𝙣𝙙 𝙢𝙚 𝙩𝙝𝙚 𝘽𝙐𝙏𝙏𝙊𝙉 𝙉𝘼𝙈𝙀:

✅ 𝙀𝙭𝙖𝙢𝙥𝙡𝙚: 𝙃𝙀𝙇𝙇𝙊 𝙒𝙊𝙍𝙇𝘿

✅ ═══════════════════════ ✅
""")
    bot.register_next_step_handler(message, get_button_name)

def get_button_name(message):
    if not is_admin(message.from_user.id):
        return
    
    button_name = message.text.strip()
    user_data[message.from_user.id] = {"button_name": button_name}
    
    _send_pe(message.chat.id, f"""
✅ ═══《 ➕ 𝘼𝘿𝘿 𝘽𝙐𝙏𝙏𝙊𝙉 》═══ ✅

✅ 𝘽𝙪𝙩𝙩𝙤𝙣 𝙉𝙖𝙢𝙚: {button_name}

✅ 𝙉𝙤𝙬 𝙨𝙚𝙣𝙙 𝙢𝙚 𝙩𝙝𝙚 𝘽𝙐𝙏𝙏𝙊𝙉 𝙐𝙍𝙇/𝙇𝙄𝙉𝙆:

✅ 𝙀𝙭𝙖𝙢𝙥𝙡𝙚: 𝙝𝙩𝙩𝙥𝙨://𝙩.𝙢𝙚/𝙞𝙛𝙡𝙚𝙭𝙯𝙮𝙖𝙣

✅ ═══════════════════════ ✅
""")
    bot.register_next_step_handler(message, get_button_url)

def get_button_url(message):
    if not is_admin(message.from_user.id):
        return
    
    button_url = message.text.strip()
    button_name = user_data.get(message.from_user.id, {}).get("button_name", "Unknown")
    
    buttons = load_buttons()
    buttons[button_name] = {
        "name": button_name,
        "url": button_url,
        "added_by": message.from_user.id,
        "added_at": datetime.now().isoformat()
    }
    save_buttons(buttons)
    
    _send_pe(message.chat.id, f"""
✅ ═══《 ✅ 𝘽𝙐𝙏𝙏𝙊𝙉 𝘼𝘿𝘿𝙀𝘿 》═══ ✅

✅ 📌 𝙉𝙖𝙢𝙚: {button_name}
✅ 🔗 𝙐𝙍𝙇: {button_url}

✅ ✅ 𝘽𝙪𝙩𝙩𝙤𝙣 𝙖𝙙𝙙𝙚𝙙 𝙨𝙪𝙘𝙘𝙚𝙨𝙨𝙛𝙪𝙡𝙡𝙮!

✅ ═══════════════════════ ✅
""")
    
    user_data.pop(message.from_user.id, None)

@bot.message_handler(commands=['listbuttons'])
def list_buttons_cmd(message):
    if not is_admin(message.from_user.id):
        _send_pe(message.chat.id, f"❌ 𝙐𝙣𝙖𝙪𝙩𝙝𝙤𝙧𝙞𝙯𝙚𝙙!")
        return
    
    buttons = load_buttons()
    if not buttons:
        _send_pe(message.chat.id, f"✅ 𝙉𝙤 𝙗𝙪𝙩𝙩𝙤𝙣𝙨 𝙖𝙙𝙙𝙚𝙙 𝙮𝙚𝙩!")
        return
    
    text = f"""
✅ ═══《 📋 𝘾𝙐𝙎𝙏𝙊𝙈 𝘽𝙐𝙏𝙏𝙊𝙉𝙎 》═══ ✅
"""
    for name, data in buttons.items():
        text += f"""
✅ 📌 {name}
✅ 🔗 {data['url']}
✅ 👤 {data['added_by']}
✅ ⏰ {data['added_at']}
✅ ─────────────────────
"""
    
    text += f"""
✅ ═══════════════════════ ✅
✅ 𝙏𝙤𝙩𝙖𝙡 𝘽𝙪𝙩𝙩𝙤𝙣𝙨: {len(buttons)}
"""
    _send_pe(message.chat.id, text)

@bot.message_handler(commands=['removebutton'])
def remove_button_cmd(message):
    if not is_admin(message.from_user.id):
        _send_pe(message.chat.id, f"❌ 𝙐𝙣𝙖𝙪𝙩𝙝𝙤𝙧𝙞𝙯𝙚𝙙!")
        return
    
    buttons = load_buttons()
    if not buttons:
        _send_pe(message.chat.id, f"✅ 𝙉𝙤 𝙗𝙪𝙩𝙩𝙤𝙣𝙨 𝙩𝙤 𝙧𝙚𝙢𝙤𝙫𝙚!")
        return
    
    text = f"""
✅ ═══《 ❌ 𝙍𝙀𝙈𝙊𝙑𝙀 𝘽𝙐𝙏𝙏𝙊𝙉 》═══ ✅

✅ 𝙎𝙚𝙣𝙙 𝙢𝙚 𝙩𝙝𝙚 𝙗𝙪𝙩𝙩𝙤𝙣 𝙣𝙖𝙢𝙚 𝙩𝙤 𝙧𝙚𝙢𝙤𝙫𝙚:

✅ 𝘼𝙫𝙖𝙞𝙡𝙖𝙗𝙡𝙚 𝙗𝙪𝙩𝙩𝙤𝙣𝙨:
"""
    for name in buttons.keys():
        text += f"✅ • {name}\n"
    
    text += f"""
✅ ═══════════════════════ ✅
"""
    _send_pe(message.chat.id, text)
    bot.register_next_step_handler(message, remove_button)

def remove_button(message):
    if not is_admin(message.from_user.id):
        return
    
    button_name = message.text.strip()
    buttons = load_buttons()
    
    if button_name in buttons:
        del buttons[button_name]
        save_buttons(buttons)
        _send_pe(message.chat.id, f"✅ 𝘽𝙪𝙩𝙩𝙤𝙣 '{button_name}' 𝙧𝙚𝙢𝙤𝙫𝙚𝙙!")
    else:
        _send_pe(message.chat.id, f"❌ 𝘽𝙪𝙩𝙩𝙤𝙣 '{button_name}' 𝙣𝙤𝙩 𝙛𝙤𝙪𝙣𝙙!")

# ============================================================
# HANDLE CUSTOM BUTTONS
# ============================================================
@bot.message_handler(func=lambda m: m.text and m.text in [b["name"] for b in load_buttons().values()])
def handle_custom_button(message):
    buttons = load_buttons()
    for name, data in buttons.items():
        if message.text == data["name"]:
            markup = InlineKeyboardMarkup([
                [make_blue_button("𝙊𝙋𝙀𝙉 𝙇𝙄𝙉𝙆", url=data["url"])],
                [make_red_button("𝘾𝙇𝙊𝙎𝙀", callback="close_button")]
            ])
            _send_pe(message.chat.id, f"""
✅ ═══《 {name} 》═══ ✅

✅ 𝘾𝙡𝙞𝙘𝙠 𝙗𝙚𝙡𝙤𝙬 𝙩𝙤 𝙤𝙥𝙚𝙣:

✅ ═══════════════════════ ✅
""", reply_markup=markup)
            break

# ============================================================
# BOT COMMANDS - START, HELP, ABOUT
# ============================================================

@bot.message_handler(commands=['start'])
def start_cmd(message):
    user_id = message.from_user.id
    username = message.from_user.username
    first_name = message.from_user.first_name
    
    # Check channel join
    if CHANNEL_ID and not is_user_in_channel(user_id) and not is_admin(user_id):
        send_join_channel_message(message.chat.id)
        return
    
    settings = load_settings()
    price = settings.get("price", 99)
    developer = settings.get("developer", "@iflexzyan")
    
    user = register_user(user_id, username, first_name)
    
    if user.get("banned", False):
        _send_pe(message.chat.id, f"❌ 𝙔𝙤𝙪 𝙖𝙧𝙚 𝘽𝘼𝙉𝙉𝙀𝘿 𝙛𝙧𝙤𝙢 𝙪𝙨𝙞𝙣𝙜 𝙩𝙝𝙞𝙨 𝙗𝙤𝙩!")
        return
    
    try:
        bot.send_photo(
            message.chat.id,
            photo="https://iili.io/C8DNTyQ.jpg",
            caption=f"✅ 𝙒𝙚𝙡𝙘𝙤𝙢𝙚 𝙩𝙤 𝙁𝙁 𝘽𝘼𝙉 𝘽𝙊𝙏!"
        )
    except:
        pass
    
    welcome_text = f"""
✅ ═══《 🔥 𝙒𝙀𝙇𝘾𝙊𝙈𝙀 𝙏𝙊 𝙁𝙁 𝘽𝘼𝙉 𝘽𝙊𝙏 》═══ ✅

✅ 👤 𝙐𝙨𝙚𝙧: {first_name}
✅ 🆔 𝙄𝘿: {user_id}
✅ 👾 𝙐𝙨𝙚𝙧𝙣𝙖𝙢𝙚: @{username or 'N/A'}

✅ ═══════════════════════ ✅

✅ 🎯 𝟭 𝙁𝙍𝙀𝙀 𝙏𝙍𝙄𝘼𝙇 - 𝘽𝙖𝙣 𝟭 𝘼𝙘𝙘𝙤𝙪𝙣𝙩
✅ 💰 𝙐𝙉𝙇𝙄𝙈𝙄𝙏𝙀𝘿 𝘼𝙘𝙘𝙚𝙨𝙨 - 𝙍𝙨.{price}

✅ ═══════════════════════ ✅

✅ 👨‍💻 𝘿𝙚𝙫𝙚𝙡𝙤𝙥𝙚𝙧: {developer}

✅ ═══════════════════════ ✅
"""
    
    markup = get_menu(user_id)
    _send_pe(message.chat.id, welcome_text, reply_markup=markup)

@bot.message_handler(commands=['help'])
def help_cmd(message):
    user_id = message.from_user.id
    markup = get_menu(user_id)
    
    help_text = f"""
✅ ═══《 ❓ 𝙃𝙀𝙇𝙋 》═══ ✅

✅ 𝙃𝙤𝙬 𝙩𝙤 𝙐𝙨𝙚:

✅ 𝟭️⃣ 𝘾𝙡𝙞𝙘𝙠 𝘽𝘼𝙉 𝘼𝘾𝘾𝙊𝙐𝙉𝙏
✅ 𝟮️⃣ 𝙎𝙚𝙣𝙙 𝘼𝙘𝙘𝙚𝙨𝙨 𝙏𝙤𝙠𝙚𝙣
✅ 𝟯️⃣ 𝘼𝙘𝙘𝙤𝙪𝙣𝙩 𝙬𝙞𝙡𝙡 𝙗𝙚 𝙗𝙖𝙣𝙣𝙚𝙙
✅ 𝟰️⃣ 𝙂𝙚𝙩 𝙍𝙚𝙨𝙪𝙡𝙩!

✅ ═══════════════════ ✅

✅ 🆓 𝙁𝙍𝙀𝙀 𝙏𝙍𝙄𝘼𝙇: 𝟭 𝘽𝙖𝙣
✅ 💰 𝙐𝙉𝙇𝙄𝙈𝙄𝙏𝙀𝘿: 𝙋𝙖𝙮 & 𝙂𝙚𝙩

✅ ═══════════════════ ✅

✅ 👨‍💻 𝘿𝙚𝙫𝙚𝙡𝙤𝙥𝙚𝙧: @iflexzyan
"""
    _send_pe(message.chat.id, help_text, reply_markup=markup)

@bot.message_handler(func=lambda m: m.text and "𝙃𝙀𝙇𝙋" in m.text)
def help_btn_cmd(message):
    help_cmd(message)

@bot.message_handler(func=lambda m: m.text and "𝘼𝘽𝙊𝙐𝙏" in m.text)
def about_cmd(message):
    user_id = message.from_user.id
    markup = get_menu(user_id)
    settings = load_settings()
    developer = settings.get("developer", "@iflexzyan")
    
    text = f"""
✅ ═══《 ℹ️ 𝘼𝘽𝙊𝙐𝙏 》═══ ✅

✅ 🤖 𝙁𝙁 𝘽𝘼𝙉 𝘽𝙊𝙏

✅ 🔫 𝘽𝙖𝙣 𝙁𝙧𝙚𝙚 𝙁𝙞𝙧𝙚 𝘼𝙘𝙘𝙤𝙪𝙣𝙩𝙨
✅ 💰 𝙋𝙖𝙮 & 𝙂𝙚𝙩 𝙐𝙣𝙡𝙞𝙢𝙞𝙩𝙚𝙙 𝘼𝙘𝙘𝙚𝙨𝙨
✅ 🆓 𝟭 𝙁𝙧𝙚𝙚 𝙏𝙧𝙞𝙖𝙡

✅ ═══════════════════════ ✅

✅ 👨‍💻 𝘿𝙚𝙫𝙚𝙡𝙤𝙥𝙚𝙧: {developer}

✅ ═══════════════════════ ✅
"""
    _send_pe(message.chat.id, text, reply_markup=markup)

@bot.message_handler(func=lambda m: m.text and "𝙎𝙐𝙋𝙋𝙊𝙍𝙏" in m.text)
def support_cmd(message):
    settings = load_settings()
    support = settings.get("support", "@iflexzyan")
    developer = settings.get("developer", "@iflexzyan")
    
    text = f"""
✅ ═══《 📞 𝙎𝙐𝙋𝙋𝙊𝙍𝙏 》═══ ✅

✅ 👨‍💻 𝘿𝙚𝙫𝙚𝙡𝙤𝙥𝙚𝙧: {developer}

✅ ═══════════════════════ ✅

✅ 𝙁𝙤𝙧 𝙖𝙣𝙮 𝙞𝙨𝙨𝙪𝙚𝙨, 𝙘𝙤𝙣𝙩𝙖𝙘𝙩:
✅ 📱 𝙏𝙚𝙡𝙚𝙜𝙧𝙖𝙢: {support}

✅ ═══════════════════════ ✅
"""
    markup = InlineKeyboardMarkup([
        [make_blue_button("𝘾𝙊𝙉𝙏𝘼𝘾𝙏 𝙎𝙐𝙋𝙋𝙊𝙍𝙏", url=f"https://t.me/{support.replace('@', '')}")]
    ])
    _send_pe(message.chat.id, text, reply_markup=markup)

# ============================================================
# BAN ACCOUNT
# ============================================================

@bot.message_handler(func=lambda m: m.text and "𝘽𝘼𝙉 𝘼𝘾𝘾𝙊𝙐𝙉𝙏" in m.text)
def ban_account_start(message):
    user_id = message.from_user.id
    user = get_user(user_id)
    
    if not user or user.get("banned", False):
        _send_pe(message.chat.id, f"❌ 𝙔𝙤𝙪 𝙖𝙧𝙚 𝘽𝘼𝙉𝙉𝙀𝘿!")
        return
    
    if not user.get("unlimited", False):
        uses = user.get("uses", 0)
        if uses >= 1:
            _send_pe(message.chat.id, f"⚠️ 𝙁𝙧𝙚𝙚 𝙏𝙧𝙞𝙖𝙡 𝙐𝙨𝙚𝙙!\n💰 𝙋𝙖𝙮 𝙍𝙨.{load_settings().get('price', 99)} 𝙛𝙤𝙧 𝙐𝙉𝙇𝙄𝙈𝙄𝙏𝙀𝘿")
            send_payment_qr(message.chat.id)
            return
    
    _send_pe(message.chat.id, f"🔑 𝙎𝙚𝙣𝙙 𝙢𝙚 𝙩𝙝𝙚 𝘼𝙘𝙘𝙚𝙨𝙨 𝙏𝙤𝙠𝙚𝙣 𝙩𝙤 𝘽𝙖𝙣!")
    bot.register_next_step_handler(message, process_ban_token)

def process_ban_token(message):
    user_id = message.from_user.id
    token = message.text.strip()
    
    if len(token) < 30:
        _send_pe(message.chat.id, f"❌ 𝙄𝙣𝙫𝙖𝙡𝙞𝙙 𝙏𝙤𝙠𝙚𝙣! 𝙋𝙡𝙚𝙖𝙨𝙚 𝙨𝙚𝙣𝙙 𝙘𝙤𝙧𝙧𝙚𝙘𝙩 𝘼𝙘𝙘𝙚𝙨𝙨 𝙏𝙤𝙠𝙚𝙣.")
        return
    
    msg = _send_pe_return(message.chat.id, f"⏳ 𝘽𝙖𝙣𝙣𝙞𝙣𝙜 𝘼𝙘𝙘𝙤𝙪𝙣𝙩... 𝙋𝙡𝙚𝙖𝙨𝙚 𝙒𝙖𝙞𝙩!")
    
    try:
        url = f"https://ffidbanapi.vercel.app/ban-account?access-token={token}&key=ANIXH"
        response = requests.get(url, timeout=30)
        data = response.json()
        
        account_id = data.get('id', 'N/A')
        account_name = data.get('name', 'N/A')
        account_uid = data.get('uid', 'N/A')
        status = data.get('status', 'UNKNOWN')
        
        is_banned = "BANNED" in str(status).upper() or "BAN" in str(data.get('message', '')).upper()
        
        bot.delete_message(message.chat.id, msg.message_id)
        
        if is_banned:
            user = get_user(user_id)
            if user:
                uses = user.get("uses", 0) + 1
                update_user(user_id, "uses", uses)
            
            result_text = f"""
✅ ═══《 ✅ 𝘼𝘾𝘾𝙊𝙐𝙉𝙏 𝘽𝘼𝙉𝙉𝙀𝘿 》═══ ✅

✅ 🎯 𝘼𝘾𝘾𝙊𝙐𝙉𝙏 𝘽𝘼𝙉 𝙎𝙐𝘾𝘾𝙀𝙎𝙎𝙁𝙐𝙇!

✅ ═══════════════════════ ✅

✅ 🆔 𝙄𝘿: {account_id}
✅ 👤 𝙉𝘼𝙈𝙀: {account_name}
✅ 🔢 𝙐𝙄𝘿: {account_uid}

✅ ═══════════════════════ ✅

✅ 👨‍💻 𝘿𝙚𝙫𝙚𝙡𝙤𝙥𝙚𝙧: @iflexzyan

✅ ═══════════════════════ ✅
"""
            keyboard = [
                [make_green_button("𝘽𝘼𝙉 𝘼𝙉𝙊𝙏𝙃𝙀𝙍", callback="ban_another")],
                [make_blue_button("𝙂𝙀𝙏 𝙐𝙉𝙇𝙄𝙈𝙄𝙏𝙀𝘿", callback="get_unlimited")],
                [make_red_button("𝙎𝙐𝙋𝙋𝙊𝙍𝙏", callback="support_contact")]
            ]
            markup = InlineKeyboardMarkup(keyboard)
            _send_pe(message.chat.id, result_text, reply_markup=markup)
            
            notify_owner(f"✅ 𝘼𝙘𝙘𝙤𝙪𝙣𝙩 𝘽𝙖𝙣𝙣𝙚𝙙!\n👤 𝙐𝙨𝙚𝙧: {user_id}\n🔢 𝙐𝙄𝘿: {account_uid}")
            
        else:
            result_text = f"""
❌ ═══《 ❌ 𝘽𝘼𝙉 𝙁𝘼𝙄𝙇𝙀𝘿 》═══ ❌

❌ 𝘼𝘾𝘾𝙊𝙐𝙉𝙏 𝙉𝙊𝙏 𝘽𝘼𝙉𝙉𝙀𝘿!

❌ ═══════════════════════ ❌

❌ 🆔 𝙄𝘿: {account_id}
❌ 👤 𝙉𝘼𝙈𝙀: {account_name}
❌ 🔢 𝙐𝙄𝘿: {account_uid}
❌ 📌 𝙎𝙩𝙖𝙩𝙪𝙨: {status}

❌ ═══════════════════════ ❌

❌ ⚠️ 𝙍𝙚𝙖𝙨𝙤𝙣𝙨:
❌ • 𝙄𝙣𝙫𝙖𝙡𝙞𝙙 𝙏𝙤𝙠𝙚𝙣
❌ • 𝘼𝙡𝙧𝙚𝙖𝙙𝙮 𝘽𝙖𝙣𝙣𝙚𝙙
❌ • 𝙎𝙚𝙧𝙫𝙚𝙧 𝙀𝙧𝙧𝙤𝙧

❌ ═══════════════════════ ❌

❌ 👨‍💻 𝘿𝙚𝙫𝙚𝙡𝙤𝙥𝙚𝙧: @iflexzyan
"""
            _send_pe(message.chat.id, result_text)
            
    except Exception as e:
        bot.delete_message(message.chat.id, msg.message_id)
        _send_pe(message.chat.id, f"❌ 𝙀𝙧𝙧𝙤𝙧: {str(e)}")

# ============================================================
# PAYMENT SYSTEM - WITH STYLISH TEXT
# ============================================================

def send_payment_qr(chat_id):
    settings = load_settings()
    upi = settings.get("upi", "vanshx111@naviaxis")
    price = settings.get("price", 99)
    
    qr_url = f"https://api.qrserver.com/v1/create-qr-code/?size=300x300&data=upi://pay?pa={upi}&am={price}&cu=INR"
    
    text = f"""
✅ ═══《 💰 𝙋𝘼𝙔𝙈𝙀𝙉𝙏 》═══ ✅

✅ 💳 𝙐𝙋𝙄: {upi}
✅ 💰 𝘼𝙢𝙤𝙪𝙣𝙩: 𝙍𝙨.{price}

✅ ═══════════════════════ ✅

✅ 📱 𝙎𝙘𝙖𝙣 𝙌𝙍 𝙩𝙤 𝙋𝙖𝙮

✅ ═══════════════════════ ✅
"""
    
    keyboard = [
        [make_green_button("𝙄 𝙃𝘼𝙑𝙀 𝙋𝘼𝙄𝘿", callback=f"paid_{chat_id}")],
        [make_blue_button("𝙎𝙐𝙋𝙋𝙊𝙍𝙏", url="https://t.me/iflexzyan")],
        [make_red_button("𝘾𝘼𝙉𝘾𝙀𝙇", callback="cancel_payment")]
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
    
    _send_pe(chat_id, f"📸 𝙎𝙚𝙣𝙙 𝙢𝙚 𝙩𝙝𝙚 𝙋𝙖𝙮𝙢𝙚𝙣𝙩 𝙎𝙘𝙧𝙚𝙚𝙣𝙨𝙝𝙤𝙩!")
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
        
        _send_pe(message.chat.id, f"✅ 𝙎𝙘𝙧𝙚𝙚𝙣𝙨𝙝𝙤𝙩 𝙍𝙚𝙘𝙚𝙞𝙫𝙚𝙙!\n⏳ 𝙒𝙖𝙞𝙩𝙞𝙣𝙜 𝙛𝙤𝙧 𝘼𝙙𝙢𝙞𝙣 𝘼𝙥𝙥𝙧𝙤𝙫𝙖𝙡.")
        
        admin_text = f"""
✅ ═══《 💰 𝙉𝙀𝙒 𝙋𝘼𝙔𝙈𝙀𝙉𝙏 》═══ ✅

✅ 👤 𝙐𝙨𝙚𝙧: {message.from_user.first_name}
✅ 🆔 𝙄𝘿: {user_id}
✅ 👾 @{message.from_user.username or 'N/A'}

✅ ═══════════════════════ ✅

✅ 📌 𝙐𝙨𝙚: /approve {user_id}
✅ 📌 𝙐𝙨𝙚: /disapprove {user_id}

✅ ═══════════════════════ ✅
"""
        for admin in ADMIN_IDS:
            try:
                bot.send_photo(admin, photo=file_id, caption=admin_text)
            except:
                bot.send_message(admin, admin_text)
    else:
        _send_pe(message.chat.id, f"❌ 𝙋𝙡𝙚𝙖𝙨𝙚 𝙨𝙚𝙣𝙙 𝙖 𝙋𝙃𝙊𝙏𝙊 𝙖𝙨 𝙨𝙘𝙧𝙚𝙚𝙣𝙨𝙝𝙤𝙩!")

# ============================================================
# FREE TRIAL & UNLIMITED
# ============================================================

@bot.message_handler(func=lambda m: m.text and "𝙁𝙍𝙀𝙀 𝙏𝙍𝙄𝘼𝙇" in m.text)
def free_trial_cmd(message):
    user_id = message.from_user.id
    user = get_user(user_id)
    
    if not user:
        _send_pe(message.chat.id, f"❌ 𝙋𝙡𝙚𝙖𝙨𝙚 /start 𝙛𝙞𝙧𝙨𝙩!")
        return
    
    if user.get("unlimited", False):
        _send_pe(message.chat.id, f"✅ 𝙔𝙤𝙪 𝙖𝙡𝙧𝙚𝙖𝙙𝙮 𝙝𝙖𝙫𝙚 𝙐𝙉𝙇𝙄𝙈𝙄𝙏𝙀𝘿 𝙖𝙘𝙘𝙚𝙨𝙨!")
        return
    
    uses = user.get("uses", 0)
    if uses >= 1:
        _send_pe(message.chat.id, f"⚠️ 𝙁𝙧𝙚𝙚 𝙏𝙧𝙞𝙖𝙡 𝘼𝙡𝙧𝙚𝙖𝙙𝙮 𝙐𝙨𝙚𝙙!\n💰 𝙋𝙖𝙮 𝙍𝙨.{load_settings().get('price', 99)} 𝙛𝙤𝙧 𝙐𝙉𝙇𝙄𝙈𝙄𝙏𝙀𝘿")
        send_payment_qr(message.chat.id)
        return
    
    _send_pe(message.chat.id, f"🆓 𝙁𝙍𝙀𝙀 𝙏𝙍𝙄𝘼𝙇 𝘼𝘾𝙏𝙄𝙑𝘼𝙏𝙀𝘿!\n🔫 𝙎𝙚𝙣𝙙 𝘼𝙘𝙘𝙚𝙨𝙨 𝙏𝙤𝙠𝙚𝙣 𝙩𝙤 𝘽𝙖𝙣!")

@bot.message_handler(func=lambda m: m.text and "𝙐𝙉𝙇𝙄𝙈𝙄𝙏𝙀𝘿" in m.text)
def unlimited_cmd(message):
    user_id = message.from_user.id
    user = get_user(user_id)
    
    if user and user.get("unlimited", False):
        _send_pe(message.chat.id, f"✅ 𝙔𝙤𝙪 𝙖𝙡𝙧𝙚𝙖𝙙𝙮 𝙝𝙖𝙫𝙚 𝙐𝙉𝙇𝙄𝙈𝙄𝙏𝙀𝘿 𝙖𝙘𝙘𝙚𝙨𝙨!")
        return
    
    send_payment_qr(message.chat.id)

# ============================================================
# ADMIN COMMANDS
# ============================================================

@bot.message_handler(commands=['approve'])
def approve_user(message):
    if not is_admin(message.from_user.id):
        _send_pe(message.chat.id, f"❌ 𝙐𝙣𝙖𝙪𝙩𝙝𝙤𝙧𝙞𝙯𝙚𝙙!")
        return
    
    parts = message.text.split()
    if len(parts) < 2:
        _send_pe(message.chat.id, f"❌ 𝙐𝙨𝙖𝙜𝙚: /approve 𝙪𝙨𝙚𝙧_𝙞𝙙")
        return
    
    try:
        user_id = int(parts[1])
    except:
        _send_pe(message.chat.id, f"❌ 𝙄𝙣𝙫𝙖𝙡𝙞𝙙 𝙐𝙨𝙚𝙧 𝙄𝘿!")
        return
    
    update_user(user_id, "unlimited", True)
    update_user(user_id, "uses", 0)
    
    pending = load_pending()
    if str(user_id) in pending:
        del pending[str(user_id)]
        save_pending(pending)
    
    _send_pe(message.chat.id, f"✅ 𝙐𝙨𝙚𝙧 {user_id} 𝙖𝙥𝙥𝙧𝙤𝙫𝙚𝙙 𝙛𝙤𝙧 𝙐𝙉𝙇𝙄𝙈𝙄𝙏𝙀𝘿 𝙖𝙘𝙘𝙚𝙨𝙨!")
    
    try:
        bot.send_message(user_id, f"✅ 𝘾𝙤𝙣𝙜𝙧𝙖𝙩𝙪𝙡𝙖𝙩𝙞𝙤𝙣𝙨! 𝙔𝙤𝙪 𝙣𝙤𝙬 𝙝𝙖𝙫𝙚 𝙐𝙉𝙇𝙄𝙈𝙄𝙏𝙀𝘿 𝙖𝙘𝙘𝙚𝙨𝙨! 🎉")
    except:
        pass

@bot.message_handler(commands=['disapprove'])
def disapprove_user(message):
    if not is_admin(message.from_user.id):
        _send_pe(message.chat.id, f"❌ 𝙐𝙣𝙖𝙪𝙩𝙝𝙤𝙧𝙞𝙯𝙚𝙙!")
        return
    
    parts = message.text.split()
    if len(parts) < 2:
        _send_pe(message.chat.id, f"❌ 𝙐𝙨𝙖𝙜𝙚: /disapprove 𝙪𝙨𝙚𝙧_𝙞𝙙")
        return
    
    try:
        user_id = int(parts[1])
    except:
        _send_pe(message.chat.id, f"❌ 𝙄𝙣𝙫𝙖𝙡𝙞𝙙 𝙐𝙨𝙚𝙧 𝙄𝘿!")
        return
    
    pending = load_pending()
    if str(user_id) in pending:
        del pending[str(user_id)]
        save_pending(pending)
    
    _send_pe(message.chat.id, f"❌ 𝙐𝙨𝙚𝙧 {user_id} 𝙙𝙞𝙨𝙖𝙥𝙥𝙧𝙤𝙫𝙚𝙙!")
    
    try:
        bot.send_message(user_id, f"❌ 𝙔𝙤𝙪𝙧 𝙥𝙖𝙮𝙢𝙚𝙣𝙩 𝙬𝙖𝙨 𝙣𝙤𝙩 𝙖𝙥𝙥𝙧𝙤𝙫𝙚𝙙. 𝙋𝙡𝙚𝙖𝙨𝙚 𝙘𝙤𝙣𝙩𝙖𝙘𝙩 𝙨𝙪𝙥𝙥𝙤𝙧𝙩.")
    except:
        pass

@bot.message_handler(commands=['ban'])
def ban_user_cmd(message):
    if not is_admin(message.from_user.id):
        _send_pe(message.chat.id, f"❌ 𝙐𝙣𝙖𝙪𝙩𝙝𝙤𝙧𝙞𝙯𝙚𝙙!")
        return
    
    parts = message.text.split()
    if len(parts) < 2:
        _send_pe(message.chat.id, f"❌ 𝙐𝙨𝙖𝙜𝙚: /ban 𝙪𝙨𝙚𝙧_𝙞𝙙")
        return
    
    try:
        user_id = int(parts[1])
    except:
        _send_pe(message.chat.id, f"❌ 𝙄𝙣𝙫𝙖𝙡𝙞𝙙 𝙐𝙨𝙚𝙧 𝙄𝘿!")
        return
    
    update_user(user_id, "banned", True)
    _send_pe(message.chat.id, f"✅ 𝙐𝙨𝙚𝙧 {user_id} 𝘽𝘼𝙉𝙉𝙀𝘿!")
    
    try:
        bot.send_message(user_id, f"❌ 𝙔𝙤𝙪 𝙝𝙖𝙫𝙚 𝙗𝙚𝙚𝙣 𝘽𝘼𝙉𝙉𝙀𝘿 𝙛𝙧𝙤𝙢 𝙪𝙨𝙞𝙣𝙜 𝙩𝙝𝙞𝙨 𝙗𝙤𝙩!")
    except:
        pass

@bot.message_handler(commands=['unban'])
def unban_user_cmd(message):
    if not is_admin(message.from_user.id):
        _send_pe(message.chat.id, f"❌ 𝙐𝙣𝙖𝙪𝙩𝙝𝙤𝙧𝙞𝙯𝙚𝙙!")
        return
    
    parts = message.text.split()
    if len(parts) < 2:
        _send_pe(message.chat.id, f"❌ 𝙐𝙨𝙖𝙜𝙚: /unban 𝙪𝙨𝙚𝙧_𝙞𝙙")
        return
    
    try:
        user_id = int(parts[1])
    except:
        _send_pe(message.chat.id, f"❌ 𝙄𝙣𝙫𝙖𝙡𝙞𝙙 𝙐𝙨𝙚𝙧 𝙄𝘿!")
        return
    
    update_user(user_id, "banned", False)
    _send_pe(message.chat.id, f"✅ 𝙐𝙨𝙚𝙧 {user_id} 𝙐𝙉𝘽𝘼𝙉𝙉𝙀𝘿!")

@bot.message_handler(commands=['users'])
def users_cmd(message):
    if not is_admin(message.from_user.id):
        _send_pe(message.chat.id, f"❌ 𝙐𝙣𝙖𝙪𝙩𝙝𝙤𝙧𝙞𝙯𝙚𝙙!")
        return
    
    users = load_users()
    total = len(users)
    unlimited = sum(1 for u in users.values() if u.get("unlimited", False))
    banned = sum(1 for u in users.values() if u.get("banned", False))
    
    text = f"""
✅ ═══《 👥 𝙐𝙎𝙀𝙍𝙎 》═══ ✅

✅ 📊 𝙏𝙤𝙩𝙖𝙡 𝙐𝙨𝙚𝙧𝙨: {total}
✅ 💎 𝙐𝙣𝙡𝙞𝙢𝙞𝙩𝙚𝙙: {unlimited}
✅ 🚫 𝘽𝙖𝙣𝙣𝙚𝙙: {banned}

✅ ═══════════════════════ ✅

✅ 👥 𝙐𝙨𝙚𝙧 𝙇𝙞𝙨𝙩:
"""
    
    for uid, data in users.items():
        user_status = "✅" if data.get("unlimited", False) else "🆓"
        banned_status = "🚫" if data.get("banned", False) else "✅"
        text += f"✅ • {data.get('name', 'Unknown')} (@{data.get('username', 'N/A')}) - {user_status} {banned_status}\n"
    
    _send_pe(message.chat.id, text)

@bot.message_handler(commands=['data'])
def data_cmd(message):
    if not is_admin(message.from_user.id):
        _send_pe(message.chat.id, f"❌ 𝙐𝙣𝙖𝙪𝙩𝙝𝙤𝙧𝙞𝙯𝙚𝙙!")
        return
    
    users = load_users()
    orders = load_orders()
    pending = load_pending()
    settings = load_settings()
    buttons = load_buttons()
    
    data = {
        "users": users,
        "orders": orders,
        "pending": pending,
        "settings": settings,
        "buttons": buttons,
        "total_users": len(users),
        "total_bans": len(orders),
        "pending_payments": len(pending),
        "total_buttons": len(buttons),
        "generated": datetime.now().isoformat()
    }
    
    file_path = "bot_data.json"
    with open(file_path, "w") as f:
        json.dump(data, f, indent=2)
    
    with open(file_path, "rb") as f:
        bot.send_document(message.chat.id, f, caption=f"✅ 📥 𝘽𝙤𝙩 𝘿𝙖𝙩𝙖 𝙀𝙭𝙥𝙤𝙧𝙩")

@bot.message_handler(commands=['price'])
def price_cmd(message):
    if not is_admin(message.from_user.id):
        _send_pe(message.chat.id, f"❌ 𝙐𝙣𝙖𝙪𝙩𝙝𝙤𝙧𝙞𝙯𝙚𝙙!")
        return
    
    parts = message.text.split()
    if len(parts) < 2:
        settings = load_settings()
        _send_pe(message.chat.id, f"✅ 💰 𝘾𝙪𝙧𝙧𝙚𝙣𝙩 𝙋𝙧𝙞𝙘𝙚: 𝙍𝙨.{settings.get('price', 99)}\n✅ 📌 𝙐𝙨𝙚: /price <𝙖𝙢𝙤𝙪𝙣𝙩>")
        return
    
    try:
        price = int(parts[1])
        settings = load_settings()
        settings["price"] = price
        save_settings(settings)
        _send_pe(message.chat.id, f"✅ 𝙋𝙧𝙞𝙘𝙚 𝙪𝙥𝙙𝙖𝙩𝙚𝙙 𝙩𝙤 𝙍𝙨.{price}!")
    except:
        _send_pe(message.chat.id, f"❌ 𝙄𝙣𝙫𝙖𝙡𝙞𝙙 𝙖𝙢𝙤𝙪𝙣𝙩!")

@bot.message_handler(commands=['upi'])
def upi_cmd(message):
    if not is_admin(message.from_user.id):
        _send_pe(message.chat.id, f"❌ 𝙐𝙣𝙖𝙪𝙩𝙝𝙤𝙧𝙞𝙯𝙚𝙙!")
        return
    
    parts = message.text.split()
    if len(parts) < 2:
        settings = load_settings()
        _send_pe(message.chat.id, f"✅ 🏦 𝘾𝙪𝙧𝙧𝙚𝙣𝙩 𝙐𝙋𝙄: {settings.get('upi', 'vanshx111@naviaxis')}\n✅ 📌 𝙐𝙨𝙚: /upi <𝙣𝙚𝙬_𝙪𝙥𝙞>")
        return
    
    upi = parts[1]
    settings = load_settings()
    settings["upi"] = upi
    save_settings(settings)
    _send_pe(message.chat.id, f"✅ 𝙐𝙋𝙄 𝙪𝙥𝙙𝙖𝙩𝙚𝙙 𝙩𝙤: {upi}!")

@bot.message_handler(commands=['developer'])
def developer_cmd(message):
    if not is_admin(message.from_user.id):
        _send_pe(message.chat.id, f"❌ 𝙐𝙣𝙖𝙪𝙩𝙝𝙤𝙧𝙞𝙯𝙚𝙙!")
        return
    
    parts = message.text.split()
    if len(parts) < 2:
        settings = load_settings()
        _send_pe(message.chat.id, f"✅ 👨‍💻 𝘾𝙪𝙧𝙧𝙚𝙣𝙩 𝘿𝙚𝙫𝙚𝙡𝙤𝙥𝙚𝙧: {settings.get('developer', '@iflexzyan')}\n✅ 📌 𝙐𝙨𝙚: /developer <@𝙣𝙖𝙢𝙚>")
        return
    
    developer = parts[1]
    settings = load_settings()
    settings["developer"] = developer
    settings["support"] = developer
    save_settings(settings)
    _send_pe(message.chat.id, f"✅ 𝘿𝙚𝙫𝙚𝙡𝙤𝙥𝙚𝙧 𝙪𝙥𝙙𝙖𝙩𝙚𝙙 𝙩𝙤: {developer}!")

@bot.message_handler(commands=['addadmin'])
def add_admin_cmd(message):
    if not is_admin(message.from_user.id):
        _send_pe(message.chat.id, f"❌ 𝙐𝙣𝙖𝙪𝙩𝙝𝙤𝙧𝙞𝙯𝙚𝙙!")
        return
    
    parts = message.text.split()
    if len(parts) < 2:
        _send_pe(message.chat.id, f"❌ 𝙐𝙨𝙖𝙜𝙚: /addadmin 𝙪𝙨𝙚𝙧_𝙞𝙙")
        return
    
    try:
        user_id = int(parts[1])
        if user_id not in ADMIN_IDS:
            ADMIN_IDS.append(user_id)
            _send_pe(message.chat.id, f"✅ 𝙐𝙨𝙚𝙧 {user_id} 𝙖𝙙𝙙𝙚𝙙 𝙖𝙨 𝘼𝙙𝙢𝙞𝙣!")
        else:
            _send_pe(message.chat.id, f"⚠️ 𝙐𝙨𝙚𝙧 {user_id} 𝙞𝙨 𝙖𝙡𝙧𝙚𝙖𝙙𝙮 𝘼𝙙𝙢𝙞𝙣!")
    except:
        _send_pe(message.chat.id, f"❌ 𝙄𝙣𝙫𝙖𝙡𝙞𝙙 𝙐𝙨𝙚𝙧 𝙄𝘿!")

# ============================================================
# CLONE BOT SYSTEM - SHORT VERSION
# ============================================================

@bot.message_handler(commands=['clone'])
def clone_admin_cmd(message):
    if not is_admin(message.from_user.id):
        _send_pe(message.chat.id, f"❌ 𝙐𝙣𝙖𝙪𝙩𝙝𝙤𝙧𝙞𝙯𝙚𝙙!")
        return
    
    _send_pe(message.chat.id, f"""
✅ ═══《 📋 𝘾𝙇𝙊𝙉𝙀 𝘽𝙊𝙏 》═══ ✅

✅ 🤖 𝙀𝙣𝙩𝙚𝙧 𝙣𝙚𝙬 𝙗𝙤𝙩 𝙩𝙤𝙠𝙚𝙣 𝙩𝙤 𝙘𝙡𝙤𝙣𝙚:

✅ ═══════════════════════ ✅

✅ 📌 𝙎𝙩𝙚𝙥𝙨:
✅ 𝟭. 𝘾𝙧𝙚𝙖𝙩𝙚 𝙣𝙚𝙬 𝙗𝙤𝙩 𝙛𝙧𝙤𝙢 @BotFather
✅ 𝟮. 𝘾𝙤𝙥𝙮 𝙩𝙤𝙠𝙚𝙣
✅ 𝟯. 𝙎𝙚𝙣𝙙 𝙩𝙤𝙠𝙚𝙣 𝙝𝙚𝙧𝙚

✅ ═══════════════════════ ✅
""")
    bot.register_next_step_handler(message, process_clone_admin_token)

def process_clone_admin_token(message):
    if not is_admin(message.from_user.id):
        return
    
    token = message.text.strip()
    
    if not token or ':' not in token:
        _send_pe(message.chat.id, f"❌ 𝙄𝙣𝙫𝙖𝙡𝙞𝙙 𝘽𝙤𝙩 𝙏𝙤𝙠𝙚𝙣!")
        return
    
    try:
        test_bot = TeleBot(token)
        bot_info = test_bot.get_me()
        
        clone_data = {
            "token": token,
            "bot_name": bot_info.first_name,
            "bot_username": bot_info.username,
            "cloned_by": message.from_user.id,
            "cloned_at": datetime.now().isoformat(),
            "developer": load_settings().get("developer", "@iflexzyan"),
            "support": load_settings().get("support", "@iflexzyan"),
            "price": load_settings().get("price", 99),
            "upi": load_settings().get("upi", "vanshx111@naviaxis")
        }
        save_clone(clone_data)
        
        _send_pe(message.chat.id, f"""
✅ ═══《 ✅ 𝘽𝙊𝙏 𝘾𝙇𝙊𝙉𝙀𝘿 》═══ ✅

✅ 🤖 𝘽𝙤𝙩 𝙉𝙖𝙢𝙚: {bot_info.first_name}
✅ 👾 @{bot_info.username}

✅ ═══════════════════════ ✅

✅ 👨‍💻 𝘿𝙚𝙫𝙚𝙡𝙤𝙥𝙚𝙧: {clone_data['developer']}
✅ 💰 𝙋𝙧𝙞𝙘𝙚: 𝙍𝙨.{clone_data['price']}

✅ ═══════════════════════ ✅
""")
        
        notify_owner(f"✅ 𝘽𝙤𝙩 𝘾𝙡𝙤𝙣𝙚𝙙!\n🤖 {bot_info.first_name}\n👾 @{bot_info.username}")
        
    except Exception as e:
        _send_pe(message.chat.id, f"❌ 𝙀𝙧𝙧𝙤𝙧: {str(e)}")

# ============================================================
# BROADCAST COMMANDS
# ============================================================

@bot.message_handler(commands=['broadcastuser'])
def broadcast_user(message):
    if not is_admin(message.from_user.id):
        _send_pe(message.chat.id, f"❌ 𝙐𝙣𝙖𝙪𝙩𝙝𝙤𝙧𝙞𝙯𝙚𝙙!")
        return
    
    parts = message.text.split(maxsplit=2)
    if len(parts) < 3:
        _send_pe(message.chat.id, f"❌ 𝙐𝙨𝙖𝙜𝙚: /broadcastuser 𝙪𝙨𝙚𝙧_𝙞𝙙 𝙢𝙚𝙨𝙨𝙖𝙜𝙚")
        return
    
    try:
        user_id = int(parts[1])
        msg = parts[2]
    except:
        _send_pe(message.chat.id, f"❌ 𝙄𝙣𝙫𝙖𝙡𝙞𝙙 𝙐𝙨𝙚𝙧 𝙄𝘿!")
        return
    
    try:
        bot.send_message(user_id, f"📢 {msg}")
        _send_pe(message.chat.id, f"✅ 𝙈𝙚𝙨𝙨𝙖𝙜𝙚 𝙨𝙚𝙣𝙩 𝙩𝙤 𝙪𝙨𝙚𝙧 {user_id}!")
    except Exception as e:
        _send_pe(message.chat.id, f"❌ 𝙁𝙖𝙞𝙡𝙚𝙙: {str(e)}")

@bot.message_handler(commands=['allbroadcast'])
def all_broadcast(message):
    if not is_admin(message.from_user.id):
        _send_pe(message.chat.id, f"❌ 𝙐𝙣𝙖𝙪𝙩𝙝𝙤𝙧𝙞𝙯𝙚𝙙!")
        return
    
    parts = message.text.split(maxsplit=1)
    if len(parts) < 2:
        _send_pe(message.chat.id, f"❌ 𝙐𝙨𝙖𝙜𝙚: /allbroadcast 𝙢𝙚𝙨𝙨𝙖𝙜𝙚")
        return
    
    msg = parts[1]
    users = load_users()
    
    if not users:
        _send_pe(message.chat.id, f"❌ 𝙉𝙤 𝙪𝙨𝙚𝙧𝙨 𝙛𝙤𝙪𝙣𝙙!")
        return
    
    sent = 0
    failed = 0
    
    _send_pe(message.chat.id, f"⏳ 𝙎𝙚𝙣𝙙𝙞𝙣𝙜 𝙩𝙤 {len(users)} 𝙪𝙨𝙚𝙧𝙨...")
    
    for user_id in users.keys():
        try:
            bot.send_message(int(user_id), f"📢 {msg}")
            sent += 1
            time.sleep(0.05)
        except:
            failed += 1
    
    _send_pe(message.chat.id, f"""
✅ 𝘽𝙧𝙤𝙖𝙙𝙘𝙖𝙨𝙩 𝘾𝙤𝙢𝙥𝙡𝙚𝙩𝙚!

✅ 𝙏𝙤𝙩𝙖𝙡: {len(users)}
✅ 𝙎𝙚𝙣𝙩: {sent}
✅ 𝙁𝙖𝙞𝙡𝙚𝙙: {failed}
""")

@bot.message_handler(func=lambda m: m.text and "𝘽𝙍𝙊𝘼𝘿𝘾𝘼𝙎𝙏" in m.text)
def broadcast_btn(message):
    if not is_admin(message.from_user.id):
        _send_pe(message.chat.id, f"❌ 𝙐𝙣𝙖𝙪𝙩𝙝𝙤𝙧𝙞𝙯𝙚𝙙!")
        return
    
    _send_pe(message.chat.id, f"""
✅ ═══《 📢 𝘽𝙍𝙊𝘼𝘿𝘾𝘼𝙎𝙏 》═══ ✅

✅ /broadcastuser 𝙪𝙨𝙚𝙧_𝙞𝙙 𝙢𝙨𝙜 - 𝙎𝙥𝙚𝙘𝙞𝙛𝙞𝙘
✅ /allbroadcast 𝙢𝙨𝙜 - 𝘼𝙡𝙡 𝙪𝙨𝙚𝙧𝙨

✅ ═══════════════════════ ✅
""")

@bot.message_handler(func=lambda m: m.text and "𝘼𝙇𝙇 𝘽𝙍𝙊𝘼𝘿𝘾𝘼𝙎𝙏" in m.text)
def all_broadcast_btn(message):
    if not is_admin(message.from_user.id):
        _send_pe(message.chat.id, f"❌ 𝙐𝙣𝙖𝙪𝙩𝙝𝙤𝙧𝙞𝙯𝙚𝙙!")
        return
    
    _send_pe(message.chat.id, f"""
✅ ═══《 📢 𝘼𝙇𝙇 𝘽𝙍𝙊𝘼𝘿𝘾𝘼𝙎𝙏 》═══ ✅

✅ /allbroadcast 𝙢𝙚𝙨𝙨𝙖𝙜𝙚

✅ 𝙀𝙭𝙖𝙢𝙥𝙡𝙚:
✅ /allbroadcast 𝙃𝙚𝙡𝙡𝙤 𝙚𝙫𝙚𝙧𝙮𝙤𝙣𝙚!

✅ ═══════════════════════ ✅
""")

# ============================================================
# BOT ON/OFF
# ============================================================

@bot.message_handler(func=lambda m: m.text and "𝘽𝙊𝙏 𝙊𝙉" in m.text)
def bot_on_cmd(message):
    if not is_admin(message.from_user.id):
        _send_pe(message.chat.id, f"❌ 𝙐𝙣𝙖𝙪𝙩𝙝𝙤𝙧𝙞𝙯𝙚𝙙!")
        return
    
    global bot_active
    bot_active = True
    _send_pe(message.chat.id, f"✅ 🟢 𝘽𝙤𝙩 𝙞𝙨 𝙣𝙤𝙬 𝙊𝙉𝙇𝙄𝙉𝙀!")

@bot.message_handler(func=lambda m: m.text and "𝘽𝙊𝙏 𝙊𝙁𝙁" in m.text)
def bot_off_cmd(message):
    if not is_admin(message.from_user.id):
        _send_pe(message.chat.id, f"❌ 𝙐𝙣𝙖𝙪𝙩𝙝𝙤𝙧𝙞𝙯𝙚𝙙!")
        return
    
    global bot_active
    bot_active = False
    _send_pe(message.chat.id, f"✅ 🔴 𝘽𝙤𝙩 𝙞𝙨 𝙣𝙤𝙬 𝙊𝙁𝙁𝙇𝙄𝙉𝙀!")

# ============================================================
# STATS & ADMIN PANEL
# ============================================================

@bot.message_handler(func=lambda m: m.text and "𝙎𝙏𝘼𝙏𝙎" in m.text)
def stats_cmd(message):
    if not is_admin(message.from_user.id):
        _send_pe(message.chat.id, f"❌ 𝙐𝙣𝙖𝙪𝙩𝙝𝙤𝙧𝙞𝙯𝙚𝙙!")
        return
    
    users = load_users()
    orders = load_orders()
    pending = load_pending()
    settings = load_settings()
    buttons = load_buttons()
    
    text = f"""
✅ ═══《 📊 𝙎𝙏𝘼𝙏𝙎 》═══ ✅

✅ 👥 𝙏𝙤𝙩𝙖𝙡 𝙐𝙨𝙚𝙧𝙨: {len(users)}
✅ 🔫 𝙏𝙤𝙩𝙖𝙡 𝘽𝙖𝙣𝙨: {len(orders)}
✅ 💰 𝙋𝙚𝙣𝙙𝙞𝙣𝙜: {len(pending)}
✅ 💎 𝙐𝙣𝙡𝙞𝙢𝙞𝙩𝙚𝙙: {sum(1 for u in users.values() if u.get('unlimited', False))}
✅ 📋 𝘽𝙪𝙩𝙩𝙤𝙣𝙨: {len(buttons)}

✅ ═══════════════════════ ✅

✅ 💳 𝙋𝙧𝙞𝙘𝙚: 𝙍𝙨.{settings.get('price', 99)}
✅ 🏦 𝙐𝙋𝙄: {settings.get('upi', 'vanshx111@naviaxis')}
✅ 👨‍💻 𝘿𝙚𝙫𝙚𝙡𝙤𝙥𝙚𝙧: {settings.get('developer', '@iflexzyan')}

✅ ═══════════════════════ ✅
"""
    _send_pe(message.chat.id, text)

@bot.message_handler(func=lambda m: m.text and "𝘼𝘿𝙈𝙄𝙉 𝙋𝘼𝙉𝙀𝙇" in m.text)
def admin_panel_cmd(message):
    if not is_admin(message.from_user.id):
        _send_pe(message.chat.id, f"❌ 𝙐𝙣𝙖𝙪𝙩𝙝𝙤𝙧𝙞𝙯𝙚𝙙!")
        return
    
    text = f"""
✅ ═══《 👑 𝘼𝘿𝙈𝙄𝙉 𝙋𝘼𝙉𝙀𝙇 》═══ ✅

✅ 📌 𝘾𝙤𝙢𝙢𝙖𝙣𝙙𝙨:

✅ /approve 𝙞𝙙 - 𝘼𝙥𝙥𝙧𝙤𝙫𝙚
✅ /disapprove 𝙞𝙙 - 𝙍𝙚𝙟𝙚𝙘𝙩
✅ /ban 𝙞𝙙 - 𝘽𝙖𝙣
✅ /unban 𝙞𝙙 - 𝙐𝙣𝙗𝙖𝙣
✅ /users - 𝘼𝙡𝙡 𝙪𝙨𝙚𝙧𝙨
✅ /data - 𝘿𝙤𝙬𝙣𝙡𝙤𝙖𝙙
✅ /price <𝙖𝙢𝙩> - 𝘾𝙝𝙖𝙣𝙜𝙚
✅ /upi <𝙪𝙥𝙞> - 𝘾𝙝𝙖𝙣𝙜𝙚
✅ /developer <@> - 𝘾𝙝𝙖𝙣𝙜𝙚
✅ /addadmin 𝙞𝙙 - 𝘼𝙙𝙙
✅ /clone - 𝘾𝙡𝙤𝙣𝙚
✅ /prcclone <𝙖𝙢𝙩> - 𝘾𝙡𝙤𝙣𝙚 𝙥𝙧𝙞𝙘𝙚
✅ /broadcastuser 𝙞𝙙 𝙢𝙨𝙜 - 𝙎𝙚𝙣𝙙
✅ /allbroadcast 𝙢𝙨𝙜 - 𝘼𝙡𝙡
✅ /addbutton - 𝘼𝙙𝙙
✅ /listbuttons - 𝙇𝙞𝙨𝙩
✅ /removebutton - 𝙍𝙚𝙢𝙤𝙫𝙚
✅ /addtokenvideo - 𝙑𝙞𝙙𝙚𝙤
✅ /allcommands - 𝙏𝙝𝙞𝙨 𝙢𝙚𝙣𝙪

✅ ═══════════════════════ ✅
"""
    _send_pe(message.chat.id, text)

@bot.message_handler(commands=['prcclone'])
def clone_price_cmd(message):
    if not is_admin(message.from_user.id):
        _send_pe(message.chat.id, f"❌ 𝙐𝙣𝙖𝙪𝙩𝙝𝙤𝙧𝙞𝙯𝙚𝙙!")
        return
    
    parts = message.text.split()
    if len(parts) < 2:
        settings = load_settings()
        _send_pe(message.chat.id, f"✅ 💰 𝘾𝙡𝙤𝙣𝙚 𝙋𝙧𝙞𝙘𝙚: 𝙍𝙨.{settings.get('clone_price', 199)}\n✅ 📌 𝙐𝙨𝙚: /prcclone <𝙖𝙢𝙤𝙪𝙣𝙩>")
        return
    
    try:
        price = int(parts[1])
        settings = load_settings()
        settings["clone_price"] = price
        save_settings(settings)
        _send_pe(message.chat.id, f"✅ 𝘾𝙡𝙤𝙣𝙚 𝙋𝙧𝙞𝙘𝙚 𝙪𝙥𝙙𝙖𝙩𝙚𝙙 𝙩𝙤 𝙍𝙨.{price}!")
    except:
        _send_pe(message.chat.id, f"❌ 𝙄𝙣𝙫𝙖𝙡𝙞𝙙 𝙖𝙢𝙤𝙪𝙣𝙩!")

# ============================================================
# CALLBACK HANDLERS
# ============================================================

@bot.callback_query_handler(func=lambda c: c.data == "ban_another")
def ban_another_callback(call):
    user_id = call.from_user.id
    user = get_user(user_id)
    
    if not user or user.get("banned", False):
        _send_pe(call.message.chat.id, f"❌ 𝙔𝙤𝙪 𝙖𝙧𝙚 𝘽𝘼𝙉𝙉𝙀𝘿!")
        return
    
    if not user.get("unlimited", False):
        uses = user.get("uses", 0)
        if uses >= 1:
            _send_pe(call.message.chat.id, f"⚠️ 𝙁𝙧𝙚𝙚 𝙏𝙧𝙞𝙖𝙡 𝙐𝙨𝙚𝙙!\n💰 𝙋𝙖𝙮 𝙍𝙨.{load_settings().get('price', 99)}")
            send_payment_qr(call.message.chat.id)
            bot.answer_callback_query(call.id)
            return
    
    _send_pe(call.message.chat.id, f"🔑 𝙎𝙚𝙣𝙙 𝘼𝙘𝙘𝙚𝙨𝙨 𝙏𝙤𝙠𝙚𝙣!")
    bot.register_next_step_handler(call.message, process_ban_token)
    bot.answer_callback_query(call.id)

@bot.callback_query_handler(func=lambda c: c.data == "get_unlimited")
def get_unlimited_callback(call):
    send_payment_qr(call.message.chat.id)
    bot.answer_callback_query(call.id)

@bot.callback_query_handler(func=lambda c: c.data == "support_contact")
def support_contact_callback(call):
    settings = load_settings()
    support = settings.get("support", "@iflexzyan")
    
    text = f"""
✅ ═══《 📞 𝙎𝙐𝙋𝙋𝙊𝙍𝙏 》═══ ✅

✅ 👨‍💻 𝘿𝙚𝙫𝙚𝙡𝙤𝙥𝙚𝙧: {settings.get('developer', '@iflexzyan')}

✅ ═══════════════════════ ✅

✅ 📩 𝘾𝙤𝙣𝙩𝙖𝙘𝙩: {support}

✅ ═══════════════════════ ✅
"""
    markup = InlineKeyboardMarkup([
        [make_blue_button("𝘾𝙊𝙉𝙏𝘼𝘾𝙏", url=f"https://t.me/{support.replace('@', '')}")]
    ])
    _send_pe(call.message.chat.id, text, reply_markup=markup)
    bot.answer_callback_query(call.id)

@bot.callback_query_handler(func=lambda c: c.data == "close_button")
def close_button_callback(call):
    try:
        bot.delete_message(call.message.chat.id, call.message.message_id)
    except:
        pass
    bot.answer_callback_query(call.id)

# ============================================================
# TOKEN VIDEO
# ============================================================

@bot.message_handler(commands=['addtokenvideo'])
def add_token_video(message):
    if not is_admin(message.from_user.id):
        _send_pe(message.chat.id, f"❌ 𝙐𝙣𝙖𝙪𝙩𝙝𝙤𝙧𝙞𝙯𝙚𝙙!")
        return
    
    _send_pe(message.chat.id, f"📤 𝙎𝙚𝙣𝙙 𝙫𝙞𝙙𝙚𝙤 𝙛𝙤𝙧 '𝙃𝙊𝙒 𝙏𝙊 𝙂𝙀𝙏 𝙏𝙊𝙆𝙀𝙉'")
    bot.register_next_step_handler(message, save_token_video)

def save_token_video(message):
    if message.video:
        file_info = bot.get_file(message.video.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        with open("token_video.mp4", "wb") as f:
            f.write(downloaded_file)
        _send_pe(message.chat.id, f"✅ 𝙑𝙞𝙙𝙚𝙤 𝙨𝙖𝙫𝙚𝙙!")
    else:
        _send_pe(message.chat.id, f"❌ 𝙎𝙚𝙣𝙙 𝙖 𝙫𝙞𝙙𝙚𝙤!")

@bot.message_handler(func=lambda m: m.text and "𝙃𝙊𝙒 𝙏𝙊 𝙂𝙀𝙏 𝙏𝙊𝙆𝙀𝙉" in m.text)
def how_to_get_token(message):
    if os.path.exists("token_video.mp4"):
        with open("token_video.mp4", "rb") as f:
            bot.send_video(message.chat.id, f, caption=f"✅ 𝙃𝙤𝙬 𝙩𝙤 𝙂𝙚𝙩 𝘼𝙘𝙘𝙚𝙨𝙨 𝙏𝙤𝙠𝙚𝙣")
    else:
        text = f"""
✅ ═══《 ❓ 𝙃𝙊𝙒 𝙏𝙊 𝙂𝙀𝙏 𝙏𝙊𝙆𝙀𝙉 》═══ ✅

✅ 𝟭️⃣ 𝙊𝙥𝙚𝙣 𝙁𝙧𝙚𝙚 𝙁𝙞𝙧𝙚
✅ 𝟮️⃣ 𝙂𝙤 𝙩𝙤 𝙎𝙚𝙩𝙩𝙞𝙣𝙜𝙨 ⚙️
✅ 𝟯️⃣ 𝘾𝙡𝙞𝙘𝙠 𝘼𝙘𝙘𝙤𝙪𝙣𝙩
✅ 𝟰️⃣ 𝙁𝙞𝙣𝙙 "𝘿𝙖𝙩𝙖 𝘼𝙘𝙘𝙚𝙨𝙨"
✅ 𝟱️⃣ 𝘾𝙤𝙥𝙮 𝘼𝙘𝙘𝙚𝙨𝙨 𝙏𝙤𝙠𝙚𝙣

✅ ═══════════════════════ ✅
"""
        _send_pe(message.chat.id, text)

# ============================================================
# CLONE BOT - USER
# ============================================================

@bot.message_handler(func=lambda m: m.text and "𝘾𝙇𝙊𝙉𝙀 𝘽𝙊𝙏" in m.text)
def clone_user_cmd(message):
    user_id = message.from_user.id
    user = get_user(user_id)
    
    if not user or user.get("banned", False):
        _send_pe(message.chat.id, f"❌ 𝙔𝙤𝙪 𝙖𝙧𝙚 𝘽𝘼𝙉𝙉𝙀𝘿!")
        return
    
    settings = load_settings()
    clone_price = settings.get("clone_price", 199)
    
    if not user.get("unlimited", False):
        uses = user.get("uses", 0)
        if uses >= 1:
            _send_pe(message.chat.id, f"⚠️ 𝘾𝙡𝙤𝙣𝙚 𝙘𝙤𝙨𝙩𝙨 𝙍𝙨.{clone_price}\n💰 𝙋𝙖𝙮 𝙩𝙤 𝙜𝙚𝙩 𝙗𝙤𝙩!")
            send_clone_payment_qr(message.chat.id)
            return
    
    _send_pe(message.chat.id, f"""
✅ ═══《 📋 𝘾𝙇𝙊𝙉𝙀 𝘽𝙊𝙏 》═══ ✅

✅ 🤖 𝙎𝙚𝙣𝙙 𝙣𝙚𝙬 𝙗𝙤𝙩 𝙩𝙤𝙠𝙚𝙣:

✅ ═══════════════════════ ✅

✅ 📌 @BotFather 𝙨𝙚 𝙗𝙤𝙩 𝙗𝙣𝙖𝙤
✅ 📌 𝙏𝙤𝙠𝙚𝙣 𝙘𝙤𝙥𝙮 𝙠𝙖𝙧𝙤
✅ 📌 𝙔𝙖𝙝𝙖𝙣 𝙗𝙝𝙚𝙟𝙤

✅ ═══════════════════════ ✅
""")
    bot.register_next_step_handler(message, process_clone_user_token)

def send_clone_payment_qr(chat_id):
    settings = load_settings()
    upi = settings.get("upi", "vanshx111@naviaxis")
    clone_price = settings.get("clone_price", 199)
    
    qr_url = f"https://api.qrserver.com/v1/create-qr-code/?size=300x300&data=upi://pay?pa={upi}&am={clone_price}&cu=INR"
    
    text = f"""
✅ ═══《 💰 𝘾𝙇𝙊𝙉𝙀 𝙋𝘼𝙔𝙈𝙀𝙉𝙏 》═══ ✅

✅ 💳 𝙐𝙋𝙄: {upi}
✅ 💰 𝘼𝙢𝙤𝙪𝙣𝙩: 𝙍𝙨.{clone_price}

✅ ═══════════════════════ ✅

✅ 📱 𝙎𝙘𝙖𝙣 𝙌𝙍 𝙩𝙤 𝙋𝙖𝙮

✅ ═══════════════════════ ✅
"""
    
    keyboard = [
        [make_green_button("𝙄 𝙃𝘼𝙑𝙀 𝙋𝘼𝙄𝘿", callback=f"clone_paid_{chat_id}")],
        [make_blue_button("𝙎𝙐𝙋𝙋𝙊𝙍𝙏", url="https://t.me/iflexzyan")]
    ]
    markup = InlineKeyboardMarkup(keyboard)
    
    try:
        bot.send_photo(chat_id, photo=qr_url, caption=text, reply_markup=markup)
    except:
        _send_pe(chat_id, text, reply_markup=markup)

@bot.callback_query_handler(func=lambda c: c.data and c.data.startswith("clone_paid_"))
def handle_clone_paid(call):
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
        "status": "clone_pending",
        "type": "clone",
        "requested": datetime.now().isoformat()
    }
    save_pending(pending)
    
    _send_pe(chat_id, f"📸 𝙎𝙚𝙣𝙙 𝙘𝙡𝙤𝙣𝙚 𝙥𝙖𝙮𝙢𝙚𝙣𝙩 𝙨𝙘𝙧𝙚𝙚𝙣𝙨𝙝𝙤𝙩!")
    bot.register_next_step_handler(call.message, receive_clone_screenshot)
    bot.answer_callback_query(call.id)

def receive_clone_screenshot(message):
    user_id = message.from_user.id
    
    if message.photo:
        file_id = message.photo[-1].file_id
        pending = load_pending()
        if str(user_id) in pending:
            pending[str(user_id)]["screenshot"] = file_id
            pending[str(user_id)]["status"] = "clone_pending"
            save_pending(pending)
        
        _send_pe(message.chat.id, f"✅ 𝙎𝙘𝙧𝙚𝙚𝙣𝙨𝙝𝙤𝙩 𝙍𝙚𝙘𝙚𝙞𝙫𝙚𝙙!\n⏳ 𝙒𝙖𝙞𝙩𝙞𝙣𝙜 𝙛𝙤𝙧 𝘼𝙙𝙢𝙞𝙣.")
        
        admin_text = f"""
✅ ═══《 💰 𝘾𝙇𝙊𝙉𝙀 𝙋𝘼𝙔𝙈𝙀𝙉𝙏 》═══ ✅

✅ 👤 𝙐𝙨𝙚𝙧: {message.from_user.first_name}
✅ 🆔 𝙄𝘿: {user_id}
✅ 👾 @{message.from_user.username or 'N/A'}

✅ ═══════════════════════ ✅

✅ 📌 /approveclone {user_id}
✅ 📌 /disapproveclone {user_id}

✅ ═══════════════════════ ✅
"""
        for admin in ADMIN_IDS:
            try:
                bot.send_photo(admin, photo=file_id, caption=admin_text)
            except:
                bot.send_message(admin, admin_text)
    else:
        _send_pe(message.chat.id, f"❌ 𝙎𝙚𝙣𝙙 𝙖 𝙋𝙃𝙊𝙏𝙊!")

@bot.message_handler(commands=['approveclone'])
def approve_clone(message):
    if not is_admin(message.from_user.id):
        _send_pe(message.chat.id, f"❌ 𝙐𝙣𝙖𝙪𝙩𝙝𝙤𝙧𝙞𝙯𝙚𝙙!")
        return
    
    parts = message.text.split()
    if len(parts) < 2:
        _send_pe(message.chat.id, f"❌ /approveclone 𝙪𝙨𝙚𝙧_𝙞𝙙")
        return
    
    try:
        user_id = int(parts[1])
    except:
        _send_pe(message.chat.id, f"❌ 𝙄𝙣𝙫𝙖𝙡𝙞𝙙!")
        return
    
    pending = load_pending()
    if str(user_id) in pending:
        del pending[str(user_id)]
        save_pending(pending)
    
    _send_pe(message.chat.id, f"✅ 𝙐𝙨𝙚𝙧 {user_id} 𝙘𝙡𝙤𝙣𝙚 𝙖𝙥𝙥𝙧𝙤𝙫𝙚𝙙!")
    
    try:
        bot.send_message(user_id, f"✅ 𝘾𝙡𝙤𝙣𝙚 𝙋𝙖𝙮𝙢𝙚𝙣𝙩 𝘼𝙥𝙥𝙧𝙤𝙫𝙚𝙙!\n📌 𝙐𝙨𝙚 /clone")
    except:
        pass

def process_clone_user_token(message):
    user_id = message.from_user.id
    token = message.text.strip()
    
    if not token or ':' not in token:
        _send_pe(message.chat.id, f"❌ 𝙄𝙣𝙫𝙖𝙡𝙞𝙙 𝙏𝙤𝙠𝙚𝙣!")
        return
    
    try:
        test_bot = TeleBot(token)
        bot_info = test_bot.get_me()
        
        clone_data = {
            "token": token,
            "bot_name": bot_info.first_name,
            "bot_username": bot_info.username,
            "cloned_by": user_id,
            "cloned_at": datetime.now().isoformat(),
            "developer": load_settings().get("developer", "@iflexzyan"),
            "support": load_settings().get("support", "@iflexzyan"),
            "price": load_settings().get("price", 99),
            "upi": load_settings().get("upi", "vanshx111@naviaxis")
        }
        save_clone(clone_data)
        
        _send_pe(message.chat.id, f"""
✅ ═══《 ✅ 𝘽𝙊𝙏 𝘾𝙇𝙊𝙉𝙀𝘿 》═══ ✅

✅ 🤖 {bot_info.first_name}
✅ 👾 @{bot_info.username}

✅ ═══════════════════════ ✅

✅ 👨‍💻 {clone_data['developer']}
✅ 💰 𝙍𝙨.{clone_data['price']}
✅ 🏦 {clone_data['upi']}

✅ ═══════════════════════ ✅
""")
        
        try:
            test_bot.send_message(user_id, f"✅ 𝙒𝙚𝙡𝙘𝙤𝙢𝙚 𝙩𝙤 𝙮𝙤𝙪𝙧 𝙘𝙡𝙤𝙣𝙚𝙙 𝙗𝙤𝙩!\n👨‍💻 {clone_data['developer']}")
        except:
            pass
        
        notify_owner(f"✅ 𝘽𝙤𝙩 𝘾𝙡𝙤𝙣𝙚𝙙!\n🤖 {bot_info.first_name}\n👤 𝘽𝙮: {user_id}")
        
    except Exception as e:
        _send_pe(message.chat.id, f"❌ 𝙀𝙧𝙧𝙤𝙧: {str(e)}")

# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":
    print("✅ 𝙁𝙁 𝘽𝘼𝙉 𝘽𝙊𝙏 𝙎𝙩𝙖𝙧𝙩𝙚𝙙!")
    print(f"✅ 𝙊𝙬𝙣𝙚𝙧 𝙄𝘿: {OWNER_ID}")
    print(f"✅ 𝙏𝙤𝙩𝙖𝙡 𝙐𝙨𝙚𝙧𝙨: {len(load_users())}")
    
    try:
        bot.remove_webhook()
        print("✅ 𝙒𝙚𝙗𝙝𝙤𝙤𝙠 𝙧𝙚𝙢𝙤𝙫𝙚𝙙!")
    except:
        pass
    
    bot.infinity_polling()