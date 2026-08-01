import os
import json
import time
import random
import requests
from datetime import datetime
from flask import Flask, request
from telebot import TeleBot, types
from telebot.types import MessageEntity, InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton

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

print("✅ Bot token loaded!")

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
        "8586849798": {"id": 8586849798, "username": "Ffaccsellerx", "name": "FF SELLER", "joined": "2026-07-31T05:18:43.493579", "uses": 0, "unlimited": True, "banned": False},
        "8471373583": {"id": 8471373583, "username": "iflexzyan", "name": "ZYAN", "joined": "2026-07-31T05:30:31.611686", "uses": 0, "unlimited": False, "banned": False},
        "8955229317": {"id": 8955229317, "username": "LEGENDxFIRE", "name": "LEGEND X FIRE 🔥", "joined": "2026-07-31T05:39:01.873843", "uses": 0, "unlimited": True, "banned": False},
        "7977493987": {"id": 7977493987, "username": "Havkerbabaybaba", "name": "Bhai on top", "joined": "2026-07-31T05:39:30.486969", "uses": 1, "unlimited": True, "banned": False},
        "8225378024": {"id": 8225378024, "username": "Wizz_escrower", "name": "WIZZ_ESCROWER", "joined": "2026-08-01T01:58:48.326756", "uses": 0, "unlimited": False, "banned": False},
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
        "guest_token_price": 0,
        "eat_token_price": 0,
        "upi": "vanshx111@naviaxis",
        "free_trial": True,
        "bot_name": "FF BAN BOT",
        "developer": "@iflexzyan",
        "support": "@iflexzyan",
        "welcome_image": "https://iili.io/C8DNTyQ.jpg",
        "token_text": "1️⃣ Open Free Fire\n2️⃣ Go to Settings\n3️⃣ Click Account\n4️⃣ Find Data Access\n5️⃣ Copy Token"
    }
    data = load_data(SETTINGS_FILE)
    for key, val in default.items():
        if key not in data:
            data[key] = val
    return data

def save_settings(settings):
    save_data(SETTINGS_FILE, settings)

# ============================================================
# STYLISH TEXT
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
# PREMIUM EMOJIS
# ============================================================
PREMIUM_EMOJIS = {
    "✅": ["6246537187614005254", "6246782404476803545"],
    "🔥": ["4956222745814762495", "4956606007221421405"],
    "❤️": ["5783157259152397008", "5801084710343938087"],
    "⭐": ["6244496562752331516", "5904618938578243567"],
    "💎": ["6086778246882399112", "5791697221799907788"],
    "👑": ["5794422335599546668", "6089003761496232797"],
    "💰": ["6089104607328342288", "6086730718774300509"],
    "🔫": ["6035243995154616907"],
    "🆓": ["6035060329468137931"],
    "📞": ["6035072209347678547"],
    "👍": ["6089313931149448495"],
    "🔄": ["6035173858338672933"],
    "🔑": ["6035137110598492010"],
    "👤": ["6035051267087143217"],
    "🆔": ["6034945975963881533"],
    "🌍": ["6035081585261287115"],
    "📊": ["6035085583875837709"],
}

def get_premium_emoji():
    return random.choice(list(PREMIUM_EMOJIS.keys()))

def get_premium_id(emoji):
    if emoji in PREMIUM_EMOJIS:
        return int(random.choice(PREMIUM_EMOJIS[emoji]))
    return 6147565374289220368

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
            eid = int(random.choice(PREMIUM_EMOJIS[ch]))
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
    try:
        entities = _build_pe_entities(text)
        return bot.send_message(chat_id, text, entities=entities, reply_markup=reply_markup, parse_mode=None)
    except:
        return bot.send_message(chat_id, text, reply_markup=reply_markup)

def _send_pe_return(chat_id, text: str, reply_markup=None):
    try:
        entities = _build_pe_entities(text)
        return bot.send_message(chat_id, text, entities=entities, reply_markup=reply_markup, parse_mode=None)
    except:
        return bot.send_message(chat_id, text, reply_markup=reply_markup)

# ============================================================
# MAKE GREEN BUTTONS
# ============================================================
def make_green_button(text: str, callback: str = None, url: str = None):
    final_text = stylish_text(text)
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

