import os
import json
import time
import random
import requests
from datetime import datetime
from flask import Flask, request
from telebot import TeleBot, types
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton, MessageEntity

# ============================================================
# ENVIRONMENT VARIABLES
# ============================================================
BOT_TOKEN = os.environ.get("BOT_TOKEN")
OWNER_ID = int(os.environ.get("OWNER_ID", "8471373583"))
ADMIN_IDS = [OWNER_ID]
PORT = int(os.environ.get("PORT", 10000))

if not BOT_TOKEN:
    print("❌ ERROR: BOT_TOKEN not set!")
    exit(1)

bot = TeleBot(BOT_TOKEN, threaded=False)
app = Flask(__name__)

# ============================================================
# FILES & DATA
# ============================================================
USERS_FILE = "users.json"
ORDERS_FILE = "orders.json"
PENDING_FILE = "pending.json"
SETTINGS_FILE = "settings.json"

bot_active = True

# ============================================================
# PREMIUM EMOJIS
# ============================================================
PREMIUM_EMOJIS = {
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

# ============================================================
# STYLISH CHARACTERS
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
# ALL 22 USERS DATA
# ============================================================
def load_users():
    if os.path.exists(USERS_FILE):
        try:
            with open(USERS_FILE, "r") as f:
                return json.load(f)
        except:
            pass
    
    users = {
        "8586849798": {"id": 8586849798, "username": "Ffaccsellerx", "name": "FF SELLER", "joined": "2026-07-31T05:18:43.493579", "uses": 0, "unlimited": True, "banned": False},
        "8908882066": {"id": 8908882066, "username": None, "name": "Dice", "joined": "2026-07-31T05:30:04.435718", "uses": 0, "unlimited": False, "banned": False},
        "8471373583": {"id": 8471373583, "username": "iflexzyan", "name": "ZYAN", "joined": "2026-07-31T05:30:31.611686", "uses": 0, "unlimited": False, "banned": False},
        "6729963447": {"id": 6729963447, "username": "ZIXU_NXT", "name": "BUNNY !!!", "joined": "2026-07-31T05:31:09.765285", "uses": 0, "unlimited": False, "banned": False},
        "8955229317": {"id": 8955229317, "username": "LEGENDxFIRE", "name": "LEGEND X FIRE", "joined": "2026-07-31T05:39:01.873843", "uses": 0, "unlimited": True, "banned": False},
        "7977493987": {"id": 7977493987, "username": "Havkerbabaybaba", "name": "Bhai on top", "joined": "2026-07-31T05:39:30.486969", "uses": 1, "unlimited": True, "banned": False},
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
        "ban_price": 29,
        "ban_check_price": 0,
        "revoke_price": 0,
        "eat_token_price": 0,
        "upi": "vanshx111@naviaxis",
        "free_trial": True,
        "bot_name": "FF BAN BOT",
        "developer": "@iflexzyan",
        "support": "@iflexzyan",
        "welcome_image": "https://iili.io/C8DNTyQ.jpg",
        "token_text": "1. Open Free Fire\n2. Go to Settings\n3. Click Account\n4. Find Data Access\n5. Copy Token"
    }
    data = load_data(SETTINGS_FILE)
    for key, val in default.items():
        if key not in data:
            data[key] = val
    return data

def save_settings(settings):
    save_data(SETTINGS_FILE, settings)

# ============================================================
# PREMIUM EMOJI + STYLISH HELPERS
# ============================================================
def get_premium_id(name):
    if name in PREMIUM_EMOJIS:
        return PREMIUM_EMOJIS[name]["id"]
    return None

def get_premium_fallback(name):
    if name in PREMIUM_EMOJIS:
        return PREMIUM_EMOJIS[name]["fallback"]
    return ""

def get_random_premium():
    return random.choice(list(PREMIUM_EMOJIS.keys()))

def build_entities_and_text(text):
    lines = text.split('\n')
    result_lines = []
    entities = []
    offset = 0
    
    for line in lines:
        if line.strip():
            emoji_name = get_random_premium()
            emoji_data = PREMIUM_EMOJIS[emoji_name]
            fallback = emoji_data["fallback"]
            new_line = f"{fallback} {line}"
            result_lines.append(new_line)
            entities.append(MessageEntity(
                type="custom_emoji",
                offset=offset,
                length=1,
                custom_emoji_id=emoji_data["id"]
            ))
            offset += len(new_line) + 1
        else:
            result_lines.append(line)
            offset += len(line) + 1
    
    return '\n'.join(result_lines), entities

def send_pe(chat_id, text, reply_markup=None):
    processed_text, entities = build_entities_and_text(text)
    try:
        return bot.send_message(
            chat_id,
            processed_text,
            entities=entities,
            reply_markup=reply_markup,
            parse_mode=None
        )
    except Exception as e:
        print(f"Send PE error: {e}")
        return bot.send_message(chat_id, text, reply_markup=reply_markup)

# ============================================================
# COLORFUL BUTTONS
# ============================================================
def make_green_button(text: str, callback: str = None, url: str = None):
    final_text = stylish_text(text)
    emoji_name = get_random_premium()
    fallback = get_premium_fallback(emoji_name)
    final_text = f"{fallback} {final_text} {fallback}"
    try:
        if callback:
            return InlineKeyboardButton(text=final_text, style="success", callback_data=callback)
        elif url:
            return InlineKeyboardButton(text=final_text, style="success", url=url)
        else:
            return InlineKeyboardButton(text=final_text, style="success")
    except:
        if callback:
            return InlineKeyboardButton(text=final_text, callback_data=callback)
        elif url:
            return InlineKeyboardButton(text=final_text, url=url)
        else:
            return InlineKeyboardButton(text=final_text)

def make_red_button(text: str, callback: str = None, url: str = None):
    final_text = stylish_text(text)
    emoji_name = get_random_premium()
    fallback = get_premium_fallback(emoji_name)
    final_text = f"{fallback} {final_text} {fallback}"
    try:
        if callback:
            return InlineKeyboardButton(text=final_text, style="danger", callback_data=callback)
        elif url:
            return InlineKeyboardButton(text=final_text, style="danger", url=url)
        else:
            return InlineKeyboardButton(text=final_text, style="danger")
    except:
        if callback:
            return InlineKeyboardButton(text=final_text, callback_data=callback)
        elif url:
            return InlineKeyboardButton(text=final_text, url=url)
        else:
            return InlineKeyboardButton(text=final_text)

def make_blue_button(text: str, callback: str = None, url: str = None):
    final_text = stylish_text(text)
    emoji_name = get_random_premium()
    fallback = get_premium_fallback(emoji_name)
    final_text = f"{fallback} {final_text} {fallback}"
    try:
        if callback:
            return InlineKeyboardButton(text=final_text, style="primary", callback_data=callback)
        elif url:
            return InlineKeyboardButton(text=final_text, style="primary", url=url)
        else:
            return InlineKeyboardButton(text=final_text, style="primary")
    except:
        if callback:
            return InlineKeyboardButton(text=final_text, callback_data=callback)
        elif url:
            return InlineKeyboardButton(text=final_text, url=url)
        else:
            return InlineKeyboardButton(text=final_text)

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
        send_pe(OWNER_ID, f"✅ New User Joined!\n👤 ID: {user_id}\n👾 @{username or 'N/A'}")
    return users[str(user_id)]

def get_user(user_id):
    users = load_users()
    return users.get(str(user_id))

def update_user(user_id, key, value):
    users = load_users()
    if str(user_id) in users:
        users[str(user_id)][key] = value
        save_users(users)

def get_price(feature):
    settings = load_settings()
    prices = {
        "ban": settings.get("ban_price", 29),
        "ban_check": settings.get("ban_check_price", 0),
        "revoke": settings.get("revoke_price", 0),
        "eat_token": settings.get("eat_token_price", 0),
    }
    return prices.get(feature, 0)

def use_free_trial(user_id):
    user = get_user(user_id)
    if user and not user.get("unlimited", False):
        uses = user.get("uses", 0) + 1
        update_user(user_id, "uses", uses)
        return True
    return False

# ============================================================
# USER MENU
# ============================================================
def get_user_menu(user_id):
    markup = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    markup.row(KeyboardButton(stylish_text("BAN ACCOUNT")))
    markup.row(KeyboardButton(stylish_text("CHECK BAN INFO")))
    markup.row(KeyboardButton(stylish_text("REVOKE TOKEN")))
    markup.row(KeyboardButton(stylish_text("EAT TO TOKEN")))
    markup.row(KeyboardButton(stylish_text("FREE TRIAL")), KeyboardButton(stylish_text("UNLIMITED")))
    markup.row(KeyboardButton(stylish_text("HOW TO GET TOKEN")), KeyboardButton(stylish_text("SUPPORT")))
    markup.row(KeyboardButton(stylish_text("HELP")), KeyboardButton(stylish_text("ABOUT")))
    return markup

# ============================================================
# ADMIN MENU
# ============================================================
def get_admin_menu(user_id):
    markup = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    markup.row(KeyboardButton(stylish_text("BOT OFF")), KeyboardButton(stylish_text("BOT ON")))
    markup.row(KeyboardButton(stylish_text("ADMIN PANEL")), KeyboardButton(stylish_text("STATS")))
    markup.row(KeyboardButton(stylish_text("USERS")), KeyboardButton(stylish_text("DATA")))
    markup.row(KeyboardButton(stylish_text("CHECK ALL")), KeyboardButton(stylish_text("TOTAL ADMINS")))
    markup.row(KeyboardButton(stylish_text("BAN PRICE")), KeyboardButton(stylish_text("CHECK PRICE")))
    markup.row(KeyboardButton(stylish_text("REVOKE PRICE")), KeyboardButton(stylish_text("EAT PRICE")))
    markup.row(KeyboardButton(stylish_text("UPI")), KeyboardButton(stylish_text("ADD ADMIN")))
    markup.row(KeyboardButton(stylish_text("ALL COMMANDS")), KeyboardButton(stylish_text("HOW TO GET TOKEN")))
    markup.row(KeyboardButton(stylish_text("BROADCAST")), KeyboardButton(stylish_text("ALL BROADCAST")))
    markup.row(KeyboardButton(stylish_text("SET WELCOME IMAGE")), KeyboardButton(stylish_text("SET TOKEN TEXT")))
    markup.row(KeyboardButton(stylish_text("ADD TOKEN VIDEO")), KeyboardButton(stylish_text("")))
    return markup

# ============================================================
# API FUNCTIONS - FIXED
# ============================================================

def eat_to_token(eat_token):
    try:
        url = f"https://access.killersharmabot.online/access?access_token={eat_token}"
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            token = data.get("access_token") or data.get("token")
            if token:
                return token
        return None
    except:
        return None

def revoke_token(access_token):
    try:
        url = f"https://crownxrevoker73.vercel.app/revoke?access_token={access_token}"
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            return data.get("success", False)
        return False
    except:
        return False

def check_ban_info(uid):
    """Check ban info with proper error handling"""
    try:
        url = f"https://crownx-premium-bancheck.vercel.app/baninfo?uid={uid}"
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            if data and 'account_id' in data:
                return data
        return None
    except requests.exceptions.Timeout:
        print(f"Timeout for UID: {uid}")
        return None
    except requests.exceptions.ConnectionError:
        print(f"Connection error for UID: {uid}")
        return None
    except Exception as e:
        print(f"Check ban error: {e}")
        return None

def ban_account(access_token):
    try:
        url = f"https://ffidbanapi.vercel.app/ban-account?access-token={access_token}&key=ANIXH"
        response = requests.get(url, timeout=20)
        if response.status_code == 200:
            return response.json()
        return None
    except:
        return None

def get_ban_info_text(uid):
    """Get ban info - FIXED"""
    data = check_ban_info(uid)
    
    if not data:
        return """
BAN INFO FAILED
═══════════════════════

COULD NOT FETCH BAN INFORMATION!

REASONS:
• INVALID UID
• API TIMEOUT
• SERVER ERROR

TIPS:
• CHECK UID IS CORRECT
• TRY AGAIN LATER
• CONTACT SUPPORT

═══════════════════════
"""
    
    try:
        account_id = data.get('account_id', 'N/A')
        nickname = data.get('nickname', 'Unknown')
        region = data.get('region', 'N/A')
        level = data.get('level', 'N/A')
        ban_info = data.get('ban_info', {})
        is_banned = ban_info.get('is_banned', False)
        
        text = f"""
BAN INFORMATION
═══════════════════════
ACCOUNT ID: {account_id}
NICKNAME: {nickname}
REGION: {region}
LEVEL: {level}
═══════════════════════
STATUS: {'BANNED' if is_banned else 'ACTIVE'}
"""
        if is_banned:
            text += f"""
BAN START: {ban_info.get('ban_start_time', 'N/A')}
BAN END: {ban_info.get('ban_end_time', 'N/A')}
REMAINING: {ban_info.get('ban_expire_duration', 'N/A')}
"""
        else:
            text += """
ACCOUNT IS NOT BANNED!
"""
        
        text += """
═══════════════════════
"""
        return text
    except Exception as e:
        print(f"Get ban info text error: {e}")
        return """
BAN INFO ERROR
═══════════════════════

COULD NOT PARSE BAN INFORMATION!

PLEASE TRY AGAIN LATER.

═══════════════════════
"""

# ============================================================
# BOT COMMANDS
# ============================================================

@bot.message_handler(commands=['start'])
def start_cmd(message):
    try:
        user_id = message.from_user.id
        username = message.from_user.username
        first_name = message.from_user.first_name
        
        settings = load_settings()
        developer = settings.get("developer", "@iflexzyan")
        welcome_image = settings.get("welcome_image", "https://iili.io/C8DNTyQ.jpg")
        
        user = register_user(user_id, username, first_name)
        if user.get("banned", False):
            send_pe(message.chat.id, "You are banned from using this bot!")
            return
        
        try:
            if welcome_image.startswith("http"):
                bot.send_photo(message.chat.id, photo=welcome_image)
            else:
                bot.send_photo(message.chat.id, photo=welcome_image)
        except:
            pass
        
        text = f"""
WELCOME TO FF BAN BOT
═══════════════════════
USER: {first_name}
ID: {user_id}
USERNAME: @{username or 'N/A'}
═══════════════════════
1 FREE TRIAL - ALL FEATURES
UNLIMITED ACCESS - PAY & GET
═══════════════════════
DEVELOPER: {developer}
"""
        if is_admin(user_id):
            markup = get_admin_menu(user_id)
        else:
            markup = get_user_menu(user_id)
        
        send_pe(message.chat.id, text, reply_markup=markup)
    except Exception as e:
        print(f"Start error: {e}")

@bot.message_handler(commands=['help'])
def help_cmd(message):
    text = """
HELP
═══════════════════════

AVAILABLE FEATURES:

1. BAN ACCOUNT - Access token se ban
2. CHECK BAN INFO - UID se ban status
3. REVOKE TOKEN - Access token revoke
4. EAT TO TOKEN - EAT to Access token

═══════════════════════

FREE TRIAL: 1 USE
UNLIMITED: PAY & GET

═══════════════════════
"""
    send_pe(message.chat.id, text)

# ============================================================
# BAN ACCOUNT
# ============================================================

@bot.message_handler(func=lambda m: m.text and stylish_text("BAN ACCOUNT") in m.text)
def ban_account_start(message):
    try:
        user_id = message.from_user.id
        user = get_user(user_id)
        if not user or user.get("banned", False):
            send_pe(message.chat.id, "You are banned!")
            return
        
        price = get_price("ban")
        if price > 0 and not user.get("unlimited", False):
            uses = user.get("uses", 0)
            if uses >= 1:
                send_pe(message.chat.id, f"Free trial used!\nPay Rs.{price} for unlimited")
                send_payment_qr(message.chat.id, "ban")
                return
        
        send_pe(message.chat.id, "Send the access token:")
        bot.register_next_step_handler(message, process_ban_token)
    except Exception as e:
        print(f"Ban start error: {e}")

def process_ban_token(message):
    try:
        user_id = message.from_user.id
        token = message.text.strip()
        if len(token) < 30:
            send_pe(message.chat.id, "Invalid token!")
            return
        
        msg = send_pe(message.chat.id, "Banning...")
        data = ban_account(token)
        bot.delete_message(message.chat.id, msg.message_id)
        
        if data and "BANNED" in str(data.get('status', '')).upper():
            use_free_trial(user_id)
            text = f"""
ACCOUNT BANNED
═══════════════════════
BAN SUCCESSFUL!
ID: {data.get('id', 'N/A')}
NAME: {data.get('name', 'N/A')}
UID: {data.get('uid', 'N/A')}
═══════════════════════
DEVELOPER: @iflexzyan
"""
            keyboard = [
                [make_green_button("BAN ANOTHER", callback="ban_another")],
                [make_green_button("GET UNLIMITED", callback="get_unlimited")]
            ]
            markup = InlineKeyboardMarkup(keyboard)
            send_pe(message.chat.id, text, reply_markup=markup)
        else:
            text = """
BAN FAILED
═══════════════════════
NOT BANNED!
═══════════════════════
DEVELOPER: @iflexzyan
"""
            send_pe(message.chat.id, text)
    except Exception as e:
        print(f"Process ban error: {e}")

# ============================================================
# CHECK BAN INFO - FIXED
# ============================================================

@bot.message_handler(func=lambda m: m.text and stylish_text("CHECK BAN INFO") in m.text)
def check_ban_info_start(message):
    try:
        user_id = message.from_user.id
        user = get_user(user_id)
        if not user or user.get("banned", False):
            send_pe(message.chat.id, "You are banned!")
            return
        
        price = get_price("ban_check")
        if price > 0 and not user.get("unlimited", False):
            uses = user.get("uses", 0)
            if uses >= 1:
                send_pe(message.chat.id, f"Free trial used!\nPay Rs.{price}")
                send_payment_qr(message.chat.id, "ban_check")
                return
        
        send_pe(message.chat.id, "Send the Free Fire UID:")
        bot.register_next_step_handler(message, process_ban_check)
    except Exception as e:
        print(f"Check ban error: {e}")

def process_ban_check(message):
    try:
        user_id = message.from_user.id
        uid = message.text.strip()
        if not uid.isdigit() or len(uid) < 5:
            send_pe(message.chat.id, "Invalid UID! Please send a valid Free Fire UID.")
            return
        
        msg = send_pe(message.chat.id, f"Checking ban info for UID {uid}...")
        response_text = get_ban_info_text(uid)
        bot.delete_message(message.chat.id, msg.message_id)
        
        if "FAILED" not in response_text and "ERROR" not in response_text:
            use_free_trial(user_id)
            keyboard = [
                [make_green_button("CHECK ANOTHER", callback="check_another")],
                [make_green_button("GET UNLIMITED", callback="get_unlimited")]
            ]
            markup = InlineKeyboardMarkup(keyboard)
            send_pe(message.chat.id, response_text, reply_markup=markup)
        else:
            send_pe(message.chat.id, response_text)
    except Exception as e:
        print(f"Process check error: {e}")

# ============================================================
# REVOKE TOKEN
# ============================================================

@bot.message_handler(func=lambda m: m.text and stylish_text("REVOKE TOKEN") in m.text)
def revoke_token_start(message):
    try:
        user_id = message.from_user.id
        user = get_user(user_id)
        if not user or user.get("banned", False):
            send_pe(message.chat.id, "You are banned!")
            return
        
        price = get_price("revoke")
        if price > 0 and not user.get("unlimited", False):
            uses = user.get("uses", 0)
            if uses >= 1:
                send_pe(message.chat.id, f"Free trial used!\nPay Rs.{price}")
                send_payment_qr(message.chat.id, "revoke")
                return
        
        send_pe(message.chat.id, "Send the access token to revoke:")
        bot.register_next_step_handler(message, process_revoke)
    except Exception as e:
        print(f"Revoke error: {e}")

def process_revoke(message):
    try:
        user_id = message.from_user.id
        token = message.text.strip()
        if len(token) < 30:
            send_pe(message.chat.id, "Invalid token!")
            return
        
        msg = send_pe(message.chat.id, "Revoking...")
        success = revoke_token(token)
        bot.delete_message(message.chat.id, msg.message_id)
        
        if success:
            use_free_trial(user_id)
            text = """
TOKEN REVOKED
═══════════════════════
TOKEN REVOKED SUCCESSFULLY!
═══════════════════════
"""
            send_pe(message.chat.id, text)
        else:
            text = """
REVOKE FAILED
═══════════════════════
COULD NOT REVOKE TOKEN!
═══════════════════════
"""
            send_pe(message.chat.id, text)
    except Exception as e:
        print(f"Process revoke error: {e}")

# ============================================================
# EAT TO TOKEN
# ============================================================

@bot.message_handler(func=lambda m: m.text and stylish_text("EAT TO TOKEN") in m.text)
def eat_to_token_start(message):
    try:
        user_id = message.from_user.id
        user = get_user(user_id)
        if not user or user.get("banned", False):
            send_pe(message.chat.id, "You are banned!")
            return
        
        price = get_price("eat_token")
        if price > 0 and not user.get("unlimited", False):
            uses = user.get("uses", 0)
            if uses >= 1:
                send_pe(message.chat.id, f"Free trial used!\nPay Rs.{price}")
                send_payment_qr(message.chat.id, "eat_token")
                return
        
        send_pe(message.chat.id, """
EAT TO TOKEN
═══════════════════════
Send your EAT token:
═══════════════════════
""")
        bot.register_next_step_handler(message, process_eat_to_token)
    except Exception as e:
        print(f"Eat to token error: {e}")

def process_eat_to_token(message):
    try:
        user_id = message.from_user.id
        eat_token = message.text.strip()
        if len(eat_token) < 10:
            send_pe(message.chat.id, "Invalid EAT token!")
            return
        
        msg = send_pe(message.chat.id, "Converting EAT token...")
        token = eat_to_token(eat_token)
        bot.delete_message(message.chat.id, msg.message_id)
        
        if token:
            use_free_trial(user_id)
            text = f"""
TOKEN GENERATED
═══════════════════════
ACCESS TOKEN:
{token}
═══════════════════════
"""
            send_pe(message.chat.id, text)
        else:
            text = """
CONVERSION FAILED
═══════════════════════
COULD NOT CONVERT EAT TOKEN!
CHECK YOUR EAT TOKEN.
═══════════════════════
"""
            send_pe(message.chat.id, text)
    except Exception as e:
        print(f"Process eat error: {e}")

# ============================================================
# FREE TRIAL & UNLIMITED
# ============================================================

@bot.message_handler(func=lambda m: m.text and stylish_text("FREE TRIAL") in m.text)
def free_trial_cmd(message):
    try:
        user_id = message.from_user.id
        user = get_user(user_id)
        if not user:
            send_pe(message.chat.id, "Please /start first!")
            return
        if user.get("unlimited", False):
            send_pe(message.chat.id, "Already unlimited!")
            return
        uses = user.get("uses", 0)
        if uses >= 1:
            send_pe(message.chat.id, "Free trial used!\nPay for unlimited")
            send_payment_qr(message.chat.id, "unlimited")
            return
        text = """
FREE TRIAL ACTIVATED
═══════════════════════
USE ANY FEATURE ONCE!
═══════════════════════
"""
        send_pe(message.chat.id, text)
    except Exception as e:
        print(f"Free trial error: {e}")

@bot.message_handler(func=lambda m: m.text and stylish_text("UNLIMITED") in m.text)
def unlimited_cmd(message):
    try:
        user_id = message.from_user.id
        user = get_user(user_id)
        if user and user.get("unlimited", False):
            send_pe(message.chat.id, "Already unlimited!")
            return
        send_payment_qr(message.chat.id, "unlimited")
    except Exception as e:
        print(f"Unlimited error: {e}")

# ============================================================
# PAYMENT SYSTEM
# ============================================================

def send_payment_qr(chat_id, feature="unlimited"):
    try:
        settings = load_settings()
        upi = settings.get("upi", "vanshx111@naviaxis")
        
        prices = {
            "ban": settings.get("ban_price", 29),
            "ban_check": settings.get("ban_check_price", 0),
            "revoke": settings.get("revoke_price", 0),
            "eat_token": settings.get("eat_token_price", 0),
            "unlimited": 199,
        }
        price = prices.get(feature, 99)
        if price == 0:
            send_pe(chat_id, "This feature is free!")
            return
        
        qr_url = f"https://api.qrserver.com/v1/create-qr-code/?size=300x300&data=upi://pay?pa={upi}&am={price}&cu=INR"
        
        text = f"""
PAYMENT
═══════════════════════
UPI: {upi}
AMOUNT: Rs.{price}
FEATURE: {feature.upper()}
═══════════════════════
SCAN QR TO PAY
═══════════════════════
{upi}
"""
        keyboard = [
            [make_green_button("I HAVE PAID", callback=f"paid_{feature}")],
            [make_red_button("CANCEL", callback="cancel_payment")]
        ]
        markup = InlineKeyboardMarkup(keyboard)
        
        try:
            bot.send_photo(chat_id, photo=qr_url, caption=text, reply_markup=markup)
        except:
            send_pe(chat_id, text, reply_markup=markup)
    except Exception as e:
        print(f"Payment QR error: {e}")

@bot.callback_query_handler(func=lambda c: c.data and c.data.startswith("paid_"))
def handle_paid(call):
    try:
        user_id = call.from_user.id
        chat_id = call.message.chat.id
        feature = call.data.split("_")[1]
        
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
            "feature": feature,
            "requested": datetime.now().isoformat()
        }
        save_pending(pending)
        
        send_pe(chat_id, "Send payment screenshot!")
        bot.register_next_step_handler(call.message, receive_payment_screenshot, feature)
        bot.answer_callback_query(call.id)
    except Exception as e:
        print(f"Paid callback error: {e}")

