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
CLONE_FILE = "clone.json"
BUTTONS_FILE = "buttons.json"

# ============================================================
# USERS DATA - JO TUMPE DIYA THA
# ============================================================
def load_users():
    if os.path.exists(USERS_FILE):
        try:
            with open(USERS_FILE, "r") as f:
                return json.load(f)
        except:
            pass
    
    # Default users data
    users = {
        "8586849798": {
            "id": 8586849798,
            "username": "Ffaccsellerx",
            "name": "FF SELLER",
            "joined": "2026-07-31T05:18:43.493579",
            "uses": 1,
            "unlimited": False,
            "banned": False
        },
        "8908882066": {
            "id": 8908882066,
            "username": None,
            "name": "Dice",
            "joined": "2026-07-31T05:30:04.435718",
            "uses": 0,
            "unlimited": False,
            "banned": False
        },
        "8471373583": {
            "id": 8471373583,
            "username": "iflexzyan",
            "name": "ZYAN",
            "joined": "2026-07-31T05:30:31.611686",
            "uses": 0,
            "unlimited": False,
            "banned": False
        },
        "6729963447": {
            "id": 6729963447,
            "username": "ZIXU_NXT",
            "name": "BUNNY !!! ✨",
            "joined": "2026-07-31T05:31:09.765285",
            "uses": 0,
            "unlimited": False,
            "banned": False
        },
        "8955229317": {
            "id": 8955229317,
            "username": "LEGENDxFIRE",
            "name": "LEGEND X FIRE 🔥",
            "joined": "2026-07-31T05:39:01.873843",
            "uses": 0,
            "unlimited": True,
            "banned": False
        },
        "7977493987": {
            "id": 7977493987,
            "username": "Havkerbabaybaba",
            "name": "Bhai on top",
            "joined": "2026-07-31T05:39:30.486969",
            "uses": 0,
            "unlimited": False,
            "banned": False
        },
        "6415045552": {
            "id": 6415045552,
            "username": "FOREXX_XD",
            "name": "FOREXX !!",
            "joined": "2026-07-31T06:16:36.698711",
            "uses": 0,
            "unlimited": False,
            "banned": False
        },
        "5961757687": {
            "id": 5961757687,
            "username": "Nexo4a",
            "name": "NEXO",
            "joined": "2026-07-31T06:17:15.251743",
            "uses": 0,
            "unlimited": False,
            "banned": False
        },
        "7710991582": {
            "id": 7710991582,
            "username": "VccvNomoreccBOT",
            "name": "Shsb",
            "joined": "2026-07-31T06:19:52.133642",
            "uses": 0,
            "unlimited": False,
            "banned": False
        },
        "8741006842": {
            "id": 8741006842,
            "username": "LUXFIRE10",
            "name": "Hello",
            "joined": "2026-07-31T06:22:17.941171",
            "uses": 0,
            "unlimited": False,
            "banned": False
        },
        "7896163877": {
            "id": 7896163877,
            "username": "cbwel",
            "name": "VARDAN !!!",
            "joined": "2026-07-31T06:23:29.242823",
            "uses": 0,
            "unlimited": False,
            "banned": False
        },
        "8894084046": {
            "id": 8894084046,
            "username": None,
            "name": "Jatin",
            "joined": "2026-07-31T06:54:35.530336",
            "uses": 0,
            "unlimited": False,
            "banned": False
        },
        "8345492643": {
            "id": 8345492643,
            "username": None,
            "name": "Fxiiznnn.1",
            "joined": "2026-07-31T07:06:34.662687",
            "uses": 0,
            "unlimited": True,
            "banned": False
        },
        "7222081143": {
            "id": 7222081143,
            "username": None,
            "name": "Autopay Agent",
            "joined": "2026-07-31T07:33:26.632237",
            "uses": 0,
            "unlimited": False,
            "banned": False
        },
        "8763036983": {
            "id": 8763036983,
            "username": "TGKNOWBIKASH",
            "name": "BIKASH !!!!",
            "joined": "2026-07-31T07:34:18.997414",
            "uses": 0,
            "unlimited": False,
            "banned": False
        },
        "6519679140": {
            "id": 6519679140,
            "username": "Errorzlive",
            "name": "ERROR ERA !!",
            "joined": "2026-07-31T07:34:51.396062",
            "uses": 0,
            "unlimited": False,
            "banned": False
        },
        "5506071596": {
            "id": 5506071596,
            "username": "Zexyxexe",
            "name": "ZEXY",
            "joined": "2026-07-31T07:57:02.898103",
            "uses": 0,
            "unlimited": False,
            "banned": False
        },
        "5749912145": {
            "id": 5749912145,
            "username": "Zetoxexe",
            "name": "ZETOX",
            "joined": "2026-07-31T07:59:50.685331",
            "uses": 0,
            "unlimited": False,
            "banned": False
        },
        "8690459200": {
            "id": 8690459200,
            "username": "SAITAMAxFF",
            "name": "SAITAMA FF...!!!",
            "joined": "2026-07-31T08:56:45.327673",
            "uses": 0,
            "unlimited": False,
            "banned": False
        },
        "7178372394": {
            "id": 7178372394,
            "username": "Abhi_sama1",
            "name": "Abhi",
            "joined": "2026-07-31T12:08:57.178524",
            "uses": 0,
            "unlimited": False,
            "banned": False
        },
        "6776661878": {
            "id": 6776661878,
            "username": "TNSELLERFFID",
            "name": "ITAN",
            "joined": "2026-07-31T12:10:03.408531",
            "uses": 0,
            "unlimited": False,
            "banned": False
        },
        "7796329793": {
            "id": 7796329793,
            "username": "Vir4jsharma2069",
            "name": "VIRAJ SHARMA",
            "joined": "2026-07-31T12:17:34.926080",
            "uses": 0,
            "unlimited": False,
            "banned": False
        }
    }
    save_users(users)
    return users

def save_users(users):
    with open(USERS_FILE, "w") as f:
        json.dump(users, f, indent=2)

# ============================================================
# LOAD BUTTONS
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