def get_price(feature):
    settings = load_settings()
    prices = {
        "ban": settings.get("ban_price", 29),
        "ban_check": settings.get("ban_check_price", 0),
        "revoke": settings.get("revoke_price", 0),
        "guest_token": settings.get("guest_token_price", 0),
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
# GET USER MENU
# ============================================================
def get_user_menu(user_id):
    markup = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    markup.row(KeyboardButton(stylish_text("BAN ACCOUNT")))
    markup.row(KeyboardButton(stylish_text("CHECK BAN INFO")))
    markup.row(KeyboardButton(stylish_text("REVOKE TOKEN")))
    markup.row(KeyboardButton(stylish_text("GUEST TO TOKEN")))
    markup.row(KeyboardButton(stylish_text("EAT TO TOKEN")))
    markup.row(KeyboardButton(stylish_text("FREE TRIAL")), KeyboardButton(stylish_text("UNLIMITED")))
    markup.row(KeyboardButton(stylish_text("HOW TO GET TOKEN")), KeyboardButton(stylish_text("SUPPORT")))
    markup.row(KeyboardButton(stylish_text("HELP")), KeyboardButton(stylish_text("ABOUT")))
    return markup

# ============================================================
# GET ADMIN MENU
# ============================================================
def get_admin_menu(user_id):
    markup = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    markup.row(KeyboardButton(stylish_text("BOT OFF")), KeyboardButton(stylish_text("BOT ON")))
    markup.row(KeyboardButton(stylish_text("ADMIN PANEL")), KeyboardButton(stylish_text("STATS")))
    markup.row(KeyboardButton(stylish_text("USERS")), KeyboardButton(stylish_text("DATA")))
    markup.row(KeyboardButton(stylish_text("CHECK ALL")), KeyboardButton(stylish_text("TOTAL ADMINS")))
    markup.row(KeyboardButton(stylish_text("BAN PRICE")), KeyboardButton(stylish_text("CHECK PRICE")))
    markup.row(KeyboardButton(stylish_text("REVOKE PRICE")), KeyboardButton(stylish_text("GUEST PRICE")))
    markup.row(KeyboardButton(stylish_text("EAT PRICE")), KeyboardButton(stylish_text("UPI")))
    markup.row(KeyboardButton(stylish_text("ADD ADMIN")), KeyboardButton(stylish_text("ALL COMMANDS")))
    markup.row(KeyboardButton(stylish_text("HOW TO GET TOKEN")), KeyboardButton(stylish_text("BROADCAST")))
    markup.row(KeyboardButton(stylish_text("ALL BROADCAST")), KeyboardButton(stylish_text("SET WELCOME IMAGE")))
    markup.row(KeyboardButton(stylish_text("SET TOKEN TEXT")), KeyboardButton(stylish_text("ADD TOKEN VIDEO")))
    return markup

# ============================================================
# API FUNCTIONS - PROPERLY INTEGRATED
# ============================================================

def guest_to_token(uid, password):
    """UID + Password se Access Token"""
    try:
        url = f"https://token.killersharmabot.online/token?uid={uid}&password={password}"
        response = requests.get(url, timeout=15)
        if response.status_code == 200:
            data = response.json()
            token = data.get("access_token") or data.get("token")
            if token:
                return token
        return None
    except Exception as e:
        print(f"Guest to token error: {e}")
        return None

def eat_to_token(eat_token):
    """EAT token se Access Token"""
    try:
        url = f"https://access.killersharmabot.online/access?access_token={eat_token}"
        response = requests.get(url, timeout=15)
        if response.status_code == 200:
            data = response.json()
            token = data.get("access_token") or data.get("token")
            if token:
                return token
        return None
    except Exception as e:
        print(f"Eat to token error: {e}")
        return None

def revoke_token(access_token):
    """Revoke Access Token"""
    try:
        url = f"https://crownxrevoker73.vercel.app/revoke?access_token={access_token}"
        response = requests.get(url, timeout=15)
        if response.status_code == 200:
            data = response.json()
            return data.get("success", False)
        return False
    except Exception as e:
        print(f"Revoke error: {e}")
        return False

def check_ban_info(uid):
    """Check ban info using API"""
    try:
        url = f"https://crownx-premium-bancheck.vercel.app/baninfo?uid={uid}"
        response = requests.get(url, timeout=15)
        if response.status_code == 200:
            return response.json()
        return None
    except Exception as e:
        print(f"Check ban error: {e}")
        return None

def ban_account(access_token):
    """Ban account using API"""
    try:
        url = f"https://ffidbanapi.vercel.app/ban-account?access-token={access_token}&key=ANIXH"
        response = requests.get(url, timeout=30)
        if response.status_code == 200:
            return response.json()
        return None
    except Exception as e:
        print(f"Ban error: {e}")
        return None

def get_ban_info_text(uid):
    """Get ban info and return as text - NO JSON"""
    data = check_ban_info(uid)
    
    if not data:
        return "❌ ғᴀɪʟᴇᴅ ᴛᴏ ғᴇᴛᴄʜ ʙᴀɴ ɪɴғᴏʀᴍᴀᴛɪᴏɴ! ᴘʟᴇᴀsᴇ ᴛʀʏ ᴀɢᴀɪɴ."
    
    account_id = data.get('account_id', 'N/A')
    nickname = data.get('nickname', 'Unknown')
    region = data.get('region', 'N/A')
    level = data.get('level', 'N/A')
    
    ban_info = data.get('ban_info', {})
    is_banned = ban_info.get('is_banned', False)
    
    text = f"""
✅ ═══《 🔍 ʙᴀɴ ɪɴғᴏʀᴍᴀᴛɪᴏɴ 》═══ ✅

✅ 🆔 ᴀᴄᴄᴏᴜɴᴛ: {account_id}
✅ 👤 ɴɪᴄᴋɴᴀᴍᴇ: {nickname}
✅ 🌍 ʀᴇɢɪᴏɴ: {region}
✅ 📊 ʟᴇᴠᴇʟ: {level}

✅ ═══════════════════════ ✅

"""
    
    if is_banned:
        ban_start = ban_info.get('ban_start_time', 'N/A')
        ban_end = ban_info.get('ban_end_time', 'N/A')
        ban_duration = ban_info.get('ban_expire_duration', 'N/A')
        
        text += f"""
✅ 📌 sᴛᴀᴛᴜs: 🔴 ʙᴀɴɴᴇᴅ

✅ ⏰ ʙᴀɴ sᴛᴀʀᴛ: {ban_start}
✅ ⏳ ʙᴀɴ ᴇɴᴅ: {ban_end}
✅ 📅 ʀᴇᴍᴀɪɴɪɴɢ: {ban_duration}
"""
    else:
        text += """
✅ 📌 sᴛᴀᴛᴜs: 🟢 ᴀᴄᴛɪᴠᴇ

✅ ✅ ᴀᴄᴄᴏᴜɴᴛ ɪs ɴᴏᴛ ʙᴀɴɴᴇᴅ!
"""
    
    text += """
✅ ═══════════════════════ ✅
"""
    return text

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
            _send_pe(message.chat.id, f"❌ ʏᴏᴜ ᴀʀᴇ ʙᴀɴɴᴇᴅ!")
            return
        
        try:
            if welcome_image.startswith("http"):
                bot.send_photo(message.chat.id, photo=welcome_image)
            else:
                bot.send_photo(message.chat.id, photo=welcome_image)
        except:
            pass
        
        welcome_text = f"""
✅ ═══《 🔥 ᴡᴇʟᴄᴏᴍᴇ ᴛᴏ ғғ ʙᴀɴ ʙᴏᴛ 》═══ ✅

✅ 👤 ᴜsᴇʀ: {first_name}
✅ 🆔 ɪᴅ: {user_id}
✅ 👾 ᴜsᴇʀɴᴀᴍᴇ: @{username or 'N/A'}

✅ ═══════════════════════ ✅

✅ 🎯 𝟷 ғʀᴇᴇ ᴛʀɪᴀʟ - ᴀʟʟ ғᴇᴀᴛᴜʀᴇs
✅ 💰 ᴜɴʟɪᴍɪᴛᴇᴅ ᴀᴄᴄᴇss

✅ ═══════════════════════ ✅

✅ 👨‍💻 ᴅᴇᴠᴇʟᴏᴘᴇʀ: {developer}

✅ ═══════════════════════ ✅
"""
        
        if is_admin(user_id):
            markup = get_admin_menu(user_id)
        else:
            markup = get_user_menu(user_id)
        
        _send_pe(message.chat.id, welcome_text, reply_markup=markup)
    except Exception as e:
        print(f"❌ Start error: {e}")

# ============================================================
# BAN ACCOUNT
# ============================================================

@bot.message_handler(func=lambda m: m.text and stylish_text("BAN ACCOUNT") in m.text)
def ban_account_start(message):
    try:
        user_id = message.from_user.id
        user = get_user(user_id)
        
        if not user or user.get("banned", False):
            _send_pe(message.chat.id, f"❌ ʏᴏᴜ ᴀʀᴇ ʙᴀɴɴᴇᴅ!")
            return
        
        price = get_price("ban")
        if price > 0 and not user.get("unlimited", False):
            uses = user.get("uses", 0)
            if uses >= 1:
                _send_pe(message.chat.id, f"⚠️ ғʀᴇᴇ ᴛʀɪᴀʟ ᴜsᴇᴅ!\n💰 ᴘᴀʏ ʀs.{price} ғᴏʀ ᴜɴʟɪᴍɪᴛᴇᴅ")
                send_payment_qr(message.chat.id, "ban")
                return
        
        _send_pe(message.chat.id, f"🔑 sᴇɴᴅ ᴛʜᴇ ᴀᴄᴄᴇss ᴛᴏᴋᴇɴ:")
        bot.register_next_step_handler(message, process_ban_token)
    except Exception as e:
        print(f"❌ Ban start error: {e}")

def process_ban_token(message):
    try:
        user_id = message.from_user.id
        token = message.text.strip()
        
        if len(token) < 30:
            _send_pe(message.chat.id, f"❌ ɪɴᴠᴀʟɪᴅ ᴛᴏᴋᴇɴ!")
            return
        
        msg = _send_pe_return(message.chat.id, f"⏳ ʙᴀɴɴɪɴɢ...")
        
        data = ban_account(token)
        
        bot.delete_message(message.chat.id, msg.message_id)
        
        if data and "BANNED" in str(data.get('status', '')).upper():
            use_free_trial(user_id)
            
            result_text = f"""
✅ ═══《 ✅ ᴀᴄᴄᴏᴜɴᴛ ʙᴀɴɴᴇᴅ 》═══ ✅

✅ 🎯 ʙᴀɴ sᴜᴄᴄᴇssғᴜʟ!

✅ ═══════════════════════ ✅

✅ 🆔 ɪᴅ: {data.get('id', 'N/A')}
✅ 👤 ɴᴀᴍᴇ: {data.get('name', 'N/A')}
✅ 🔢 ᴜɪᴅ: {data.get('uid', 'N/A')}

✅ ═══════════════════════ ✅

✅ 👨‍💻 @iflexzyan
"""
            keyboard = [
                [make_green_button("ʙᴀɴ ᴀɴᴏᴛʜᴇʀ", callback="ban_another")],
                [make_green_button("ɢᴇᴛ ᴜɴʟɪᴍɪᴛᴇᴅ", callback="get_unlimited")]
            ]
            markup = InlineKeyboardMarkup(keyboard)
            _send_pe(message.chat.id, result_text, reply_markup=markup)
            notify_owner(f"✅ ʙᴀɴɴᴇᴅ!\n👤 {user_id}")
        else:
            result_text = f"""
❌ ═══《 ❌ ʙᴀɴ ғᴀɪʟᴇᴅ 》═══ ❌

❌ ɴᴏᴛ ʙᴀɴɴᴇᴅ!

❌ ═══════════════════════ ❌

❌ 👨‍💻 @iflexzyan
"""
            _send_pe(message.chat.id, result_text)
    except Exception as e:
        print(f"❌ Process ban error: {e}")

# ============================================================
# CHECK BAN INFO - TEXT RESPONSE ONLY
# ============================================================

@bot.message_handler(func=lambda m: m.text and stylish_text("CHECK BAN INFO") in m.text)
def check_ban_info_start(message):
    try:
        user_id = message.from_user.id
        user = get_user(user_id)
        
        if not user or user.get("banned", False):
            _send_pe(message.chat.id, f"❌ ʏᴏᴜ ᴀʀᴇ ʙᴀɴɴᴇᴅ!")
            return
        
        price = get_price("ban_check")
        if price > 0 and not user.get("unlimited", False):
            uses = user.get("uses", 0)
            if uses >= 1:
                _send_pe(message.chat.id, f"⚠️ ғʀᴇᴇ ᴛʀɪᴀʟ ᴜsᴇᴅ!\n💰 ᴘᴀʏ ʀs.{price}")
                send_payment_qr(message.chat.id, "ban_check")
                return
        
        _send_pe(message.chat.id, f"🔍 sᴇɴᴅ ᴛʜᴇ ғʀᴇᴇ ғɪʀᴇ ᴜɪᴅ:")
        bot.register_next_step_handler(message, process_ban_check)
    except Exception as e:
        print(f"❌ Check ban error: {e}")

def process_ban_check(message):
    try:
        user_id = message.from_user.id
        uid = message.text.strip()
        
        if not uid.isdigit() or len(uid) < 5:
            _send_pe(message.chat.id, f"❌ ɪɴᴠᴀʟɪᴅ ᴜɪᴅ! ᴘʟᴇᴀsᴇ sᴇɴᴅ ᴀ ᴠᴀʟɪᴅ ғʀᴇᴇ ғɪʀᴇ ᴜɪᴅ.")
            return
        
        msg = _send_pe_return(message.chat.id, f"⏳ ᴄʜᴇᴄᴋɪɴɢ ʙᴀɴ ɪɴғᴏ ғᴏʀ ᴜɪᴅ {uid}...")
        
        # Get text response - NO JSON
        response_text = get_ban_info_text(uid)
        
        bot.delete_message(message.chat.id, msg.message_id)
        
        if "❌ ғᴀɪʟᴇᴅ" not in response_text:
            use_free_trial(user_id)
            
            keyboard = [
                [make_green_button("ᴄʜᴇᴄᴋ ᴀɴᴏᴛʜᴇʀ", callback="check_another")],
                [make_green_button("ɢᴇᴛ ᴜɴʟɪᴍɪᴛᴇᴅ", callback="get_unlimited")]
            ]
            markup = InlineKeyboardMarkup(keyboard)
            _send_pe(message.chat.id, response_text, reply_markup=markup)
        else:
            _send_pe(message.chat.id, response_text)
    except Exception as e:
        print(f"❌ Process check error: {e}")

# ============================================================
# REVOKE TOKEN
# ============================================================

@bot.message_handler(func=lambda m: m.text and stylish_text("REVOKE TOKEN") in m.text)
def revoke_token_start(message):
    try:
        user_id = message.from_user.id
        user = get_user(user_id)
        
        if not user or user.get("banned", False):
            _send_pe(message.chat.id, f"❌ ʏᴏᴜ ᴀʀᴇ ʙᴀɴɴᴇᴅ!")
            return
        
        price = get_price("revoke")
        if price > 0 and not user.get("unlimited", False):
            uses = user.get("uses", 0)
            if uses >= 1:
                _send_pe(message.chat.id, f"⚠️ ғʀᴇᴇ ᴛʀɪᴀʟ ᴜsᴇᴅ!\n💰 ᴘᴀʏ ʀs.{price}")
                send_payment_qr(message.chat.id, "revoke")
                return
        
        _send_pe(message.chat.id, f"🔑 sᴇɴᴅ ᴛʜᴇ ᴀᴄᴄᴇss ᴛᴏᴋᴇɴ ᴛᴏ ʀᴇᴠᴏᴋᴇ:")
        bot.register_next_step_handler(message, process_revoke)
    except Exception as e:
        print(f"❌ Revoke error: {e}")

def process_revoke(message):
    try:
        user_id = message.from_user.id
        token = message.text.strip()
        
        if len(token) < 30:
            _send_pe(message.chat.id, f"❌ ɪɴᴠᴀʟɪᴅ ᴛᴏᴋᴇɴ!")
            return
        
        msg = _send_pe_return(message.chat.id, f"⏳ ʀᴇᴠᴏᴋɪɴɢ...")
        
        success = revoke_token(token)
        
        bot.delete_message(message.chat.id, msg.message_id)
        
        if success:
            use_free_trial(user_id)
            _send_pe(message.chat.id, f"""
✅ ═══《 ✅ ᴛᴏᴋᴇɴ ʀᴇᴠᴏᴋᴇᴅ 》═══ ✅

✅ 🎯 ᴛᴏᴋᴇɴ ʀᴇᴠᴏᴋᴇᴅ sᴜᴄᴄᴇssғᴜʟʟʏ!

✅ ═══════════════════════ ✅
""")
        else:
            _send_pe(message.chat.id, f"""
❌ ═══《 ❌ ʀᴇᴠᴏᴋᴇ ғᴀɪʟᴇᴅ 》═══ ❌

❌ ᴄᴏᴜʟᴅ ɴᴏᴛ ʀᴇᴠᴏᴋᴇ ᴛᴏᴋᴇɴ!

❌ ═══════════════════════ ❌
""")
    except Exception as e:
        print(f"❌ Process revoke error: {e}")

# ============================================================
# GUEST TO TOKEN
# ============================================================

@bot.message_handler(func=lambda m: m.text and stylish_text("GUEST TO TOKEN") in m.text)
def guest_to_token_start(message):
    try:
        user_id = message.from_user.id
        user = get_user(user_id)
        
        if not user or user.get("banned", False):
            _send_pe(message.chat.id, f"❌ ʏᴏᴜ ᴀʀᴇ ʙᴀɴɴᴇᴅ!")
            return
        
        price = get_price("guest_token")
        if price > 0 and not user.get("unlimited", False):
            uses = user.get("uses", 0)
            if uses >= 1:
                _send_pe(message.chat.id, f"⚠️ ғʀᴇᴇ ᴛʀɪᴀʟ ᴜsᴇᴅ!\n💰 ᴘᴀʏ ʀs.{price}")
                send_payment_qr(message.chat.id, "guest_token")
                return
        
        _send_pe(message.chat.id, f"""
✅ ═══《 👤 ɢᴜᴇsᴛ ᴛᴏ ᴛᴏᴋᴇɴ 》═══ ✅

✅ sᴇɴᴅ ɪɴ ᴛʜɪs ғᴏʀᴍᴀᴛ:
✅ ᴜɪᴅ|ᴘᴀssᴡᴏʀᴅ

✅ ᴇxᴀᴍᴘʟᴇ:
✅ 123456789|ᴍʏᴘᴀss123

✅ ═══════════════════════ ✅
""")
        bot.register_next_step_handler(message, process_guest_to_token)
    except Exception as e:
        print(f"❌ Guest to token error: {e}")

def process_guest_to_token(message):
    try:
        user_id = message.from_user.id
        data = message.text.strip()
        
        if '|' not in data:
            _send_pe(message.chat.id, f"❌ ɪɴᴠᴀʟɪᴅ ғᴏʀᴍᴀᴛ! ᴜsᴇ: ᴜɪᴅ|ᴘᴀssᴡᴏʀᴅ")
            return
        
        uid, password = data.split('|', 1)
        uid = uid.strip()
        password = password.strip()
        
        if not uid.isdigit() or len(uid) < 5:
            _send_pe(message.chat.id, f"❌ ɪɴᴠᴀʟɪᴅ ᴜɪᴅ!")
            return
        
        msg = _send_pe_return(message.chat.id, f"⏳ ɢᴇɴᴇʀᴀᴛɪɴɢ ᴛᴏᴋᴇɴ ғᴏʀ ᴜɪᴅ {uid}...")
        
        token = guest_to_token(uid, password)
        
        bot.delete_message(message.chat.id, msg.message_id)
        
        if token:
            use_free_trial(user_id)
            _send_pe(message.chat.id, f"""
✅ ═══《 ✅ ᴛᴏᴋᴇɴ ɢᴇɴᴇʀᴀᴛᴇᴅ 》═══ ✅

✅ 🎯 ᴀᴄᴄᴇss ᴛᴏᴋᴇɴ:

✅ <code>{token}</code>

✅ ═══════════════════════ ✅
""", parse_mode="HTML")
        else:
            _send_pe(message.chat.id, f"""
❌ ═══《 ❌ ғᴀɪʟᴇᴅ 》═══ ❌

❌ ᴄᴏᴜʟᴅ ɴᴏᴛ ɢᴇɴᴇʀᴀᴛᴇ ᴛᴏᴋᴇɴ!

❌ ᴄʜᴇᴄᴋ ᴜɪᴅ ᴀɴᴅ ᴘᴀssᴡᴏʀᴅ.

❌ ═══════════════════════ ❌
""")
    except Exception as e:
        print(f"❌ Process guest error: {e}")

# ============================================================
# EAT TO TOKEN
# ============================================================

@bot.message_handler(func=lambda m: m.text and stylish_text("EAT TO TOKEN") in m.text)
def eat_to_token_start(message):
    try:
        user_id = message.from_user.id
        user = get_user(user_id)
        
        if not user or user.get("banned", False):
            _send_pe(message.chat.id, f"❌ ʏᴏᴜ ᴀʀᴇ ʙᴀɴɴᴇᴅ!")
            return
        
        price = get_price("eat_token")
        if price > 0 and not user.get("unlimited", False):
            uses = user.get("uses", 0)
            if uses >= 1:
                _send_pe(message.chat.id, f"⚠️ ғʀᴇᴇ ᴛʀɪᴀʟ ᴜsᴇᴅ!\n💰 ᴘᴀʏ ʀs.{price}")
                send_payment_qr(message.chat.id, "eat_token")
                return
        
        _send_pe(message.chat.id, f"""
✅ ═══《 🍽️ ᴇᴀᴛ ᴛᴏ ᴛᴏᴋᴇɴ 》═══ ✅

✅ sᴇɴᴅ ʏᴏᴜʀ ᴇᴀᴛ ᴛᴏᴋᴇɴ:

✅ ═══════════════════════ ✅
""")
        bot.register_next_step_handler(message, process_eat_to_token)
    except Exception as e:
        print(f"❌ Eat to token error: {e}")

def process_eat_to_token(message):
    try:
        user_id = message.from_user.id
        eat_token = message.text.strip()
        
        if len(eat_token) < 10:
            _send_pe(message.chat.id, f"❌ ɪɴᴠᴀʟɪᴅ ᴇᴀᴛ ᴛᴏᴋᴇɴ!")
            return
        
        msg = _send_pe_return(message.chat.id, f"⏳ ᴄᴏɴᴠᴇʀᴛɪɴɢ ᴇᴀᴛ ᴛᴏᴋᴇɴ...")
        
        token = eat_to_token(eat_token)
        
        bot.delete_message(message.chat.id, msg.message_id)
        
        if token:
            use_free_trial(user_id)
            _send_pe(message.chat.id, f"""
✅ ═══《 ✅ ᴛᴏᴋᴇɴ ɢᴇɴᴇʀᴀᴛᴇᴅ 》═══ ✅

✅ 🎯 ᴀᴄᴄᴇss ᴛᴏᴋᴇɴ:

✅ <code>{token}</code>

✅ ═══════════════════════ ✅
""", parse_mode="HTML")
        else:
            _send_pe(message.chat.id, f"""
❌ ═══《 ❌ ᴄᴏɴᴠᴇʀsɪᴏɴ ғᴀɪʟᴇᴅ 》═══ ❌

❌ ᴄᴏᴜʟᴅ ɴᴏᴛ ᴄᴏɴᴠᴇʀᴛ ᴇᴀᴛ ᴛᴏᴋᴇɴ!

❌ ᴄʜᴇᴄᴋ ʏᴏᴜʀ ᴇᴀᴛ ᴛᴏᴋᴇɴ.

❌ ═══════════════════════ ❌
""")
    except Exception as e:
        print(f"❌ Process eat error: {e}")

# ============================================================
# FREE TRIAL & UNLIMITED
# ============================================================

@bot.message_handler(func=lambda m: m.text and stylish_text("FREE TRIAL") in m.text)
def free_trial_cmd(message):
    try:
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
            _send_pe(message.chat.id, f"⚠️ ғʀᴇᴇ ᴛʀɪᴀʟ ᴜsᴇᴅ!\n💰 ᴘᴀʏ ғᴏʀ ᴜɴʟɪᴍɪᴛᴇᴅ")
            send_payment_qr(message.chat.id, "unlimited")
            return
        
        _send_pe(message.chat.id, f"🆓 ғʀᴇᴇ ᴛʀɪᴀʟ ᴀᴄᴛɪᴠᴀᴛᴇᴅ!\n✅ ᴜsᴇ ᴀɴʏ ғᴇᴀᴛᴜʀᴇ ᴏɴᴄᴇ!")
    except Exception as e:
        print(f"❌ Free trial error: {e}")

@bot.message_handler(func=lambda m: m.text and stylish_text("UNLIMITED") in m.text)
def unlimited_cmd(message):
    try:
        user_id = message.from_user.id
        user = get_user(user_id)
        
        if user and user.get("unlimited", False):
            _send_pe(message.chat.id, f"✅ ᴀʟʀᴇᴀᴅʏ ᴜɴʟɪᴍɪᴛᴇᴅ!")
            return
        
        send_payment_qr(message.chat.id, "unlimited")
    except Exception as e:
        print(f"❌ Unlimited error: {e}")

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
            "guest_token": settings.get("guest_token_price", 0),
            "eat_token": settings.get("eat_token_price", 0),
            "unlimited": 199,
        }
        price = prices.get(feature, 99)
        
        if price == 0:
            _send_pe(chat_id, f"✅ ᴛʜɪs ғᴇᴀᴛᴜʀᴇ ɪs ғʀᴇᴇ!")
            return
        
        qr_url = f"https://api.qrserver.com/v1/create-qr-code/?size=300x300&data=upi://pay?pa={upi}&am={price}&cu=INR"
        
        text = f"""
✅ ═══《 💰 ᴘᴀʏᴍᴇɴᴛ 》═══ ✅

✅ 💳 ᴜᴘɪ: {upi}
✅ 💰 ᴀᴍᴏᴜɴᴛ: ʀs.{price}
✅ 📌 ғᴇᴀᴛᴜʀᴇ: {feature.upper()}

✅ ═══════════════════════ ✅

✅ 📱 sᴄᴀɴ ǫʀ ᴛᴏ ᴘᴀʏ

✅ ═══════════════════════ ✅

`{upi}`
"""
        
        keyboard = [
            [make_green_button("ɪ ʜᴀᴠᴇ ᴘᴀɪᴅ", callback=f"paid_{feature}")],
            [make_red_button("ᴄᴀɴᴄᴇʟ", callback="cancel_payment")]
        ]
        markup = InlineKeyboardMarkup(keyboard)
        
        try:
            bot.send_photo(chat_id, photo=qr_url, caption=text, reply_markup=markup)
        except:
            _send_pe(chat_id, text, reply_markup=markup)
    except Exception as e:
        print(f"❌ Payment QR error: {e}")

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
        
        _send_pe(chat_id, f"📸 sᴇɴᴅ sᴄʀᴇᴇɴsʜᴏᴛ!")
        bot.register_next_step_handler(call.message, receive_payment_screenshot, feature)
        bot.answer_callback_query(call.id)
    except Exception as e:
        print(f"❌ Paid callback error: {e}")

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
            
            _send_pe(message.chat.id, f"✅ ʀᴇᴄᴇɪᴠᴇᴅ!\n⏳ ᴡᴀɪᴛ ғᴏʀ ᴀᴅᴍɪɴ")
            
            admin_text = f"""
✅ ═══《 💰 ɴᴇᴡ ᴘᴀʏᴍᴇɴᴛ 》═══ ✅

✅ 👤 {message.from_user.first_name}
✅ 🆔 {user_id}
✅ 👾 @{message.from_user.username or 'N/A'}
✅ 📌 ғᴇᴀᴛᴜʀᴇ: {feature}

✅ ═══════════════════════ ✅
"""
            keyboard = [
                [make_green_button("✅ ᴀᴘᴘʀᴏᴠᴇ", callback=f"admin_approve_{user_id}_{feature}")],
                [make_red_button("❌ ʀᴇᴊᴇᴄᴛ", callback=f"admin_reject_{user_id}")]
            ]
            markup = InlineKeyboardMarkup(keyboard)
            
            for admin in ADMIN_IDS:
                try:
                    bot.send_photo(admin, photo=file_id, caption=admin_text, reply_markup=markup)
                except:
                    bot.send_message(admin, admin_text, reply_markup=markup)
        else:
            _send_pe(message.chat.id, f"❌ sᴇɴᴅ ᴀ ᴘʜᴏᴛᴏ!")
    except Exception as e:
        print(f"❌ Screenshot receive error: {e}")