def receive_payment_screenshot(message, feature="unlimited"):
    try:
        user_id = message.from_user.id
        if message.photo:
            file_id = message.photo[-1].file_id
            pending = load_pending()
            if str(user_id) in pending:
                pending[str(user_id)]["screenshot"] = file_id
                pending[str(user_id)]["feature"] = feature
                save_pending(pending)
            
            send_pe(message.chat.id, "Received! Waiting for admin approval.")
            
            admin_text = f"""
NEW PAYMENT
═══════════════════════
USER: {message.from_user.first_name}
ID: {user_id}
USERNAME: @{message.from_user.username or 'N/A'}
FEATURE: {feature}
═══════════════════════
"""
            keyboard = [
                [make_green_button("APPROVE", callback=f"admin_approve_{user_id}_{feature}")],
                [make_red_button("REJECT", callback=f"admin_reject_{user_id}")]
            ]
            markup = InlineKeyboardMarkup(keyboard)
            
            for admin in ADMIN_IDS:
                try:
                    bot.send_photo(admin, photo=file_id, caption=admin_text, reply_markup=markup)
                except:
                    send_pe(admin, admin_text, reply_markup=markup)
        else:
            send_pe(message.chat.id, "Send a photo!")
    except Exception as e:
        print(f"Screenshot receive error: {e}")