# ============================================================
# VERIFIED PREMIUM EMOJIS
# ============================================================
VERIFIED_EMOJIS = {
    "verified": {"id": "6147565374289220368", "fallback": "✅"},
    "flex": {"id": "6147464060305676048", "fallback": "😎"},
    "blue_verification": {"id": "6147524086768604985", "fallback": "💎"},
    "frozen": {"id": "5449449325434266744", "fallback": "❄️"},
    "crying": {"id": "6273840152980755328", "fallback": "😭"},
    "smiling": {"id": "6276057176444246654", "fallback": "🙂"},
    "seeing_up": {"id": "6273997026661241933", "fallback": "😋"},
    "teeth": {"id": "6273726078649372769", "fallback": "😁"},
    "done": {"id": "6274007313107915274", "fallback": "👍"},
    "blue_badge": {"id": "5978776771623914876", "fallback": "🟫"},
    "black_badge": {"id": "5978686323907628843", "fallback": "🔸"},
    "busy_tag": {"id": "5852873584912896283", "fallback": "🟧"},
    "instagram": {"id": "5895297528106061174", "fallback": "🌐"},
    "telegram": {"id": "5895735846698487922", "fallback": "🌐"},
    "whatsapp": {"id": "5895343514320899727", "fallback": "🌐"},
    "india": {"id": "5913754823643107921", "fallback": "🇮🇳"},
    "dollar": {"id": "5197434882321567830", "fallback": "💵"},
    "top": {"id": "5463071033256848094", "fallback": "🔝"},
    "bro": {"id": "5463256910851546817", "fallback": "🤝"},
    "yes": {"id": "5463423955014529788", "fallback": "👌"},
    "lock": {"id": "5465443379917629504", "fallback": "🔓"},
    "good": {"id": "5465465194056525619", "fallback": "👍"},
    "sigma": {"id": "6235620067942341623", "fallback": "🥃"},
    "don": {"id": "6235717714023814969", "fallback": "🍂"},
    "skills": {"id": "6235593671073339928", "fallback": "💀"},
    "heart": {"id": "6147617184479711380", "fallback": "❤️‍🔥"},
    "stars": {"id": "6235403472741603087", "fallback": "⭐"},
    "github": {"id": "5346181118884331907", "fallback": "📱"},
    "motion": {"id": "5971944878815317190", "fallback": "💠"},
}

PRIMARY_EMOJIS = list(VERIFIED_EMOJIS.values())
PLACEHOLDER = "🌟"

# ============================================================
# STYLISH FONT
# ============================================================
def stylish_text(text: str) -> str:
    stylish_chars = {
        'A': '𝐀', 'B': '𝐁', 'C': '𝐂', 'D': '𝐃', 'E': '𝐄', 'F': '𝐅', 'G': '𝐆',
        'H': '𝐇', 'I': '𝐈', 'J': '𝐉', 'K': '𝐊', 'L': '𝐋', 'M': '𝐌', 'N': '𝐍',
        'O': '𝐎', 'P': '𝐏', 'Q': '𝐐', 'R': '𝐑', 'S': '𝐒', 'T': '𝐓', 'U': '𝐔',
        'V': '𝐕', 'W': '𝐖', 'X': '𝐗', 'Y': '𝐘', 'Z': '𝐙',
        'a': '𝐚', 'b': '𝐛', 'c': '𝐜', 'd': '𝐝', 'e': '𝐞', 'f': '𝐟', 'g': '𝐠',
        'h': '𝐡', 'i': '𝐢', 'j': '𝐣', 'k': '𝐤', 'l': '𝐥', 'm': '𝐦', 'n': '𝐧',
        'o': '𝐨', 'p': '𝐩', 'q': '𝐪', 'r': '𝐫', 's': '𝐬', 't': '𝐭', 'u': '𝐮',
        'v': '𝐯', 'w': '𝐰', 'x': '𝐱', 'y': '𝐲', 'z': '𝐳',
        '0': '𝟎', '1': '𝟏', '2': '𝟐', '3': '𝟑', '4': '𝟒',
        '5': '𝟓', '6': '𝟔', '7': '𝟕', '8': '𝟖', '9': '𝟗'
    }
    result = ""
    for char in text:
        result += stylish_chars.get(char, char)
    return result

def get_verified_emoji_id(fallback: str) -> str:
    for key, val in VERIFIED_EMOJIS.items():
        if val["fallback"] == fallback:
            return val["id"]
    return VERIFIED_EMOJIS["verified"]["id"]

# ============================================================
# EMOJI HELPERS
# ============================================================
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
        
        if ch == PLACEHOLDER:
            eid = random.choice(PRIMARY_EMOJIS)
            entities.append(MessageEntity(
                type="custom_emoji",
                offset=utf16_offset,
                length=ch_len,
                custom_emoji_id=eid
            ))
        elif ch in [v["fallback"] for v in VERIFIED_EMOJIS.values()]:
            for key, val in VERIFIED_EMOJIS.items():
                if val["fallback"] == ch:
                    entities.append(MessageEntity(
                        type="custom_emoji",
                        offset=utf16_offset,
                        length=ch_len,
                        custom_emoji_id=val["id"]
                    ))
                    break
        utf16_offset += ch_len
        i += 1
    
    return entities

def _send_pe(chat_id, text: str, reply_markup=None):
    entities = _build_pe_entities(text)
    return bot.send_message(chat_id, text, entities=entities, reply_markup=reply_markup, parse_mode=None)

def _send_pe_return(chat_id, text: str, reply_markup=None):
    entities = _build_pe_entities(text)
    return bot.send_message(chat_id, text, entities=entities, reply_markup=reply_markup, parse_mode=None)

# ============================================================
# MAKE BUTTONS
# ============================================================
def make_verified_button(text: str, style: str = None, callback: str = None, url: str = None):
    stylish_text_result = stylish_text(text)
    left_verified = random.choice(["✅", "💎", "⭐", "🔥", "❤️", "👍"])
    right_verified = random.choice(["✅", "💎", "⭐", "🔥", "❤️", "👍"])
    final_text = f"{left_verified} {stylish_text_result} {right_verified}"
    
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
    return make_verified_button(text, style="success", callback=callback, url=url)

def make_red_button(text: str, callback: str = None, url: str = None):
    return make_verified_button(text, style="danger", callback=callback, url=url)

def make_blue_button(text: str, callback: str = None, url: str = None):
    return make_verified_button(text, style="primary", callback=callback, url=url)

# ============================================================
# DATA MANAGEMENT
# ============================================================
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
# BOT STATE
# ============================================================
user_data = {}
bot_active = True

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
        notify_owner(f"✅ New User Joined!\n👤 ID: {user_id}\n👾 @{username or 'N/A'}")
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

def get_menu(user_id):
    markup = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    is_admin_user = is_admin(user_id)
    
    if is_admin_user:
        markup.row(
            KeyboardButton("🔴 BOT OFF"),
            KeyboardButton("🟢 BOT ON")
        )
        markup.row(
            KeyboardButton("👑 ADMIN PANEL"),
            KeyboardButton("📊 STATS")
        )
        markup.row(
            KeyboardButton("👥 USERS"),
            KeyboardButton("📥 DATA")
        )
        markup.row(
            KeyboardButton("💳 PRICE"),
            KeyboardButton("🏦 UPI")
        )
        markup.row(
            KeyboardButton("➕ ADD ADMIN"),
            KeyboardButton("📋 CLONE")
        )
        markup.row(
            KeyboardButton("❓ HOW TO GET TOKEN"),
            KeyboardButton("💎 CLONE PRICE")
        )
        markup.row(
            KeyboardButton("📢 BROADCAST"),
            KeyboardButton("📢 ALL BROADCAST")
        )
        markup.row(
            KeyboardButton("➕ ADD BUTTON"),
            KeyboardButton("📋 LIST BUTTONS")
        )
        markup.row(
            KeyboardButton("❌ REMOVE BUTTON"),
            KeyboardButton("")
        )
    else:
        markup.row(KeyboardButton("🔫 BAN ACCOUNT"))
        markup.row(
            KeyboardButton("🆓 FREE TRIAL"),
            KeyboardButton("💎 UNLIMITED")
        )
        markup.row(
            KeyboardButton("❓ HOW TO GET TOKEN"),
            KeyboardButton("📋 CLONE BOT")
        )
    
    # Custom buttons from database
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
        KeyboardButton("❓ HELP"),
        KeyboardButton("ℹ️ ABOUT")
    )
    markup.row(KeyboardButton("📞 SUPPORT"))
    
    return markup