@bot.callback_query_handler(func=lambda c: c.data and c.data.startswith("admin_approve_"))
def admin_approve_callback(call):
    try:
        if not is_admin(call.from_user.id):
            _send_pe(call.message.chat.id, f"❌ ᴜɴᴀᴜᴛʜᴏʀɪᴢᴇᴅ!")
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
        
        _send_pe(call.message.chat.id, f"✅ ᴜsᴇʀ {user_id} ᴀᴘᴘʀᴏᴠᴇᴅ ғᴏʀ {feature}!")
        
        try:
            bot.send_message(user_id, f"✅ ᴄᴏɴɢʀᴀᴛs! ᴜɴʟɪᴍɪᴛᴇᴅ {feature} ᴀᴄᴄᴇss! 🎉")
        except:
            pass
        
        bot.answer_callback_query(call.id)
    except Exception as e:
        print(f"❌ Admin approve error: {e}")

@bot.callback_query_handler(func=lambda c: c.data == "cancel_payment")
def cancel_payment_callback(call):
    try:
        bot.delete_message(call.message.chat.id, call.message.message_id)
    except:
        pass
    _send_pe(call.message.chat.id, f"✅ ᴄᴀɴᴄᴇʟʟᴇᴅ!")
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
            _send_pe(call.message.chat.id, f"❌ ʙᴀɴɴᴇᴅ!")
            return
        
        price = get_price("ban")
        if price > 0 and not user.get("unlimited", False):
            uses = user.get("uses", 0)
            if uses >= 1:
                _send_pe(call.message.chat.id, f"⚠️ ᴜsᴇᴅ!\n💰 ᴘᴀʏ ʀs.{price}")
                send_payment_qr(call.message.chat.id, "ban")
                bot.answer_callback_query(call.id)
                return
        
        _send_pe(call.message.chat.id, f"🔑 sᴇɴᴅ ᴛᴏᴋᴇɴ:")
        bot.register_next_step_handler(call.message, process_ban_token)
        bot.answer_callback_query(call.id)
    except Exception as e:
        print(f"❌ Ban another error: {e}")