@bot.callback_query_handler(func=lambda c: c.data and c.data.startswith("admin_approve_"))
def admin_approve_callback(call):
    try:
        if not is_admin(call.from_user.id):
            send_pe(call.message.chat.id, "Unauthorized!")
            bot.answer_callback_query(call.id)
            return
        
        parts = call.data.split("_")
        user_id = int(parts[2])
        feature = parts[3] if len(parts) > 3 else "unlimited"
        
        update_user(user_id, "unlimited", True)
        update_user(user_id, "uses", 0)
        
        pending = load_pending()
        if str(user_id) in pending:
            del pending[str(user_id)]
            save_pending(pending)
        
        try:
            bot.delete_message(call.message.chat.id, call.message.message_id)
        except:
            pass
        
        send_pe(call.message.chat.id, f"User {user_id} approved for {feature}!")
        
        try:
            send_pe(user_id, f"Congratulations! Unlimited {feature} access! 🎉")
        except:
            pass
        
        bot.answer_callback_query(call.id)
    except Exception as e:
        print(f"Admin approve error: {e}")

@bot.callback_query_handler(func=lambda c: c.data == "cancel_payment")
def cancel_payment_callback(call):
    try:
        bot.delete_message(call.message.chat.id, call.message.message_id)
    except:
        pass
    send_pe(call.message.chat.id, "Cancelled!")
    bot.answer_callback_query(call.id)