# ============================================================
# ADD BUTTON COMMAND
# ============================================================
@bot.message_handler(commands=['addbutton'])
def add_button_cmd(message):
    if not is_admin(message.from_user.id):
        _send_pe(message.chat.id, f"❌ Unauthorized!")
        return
    
    _send_pe(message.chat.id, f"""
🌟 ═══《 ➕ ADD BUTTON 》═══ 🌟

🌟 Send me the BUTTON NAME:

🌟 Example: HELLO WORLD

🌟 ═══════════════════════ 🌟
""")
    bot.register_next_step_handler(message, get_button_name)

def get_button_name(message):
    if not is_admin(message.from_user.id):
        return
    
    button_name = message.text.strip()
    user_data[message.from_user.id] = {"button_name": button_name}
    
    _send_pe(message.chat.id, f"""
🌟 ═══《 ➕ ADD BUTTON 》═══ 🌟

🌟 Button Name: {button_name}

🌟 Now send me the BUTTON URL/LINK:

🌟 Example: https://t.me/iflexzyan

🌟 ═══════════════════════ 🌟
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
🌟 ═══《 ✅ BUTTON ADDED 》═══ 🌟

🌟 📌 Name: {button_name}
🌟 🔗 URL: {button_url}

🌟 ✅ Button added successfully!

🌟 ═══════════════════════ 🌟
""")
    
    user_data.pop(message.from_user.id, None)

# ============================================================
# LIST BUTTONS COMMAND
# ============================================================
@bot.message_handler(commands=['listbuttons'])
def list_buttons_cmd(message):
    if not is_admin(message.from_user.id):
        _send_pe(message.chat.id, f"❌ Unauthorized!")
        return
    
    buttons = load_buttons()
    if not buttons:
        _send_pe(message.chat.id, f"🌟 No buttons added yet!")
        return
    
    text = f"""
🌟 ═══《 📋 CUSTOM BUTTONS 》═══ 🌟
"""
    for name, data in buttons.items():
        text += f"""
🌟 📌 {name}
🌟 🔗 {data['url']}
🌟 👤 Added by: {data['added_by']}
🌟 ⏰ {data['added_at']}
🌟 ─────────────────────
"""
    
    text += f"""
🌟 ═══════════════════════ 🌟
🌟 Total Buttons: {len(buttons)}
"""
    _send_pe(message.chat.id, text)

# ============================================================
# REMOVE BUTTON COMMAND
# ============================================================
@bot.message_handler(commands=['removebutton'])
def remove_button_cmd(message):
    if not is_admin(message.from_user.id):
        _send_pe(message.chat.id, f"❌ Unauthorized!")
        return
    
    buttons = load_buttons()
    if not buttons:
        _send_pe(message.chat.id, f"🌟 No buttons to remove!")
        return
    
    text = f"""
🌟 ═══《 ❌ REMOVE BUTTON 》═══ 🌟

🌟 Send me the button name to remove:

🌟 Available buttons:
"""
    for name in buttons.keys():
        text += f"🌟 • {name}\n"
    
    text += f"""
🌟 ═══════════════════════ 🌟
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
        _send_pe(message.chat.id, f"✅ Button '{button_name}' removed!")
    else:
        _send_pe(message.chat.id, f"❌ Button '{button_name}' not found!")

# ============================================================
# HANDLE CUSTOM BUTTONS
# ============================================================
@bot.message_handler(func=lambda m: m.text and m.text in [b["name"] for b in load_buttons().values()])
def handle_custom_button(message):
    buttons = load_buttons()
    for name, data in buttons.items():
        if message.text == data["name"]:
            markup = InlineKeyboardMarkup([
                [make_blue_button("OPEN LINK", url=data["url"])],
                [make_red_button("CLOSE", callback="close_button")]
            ])
            _send_pe(message.chat.id, f"""
🌟 ═══《 {name} 》═══ 🌟

🌟 Click below to open:

🌟 ═══════════════════════ 🌟
""", reply_markup=markup)
            break

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
    
    user = register_user(user_id, username, first_name)
    
    if user.get("banned", False):
        _send_pe(message.chat.id, f"❌ You are BANNED from using this bot!")
        return
    
    try:
        bot.send_photo(
            message.chat.id,
            photo="https://iili.io/C8DNTyQ.jpg",
            caption=f"🌟 Welcome to FF BAN BOT!"
        )
    except:
        pass
    
    welcome_text = f"""
🌟 ═══《 🔥 WELCOME TO FF BAN BOT 》═══ 🌟

🌟 👤 User: {first_name}
🌟 🆔 ID: {user_id}
🌟 👾 Username: @{username or 'N/A'}

🌟 ═══════════════════════ 🌟

🌟 🎯 1 FREE TRIAL - Ban 1 Account
🌟 💰 UNLIMITED Access - Rs.{price}

🌟 ═══════════════════════ 🌟

🌟 👨‍💻 Developer: {developer}

🌟 ═══════════════════════ 🌟
"""
    
    markup = get_menu(user_id)
    _send_pe(message.chat.id, welcome_text, reply_markup=markup)

@bot.message_handler(commands=['help'])
def help_cmd(message):
    user_id = message.from_user.id
    markup = get_menu(user_id)
    
    help_text = f"""
🌟 ═══《 ❓ HELP 》═══ 🌟

🌟 How to Use:

🌟 1️⃣ Click BAN ACCOUNT
🌟 2️⃣ Send Access Token
🌟 3️⃣ Account will be banned
🌟 4️⃣ Get Result!

🌟 ═══════════════════ 🌟

🌟 🆓 FREE TRIAL: 1 Ban
🌟 💰 UNLIMITED: Pay & Get

🌟 ═══════════════════ 🌟