@bot.callback_query_handler(func=lambda c: c.data == "check_another")
def check_another_callback(call):
    try:
        user_id = call.from_user.id
        user = get_user(user_id)
        if not user or user.get("banned", False):
            _send_pe(call.message.chat.id, f"❌ ʙᴀɴɴᴇᴅ!")
            return
        
        price = get_price("ban_check")
        if price > 0 and not user.get("unlimited", False):
            uses = user.get("uses", 0)
            if uses >= 1:
                _send_pe(call.message.chat.id, f"⚠️ ᴜsᴇᴅ!\n💰 ᴘᴀʏ ʀs.{price}")
                send_payment_qr(call.message.chat.id, "ban_check")
                bot.answer_callback_query(call.id)
                return
        
        _send_pe(call.message.chat.id, f"🔍 sᴇɴᴅ ᴜɪᴅ:")
        bot.register_next_step_handler(call.message, process_ban_check)
        bot.answer_callback_query(call.id)
    except Exception as e:
        print(f"❌ Check another error: {e}")

@bot.callback_query_handler(func=lambda c: c.data == "get_unlimited")
def get_unlimited_callback(call):
    try:
        send_payment_qr(call.message.chat.id, "unlimited")
        bot.answer_callback_query(call.id)
    except Exception as e:
        print(f"❌ Get unlimited error: {e}")