# ============================================================
# CALLBACK HANDLERS
# ============================================================

@bot.callback_query_handler(func=lambda c: c.data == "ban_another")
def ban_another_callback(call):
    try:
        user_id = call.from_user.id
        user = get_user(user_id)
        if not user or user.get("banned", False):
            send_pe(call.message.chat.id, "Banned!")
            return
        
        price = get_price("ban")
        if price > 0 and not user.get("unlimited", False):
            uses = user.get("uses", 0)
            if uses >= 1:
                send_pe(call.message.chat.id, f"Used!\nPay Rs.{price}")
                send_payment_qr(call.message.chat.id, "ban")
                bot.answer_callback_query(call.id)
                return
        
        send_pe(call.message.chat.id, "Send token:")
        bot.register_next_step_handler(call.message, process_ban_token)
        bot.answer_callback_query(call.id)
    except Exception as e:
        print(f"Ban another error: {e}")

@bot.callback_query_handler(func=lambda c: c.data == "check_another")
def check_another_callback(call):
    try:
        user_id = call.from_user.id
        user = get_user(user_id)
        if not user or user.get("banned", False):
            send_pe(call.message.chat.id, "Banned!")
            return
        
        price = get_price("ban_check")
        if price > 0 and not user.get("unlimited", False):
            uses = user.get("uses", 0)
            if uses >= 1:
                send_pe(call.message.chat.id, f"Used!\nPay Rs.{price}")
                send_payment_qr(call.message.chat.id, "ban_check")
                bot.answer_callback_query(call.id)
                return
        
        send_pe(call.message.chat.id, "Send UID:")
        bot.register_next_step_handler(call.message, process_ban_check)
        bot.answer_callback_query(call.id)
    except Exception as e:
        print(f"Check another error: {e}")