🌟 👨‍💻 Developer: @iflexzyan
"""
    _send_pe(message.chat.id, help_text, reply_markup=markup)

# ============================================================
# HOW TO GET TOKEN
# ============================================================
TOKEN_VIDEO_FILE = "token_video.mp4"

@bot.message_handler(commands=['addtokenvideo'])
def add_token_video(message):
    if not is_admin(message.from_user.id):
        _send_pe(message.chat.id, f"❌ Unauthorized!")
        return
    
    _send_pe(message.chat.id, f"📤 Send me the video for 'HOW TO GET TOKEN'")
    bot.register_next_step_handler(message, save_token_video)

def save_token_video(message):
    if message.video:
        file_info = bot.get_file(message.video.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        with open(TOKEN_VIDEO_FILE, 'wb') as f:
            f.write(downloaded_file)
        _send_pe(message.chat.id, f"✅ Video saved successfully!")
    else:
        _send_pe(message.chat.id, f"❌ Please send a video!")

@bot.message_handler(func=lambda m: m.text and "HOW TO GET TOKEN" in m.text)
def how_to_get_token(message):
    if os.path.exists(TOKEN_VIDEO_FILE):
        with open(TOKEN_VIDEO_FILE, 'rb') as f:
            bot.send_video(message.chat.id, f, caption=f"🌟 How to Get Access Token")
    else:
        text = f"""
🌟 ═══《 ❓ HOW TO GET TOKEN 》═══ 🌟

🌟 1️⃣ Open Free Fire Game
🌟 2️⃣ Go to Settings ⚙️
🌟 3️⃣ Click on Account
🌟 4️⃣ Find "Data Access"
🌟 5️⃣ Copy Access Token

🌟 ═══════════════════════ 🌟
"""
        _send_pe(message.chat.id, text)

# ============================================================
# BROADCAST COMMANDS
# ============================================================

@bot.message_handler(commands=['broadcastuser'])
def broadcast_user(message):
    if not is_admin(message.from_user.id):
        _send_pe(message.chat.id, f"❌ Unauthorized!")
        return
    
    parts = message.text.split(maxsplit=2)
    if len(parts) < 3:
        _send_pe(message.chat.id, f"❌ Usage: /broadcastuser user_id message")
        return
    
    try:
        user_id = int(parts[1])
        msg = parts[2]
    except:
        _send_pe(message.chat.id, f"❌ Invalid User ID!")
        return
    
    try:
        bot.send_message(user_id, f"📢 {msg}")
        _send_pe(message.chat.id, f"✅ Message sent to user {user_id}!")
    except Exception as e:
        _send_pe(message.chat.id, f"❌ Failed to send: {str(e)}")

@bot.message_handler(commands=['allbroadcast'])
def all_broadcast(message):
    if not is_admin(message.from_user.id):
        _send_pe(message.chat.id, f"❌ Unauthorized!")
        return
    
    parts = message.text.split(maxsplit=1)
    if len(parts) < 2:
        _send_pe(message.chat.id, f"❌ Usage: /allbroadcast message")
        return
    
    msg = parts[1]
    users = load_users()
    
    if not users:
        _send_pe(message.chat.id, f"❌ No users found!")
        return
    
    sent = 0
    failed = 0
    
    _send_pe(message.chat.id, f"⏳ Sending broadcast to {len(users)} users...")
    
    for user_id in users.keys():
        try:
            bot.send_message(int(user_id), f"📢 {msg}")
            sent += 1
            time.sleep(0.05)
        except:
            failed += 1
    
    _send_pe(message.chat.id, f"""
✅ Broadcast Complete!

🌟 Total Users: {len(users)}
🌟 Sent: {sent}
🌟 Failed: {failed}
""")

@bot.message_handler(func=lambda m: m.text and "BROADCAST" in m.text and "ALL" not in m.text)
def broadcast_btn(message):
    if not is_admin(message.from_user.id):
        _send_pe(message.chat.id, f"❌ Unauthorized!")
        return
    
    _send_pe(message.chat.id, f"""
🌟 ═══《 📢 BROADCAST 》═══ 🌟

🌟 Send message to specific user:

🌟 /broadcastuser user_id message

🌟 Example:
🌟 /broadcastuser 8471373583 Hello!

🌟 ═══════════════════════ 🌟
""")

@bot.message_handler(func=lambda m: m.text and "ALL BROADCAST" in m.text)
def all_broadcast_btn(message):
    if not is_admin(message.from_user.id):
        _send_pe(message.chat.id, f"❌ Unauthorized!")
        return
    
    _send_pe(message.chat.id, f"""
🌟 ═══《 📢 ALL BROADCAST 》═══ 🌟

🌟 Send message to ALL users:

🌟 /allbroadcast message

🌟 Example:
🌟 /allbroadcast Hello everyone!

🌟 ═══════════════════════ 🌟
""")

# ============================================================
# BAN ACCOUNT
# ============================================================

@bot.message_handler(func=lambda m: m.text and "BAN ACCOUNT" in m.text)
def ban_account_start(message):
    user_id = message.from_user.id
    user = get_user(user_id)
    
    if not user or user.get("banned", False):
        _send_pe(message.chat.id, f"❌ You are BANNED!")
        return
    
    if not user.get("unlimited", False):
        uses = user.get("uses", 0)
        if uses >= 1:
            _send_pe(message.chat.id, f"⚠️ Free Trial Used!\n💰 Pay Rs.{load_settings().get('price', 99)} for UNLIMITED")
            send_payment_qr(message.chat.id)
            return
    
    _send_pe(message.chat.id, f"🔑 Send me the Access Token to Ban!")
    bot.register_next_step_handler(message, process_ban_token)

def process_ban_token(message):
    user_id = message.from_user.id
    token = message.text.strip()
    
    if len(token) < 30:
        _send_pe(message.chat.id, f"❌ Invalid Token! Please send correct Access Token.")
        return
    
    msg = _send_pe_return(message.chat.id, f"⏳ Banning Account... Please Wait!")
    
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
🌟 ═══《 ✅ ACCOUNT BANNED 》═══ 🌟

🌟 🎯 ACCOUNT BAN SUCCESSFUL!

🌟 ═══════════════════════ 🌟

🌟 🆔 ID: {account_id}
🌟 👤 NAME: {account_name}
🌟 🔢 UID: {account_uid}

🌟 ═══════════════════════ 🌟

🌟 👨‍💻 Developer: @iflexzyan

🌟 ═══════════════════════ 🌟
"""
            keyboard = [
                [make_green_button("BAN ANOTHER", callback="ban_another")],
                [make_blue_button("GET UNLIMITED", callback="get_unlimited")],
                [make_red_button("SUPPORT", callback="support_contact")]
            ]
            markup = InlineKeyboardMarkup(keyboard)
            _send_pe(message.chat.id, result_text, reply_markup=markup)
            
            notify_owner(f"✅ Account Banned!\n👤 User: {user_id}\n🔢 UID: {account_uid}")
            
        else:
            result_text = f"""
🌟 ═══《 ❌ BAN FAILED 》═══ 🌟

🌟 ACCOUNT NOT BANNED!

🌟 ═══════════════════════ 🌟

🌟 🆔 ID: {account_id}
🌟 👤 NAME: {account_name}
🌟 🔢 UID: {account_uid}
🌟 📌 Status: {status}

🌟 ═══════════════════════ 🌟

🌟 ⚠️ Reasons:
🌟 • Invalid Token
🌟 • Already Banned
🌟 • Server Error

🌟 ═══════════════════════ 🌟

🌟 👨‍💻 Developer: @iflexzyan
"""
            _send_pe(message.chat.id, result_text)
            
    except Exception as e:
        bot.delete_message(message.chat.id, msg.message_id)
        _send_pe(message.chat.id, f"❌ Error: {str(e)}")