# ============================================================
# SUPPORT, ABOUT, HELP, HOW TO GET TOKEN
# ============================================================

@bot.message_handler(func=lambda m: m.text and stylish_text("SUPPORT") in m.text)
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
        [make_green_button("ᴄᴏɴᴛᴀᴄᴛ", url=f"https://t.me/{support.replace('@', '')}")]
    ])
    _send_pe(message.chat.id, text, reply_markup=markup)

@bot.message_handler(func=lambda m: m.text and stylish_text("ABOUT") in m.text)
def about_cmd(message):
    settings = load_settings()
    developer = settings.get("developer", "@iflexzyan")
    
    text = f"""
✅ ═══《 ℹ️ ᴀʙᴏᴜᴛ 》═══ ✅

✅ 🤖 ғғ ʙᴀɴ ʙᴏᴛ

✅ 🔫 ʙᴀɴ ᴀᴄᴄᴏᴜɴᴛs
✅ 🔍 ᴄʜᴇᴄᴋ ʙᴀɴ ɪɴғᴏ
✅ 🔄 ʀᴇᴠᴏᴋᴇ ᴛᴏᴋᴇɴ
✅ 👤 ɢᴜᴇsᴛ ᴛᴏ ᴛᴏᴋᴇɴ
✅ 🍽️ ᴇᴀᴛ ᴛᴏ ᴛᴏᴋᴇɴ

✅ 👨‍💻 {developer}
"""
    _send_pe(message.chat.id, text)