@bot.callback_query_handler(func=lambda c: c.data == "get_unlimited")
def get_unlimited_callback(call):
    try:
        send_payment_qr(call.message.chat.id, "unlimited")
        bot.answer_callback_query(call.id)
    except Exception as e:
        print(f"Get unlimited error: {e}")

# ============================================================
# SUPPORT, ABOUT, HOW TO GET TOKEN
# ============================================================

@bot.message_handler(func=lambda m: m.text and stylish_text("SUPPORT") in m.text)
def support_cmd(message):
    settings = load_settings()
    support = settings.get("support", "@iflexzyan")
    developer = settings.get("developer", "@iflexzyan")
    
    text = f"""
SUPPORT
═══════════════════════
DEVELOPER: {developer}
FOR ANY ISSUE:
TELEGRAM: {support}
═══════════════════════
"""
    markup = InlineKeyboardMarkup([
        [make_green_button("CONTACT", url=f"https://t.me/{support.replace('@', '')}")]
    ])
    send_pe(message.chat.id, text, reply_markup=markup)

@bot.message_handler(func=lambda m: m.text and stylish_text("ABOUT") in m.text)
def about_cmd(message):
    settings = load_settings()
    developer = settings.get("developer", "@iflexzyan")
    
    text = f"""
ABOUT
═══════════════════════
FF BAN BOT
BAN ACCOUNTS
CHECK BAN INFO
REVOKE TOKEN
EAT TO TOKEN
DEVELOPER: {developer}
═══════════════════════
"""
    send_pe(message.chat.id, text)