# ============================================================
# PAYMENT SYSTEM
# ============================================================

def send_payment_qr(chat_id):
    settings = load_settings()
    upi = settings.get("upi", "vanshx111@naviaxis")
    price = settings.get("price", 99)
    
    qr_url = f"https://api.qrserver.com/v1/create-qr-code/?size=300x300&data=upi://pay?pa={upi}&am={price}&cu=INR"
    
    text = f"""
🌟 ═══《 💰 PAYMENT 》═══ 🌟

🌟 💳 UPI: {upi}
🌟 💰 Amount: Rs.{price}

🌟 ═══════════════════════ 🌟

🌟 📱 Scan QR to Pay

🌟 ═══════════════════════ 🌟
"""
    
    keyboard = [
        [make_green_button("I HAVE PAID", callback=f"paid_{chat_id}")],
        [make_blue_button("SUPPORT", url="https://t.me/iflexzyan")],
        [make_red_button("CANCEL", callback="cancel_payment")]
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
    
    _send_pe(chat_id, f"📸 Send me the Payment Screenshot!")
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
        
        _send_pe(message.chat.id, f"✅ Screenshot Received!\n⏳ Waiting for Admin Approval.")
        
        admin_text = f"""
🌟 ═══《 💰 NEW PAYMENT 》═══ 🌟

🌟 👤 User: {message.from_user.first_name}
🌟 🆔 ID: {user_id}
🌟 👾 @{message.from_user.username or 'N/A'}

🌟 ═══════════════════════ 🌟

🌟 📌 Use: /approve {user_id}
🌟 📌 Use: /disapprove {user_id}

🌟 ═══════════════════════ 🌟
"""
        for admin in ADMIN_IDS:
            try:
                bot.send_photo(admin, photo=file_id, caption=admin_text)
            except:
                bot.send_message(admin, admin_text)
    else:
        _send_pe(message.chat.id, f"❌ Please send a PHOTO as screenshot!")

# ============================================================
# FREE TRIAL & UNLIMITED
# ============================================================

@bot.message_handler(func=lambda m: m.text and "FREE TRIAL" in m.text)
def free_trial_cmd(message):
    user_id = message.from_user.id
    user = get_user(user_id)
    
    if not user:
        _send_pe(message.chat.id, f"❌ Please /start first!")
        return
    
    if user.get("unlimited", False):
        _send_pe(message.chat.id, f"✅ You already have UNLIMITED access!")
        return
    
    uses = user.get("uses", 0)
    if uses >= 1:
        _send_pe(message.chat.id, f"⚠️ Free Trial Already Used!\n💰 Pay Rs.{load_settings().get('price', 99)} for UNLIMITED")
        send_payment_qr(message.chat.id)
        return
    
    _send_pe(message.chat.id, f"🆓 FREE TRIAL ACTIVATED!\n🔫 Send Access Token to Ban!")

@bot.message_handler(func=lambda m: m.text and "UNLIMITED" in m.text)
def unlimited_cmd(message):
    user_id = message.from_user.id
    user = get_user(user_id)
    
    if user and user.get("unlimited", False):
        _send_pe(message.chat.id, f"✅ You already have UNLIMITED access!")
        return
    
    send_payment_qr(message.chat.id)

# ============================================================
# SUPPORT
# ============================================================

@bot.message_handler(func=lambda m: m.text and "SUPPORT" in m.text)
def support_cmd(message):
    settings = load_settings()
    support = settings.get("support", "@iflexzyan")
    developer = settings.get("developer", "@iflexzyan")
    
    text = f"""
🌟 ═══《 📞 SUPPORT 》═══ 🌟

🌟 👨‍💻 Developer: {developer}

🌟 ═══════════════════════ 🌟

🌟 For any issues, contact:
🌟 📱 Telegram: {support}

🌟 ═══════════════════════ 🌟
"""
    markup = InlineKeyboardMarkup([
        [make_blue_button("CONTACT SUPPORT", url=f"https://t.me/{support.replace('@', '')}")]
    ])
    _send_pe(message.chat.id, text, reply_markup=markup)

@bot.message_handler(func=lambda m: m.text and "ABOUT" in m.text)
def about_cmd(message):
    user_id = message.from_user.id
    markup = get_menu(user_id)
    settings = load_settings()
    developer = settings.get("developer", "@iflexzyan")
    
    text = f"""
🌟 ═══《 ℹ️ ABOUT 》═══ 🌟

🌟 🤖 FF BAN BOT

🌟 🔫 Ban Free Fire Accounts
🌟 💰 Pay & Get Unlimited Access
🌟 🆓 1 Free Trial

🌟 ═══════════════════════ 🌟

🌟 👨‍💻 Developer: {developer}

🌟 ═══════════════════════ 🌟
"""
    _send_pe(message.chat.id, text, reply_markup=markup)

# ============================================================
# ADMIN COMMANDS
# ============================================================

@bot.message_handler(commands=['approve'])
def approve_user(message):
    if not is_admin(message.from_user.id):
        _send_pe(message.chat.id, f"❌ Unauthorized!")
        return
    
    parts = message.text.split()
    if len(parts) < 2:
        _send_pe(message.chat.id, f"❌ Usage: /approve user_id")
        return
    
    try:
        user_id = int(parts[1])
    except:
        _send_pe(message.chat.id, f"❌ Invalid User ID!")
        return
    
    update_user(user_id, "unlimited", True)
    update_user(user_id, "uses", 0)
    
    pending = load_pending()
    if str(user_id) in pending:
        del pending[str(user_id)]
        save_pending(pending)
    
    _send_pe(message.chat.id, f"✅ User {user_id} approved for UNLIMITED access!")
    
    try:
        bot.send_message(user_id, f"✅ Congratulations! You now have UNLIMITED access! 🎉")
    except:
        pass

@bot.message_handler(commands=['disapprove'])
def disapprove_user(message):
    if not is_admin(message.from_user.id):
        _send_pe(message.chat.id, f"❌ Unauthorized!")
        return
    
    parts = message.text.split()
    if len(parts) < 2:
        _send_pe(message.chat.id, f"❌ Usage: /disapprove user_id")
        return
    
    try:
        user_id = int(parts[1])
    except:
        _send_pe(message.chat.id, f"❌ Invalid User ID!")
        return
    
    pending = load_pending()
    if str(user_id) in pending:
        del pending[str(user_id)]
        save_pending(pending)
    
    _send_pe(message.chat.id, f"❌ User {user_id} disapproved!")
    
    try:
        bot.send_message(user_id, f"❌ Your payment was not approved. Please contact support.")
    except:
        pass

@bot.message_handler(commands=['ban'])
def ban_user_cmd(message):
    if not is_admin(message.from_user.id):
        _send_pe(message.chat.id, f"❌ Unauthorized!")
        return
    
    parts = message.text.split()
    if len(parts) < 2:
        _send_pe(message.chat.id, f"❌ Usage: /ban user_id")
        return
    
    try:
        user_id = int(parts[1])
    except:
        _send_pe(message.chat.id, f"❌ Invalid User ID!")
        return
    
    update_user(user_id, "banned", True)
    _send_pe(message.chat.id, f"✅ User {user_id} BANNED!")
    
    try:
        bot.send_message(user_id, f"❌ You have been BANNED from using this bot!")
    except:
        pass

@bot.message_handler(commands=['unban'])
def unban_user_cmd(message):
    if not is_admin(message.from_user.id):
        _send_pe(message.chat.id, f"❌ Unauthorized!")
        return
    
    parts = message.text.split()
    if len(parts) < 2:
        _send_pe(message.chat.id, f"❌ Usage: /unban user_id")
        return
    
    try:
        user_id = int(parts[1])
    except:
        _send_pe(message.chat.id, f"❌ Invalid User ID!")
        return
    
    update_user(user_id, "banned", False)
    _send_pe(message.chat.id, f"✅ User {user_id} UNBANNED!")

@bot.message_handler(commands=['users'])
def users_cmd(message):
    if not is_admin(message.from_user.id):
        _send_pe(message.chat.id, f"❌ Unauthorized!")
        return
    
    users = load_users()
    total = len(users)
    unlimited = sum(1 for u in users.values() if u.get("unlimited", False))
    banned = sum(1 for u in users.values() if u.get("banned", False))
    
    text = f"""
🌟 ═══《 👥 USERS 》═══ 🌟

🌟 📊 Total Users: {total}
🌟 💎 Unlimited: {unlimited}
🌟 🚫 Banned: {banned}

🌟 ═══════════════════════ 🌟

🌟 👥 User List:
"""
    
    for uid, data in users.items():
        user_status = "✅" if data.get("unlimited", False) else "🆓"
        banned_status = "🚫" if data.get("banned", False) else "✅"
        text += f"🌟 • {data.get('name', 'Unknown')} (@{data.get('username', 'N/A')}) - {user_status} {banned_status}\n"
    
    _send_pe(message.chat.id, text)

@bot.message_handler(commands=['data'])
def data_cmd(message):
    if not is_admin(message.from_user.id):
        _send_pe(message.chat.id, f"❌ Unauthorized!")
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
        bot.send_document(message.chat.id, f, caption=f"🌟 📥 Bot Data Export")

@bot.message_handler(commands=['price'])
def price_cmd(message):
    if not is_admin(message.from_user.id):
        _send_pe(message.chat.id, f"❌ Unauthorized!")
        return
    
    parts = message.text.split()
    if len(parts) < 2:
        settings = load_settings()
        _send_pe(message.chat.id, f"🌟 💰 Current Price: Rs.{settings.get('price', 99)}\n🌟 📌 Use: /price <amount>")
        return
    
    try:
        price = int(parts[1])
        settings = load_settings()
        settings["price"] = price
        save_settings(settings)
        _send_pe(message.chat.id, f"✅ Price updated to Rs.{price}!")
    except:
        _send_pe(message.chat.id, f"❌ Invalid amount!")

@bot.message_handler(commands=['upi'])
def upi_cmd(message):
    if not is_admin(message.from_user.id):
        _send_pe(message.chat.id, f"❌ Unauthorized!")
        return
    
    parts = message.text.split()
    if len(parts) < 2:
        settings = load_settings()
        _send_pe(message.chat.id, f"🌟 🏦 Current UPI: {settings.get('upi', 'vanshx111@naviaxis')}\n🌟 📌 Use: /upi <new_upi>")
        return
    
    upi = parts[1]
    settings = load_settings()
    settings["upi"] = upi
    save_settings(settings)
    _send_pe(message.chat.id, f"✅ UPI updated to: {upi}!")

@bot.message_handler(commands=['developer'])
def developer_cmd(message):
    if not is_admin(message.from_user.id):
        _send_pe(message.chat.id, f"❌ Unauthorized!")
        return
    
    parts = message.text.split()
    if len(parts) < 2:
        settings = load_settings()
        _send_pe(message.chat.id, f"🌟 👨‍💻 Current Developer: {settings.get('developer', '@iflexzyan')}\n🌟 📌 Use: /developer <new_developer>")
        return
    
    developer = parts[1]
    settings = load_settings()
    settings["developer"] = developer
    settings["support"] = developer
    save_settings(settings)
    _send_pe(message.chat.id, f"✅ Developer updated to: {developer}!")

@bot.message_handler(commands=['addadmin'])
def add_admin_cmd(message):
    if not is_admin(message.from_user.id):
        _send_pe(message.chat.id, f"❌ Unauthorized!")
        return
    
    parts = message.text.split()
    if len(parts) < 2:
        _send_pe(message.chat.id, f"❌ Usage: /addadmin user_id")
        return
    
    try:
        user_id = int(parts[1])
        if user_id not in ADMIN_IDS:
            ADMIN_IDS.append(user_id)
            _send_pe(message.chat.id, f"✅ User {user_id} added as Admin!")
        else:
            _send_pe(message.chat.id, f"⚠️ User {user_id} is already Admin!")
    except:
        _send_pe(message.chat.id, f"❌ Invalid User ID!")

@bot.message_handler(commands=['prcclone'])
def clone_price_cmd(message):
    if not is_admin(message.from_user.id):
        _send_pe(message.chat.id, f"❌ Unauthorized!")
        return
    
    parts = message.text.split()
    if len(parts) < 2:
        settings = load_settings()
        _send_pe(message.chat.id, f"🌟 💰 Clone Price: Rs.{settings.get('clone_price', 199)}\n🌟 📌 Use: /prcclone <amount>")
        return
    
    try:
        price = int(parts[1])
        settings = load_settings()
        settings["clone_price"] = price
        save_settings(settings)
        _send_pe(message.chat.id, f"✅ Clone Price updated to Rs.{price}!")
    except:
        _send_pe(message.chat.id, f"❌ Invalid amount!")

# ============================================================
# CLONE BOT SYSTEM
# ============================================================

@bot.message_handler(func=lambda m: m.text and "CLONE BOT" in m.text)
def clone_user_cmd(message):
    user_id = message.from_user.id
    user = get_user(user_id)
    
    if not user or user.get("banned", False):
        _send_pe(message.chat.id, f"❌ You are BANNED!")
        return
    
    settings = load_settings()
    clone_price = settings.get("clone_price", 199)
    
    if not user.get("unlimited", False):
        uses = user.get("uses", 0)
        if uses >= 1:
            _send_pe(message.chat.id, f"⚠️ Clone Bot costs Rs.{clone_price}\n💰 Pay to get your own bot!")
            send_clone_payment_qr(message.chat.id)
            return
    
    text = f"""
🌟 ═══《 📋 CLONE BOT 》═══ 🌟

🌟 🤖 Enter new bot token to clone:

🌟 ═══════════════════════ 🌟

🌟 📌 Steps:
🌟 1. Create new bot from @BotFather
🌟 2. Copy token
🌟 3. Send token here

🌟 ═══════════════════════ 🌟
"""
    _send_pe(message.chat.id, text)
    bot.register_next_step_handler(message, process_clone_user_token)

def send_clone_payment_qr(chat_id):
    settings = load_settings()
    upi = settings.get("upi", "vanshx111@naviaxis")
    clone_price = settings.get("clone_price", 199)
    
    qr_url = f"https://api.qrserver.com/v1/create-qr-code/?size=300x300&data=upi://pay?pa={upi}&am={clone_price}&cu=INR"
    
    text = f"""
🌟 ═══《 💰 CLONE PAYMENT 》═══ 🌟

🌟 💳 UPI: {upi}
🌟 💰 Amount: Rs.{clone_price}

🌟 ═══════════════════════ 🌟

🌟 📱 Scan QR to Pay

🌟 ═══════════════════════ 🌟
"""
    
    keyboard = [
        [make_green_button("I HAVE PAID", callback=f"clone_paid_{chat_id}")],
        [make_blue_button("SUPPORT", url="https://t.me/iflexzyan")]
    ]
    markup = InlineKeyboardMarkup(keyboard)
    
    try:
        bot.send_photo(chat_id, photo=qr_url, caption=text, reply_markup=markup)
    except:
        _send_pe(chat_id, text, reply_markup=markup)

def process_clone_user_token(message):
    user_id = message.from_user.id
    token = message.text.strip()
    
    if not token or ':' not in token:
        _send_pe(message.chat.id, f"❌ Invalid Bot Token!")
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
        
        result_text = f"""
🌟 ═══《 ✅ BOT CLONED 》═══ 🌟

🌟 🤖 Bot Name: {bot_info.first_name}
🌟 👾 Username: @{bot_info.username}
🌟 🆔 Bot ID: {bot_info.id}

🌟 ═══════════════════════ 🌟

🌟 👨‍💻 Developer: {clone_data['developer']}
🌟 💰 Price: Rs.{clone_data['price']}
🌟 🏦 UPI: {clone_data['upi']}

🌟 ═══════════════════════ 🌟

🌟 📌 Clone bot is ready!
🌟 📌 Use /developer to change name

🌟 ═══════════════════════ 🌟
"""
        _send_pe(message.chat.id, result_text)
        
        try:
            test_bot.send_message(
                user_id,
                f"✅ Welcome to your cloned FF BAN BOT!\n\n👨‍💻 Developer: {clone_data['developer']}\n💰 Price: Rs.{clone_data['price']}\n🏦 UPI: {clone_data['upi']}\n\n📌 Use /start to begin!"
            )
        except:
            pass
        
        notify_owner(f"✅ Bot Cloned!\n🤖 {bot_info.first_name}\n👾 @{bot_info.username}\n👤 By: {user_id}")
        
    except Exception as e:
        _send_pe(message.chat.id, f"❌ Error: {str(e)}\n\n📌 Make sure token is correct!")

@bot.message_handler(commands=['clone'])
def clone_admin_cmd(message):
    if not is_admin(message.from_user.id):
        _send_pe(message.chat.id, f"❌ Unauthorized!")
        return
    
    text = f"""
🌟 ═══《 📋 CLONE BOT 》═══ 🌟

🌟 🤖 Enter new bot token to clone:

🌟 ═══════════════════════ 🌟

🌟 📌 Steps:
🌟 1. Create new bot from @BotFather
🌟 2. Copy token
🌟 3. Send token here

🌟 ═══════════════════════ 🌟
"""
    _send_pe(message.chat.id, text)
    bot.register_next_step_handler(message, process_clone_admin_token)

def process_clone_admin_token(message):
    if not is_admin(message.from_user.id):
        return
    
    token = message.text.strip()
    
    if not token or ':' not in token:
        _send_pe(message.chat.id, f"❌ Invalid Bot Token!")
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
        
        result_text = f"""
🌟 ═══《 ✅ BOT CLONED 》═══ 🌟

🌟 🤖 Bot Name: {bot_info.first_name}
🌟 👾 Username: @{bot_info.username}
🌟 🆔 Bot ID: {bot_info.id}

🌟 ═══════════════════════ 🌟

🌟 👨‍💻 Developer: {clone_data['developer']}
🌟 💰 Price: Rs.{clone_data['price']}
🌟 🏦 UPI: {clone_data['upi']}

🌟 ═══════════════════════ 🌟
"""
        _send_pe(message.chat.id, result_text)
        
        notify_owner(f"✅ Bot Cloned by Admin!\n🤖 {bot_info.first_name}\n👾 @{bot_info.username}")
        
    except Exception as e:
        _send_pe(message.chat.id, f"❌ Error: {str(e)}")

# ============================================================
# CALLBACK HANDLERS
# ============================================================

@bot.callback_query_handler(func=lambda c: c.data == "ban_another")
def ban_another_callback(call):
    user_id = call.from_user.id
    user = get_user(user_id)
    
    if not user or user.get("banned", False):
        _send_pe(call.message.chat.id, f"❌ You are BANNED!")
        return
    
    if not user.get("unlimited", False):
        uses = user.get("uses", 0)
        if uses >= 1:
            _send_pe(call.message.chat.id, f"⚠️ Free Trial Used!\n💰 Pay Rs.{load_settings().get('price', 99)} for UNLIMITED")
            send_payment_qr(call.message.chat.id)
            bot.answer_callback_query(call.id)
            return
    
    _send_pe(call.message.chat.id, f"🔑 Send me the Access Token to Ban!")
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
🌟 ═══《 📞 SUPPORT 》═══ 🌟

🌟 👨‍💻 Developer: {settings.get('developer', '@iflexzyan')}

🌟 ═══════════════════════ 🌟

🌟 📩 Contact: {support}

🌟 ═══════════════════════ 🌟
"""
    markup = InlineKeyboardMarkup([
        [make_blue_button("CONTACT", url=f"https://t.me/{support.replace('@', '')}")]
    ])
    _send_pe(call.message.chat.id, text, reply_markup=markup)
    bot.answer_callback_query(call.id)

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
    
    _send_pe(chat_id, f"📸 Send me the Clone Payment Screenshot!")
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
        
        _send_pe(message.chat.id, f"✅ Screenshot Received!\n⏳ Waiting for Admin Approval.")
        
        admin_text = f"""
🌟 ═══《 💰 CLONE PAYMENT 》═══ 🌟

🌟 👤 User: {message.from_user.first_name}
🌟 🆔 ID: {user_id}
🌟 👾 @{message.from_user.username or 'N/A'}
🌟 📌 Type: CLONE BOT

🌟 ═══════════════════════ 🌟

🌟 📌 Use: /approveclone {user_id}
🌟 📌 Use: /disapproveclone {user_id}

🌟 ═══════════════════════ 🌟
"""
        for admin in ADMIN_IDS:
            try:
                bot.send_photo(admin, photo=file_id, caption=admin_text)
            except:
                bot.send_message(admin, admin_text)
    else:
        _send_pe(message.chat.id, f"❌ Please send a PHOTO!")

@bot.message_handler(commands=['approveclone'])
def approve_clone(message):
    if not is_admin(message.from_user.id):
        _send_pe(message.chat.id, f"❌ Unauthorized!")
        return
    
    parts = message.text.split()
    if len(parts) < 2:
        _send_pe(message.chat.id, f"❌ Usage: /approveclone user_id")
        return
    
    try:
        user_id = int(parts[1])
    except:
        _send_pe(message.chat.id, f"❌ Invalid User ID!")
        return
    
    pending = load_pending()
    if str(user_id) in pending:
        del pending[str(user_id)]
        save_pending(pending)
    
    _send_pe(message.chat.id, f"✅ User {user_id} clone payment approved!\n📌 Now they can use /clone")
    
    try:
        bot.send_message(user_id, f"✅ Clone Payment Approved!\n📌 Use /clone to get your bot!")
    except:
        pass

# ============================================================
# BOT ON/OFF
# ============================================================

@bot.message_handler(func=lambda m: m.text and "BOT ON" in m.text)
def bot_on_cmd(message):
    if not is_admin(message.from_user.id):
        _send_pe(message.chat.id, f"❌ Unauthorized!")
        return
    
    global bot_active
    bot_active = True
    _send_pe(message.chat.id, f"✅ 🟢 Bot is now ONLINE!")

@bot.message_handler(func=lambda m: m.text and "BOT OFF" in m.text)
def bot_off_cmd(message):
    if not is_admin(message.from_user.id):
        _send_pe(message.chat.id, f"❌ Unauthorized!")
        return
    
    global bot_active
    bot_active = False
    _send_pe(message.chat.id, f"✅ 🔴 Bot is now OFFLINE!")

# ============================================================
# STATS & ADMIN PANEL
# ============================================================

@bot.message_handler(func=lambda m: m.text and "STATS" in m.text)
def stats_cmd(message):
    if not is_admin(message.from_user.id):
        _send_pe(message.chat.id, f"❌ Unauthorized!")
        return
    
    users = load_users()
    orders = load_orders()
    pending = load_pending()
    settings = load_settings()
    buttons = load_buttons()
    
    text = f"""
🌟 ═══《 📊 STATS 》═══ 🌟

🌟 👥 Total Users: {len(users)}
🌟 🔫 Total Bans: {len(orders)}
🌟 💰 Pending Payments: {len(pending)}
🌟 💎 Unlimited: {sum(1 for u in users.values() if u.get('unlimited', False))}
🌟 📋 Custom Buttons: {len(buttons)}

🌟 ═══════════════════════ 🌟

🌟 💳 Price: Rs.{settings.get('price', 99)}
🌟 🏦 UPI: {settings.get('upi', 'vanshx111@naviaxis')}
🌟 👨‍💻 Developer: {settings.get('developer', '@iflexzyan')}

🌟 ═══════════════════════ 🌟
"""
    _send_pe(message.chat.id, text)

@bot.message_handler(func=lambda m: m.text and "ADMIN PANEL" in m.text)
def admin_panel_cmd(message):
    if not is_admin(message.from_user.id):
        _send_pe(message.chat.id, f"❌ Unauthorized!")
        return
    
    text = f"""
🌟 ═══《 👑 ADMIN PANEL 》═══ 🌟

🌟 📌 Commands:

🌟 /approve user_id - Approve payment
🌟 /disapprove user_id - Reject payment
🌟 /ban user_id - Ban user
🌟 /unban user_id - Unban user
🌟 /users - Show all users
🌟 /data - Download all data
🌟 /price <amount> - Change price
🌟 /upi <upi> - Change UPI
🌟 /developer <name> - Change developer
🌟 /addadmin user_id - Add admin
🌟 /clone - Clone bot (Admin)
🌟 /prcclone <amount> - Clone price
🌟 /approveclone user_id - Approve clone
🌟 /disapproveclone user_id - Reject clone
🌟 /broadcastuser user_id msg - Send to user
🌟 /allbroadcast msg - Send to all users
🌟 /addbutton - Add custom button
🌟 /listbuttons - List all buttons
🌟 /removebutton - Remove button
🌟 /addtokenvideo - Add token video

🌟 ═══════════════════════ 🌟
"""
    _send_pe(message.chat.id, text)

# ============================================================
# HELP COMMAND
# ============================================================

@bot.message_handler(func=lambda m: m.text and "HELP" in m.text)
def help_menu_cmd(message):
    user_id = message.from_user.id
    markup = get_menu(user_id)
    
    text = f"""
🌟 ═══《 ❓ HELP 》═══ 🌟

🌟 FF BAN BOT - Complete Guide

🌟 ═══════════════════════ 🌟

🌟 📌 Basic Commands:
🌟 /start - Start the bot
🌟 /help - This menu

🌟 ═══════════════════════ 🌟

🌟 🔫 Ban Account:
🌟 1. Click BAN ACCOUNT
🌟 2. Send Access Token
🌟 3. Account gets banned!

🌟 ═══════════════════════ 🌟

🌟 🆓 Free Trial:
🌟 1 FREE ban for new users
🌟 After that, pay for UNLIMITED

🌟 ═══════════════════════ 🌟

🌟 💰 Unlimited:
🌟 Pay once, get unlimited bans
🌟 Price: Rs.{load_settings().get('price', 99)}

🌟 ═══════════════════════ 🌟

🌟 👨‍💻 Developer: @iflexzyan
"""
    _send_pe(message.chat.id, text, reply_markup=markup)

@bot.callback_query_handler(func=lambda c: c.data == "close_button")
def close_button_callback(call):
    try:
        bot.delete_message(call.message.chat.id, call.message.message_id)
    except:
        pass
    bot.answer_callback_query(call.id)

# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":
    print("✅ FF BAN BOT Started!")
    print(f"✅ Owner ID: {OWNER_ID}")
    print(f"✅ Total Users: {len(load_users())}")
    print(f"✅ Total Buttons: {len(load_buttons())}")
    
    try:
        bot.remove_webhook()
        print("✅ Webhook removed!")
    except:
        pass
    
    bot.infinity_polling()