@bot.message_handler(func=lambda m: m.text and stylish_text("HELP") in m.text)
def help_cmd(message):
    text = f"""
✅ ═══《 ❓ ʜᴇʟᴘ 》═══ ✅

✅ ᴀᴠᴀɪʟᴀʙʟᴇ ғᴇᴀᴛᴜʀᴇs:

✅ 𝟷️⃣ ʙᴀɴ ᴀᴄᴄᴏᴜɴᴛ - ᴀᴄᴄᴇss ᴛᴏᴋᴇɴ sᴇ ʙᴀɴ
✅ 𝟸️⃣ ᴄʜᴇᴄᴋ ʙᴀɴ ɪɴғᴏ - ᴜɪᴅ sᴇ ʙᴀɴ sᴛᴀᴛᴜs
✅ 𝟹️⃣ ʀᴇᴠᴏᴋᴇ ᴛᴏᴋᴇɴ - ᴀᴄᴄᴇss ᴛᴏᴋᴇɴ ʀᴇᴠᴏᴋᴇ
✅ 𝟺️⃣ ɢᴜᴇsᴛ ᴛᴏ ᴛᴏᴋᴇɴ - ᴜɪᴅ+ᴘᴀss ᴛᴏ ᴛᴏᴋᴇɴ
✅ 𝟻️⃣ ᴇᴀᴛ ᴛᴏ ᴛᴏᴋᴇɴ - ᴇᴀᴛ ᴛᴏ ᴀᴄᴄᴇss ᴛᴏᴋᴇɴ

✅ ═══════════════════ ✅

✅ 🆓 ғʀᴇᴇ ᴛʀɪᴀʟ: 𝟷 ᴜsᴇ
✅ 💰 ᴜɴʟɪᴍɪᴛᴇᴅ: ᴘᴀʏ & ɢᴇᴛ

✅ ═══════════════════ ✅
"""
    _send_pe(message.chat.id, text)