@bot.message_handler(func=lambda m: m.text and stylish_text("HOW TO GET TOKEN") in m.text)
def how_to_get_token(message):
    settings = load_settings()
    token_text = settings.get("token_text", "1. Open Free Fire\n2. Go to Settings\n3. Click Account\n4. Find Data Access\n5. Copy Token")
    
    text = f"""
HOW TO GET TOKEN
═══════════════════════
{token_text}
═══════════════════════
"""
    send_pe(message.chat.id, text)
    
    if os.path.exists("token_video.mp4"):
        with open("token_video.mp4", "rb") as f:
            bot.send_video(message.chat.id, f, caption="Video Guide")

# ============================================================
# ADMIN COMMANDS
# ============================================================

@bot.message_handler(func=lambda m: m.text and stylish_text("BOT ON") in m.text)
def bot_on_btn(message):
    if not is_admin(message.from_user.id):
        send_pe(message.chat.id, "Unauthorized!")
        return
    global bot_active
    bot_active = True
    send_pe(message.chat.id, "Bot is now ONLINE!")

@bot.message_handler(func=lambda m: m.text and stylish_text("BOT OFF") in m.text)
def bot_off_btn(message):
    if not is_admin(message.from_user.id):
        send_pe(message.chat.id, "Unauthorized!")
        return
    global bot_active
    bot_active = False
    send_pe(message.chat.id, "Bot is now OFFLINE!")

@bot.message_handler(func=lambda m: m.text and stylish_text("ADMIN PANEL") in m.text)
def admin_panel_btn(message):
    admin_panel_cmd(message)

@bot.message_handler(func=lambda m: m.text and stylish_text("STATS") in m.text)
def stats_btn(message):
    stats_cmd(message)

@bot.message_handler(func=lambda m: m.text and stylish_text("USERS") in m.text)
def users_btn(message):
    users_cmd(message)

@bot.message_handler(func=lambda m: m.text and stylish_text("DATA") in m.text)
def data_btn(message):
    data_cmd(message)

@bot.message_handler(func=lambda m: m.text and stylish_text("CHECK ALL") in m.text)
def check_all_btn(message):
    check_all_cmd(message)

@bot.message_handler(func=lambda m: m.text and stylish_text("TOTAL ADMINS") in m.text)
def total_admins_btn(message):
    total_admins_cmd(message)

@bot.message_handler(func=lambda m: m.text and stylish_text("BAN PRICE") in m.text)
def ban_price_btn(message):
    settings = load_settings()
    send_pe(message.chat.id, f"Ban Price: Rs.{settings.get('ban_price', 29)}\n/banprice <amount>")

@bot.message_handler(commands=['banprice'])
def banprice_cmd(message):
    if not is_admin(message.from_user.id):
        send_pe(message.chat.id, "Unauthorized!")
        return
    parts = message.text.split()
    if len(parts) < 2:
        return
    try:
        price = int(parts[1])
        settings = load_settings()
        settings["ban_price"] = price
        save_settings(settings)
        send_pe(message.chat.id, f"Ban Price: Rs.{price}!")
    except:
        send_pe(message.chat.id, "Invalid!")

@bot.message_handler(func=lambda m: m.text and stylish_text("CHECK PRICE") in m.text)
def check_price_btn(message):
    settings = load_settings()
    send_pe(message.chat.id, f"Check Price: Rs.{settings.get('ban_check_price', 0)}\n/checkprice <amount>")

@bot.message_handler(commands=['checkprice'])
def checkprice_cmd(message):
    if not is_admin(message.from_user.id):
        send_pe(message.chat.id, "Unauthorized!")
        return
    parts = message.text.split()
    if len(parts) < 2:
        return
    try:
        price = int(parts[1])
        settings = load_settings()
        settings["ban_check_price"] = price
        save_settings(settings)
        send_pe(message.chat.id, f"Check Price: Rs.{price}!")
    except:
        send_pe(message.chat.id, "Invalid!")

@bot.message_handler(func=lambda m: m.text and stylish_text("REVOKE PRICE") in m.text)
def revoke_price_btn(message):
    settings = load_settings()
    send_pe(message.chat.id, f"Revoke Price: Rs.{settings.get('revoke_price', 0)}\n/revokeprice <amount>")

@bot.message_handler(commands=['revokeprice'])
def revokeprice_cmd(message):
    if not is_admin(message.from_user.id):
        send_pe(message.chat.id, "Unauthorized!")
        return
    parts = message.text.split()
    if len(parts) < 2:
        return
    try:
        price = int(parts[1])
        settings = load_settings()
        settings["revoke_price"] = price
        save_settings(settings)
        send_pe(message.chat.id, f"Revoke Price: Rs.{price}!")
    except:
        send_pe(message.chat.id, "Invalid!")

@bot.message_handler(func=lambda m: m.text and stylish_text("EAT PRICE") in m.text)
def eat_price_btn(message):
    settings = load_settings()
    send_pe(message.chat.id, f"Eat Price: Rs.{settings.get('eat_token_price', 0)}\n/eatprice <amount>")

@bot.message_handler(commands=['eatprice'])
def eatprice_cmd(message):
    if not is_admin(message.from_user.id):
        send_pe(message.chat.id, "Unauthorized!")
        return
    parts = message.text.split()
    if len(parts) < 2:
        return
    try:
        price = int(parts[1])
        settings = load_settings()
        settings["eat_token_price"] = price
        save_settings(settings)
        send_pe(message.chat.id, f"Eat Price: Rs.{price}!")
    except:
        send_pe(message.chat.id, "Invalid!")

@bot.message_handler(func=lambda m: m.text and stylish_text("UPI") in m.text)
def upi_btn(message):
    send_pe(message.chat.id, f"Current UPI: {load_settings().get('upi', 'vanshx111@naviaxis')}\n/upi <new>")

@bot.message_handler(commands=['upi'])
def upi_cmd(message):
    if not is_admin(message.from_user.id):
        send_pe(message.chat.id, "Unauthorized!")
        return
    parts = message.text.split()
    if len(parts) < 2:
        return
    upi = parts[1]
    settings = load_settings()
    settings["upi"] = upi
    save_settings(settings)
    send_pe(message.chat.id, f"UPI: {upi}!")

@bot.message_handler(func=lambda m: m.text and stylish_text("ADD ADMIN") in m.text)
def add_admin_btn(message):
    send_pe(message.chat.id, "/addadmin id")

@bot.message_handler(commands=['addadmin'])
def add_admin_cmd(message):
    if not is_admin(message.from_user.id):
        send_pe(message.chat.id, "Unauthorized!")
        return
    parts = message.text.split()
    if len(parts) < 2:
        return
    try:
        user_id = int(parts[1])
        if user_id not in ADMIN_IDS:
            ADMIN_IDS.append(user_id)
            send_pe(message.chat.id, "Added!")
        else:
            send_pe(message.chat.id, "Already admin!")
    except:
        send_pe(message.chat.id, "Invalid!")

@bot.message_handler(commands=['users'])
def users_cmd(message):
    if not is_admin(message.from_user.id):
        send_pe(message.chat.id, "Unauthorized!")
        return
    users = load_users()
    total = len(users)
    unlimited = sum(1 for u in users.values() if u.get("unlimited", False))
    banned = sum(1 for u in users.values() if u.get("banned", False))
    
    text = f"""
USERS
═══════════════════════
TOTAL: {total}
UNLIMITED: {unlimited}
BANNED: {banned}
LIST:
"""
    for uid, data in users.items():
        status = "UNLIMITED" if data.get("unlimited", False) else "FREE"
        banned_status = "BANNED" if data.get("banned", False) else "ACTIVE"
        text += f"• {data.get('name', 'Unknown')} (@{data.get('username', 'N/A')}) - {status} {banned_status}\n"
    send_pe(message.chat.id, text)

@bot.message_handler(commands=['data'])
def data_cmd(message):
    if not is_admin(message.from_user.id):
        send_pe(message.chat.id, "Unauthorized!")
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
        "admins": ADMIN_IDS,
        "total_users": len(users),
        "total_bans": len(orders),
        "pending_payments": len(pending),
        "total_admins": len(ADMIN_IDS),
        "generated": datetime.now().isoformat()
    }
    file_path = "bot_data.json"
    with open(file_path, "w") as f:
        json.dump(data, f, indent=2)
    with open(file_path, "rb") as f:
        bot.send_document(message.chat.id, f, caption="Data Export")