@bot.message_handler(func=lambda m: m.text and stylish_text("HOW TO GET TOKEN") in m.text)
def how_to_get_token(message):
    settings = load_settings()
    token_text = settings.get("token_text", "1️⃣ Open Free Fire\n2️⃣ Go to Settings\n3️⃣ Click Account\n4️⃣ Find Data Access\n5️⃣ Copy Token")
    
    _send_pe(message.chat.id, f"""
✅ ═══《 🔑 ʜᴏᴡ ᴛᴏ ɢᴇᴛ ᴛᴏᴋᴇɴ 》═══ ✅

✅ {token_text}

✅ ═══════════════════════ ✅
""")
    
    if os.path.exists("token_video.mp4"):
        with open("token_video.mp4", "rb") as f:
            bot.send_video(message.chat.id, f, caption=f"✅ ᴠɪᴅᴇᴏ ɢᴜɪᴅᴇ")

# ============================================================
# ADMIN COMMANDS - PRICES
# ============================================================

@bot.message_handler(func=lambda m: m.text and stylish_text("BAN PRICE") in m.text)
def ban_price_btn(message):
    settings = load_settings()
    _send_pe(message.chat.id, f"✅ 💰 ʙᴀɴ ᴘʀɪᴄᴇ: ʀs.{settings.get('ban_price', 29)}\n✅ /banprice <ᴀᴍᴛ>")

@bot.message_handler(commands=['banprice'])
def banprice_cmd(message):
    if not is_admin(message.from_user.id):
        _send_pe(message.chat.id, f"❌ ᴜɴᴀᴜᴛʜᴏʀɪᴢᴇᴅ!")
        return
    parts = message.text.split()
    if len(parts) < 2:
        return
    try:
        price = int(parts[1])
        settings = load_settings()
        settings["ban_price"] = price
        save_settings(settings)
        _send_pe(message.chat.id, f"✅ ʙᴀɴ ᴘʀɪᴄᴇ: ʀs.{price}!")
    except:
        _send_pe(message.chat.id, f"❌ ɪɴᴠᴀʟɪᴅ!")

@bot.message_handler(func=lambda m: m.text and stylish_text("CHECK PRICE") in m.text)
def check_price_btn(message):
    settings = load_settings()
    _send_pe(message.chat.id, f"✅ 🔍 ᴄʜᴇᴄᴋ ᴘʀɪᴄᴇ: ʀs.{settings.get('ban_check_price', 0)}\n✅ /checkprice <ᴀᴍᴛ>")

@bot.message_handler(commands=['checkprice'])
def checkprice_cmd(message):
    if not is_admin(message.from_user.id):
        _send_pe(message.chat.id, f"❌ ᴜɴᴀᴜᴛʜᴏʀɪᴢᴇᴅ!")
        return
    parts = message.text.split()
    if len(parts) < 2:
        return
    try:
        price = int(parts[1])
        settings = load_settings()
        settings["ban_check_price"] = price
        save_settings(settings)
        _send_pe(message.chat.id, f"✅ ᴄʜᴇᴄᴋ ᴘʀɪᴄᴇ: ʀs.{price}!")
    except:
        _send_pe(message.chat.id, f"❌ ɪɴᴠᴀʟɪᴅ!")

@bot.message_handler(func=lambda m: m.text and stylish_text("REVOKE PRICE") in m.text)
def revoke_price_btn(message):
    settings = load_settings()
    _send_pe(message.chat.id, f"✅ 🔄 ʀᴇᴠᴏᴋᴇ ᴘʀɪᴄᴇ: ʀs.{settings.get('revoke_price', 0)}\n✅ /revokeprice <ᴀᴍᴛ>")

@bot.message_handler(commands=['revokeprice'])
def revokeprice_cmd(message):
    if not is_admin(message.from_user.id):
        _send_pe(message.chat.id, f"❌ ᴜɴᴀᴜᴛʜᴏʀɪᴢᴇᴅ!")
        return
    parts = message.text.split()
    if len(parts) < 2:
        return
    try:
        price = int(parts[1])
        settings = load_settings()
        settings["revoke_price"] = price
        save_settings(settings)
        _send_pe(message.chat.id, f"✅ ʀᴇᴠᴏᴋᴇ ᴘʀɪᴄᴇ: ʀs.{price}!")
    except:
        _send_pe(message.chat.id, f"❌ ɪɴᴠᴀʟɪᴅ!")