@bot.message_handler(commands=['broadcastuser'])
def broadcast_user(message):
    if not is_admin(message.from_user.id):
        send_pe(message.chat.id, "Unauthorized!")
        return
    parts = message.text.split(maxsplit=2)
    if len(parts) < 3:
        send_pe(message.chat.id, "/broadcastuser id msg")
        return
    try:
        user_id = int(parts[1])
        msg = parts[2]
        bot.send_message(user_id, f"{msg}")
        send_pe(message.chat.id, "Sent!")
    except Exception as e:
        send_pe(message.chat.id, f"Failed: {str(e)}")

@bot.message_handler(commands=['allbroadcast'])
def all_broadcast(message):
    if not is_admin(message.from_user.id):
        send_pe(message.chat.id, "Unauthorized!")
        return
    parts = message.text.split(maxsplit=1)
    if len(parts) < 2:
        send_pe(message.chat.id, "/allbroadcast msg")
        return
    msg = parts[1]
    users = load_users()
    sent = 0
    failed = 0
    for user_id in users.keys():
        try:
            bot.send_message(int(user_id), f"{msg}")
            sent += 1
            time.sleep(0.05)
        except:
            failed += 1
    send_pe(message.chat.id, f"""
Complete!
Sent: {sent}
Failed: {failed}
""")

# ============================================================
# CHECK ALL
# ============================================================

def check_all_cmd(message):
    try:
        if not is_admin(message.from_user.id):
            send_pe(message.chat.id, "Unauthorized!")
            return
        users = load_users()
        if not users:
            send_pe(message.chat.id, "No users found!")
            return
        
        text = "ALL USERS\n═══════════════════════\n"
        for uid, data in users.items():
            status = "UNLIMITED" if data.get("unlimited", False) else "FREE"
            banned = "BANNED" if data.get("banned", False) else "ACTIVE"
            admin = "ADMIN" if int(uid) in ADMIN_IDS else ""
            text += f"• {data.get('name', 'Unknown')} (@{data.get('username', 'N/A')}) - {status} {banned} {admin}\n"
        text += f"\n═══════════════════════\nTOTAL: {len(users)}"
        send_pe(message.chat.id, text)
    except Exception as e:
        print(f"Check all error: {e}")

# ============================================================
# TOTAL ADMINS
# ============================================================

def total_admins_cmd(message):
    try:
        if not is_admin(message.from_user.id):
            send_pe(message.chat.id, "Unauthorized!")
            return
        text = "TOTAL ADMINS\n═══════════════════════\n"
        for admin_id in ADMIN_IDS:
            user = get_user(admin_id)
            if user:
                text += f"• {user.get('name', 'Unknown')} (@{user.get('username', 'N/A')}) - ID: {admin_id}\n"
            else:
                text += f"• ID: {admin_id}\n"
        text += f"\n═══════════════════════\nTOTAL: {len(ADMIN_IDS)}"
        send_pe(message.chat.id, text)
    except Exception as e:
        print(f"Total admins error: {e}")

# ============================================================
# STATS & ADMIN PANEL
# ============================================================

def stats_cmd(message):
    if not is_admin(message.from_user.id):
        send_pe(message.chat.id, "Unauthorized!")
        return
    users = load_users()
    orders = load_orders()
    pending = load_pending()
    settings = load_settings()
    
    text = f"""
STATS
═══════════════════════
USERS: {len(users)}
BANS: {len(orders)}
PENDING: {len(pending)}
UNLIMITED: {sum(1 for u in users.values() if u.get('unlimited', False))}
ADMINS: {len(ADMIN_IDS)}
BAN PRICE: Rs.{settings.get('ban_price', 29)}
CHECK PRICE: Rs.{settings.get('ban_check_price', 0)}
REVOKE PRICE: Rs.{settings.get('revoke_price', 0)}
EAT PRICE: Rs.{settings.get('eat_token_price', 0)}
UPI: {settings.get('upi', 'vanshx111@naviaxis')}
DEVELOPER: {settings.get('developer', '@iflexzyan')}
"""
    send_pe(message.chat.id, text)

def admin_panel_cmd(message):
    if not is_admin(message.from_user.id):
        send_pe(message.chat.id, "Unauthorized!")
        return
    text = """
ADMIN PANEL
═══════════════════════
/approve id - Approve
/banprice <amt> - Ban price
/checkprice <amt> - Check price
/revokeprice <amt> - Revoke price
/eatprice <amt> - Eat price
/upi <upi> - Change
/developer <@> - Change
/addadmin id - Add
/broadcastuser id msg - Send
/allbroadcast msg - All
/users - All users
/data - Download
/allcommands - This
═══════════════════════
"""
    send_pe(message.chat.id, text)

# ============================================================
# FLASK WEBHOOK - PORT FIX
# ============================================================

@app.route('/', methods=['GET'])
def index():
    return "FF BAN BOT is running on Render!"

@app.route(f'/{BOT_TOKEN}', methods=['POST'])
def webhook():
    try:
        if request.headers.get('content-type') == 'application/json':
            json_string = request.get_data().decode('utf-8')
            update = types.Update.de_json(json_string)
            bot.process_new_updates([update])
            return '', 200
    except Exception as e:
        print(f"Webhook error: {e}")
    return '', 403

# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":
    print("Bot Started!")
    print(f"Owner: {OWNER_ID}")
    print(f"Users: {len(load_users())}")
    print(f"Admins: {len(ADMIN_IDS)}")
    
    try:
        bot.remove_webhook()
        print("Webhook removed!")
    except Exception as e:
        print(f"Webhook remove error: {e}")
    
    try:
        hostname = os.environ.get('RENDER_EXTERNAL_HOSTNAME')
        if hostname:
            webhook_url = f"https://{hostname}/{BOT_TOKEN}"
            bot.set_webhook(url=webhook_url)
            print(f"Webhook set: {webhook_url}")
        else:
            print("No hostname, using polling")
            bot.infinity_polling()
            exit()
    except Exception as e:
        print(f"Webhook error: {e}, falling back to polling")
        bot.infinity_polling()
        exit()
    
    app.run(host='0.0.0.0', port=PORT)