@bot.message_handler(func=lambda m: m.text and stylish_text("GUEST PRICE") in m.text)
def guest_price_btn(message):
    settings = load_settings()
    _send_pe(message.chat.id, f"✅ 👤 ɢᴜᴇsᴛ ᴘʀɪᴄᴇ: ʀs.{settings.get('guest_token_price', 0)}\n✅ /guestprice <ᴀᴍᴛ>")

@bot.message_handler(commands=['guestprice'])
def guestprice_cmd(message):
    if not is_admin(message.from_user.id):
        _send_pe(message.chat.id, f"❌ ᴜɴᴀᴜᴛʜᴏʀɪᴢᴇᴅ!")
        return
    parts = message.text.split()
    if len(parts) < 2:
        return
    try:
        price = int(parts[1])
        settings = load_settings()
        settings["guest_token_price"] = price
        save_settings(settings)
        _send_pe(message.chat.id, f"✅ ɢᴜᴇsᴛ ᴘʀɪᴄᴇ: ʀs.{price}!")
    except:
        _send_pe(message.chat.id, f"❌ ɪɴᴠᴀʟɪᴅ!")

@bot.message_handler(func=lambda m: m.text and stylish_text("EAT PRICE") in m.text)
def eat_price_btn(message):
    settings = load_settings()
    _send_pe(message.chat.id, f"✅ 🍽️ ᴇᴀᴛ ᴘʀɪᴄᴇ: ʀs.{settings.get('eat_token_price', 0)}\n✅ /eatprice <ᴀᴍᴛ>")

@bot.message_handler(commands=['eatprice'])
def eatprice_cmd(message):
    if not is_admin(message.from_user.id):
        _send_pe(message.chat.id, f"❌ ᴜɴᴀᴜᴛʜᴏʀɪᴢᴇᴅ!")
        return
    parts = message.text.split()
    if len(parts) < 2:
        return
    try:
        price = int(parts[1])
        settings = load_settings()
        settings["eat_token_price"] = price
        save_settings(settings)
        _send_pe(message.chat.id, f"✅ ᴇᴀᴛ ᴘʀɪᴄᴇ: ʀs.{price}!")
    except:
        _send_pe(message.chat.id, f"❌ ɪɴᴠᴀʟɪᴅ!")

# ============================================================
# OTHER ADMIN COMMANDS
# ============================================================

@bot.message_handler(func=lambda m: m.text and stylish_text("UPI") in m.text)
def upi_btn(message):
    _send_pe(message.chat.id, f"✅ 🏦 ᴄᴜʀʀᴇɴᴛ: {load_settings().get('upi', 'vanshx111@naviaxis')}\n✅ /upi <ɴᴇᴡ>")

@bot.message_handler(commands=['upi'])
def upi_cmd(message):
    if not is_admin(message.from_user.id):
        _send_pe(message.chat.id, f"❌ ᴜɴᴀᴜᴛʜᴏʀɪᴢᴇᴅ!")
        return
    parts = message.text.split()
    if len(parts) < 2:
        return
    upi = parts[1]
    settings = load_settings()
    settings["upi"] = upi
    save_settings(settings)
    _send_pe(message.chat.id, f"✅ ᴜᴘɪ: {upi}!")

@bot.message_handler(func=lambda m: m.text and stylish_text("ADD ADMIN") in m.text)
def add_admin_btn(message):
    _send_pe(message.chat.id, f"✅ /addadmin ɪᴅ")

@bot.message_handler(commands=['addadmin'])
def add_admin_cmd(message):
    if not is_admin(message.from_user.id):
        _send_pe(message.chat.id, f"❌ ᴜɴᴀᴜᴛʜᴏʀɪᴢᴇᴅ!")
        return
    parts = message.text.split()
    if len(parts) < 2:
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
        bot.send_document(message.chat.id, f, caption=f"✅ 📥 ᴅᴀᴛᴀ ᴇxᴘᴏʀᴛ")

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
        bot.send_message(user_id, f"📢 {msg}")
        _send_pe(message.chat.id, f"✅ sᴇɴᴛ!")
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
    sent = 0
    failed = 0
    for user_id in users.keys():
        try:
            bot.send_message(int(user_id), f"📢 {msg}")
            sent += 1
            time.sleep(0.05)
        except:
            failed += 1
    _send_pe(message.chat.id, f"""
✅ ᴄᴏᴍᴘʟᴇᴛᴇ!

✅ sᴇɴᴛ: {sent}
✅ ғᴀɪʟᴇᴅ: {failed}
""")

# ============================================================
# FLASK WEBHOOK - PORT FIX
# ============================================================

@app.route('/', methods=['GET'])
def index():
    return "✅ FF BAN BOT is running on Render!"

@app.route(f'/{BOT_TOKEN}', methods=['POST'])
def webhook():
    try:
        if request.headers.get('content-type') == 'application/json':
            json_string = request.get_data().decode('utf-8')
            update = types.Update.de_json(json_string)
            bot.process_new_updates([update])
            return '', 200
    except Exception as e:
        print(f"❌ Webhook error: {e}")
    return '', 403

# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":
    print("✅ ʙᴏᴛ sᴛᴀʀᴛᴇᴅ!")
    print(f"✅ ᴏᴡɴᴇʀ: {OWNER_ID}")
    print(f"✅ ᴜsᴇʀs: {len(load_users())}")
    print(f"✅ ᴀᴅᴍɪɴs: {len(ADMIN_IDS)}")
    
    try:
        bot.remove_webhook()
        print("✅ ᴡᴇʙʜᴏᴏᴋ ʀᴇᴍᴏᴠᴇᴅ!")
    except Exception as e:
        print(f"⚠️ {e}")
    
    try:
        hostname = os.environ.get('RENDER_EXTERNAL_HOSTNAME')
        if hostname:
            webhook_url = f"https://{hostname}/{BOT_TOKEN}"
            bot.set_webhook(url=webhook_url)
            print(f"✅ ᴡᴇʙʜᴏᴏᴋ sᴇᴛ: {webhook_url}")
        else:
            print("⚠️ ɴᴏ ʜᴏsᴛɴᴀᴍᴇ, ᴜsɪɴɢ ᴘᴏʟʟɪɴɢ")
            bot.infinity_polling()
            exit()
    except Exception as e:
        print(f"⚠️ {e}, ғᴀʟʟɪɴɢ ʙᴀᴄᴋ ᴛᴏ ᴘᴏʟʟɪɴɢ")
        bot.infinity_polling()
        exit()
    
    app.run(host='0.0.0.0', port=PORT)