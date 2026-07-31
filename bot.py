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

# Primary emojis list
PRIMARY_EMOJIS = [
    "6035338338406242050", "6032673796530377389", "6035243995154616907",
    "6035179291472302298", "6035137110598492010", "6035374291577475270",
    "6035372401791864953", "6035355642829475999", "6035051267087143217",
    "6034945975963881533", "6035169816774446606", "6035085583875837709",
    "6035081585261287115", "6035210301136182368", "6035317340311129897",
    "6035072209347678547", "6035225389356290238", "6035173858338672933"
]

PLACEHOLDER = "🌟"
DEFAULT_EMOJI_ID = "6035338338406242050"

# ============================================================
# STYLISH FONT CONVERTER
# ============================================================
def stylish_text(text: str) -> str:
    """Convert normal text to stylish font (𝐀 𝐁 𝐂...)"""
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
    """Get verified emoji ID from fallback emoji"""
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
# MAKE BUTTONS WITH VERIFIED EMOJIS & STYLES
# ============================================================
def make_verified_button(text: str, style: str = None, callback: str = None, url: str = None):
    """Create button with stylish text + verified emojis + color"""
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

def load_users():
    return load_data(USERS_FILE)

def save_users(users):
    save_data(USERS_FILE, users)

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
        "bot_name": "FF 𝐁𝐀𝐍 𝐁𝐎𝐓",
        "developer": "@iflexzyan",
        "support": "@iflexzyan"
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
        notify_owner(f"✅ 𝐍𝐞𝐰 𝐔𝐬𝐞𝐫 𝐉𝐨𝐢𝐧𝐞𝐝!\n👤 𝐈𝐃: {user_id}\n👾 @{username or 'N/A'}")
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
            KeyboardButton("🔴 𝐁𝐎𝐓 𝐎𝐅𝐅"),
            KeyboardButton("🟢 𝐁𝐎𝐓 𝐎𝐍")
        )
        markup.row(
            KeyboardButton("👑 𝐀𝐃𝐌𝐈𝐍 𝐏𝐀𝐍𝐄𝐋"),
            KeyboardButton("📊 𝐒𝐓𝐀𝐓𝐒")
        )
        markup.row(
            KeyboardButton("👥 𝐔𝐒𝐄𝐑𝐒"),
            KeyboardButton("📥 𝐃𝐀𝐓𝐀")
        )
        markup.row(
            KeyboardButton("💳 𝐏𝐑𝐈𝐂𝐄"),
            KeyboardButton("🏦 𝐔𝐏𝐈")
        )
        markup.row(
            KeyboardButton("➕ 𝐀𝐃𝐃 𝐀𝐃𝐌𝐈𝐍"),
            KeyboardButton("📋 𝐂𝐋𝐎𝐍𝐄")
        )
        markup.row(
            KeyboardButton("❓ 𝐇𝐎𝐖 𝐓𝐎 𝐆𝐄𝐓 𝐓𝐎𝐊𝐄𝐍"),
            KeyboardButton("💎 𝐂𝐋𝐎𝐍𝐄 𝐏𝐑𝐈𝐂𝐄")
        )
    else:
        markup.row(KeyboardButton("🔫 𝐁𝐀𝐍 𝐀𝐂𝐂𝐎𝐔𝐍𝐓"))
        markup.row(
            KeyboardButton("🆓 𝐅𝐑𝐄𝐄 𝐓𝐑𝐈𝐀𝐋"),
            KeyboardButton("💎 𝐔𝐍𝐋𝐈𝐌𝐈𝐓𝐄𝐃")
        )
        markup.row(
            KeyboardButton("❓ 𝐇𝐎𝐖 𝐓𝐎 𝐆𝐄𝐓 𝐓𝐎𝐊𝐄𝐍"),
            KeyboardButton("📋 𝐂𝐋𝐎𝐍𝐄 𝐁𝐎𝐓")
        )
    
    markup.row(
        KeyboardButton("❓ 𝐇𝐄𝐋𝐏"),
        KeyboardButton("ℹ️ 𝐀𝐁𝐎𝐔𝐓")
    )
    markup.row(KeyboardButton("📞 𝐒𝐔𝐏𝐏𝐎𝐑𝐓"))
    
    return markup

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
        _send_pe(message.chat.id, f"❌ 𝐘𝐨𝐮 𝐚𝐫𝐞 𝐁𝐀𝐍𝐍𝐄𝐃 𝐟𝐫𝐨𝐦 𝐮𝐬𝐢𝐧𝐠 𝐭𝐡𝐢𝐬 𝐛𝐨𝐭!")
        return
    
    try:
        bot.send_photo(
            message.chat.id,
            photo="https://iili.io/C8DNTyQ.jpg",
            caption=f"🌟 𝐖𝐞𝐥𝐜𝐨𝐦𝐞 𝐭𝐨 𝐅𝐅 𝐁𝐀𝐍 𝐁𝐎𝐓!"
        )
    except:
        pass
    
    welcome_text = f"""
✅ ═══《 🔥 𝐖𝐄𝐋𝐂𝐎𝐌𝐄 𝐓𝐎 𝐅𝐅 𝐁𝐀𝐍 𝐁𝐎𝐓 》═══ ✅

✅ 👤 𝐔𝐬𝐞𝐫: {first_name}
✅ 🆔 𝐈𝐃: {user_id}
✅ 👾 𝐔𝐬𝐞𝐫𝐧𝐚𝐦𝐞: @{username or 'N/A'}

✅ ═══════════════════════ ✅

✅ 🎯 𝟏 𝐅𝐑𝐄𝐄 𝐓𝐑𝐈𝐀𝐋 - 𝐁𝐚𝐧 𝟏 𝐀𝐜𝐜𝐨𝐮𝐧𝐭
✅ 💰 𝐔𝐍𝐋𝐈𝐌𝐈𝐓𝐄𝐃 𝐀𝐜𝐜𝐞𝐬𝐬 - 𝐑𝐬.{price}

✅ ═══════════════════════ ✅

✅ 👨‍💻 𝐃𝐞𝐯𝐞𝐥𝐨𝐩𝐞𝐫: {developer}

✅ ═══════════════════════ ✅
"""
    
    markup = get_menu(user_id)
    _send_pe(message.chat.id, welcome_text, reply_markup=markup)

@bot.message_handler(commands=['help'])
def help_cmd(message):
    user_id = message.from_user.id
    markup = get_menu(user_id)
    
    help_text = f"""
✅ ═══《 ❓ 𝐇𝐄𝐋𝐏 》═══ ✅

✅ 𝐇𝐨𝐰 𝐭𝐨 𝐔𝐬𝐞:

✅ 𝟏️⃣ 𝐂𝐥𝐢𝐜𝐤 𝐁𝐀𝐍 𝐀𝐂𝐂𝐎𝐔𝐍𝐓
✅ 𝟐️⃣ 𝐒𝐞𝐧𝐝 𝐀𝐜𝐜𝐞𝐬𝐬 𝐓𝐨𝐤𝐞𝐧
✅ 𝟑️⃣ 𝐀𝐜𝐜𝐨𝐮𝐧𝐭 𝐰𝐢𝐥𝐥 𝐛𝐞 𝐛𝐚𝐧𝐧𝐞𝐝
✅ 𝟒️⃣ 𝐆𝐞𝐭 𝐑𝐞𝐬𝐮𝐥𝐭!

✅ ═══════════════════ ✅

✅ 🆓 𝐅𝐑𝐄𝐄 𝐓𝐑𝐈𝐀𝐋: 𝟏 𝐁𝐚𝐧
✅ 💰 𝐔𝐍𝐋𝐈𝐌𝐈𝐓𝐄𝐃: 𝐏𝐚𝐲 & 𝐆𝐞𝐭

✅ ═══════════════════ ✅

✅ 👨‍💻 𝐃𝐞𝐯𝐞𝐥𝐨𝐩𝐞𝐫: @iflexzyan
"""
    _send_pe(message.chat.id, help_text, reply_markup=markup)

# ============================================================
# HOW TO GET TOKEN - VIDEO
# ============================================================
TOKEN_VIDEO_FILE = "token_video.mp4"

@bot.message_handler(commands=['addtokenvideo'])
def add_token_video(message):
    if not is_admin(message.from_user.id):
        _send_pe(message.chat.id, f"❌ 𝐔𝐧𝐚𝐮𝐭𝐡𝐨𝐫𝐢𝐳𝐞𝐝!")
        return
    
    _send_pe(message.chat.id, f"📤 𝐒𝐞𝐧𝐝 𝐦𝐞 𝐭𝐡𝐞 𝐯𝐢𝐝𝐞𝐨 𝐟𝐨𝐫 '𝐇𝐎𝐖 𝐓𝐎 𝐆𝐄𝐓 𝐓𝐎𝐊𝐄𝐍'")
    bot.register_next_step_handler(message, save_token_video)

def save_token_video(message):
    if message.video:
        file_info = bot.get_file(message.video.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        with open(TOKEN_VIDEO_FILE, 'wb') as f:
            f.write(downloaded_file)
        _send_pe(message.chat.id, f"✅ 𝐕𝐢𝐝𝐞𝐨 𝐬𝐚𝐯𝐞𝐝 𝐬𝐮𝐜𝐜𝐞𝐬𝐬𝐟𝐮𝐥𝐥𝐲!")
    else:
        _send_pe(message.chat.id, f"❌ 𝐏𝐥𝐞𝐚𝐬𝐞 𝐬𝐞𝐧𝐝 𝐚 𝐯𝐢𝐝𝐞𝐨!")

@bot.message_handler(func=lambda m: m.text and "𝐇𝐎𝐖 𝐓𝐎 𝐆𝐄𝐓 𝐓𝐎𝐊𝐄𝐍" in m.text)
def how_to_get_token(message):
    if os.path.exists(TOKEN_VIDEO_FILE):
        with open(TOKEN_VIDEO_FILE, 'rb') as f:
            bot.send_video(message.chat.id, f, caption=f"✅ 𝐇𝐨𝐰 𝐭𝐨 𝐆𝐞𝐭 𝐀𝐜𝐜𝐞𝐬𝐬 𝐓𝐨𝐤𝐞𝐧")
    else:
        text = f"""
✅ ═══《 ❓ 𝐇𝐎𝐖 𝐓𝐎 𝐆𝐄𝐓 𝐓𝐎𝐊𝐄𝐍 》═══ ✅

✅ 𝟏️⃣ 𝐎𝐩𝐞𝐧 𝐅𝐫𝐞𝐞 𝐅𝐢𝐫𝐞 𝐆𝐚𝐦𝐞
✅ 𝟐️⃣ 𝐆𝐨 𝐭𝐨 𝐒𝐞𝐭𝐭𝐢𝐧𝐠𝐬 ⚙️
✅ 𝟑️⃣ 𝐂𝐥𝐢𝐜𝐤 𝐨𝐧 𝐀𝐜𝐜𝐨𝐮𝐧𝐭
✅ 𝟒️⃣ 𝐅𝐢𝐧𝐝 "𝐃𝐚𝐭𝐚 𝐀𝐜𝐜𝐞𝐬𝐬"
✅ 𝟓️⃣ 𝐂𝐨𝐩𝐲 𝐀𝐜𝐜𝐞𝐬𝐬 𝐓𝐨𝐤𝐞𝐧

✅ ═══════════════════════ ✅
"""
        _send_pe(message.chat.id, text)

# ============================================================
# BAN ACCOUNT
# ============================================================

@bot.message_handler(func=lambda m: m.text and "𝐁𝐀𝐍 𝐀𝐂𝐂𝐎𝐔𝐍𝐓" in m.text)
def ban_account_start(message):
    user_id = message.from_user.id
    user = get_user(user_id)
    
    if not user or user.get("banned", False):
        _send_pe(message.chat.id, f"❌ 𝐘𝐨𝐮 𝐚𝐫𝐞 𝐁𝐀𝐍𝐍𝐄𝐃!")
        return
    
    if not user.get("unlimited", False):
        uses = user.get("uses", 0)
        if uses >= 1:
            _send_pe(message.chat.id, f"⚠️ 𝐅𝐫𝐞𝐞 𝐓𝐫𝐢𝐚𝐥 𝐔𝐬𝐞𝐝!\n💰 𝐏𝐚𝐲 𝐑𝐬.{load_settings().get('price', 99)} 𝐟𝐨𝐫 𝐔𝐍𝐋𝐈𝐌𝐈𝐓𝐄𝐃")
            send_payment_qr(message.chat.id)
            return
    
    _send_pe(message.chat.id, f"🔑 𝐒𝐞𝐧𝐝 𝐦𝐞 𝐭𝐡𝐞 𝐀𝐜𝐜𝐞𝐬𝐬 𝐓𝐨𝐤𝐞𝐧 𝐭𝐨 𝐁𝐚𝐧!")
    bot.register_next_step_handler(message, process_ban_token)

def process_ban_token(message):
    user_id = message.from_user.id
    token = message.text.strip()
    
    if len(token) < 30:
        _send_pe(message.chat.id, f"❌ 𝐈𝐧𝐯𝐚𝐥𝐢𝐝 𝐓𝐨𝐤𝐞𝐧! 𝐏𝐥𝐞𝐚𝐬𝐞 𝐬𝐞𝐧𝐝 𝐜𝐨𝐫𝐫𝐞𝐜𝐭 𝐀𝐜𝐜𝐞𝐬𝐬 𝐓𝐨𝐤𝐞𝐧.")
        return
    
    msg = _send_pe_return(message.chat.id, f"⏳ 𝐁𝐚𝐧𝐧𝐢𝐧𝐠 𝐀𝐜𝐜𝐨𝐮𝐧𝐭... 𝐏𝐥𝐞𝐚𝐬𝐞 𝐖𝐚𝐢𝐭!")
    
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
✅ ═══《 ✅ 𝐀𝐂𝐂𝐎𝐔𝐍𝐓 𝐁𝐀𝐍𝐍𝐄𝐃 》═══ ✅

✅ 🎯 𝐀𝐂𝐂𝐎𝐔𝐍𝐓 𝐁𝐀𝐍 𝐒𝐔𝐂𝐂𝐄𝐒𝐒𝐅𝐔𝐋!

✅ ═══════════════════════ ✅

✅ 🆔 𝐈𝐃: {account_id}
✅ 👤 𝐍𝐀𝐌𝐄: {account_name}
✅ 🔢 𝐔𝐈𝐃: {account_uid}

✅ ═══════════════════════ ✅

✅ 👨‍💻 𝐃𝐞𝐯𝐞𝐥𝐨𝐩𝐞𝐫: @iflexzyan

✅ ═══════════════════════ ✅
"""
            keyboard = [
                [make_green_button("𝐁𝐀𝐍 𝐀𝐍𝐎𝐓𝐇𝐄𝐑", callback="ban_another")],
                [make_blue_button("𝐆𝐄𝐓 𝐔𝐍𝐋𝐈𝐌𝐈𝐓𝐄𝐃", callback="get_unlimited")],
                [make_red_button("𝐒𝐔𝐏𝐏𝐎𝐑𝐓", callback="support_contact")]
            ]
            markup = InlineKeyboardMarkup(keyboard)
            _send_pe(message.chat.id, result_text, reply_markup=markup)
            
            notify_owner(f"✅ 𝐀𝐜𝐜𝐨𝐮𝐧𝐭 𝐁𝐚𝐧𝐧𝐞𝐝!\n👤 𝐔𝐬𝐞𝐫: {user_id}\n🔢 𝐔𝐈𝐃: {account_uid}")
            
        else:
            result_text = f"""
❌ ═══《 ❌ 𝐁𝐀𝐍 𝐅𝐀𝐈𝐋𝐄𝐃 》═══ ❌

❌ 𝐀𝐂𝐂𝐎𝐔𝐍𝐓 𝐍𝐎𝐓 𝐁𝐀𝐍𝐍𝐄𝐃!

❌ ═══════════════════════ ❌

❌ 🆔 𝐈𝐃: {account_id}
❌ 👤 𝐍𝐀𝐌𝐄: {account_name}
❌ 🔢 𝐔𝐈𝐃: {account_uid}
❌ 📌 𝐒𝐭𝐚𝐭𝐮𝐬: {status}

❌ ═══════════════════════ ❌

❌ ⚠️ 𝐑𝐞𝐚𝐬𝐨𝐧𝐬:
❌ • 𝐈𝐧𝐯𝐚𝐥𝐢𝐝 𝐓𝐨𝐤𝐞𝐧
❌ • 𝐀𝐥𝐫𝐞𝐚𝐝𝐲 𝐁𝐚𝐧𝐧𝐞𝐝
❌ • 𝐒𝐞𝐫𝐯𝐞𝐫 𝐄𝐫𝐫𝐨𝐫

❌ ═══════════════════════ ❌

❌ 👨‍💻 𝐃𝐞𝐯𝐞𝐥𝐨𝐩𝐞𝐫: @iflexzyan
"""
            _send_pe(message.chat.id, result_text)
            
    except Exception as e:
        bot.delete_message(message.chat.id, msg.message_id)
        _send_pe(message.chat.id, f"❌ 𝐄𝐫𝐫𝐨𝐫: {str(e)}")

# ============================================================
# PAYMENT SYSTEM
# ============================================================

def send_payment_qr(chat_id):
    settings = load_settings()
    upi = settings.get("upi", "vanshx111@naviaxis")
    price = settings.get("price", 99)
    
    qr_url = f"https://api.qrserver.com/v1/create-qr-code/?size=300x300&data=upi://pay?pa={upi}&am={price}&cu=INR"
    
    text = f"""
✅ ═══《 💰 𝐏𝐀𝐘𝐌𝐄𝐍𝐓 》═══ ✅

✅ 💳 𝐔𝐏𝐈: {upi}
✅ 💰 𝐀𝐦𝐨𝐮𝐧𝐭: 𝐑𝐬.{price}

✅ ═══════════════════════ ✅

✅ 📱 𝐒𝐜𝐚𝐧 𝐐𝐑 𝐭𝐨 𝐏𝐚𝐲

✅ ═══════════════════════ ✅
"""
    
    keyboard = [
        [make_green_button("𝐈 𝐇𝐀𝐕𝐄 𝐏𝐀𝐈𝐃", callback=f"paid_{chat_id}")],
        [make_blue_button("𝐒𝐔𝐏𝐏𝐎𝐑𝐓", url="https://t.me/iflexzyan")],
        [make_red_button("𝐂𝐀𝐍𝐂𝐄𝐋", callback="cancel_payment")]
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
    
    _send_pe(chat_id, f"📸 𝐒𝐞𝐧𝐝 𝐦𝐞 𝐭𝐡𝐞 𝐏𝐚𝐲𝐦𝐞𝐧𝐭 𝐒𝐜𝐫𝐞𝐞𝐧𝐬𝐡𝐨𝐭!")
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
        
        _send_pe(message.chat.id, f"✅ 𝐒𝐜𝐫𝐞𝐞𝐧𝐬𝐡𝐨𝐭 𝐑𝐞𝐜𝐞𝐢𝐯𝐞𝐝!\n⏳ 𝐖𝐚𝐢𝐭𝐢𝐧𝐠 𝐟𝐨𝐫 𝐀𝐝𝐦𝐢𝐧 𝐀𝐩𝐩𝐫𝐨𝐯𝐚𝐥.")
        
        admin_text = f"""
✅ ═══《 💰 𝐍𝐄𝐖 𝐏𝐀𝐘𝐌𝐄𝐍𝐓 》═══ ✅

✅ 👤 𝐔𝐬𝐞𝐫: {message.from_user.first_name}
✅ 🆔 𝐈𝐃: {user_id}
✅ 👾 @{message.from_user.username or 'N/A'}

✅ ═══════════════════════ ✅

✅ 📌 𝐔𝐬𝐞: /approve {user_id}
✅ 📌 𝐔𝐬𝐞: /disapprove {user_id}

✅ ═══════════════════════ ✅
"""
        for admin in ADMIN_IDS:
            try:
                bot.send_photo(admin, photo=file_id, caption=admin_text)
            except:
                bot.send_message(admin, admin_text)
    else:
        _send_pe(message.chat.id, f"❌ 𝐏𝐥𝐞𝐚𝐬𝐞 𝐬𝐞𝐧𝐝 𝐚 𝐏𝐇𝐎𝐓𝐎 𝐚𝐬 𝐬𝐜𝐫𝐞𝐞𝐧𝐬𝐡𝐨𝐭!")

# ============================================================
# FREE TRIAL & UNLIMITED
# ============================================================

@bot.message_handler(func=lambda m: m.text and "𝐅𝐑𝐄𝐄 𝐓𝐑𝐈𝐀𝐋" in m.text)
def free_trial_cmd(message):
    user_id = message.from_user.id
    user = get_user(user_id)
    
    if not user:
        _send_pe(message.chat.id, f"❌ 𝐏𝐥𝐞𝐚𝐬𝐞 /start 𝐟𝐢𝐫𝐬𝐭!")
        return
    
    if user.get("unlimited", False):
        _send_pe(message.chat.id, f"✅ 𝐘𝐨𝐮 𝐚𝐥𝐫𝐞𝐚𝐝𝐲 𝐡𝐚𝐯𝐞 𝐔𝐍𝐋𝐈𝐌𝐈𝐓𝐄𝐃 𝐚𝐜𝐜𝐞𝐬𝐬!")
        return
    
    uses = user.get("uses", 0)
    if uses >= 1:
        _send_pe(message.chat.id, f"⚠️ 𝐅𝐫𝐞𝐞 𝐓𝐫𝐢𝐚𝐥 𝐀𝐥𝐫𝐞𝐚𝐝𝐲 𝐔𝐬𝐞𝐝!\n💰 𝐏𝐚𝐲 𝐑𝐬.{load_settings().get('price', 99)} 𝐟𝐨𝐫 𝐔𝐍𝐋𝐈𝐌𝐈𝐓𝐄𝐃")
        send_payment_qr(message.chat.id)
        return
    
    _send_pe(message.chat.id, f"🆓 𝐅𝐑𝐄𝐄 𝐓𝐑𝐈𝐀𝐋 𝐀𝐂𝐓𝐈𝐕𝐀𝐓𝐄𝐃!\n🔫 𝐒𝐞𝐧𝐝 𝐀𝐜𝐜𝐞𝐬𝐬 𝐓𝐨𝐤𝐞𝐧 𝐭𝐨 𝐁𝐚𝐧!")

@bot.message_handler(func=lambda m: m.text and "𝐔𝐍𝐋𝐈𝐌𝐈𝐓𝐄𝐃" in m.text)
def unlimited_cmd(message):
    user_id = message.from_user.id
    user = get_user(user_id)
    
    if user and user.get("unlimited", False):
        _send_pe(message.chat.id, f"✅ 𝐘𝐨𝐮 𝐚𝐥𝐫𝐞𝐚𝐝𝐲 𝐡𝐚𝐯𝐞 𝐔𝐍𝐋𝐈𝐌𝐈𝐓𝐄𝐃 𝐚𝐜𝐜𝐞𝐬𝐬!")
        return
    
    send_payment_qr(message.chat.id)

# ============================================================
# SUPPORT
# ============================================================

@bot.message_handler(func=lambda m: m.text and "𝐒𝐔𝐏𝐏𝐎𝐑𝐓" in m.text)
def support_cmd(message):
    settings = load_settings()
    support = settings.get("support", "@iflexzyan")
    developer = settings.get("developer", "@iflexzyan")
    
    text = f"""
✅ ═══《 📞 𝐒𝐔𝐏𝐏𝐎𝐑𝐓 》═══ ✅

✅ 👨‍💻 𝐃𝐞𝐯𝐞𝐥𝐨𝐩𝐞𝐫: {developer}

✅ ═══════════════════════ ✅

✅ 𝐅𝐨𝐫 𝐚𝐧𝐲 𝐢𝐬𝐬𝐮𝐞𝐬, 𝐜𝐨𝐧𝐭𝐚𝐜𝐭:
✅ 📱 𝐓𝐞𝐥𝐞𝐠𝐫𝐚𝐦: {support}

✅ ═══════════════════════ ✅
"""
    markup = InlineKeyboardMarkup([
        [make_blue_button("𝐂𝐎𝐍𝐓𝐀𝐂𝐓 𝐒𝐔𝐏𝐏𝐎𝐑𝐓", url=f"https://t.me/{support.replace('@', '')}")]
    ])
    _send_pe(message.chat.id, text, reply_markup=markup)

@bot.message_handler(func=lambda m: m.text and "𝐀𝐁𝐎𝐔𝐓" in m.text)
def about_cmd(message):
    user_id = message.from_user.id
    markup = get_menu(user_id)
    settings = load_settings()
    developer = settings.get("developer", "@iflexzyan")
    
    text = f"""
✅ ═══《 ℹ️ 𝐀𝐁𝐎𝐔𝐓 》═══ ✅

✅ 🤖 𝐅𝐅 𝐁𝐀𝐍 𝐁𝐎𝐓

✅ 🔫 𝐁𝐚𝐧 𝐅𝐫𝐞𝐞 𝐅𝐢𝐫𝐞 𝐀𝐜𝐜𝐨𝐮𝐧𝐭𝐬
✅ 💰 𝐏𝐚𝐲 & 𝐆𝐞𝐭 𝐔𝐧𝐥𝐢𝐦𝐢𝐭𝐞𝐝 𝐀𝐜𝐜𝐞𝐬𝐬
✅ 🆓 𝟏 𝐅𝐫𝐞𝐞 𝐓𝐫𝐢𝐚𝐥

✅ ═══════════════════════ ✅

✅ 👨‍💻 𝐃𝐞𝐯𝐞𝐥𝐨𝐩𝐞𝐫: {developer}

✅ ═══════════════════════ ✅
"""
    _send_pe(message.chat.id, text, reply_markup=markup)

# ============================================================
# ADMIN COMMANDS
# ============================================================

@bot.message_handler(commands=['approve'])
def approve_user(message):
    if not is_admin(message.from_user.id):
        _send_pe(message.chat.id, f"❌ 𝐔𝐧𝐚𝐮𝐭𝐡𝐨𝐫𝐢𝐳𝐞𝐝!")
        return
    
    parts = message.text.split()
    if len(parts) < 2:
        _send_pe(message.chat.id, f"❌ 𝐔𝐬𝐚𝐠𝐞: /approve user_id")
        return
    
    try:
        user_id = int(parts[1])
    except:
        _send_pe(message.chat.id, f"❌ 𝐈𝐧𝐯𝐚𝐥𝐢𝐝 𝐔𝐬𝐞𝐫 𝐈𝐃!")
        return
    
    update_user(user_id, "unlimited", True)
    update_user(user_id, "uses", 0)
    
    pending = load_pending()
    if str(user_id) in pending:
        del pending[str(user_id)]
        save_pending(pending)
    
    _send_pe(message.chat.id, f"✅ 𝐔𝐬𝐞𝐫 {user_id} 𝐚𝐩𝐩𝐫𝐨𝐯𝐞𝐝 𝐟𝐨𝐫 𝐔𝐍𝐋𝐈𝐌𝐈𝐓𝐄𝐃 𝐚𝐜𝐜𝐞𝐬𝐬!")
    
    try:
        bot.send_message(user_id, f"✅ 𝐂𝐨𝐧𝐠𝐫𝐚𝐭𝐮𝐥𝐚𝐭𝐢𝐨𝐧𝐬! 𝐘𝐨𝐮 𝐧𝐨𝐰 𝐡𝐚𝐯𝐞 𝐔𝐍𝐋𝐈𝐌𝐈𝐓𝐄𝐃 𝐚𝐜𝐜𝐞𝐬𝐬! 🎉")
    except:
        pass

@bot.message_handler(commands=['disapprove'])
def disapprove_user(message):
    if not is_admin(message.from_user.id):
        _send_pe(message.chat.id, f"❌ 𝐔𝐧𝐚𝐮𝐭𝐡𝐨𝐫𝐢𝐳𝐞𝐝!")
        return
    
    parts = message.text.split()
    if len(parts) < 2:
        _send_pe(message.chat.id, f"❌ 𝐔𝐬𝐚𝐠𝐞: /disapprove user_id")
        return
    
    try:
        user_id = int(parts[1])
    except:
        _send_pe(message.chat.id, f"❌ 𝐈𝐧𝐯𝐚𝐥𝐢𝐝 𝐔𝐬𝐞𝐫 𝐈𝐃!")
        return
    
    pending = load_pending()
    if str(user_id) in pending:
        del pending[str(user_id)]
        save_pending(pending)
    
    _send_pe(message.chat.id, f"❌ 𝐔𝐬𝐞𝐫 {user_id} 𝐝𝐢𝐬𝐚𝐩𝐩𝐫𝐨𝐯𝐞𝐝!")
    
    try:
        bot.send_message(user_id, f"❌ 𝐘𝐨𝐮𝐫 𝐩𝐚𝐲𝐦𝐞𝐧𝐭 𝐰𝐚𝐬 𝐧𝐨𝐭 𝐚𝐩𝐩𝐫𝐨𝐯𝐞𝐝. 𝐏𝐥𝐞𝐚𝐬𝐞 𝐜𝐨𝐧𝐭𝐚𝐜𝐭 𝐬𝐮𝐩𝐩𝐨𝐫𝐭.")
    except:
        pass

@bot.message_handler(commands=['ban'])
def ban_user_cmd(message):
    if not is_admin(message.from_user.id):
        _send_pe(message.chat.id, f"❌ 𝐔𝐧𝐚𝐮𝐭𝐡𝐨𝐫𝐢𝐳𝐞𝐝!")
        return
    
    parts = message.text.split()
    if len(parts) < 2:
        _send_pe(message.chat.id, f"❌ 𝐔𝐬𝐚𝐠𝐞: /ban user_id")
        return
    
    try:
        user_id = int(parts[1])
    except:
        _send_pe(message.chat.id, f"❌ 𝐈𝐧𝐯𝐚𝐥𝐢𝐝 𝐔𝐬𝐞𝐫 𝐈𝐃!")
        return
    
    update_user(user_id, "banned", True)
    _send_pe(message.chat.id, f"✅ 𝐔𝐬𝐞𝐫 {user_id} 𝐁𝐀𝐍𝐍𝐄𝐃!")
    
    try:
        bot.send_message(user_id, f"❌ 𝐘𝐨𝐮 𝐡𝐚𝐯𝐞 𝐛𝐞𝐞𝐧 𝐁𝐀𝐍𝐍𝐄𝐃 𝐟𝐫𝐨𝐦 𝐮𝐬𝐢𝐧𝐠 𝐭𝐡𝐢𝐬 𝐛𝐨𝐭!")
    except:
        pass

@bot.message_handler(commands=['unban'])
def unban_user_cmd(message):
    if not is_admin(message.from_user.id):
        _send_pe(message.chat.id, f"❌ 𝐔𝐧𝐚𝐮𝐭𝐡𝐨𝐫𝐢𝐳𝐞𝐝!")
        return
    
    parts = message.text.split()
    if len(parts) < 2:
        _send_pe(message.chat.id, f"❌ 𝐔𝐬𝐚𝐠𝐞: /unban user_id")
        return
    
    try:
        user_id = int(parts[1])
    except:
        _send_pe(message.chat.id, f"❌ 𝐈𝐧𝐯𝐚𝐥𝐢𝐝 𝐔𝐬𝐞𝐫 𝐈𝐃!")
        return
    
    update_user(user_id, "banned", False)
    _send_pe(message.chat.id, f"✅ 𝐔𝐬𝐞𝐫 {user_id} 𝐔𝐍𝐁𝐀𝐍𝐍𝐄𝐃!")

@bot.message_handler(commands=['users'])
def users_cmd(message):
    if not is_admin(message.from_user.id):
        _send_pe(message.chat.id, f"❌ 𝐔𝐧𝐚𝐮𝐭𝐡𝐨𝐫𝐢𝐳𝐞𝐝!")
        return
    
    users = load_users()
    total = len(users)
    unlimited = sum(1 for u in users.values() if u.get("unlimited", False))
    banned = sum(1 for u in users.values() if u.get("banned", False))
    
    text = f"""
✅ ═══《 👥 𝐔𝐒𝐄𝐑𝐒 》═══ ✅

✅ 📊 𝐓𝐨𝐭𝐚𝐥 𝐔𝐬𝐞𝐫𝐬: {total}
✅ 💎 𝐔𝐧𝐥𝐢𝐦𝐢𝐭𝐞𝐝: {unlimited}
✅ 🚫 𝐁𝐚𝐧𝐧𝐞𝐝: {banned}

✅ ═══════════════════════ ✅

✅ 👥 𝐔𝐬𝐞𝐫 𝐋𝐢𝐬𝐭:
"""
    
    for uid, data in users.items():
        user_status = "✅" if data.get("unlimited", False) else "🆓"
        banned_status = "🚫" if data.get("banned", False) else "✅"
        text += f"✅ • {data.get('name', 'Unknown')} (@{data.get('username', 'N/A')}) - {user_status} {banned_status}\n"
    
    _send_pe(message.chat.id, text)

@bot.message_handler(commands=['data'])
def data_cmd(message):
    if not is_admin(message.from_user.id):
        _send_pe(message.chat.id, f"❌ 𝐔𝐧𝐚𝐮𝐭𝐡𝐨𝐫𝐢𝐳𝐞𝐝!")
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
        bot.send_document(message.chat.id, f, caption=f"✅ 📥 𝐁𝐨𝐭 𝐃𝐚𝐭𝐚 𝐄𝐱𝐩𝐨𝐫𝐭")

@bot.message_handler(commands=['price'])
def price_cmd(message):
    if not is_admin(message.from_user.id):
        _send_pe(message.chat.id, f"❌ 𝐔𝐧𝐚𝐮𝐭𝐡𝐨𝐫𝐢𝐳𝐞𝐝!")
        return
    
    parts = message.text.split()
    if len(parts) < 2:
        settings = load_settings()
        _send_pe(message.chat.id, f"✅ 💰 𝐂𝐮𝐫𝐫𝐞𝐧𝐭 𝐏𝐫𝐢𝐜𝐞: 𝐑𝐬.{settings.get('price', 99)}\n✅ 📌 𝐔𝐬𝐞: /price <amount>")
        return
    
    try:
        price = int(parts[1])
        settings = load_settings()
        settings["price"] = price
        save_settings(settings)
        _send_pe(message.chat.id, f"✅ 𝐏𝐫𝐢𝐜𝐞 𝐮𝐩𝐝𝐚𝐭𝐞𝐝 𝐭𝐨 𝐑𝐬.{price}!")
    except:
        _send_pe(message.chat.id, f"❌ 𝐈𝐧𝐯𝐚𝐥𝐢𝐝 𝐚𝐦𝐨𝐮𝐧𝐭!")

@bot.message_handler(commands=['upi'])
def upi_cmd(message):
    if not is_admin(message.from_user.id):
        _send_pe(message.chat.id, f"❌ 𝐔𝐧𝐚𝐮𝐭𝐡𝐨𝐫𝐢𝐳𝐞𝐝!")
        return
    
    parts = message.text.split()
    if len(parts) < 2:
        settings = load_settings()
        _send_pe(message.chat.id, f"✅ 🏦 𝐂𝐮𝐫𝐫𝐞𝐧𝐭 𝐔𝐏𝐈: {settings.get('upi', 'vanshx111@naviaxis')}\n✅ 📌 𝐔𝐬𝐞: /upi <new_upi>")
        return
    
    upi = parts[1]
    settings = load_settings()
    settings["upi"] = upi
    save_settings(settings)
    _send_pe(message.chat.id, f"✅ 𝐔𝐏𝐈 𝐮𝐩𝐝𝐚𝐭𝐞𝐝 𝐭𝐨: {upi}!")

@bot.message_handler(commands=['developer'])
def developer_cmd(message):
    if not is_admin(message.from_user.id):
        _send_pe(message.chat.id, f"❌ 𝐔𝐧𝐚𝐮𝐭𝐡𝐨𝐫𝐢𝐳𝐞𝐝!")
        return
    
    parts = message.text.split()
    if len(parts) < 2:
        settings = load_settings()
        _send_pe(message.chat.id, f"✅ 👨‍💻 𝐂𝐮𝐫𝐫𝐞𝐧𝐭 𝐃𝐞𝐯𝐞𝐥𝐨𝐩𝐞𝐫: {settings.get('developer', '@iflexzyan')}\n✅ 📌 𝐔𝐬𝐞: /developer <new_developer>")
        return
    
    developer = parts[1]
    settings = load_settings()
    settings["developer"] = developer
    settings["support"] = developer
    save_settings(settings)
    _send_pe(message.chat.id, f"✅ 𝐃𝐞𝐯𝐞𝐥𝐨𝐩𝐞𝐫 𝐮𝐩𝐝𝐚𝐭𝐞𝐝 𝐭𝐨: {developer}!")

@bot.message_handler(commands=['addadmin'])
def add_admin_cmd(message):
    if not is_admin(message.from_user.id):
        _send_pe(message.chat.id, f"❌ 𝐔𝐧𝐚𝐮𝐭𝐡𝐨𝐫𝐢𝐳𝐞𝐝!")
        return
    
    parts = message.text.split()
    if len(parts) < 2:
        _send_pe(message.chat.id, f"❌ 𝐔𝐬𝐚𝐠𝐞: /addadmin user_id")
        return
    
    try:
        user_id = int(parts[1])
        if user_id not in ADMIN_IDS:
            ADMIN_IDS.append(user_id)
            _send_pe(message.chat.id, f"✅ 𝐔𝐬𝐞𝐫 {user_id} 𝐚𝐝𝐝𝐞𝐝 𝐚𝐬 𝐀𝐝𝐦𝐢𝐧!")
        else:
            _send_pe(message.chat.id, f"⚠️ 𝐔𝐬𝐞𝐫 {user_id} 𝐢𝐬 𝐚𝐥𝐫𝐞𝐚𝐝𝐲 𝐀𝐝𝐦𝐢𝐧!")
    except:
        _send_pe(message.chat.id, f"❌ 𝐈𝐧𝐯𝐚𝐥𝐢𝐝 𝐔𝐬𝐞𝐫 𝐈𝐃!")

@bot.message_handler(commands=['prcclone'])
def clone_price_cmd(message):
    if not is_admin(message.from_user.id):
        _send_pe(message.chat.id, f"❌ 𝐔𝐧𝐚𝐮𝐭𝐡𝐨𝐫𝐢𝐳𝐞𝐝!")
        return
    
    parts = message.text.split()
    if len(parts) < 2:
        settings = load_settings()
        _send_pe(message.chat.id, f"✅ 💰 𝐂𝐥𝐨𝐧𝐞 𝐏𝐫𝐢𝐜𝐞: 𝐑𝐬.{settings.get('clone_price', 199)}\n✅ 📌 𝐔𝐬𝐞: /prcclone <amount>")
        return
    
    try:
        price = int(parts[1])
        settings = load_settings()
        settings["clone_price"] = price
        save_settings(settings)
        _send_pe(message.chat.id, f"✅ 𝐂𝐥𝐨𝐧𝐞 𝐏𝐫𝐢𝐜𝐞 𝐮𝐩𝐝𝐚𝐭𝐞𝐝 𝐭𝐨 𝐑𝐬.{price}!")
    except:
        _send_pe(message.chat.id, f"❌ 𝐈𝐧𝐯𝐚𝐥𝐢𝐝 𝐚𝐦𝐨𝐮𝐧𝐭!")

# ============================================================
# CLONE BOT SYSTEM
# ============================================================

@bot.message_handler(func=lambda m: m.text and "𝐂𝐋𝐎𝐍𝐄" in m.text)
def clone_user_cmd(message):
    user_id = message.from_user.id
    user = get_user(user_id)
    
    if not user or user.get("banned", False):
        _send_pe(message.chat.id, f"❌ 𝐘𝐨𝐮 𝐚𝐫𝐞 𝐁𝐀𝐍𝐍𝐄𝐃!")
        return
    
    settings = load_settings()
    clone_price = settings.get("clone_price", 199)
    
    if not user.get("unlimited", False):
        uses = user.get("uses", 0)
        if uses >= 1:
            _send_pe(message.chat.id, f"⚠️ 𝐂𝐥𝐨𝐧𝐞 𝐁𝐨𝐭 𝐜𝐨𝐬𝐭𝐬 𝐑𝐬.{clone_price}\n💰 𝐏𝐚𝐲 𝐭𝐨 𝐠𝐞𝐭 𝐲𝐨𝐮𝐫 𝐨𝐰𝐧 𝐛𝐨𝐭!")
            send_clone_payment_qr(message.chat.id)
            return
    
    # If user has unlimited or free trial remaining
    text = f"""
✅ ═══《 📋 𝐂𝐋𝐎𝐍𝐄 𝐁𝐎𝐓 》═══ ✅

✅ 🤖 𝐄𝐧𝐭𝐞𝐫 𝐧𝐞𝐰 𝐛𝐨𝐭 𝐭𝐨𝐤𝐞𝐧 𝐭𝐨 𝐜𝐥𝐨𝐧𝐞:

✅ ═══════════════════════ ✅

✅ 📌 𝐒𝐭𝐞𝐩𝐬:
✅ 𝟏. 𝐂𝐫𝐞𝐚𝐭𝐞 𝐧𝐞𝐰 𝐛𝐨𝐭 𝐟𝐫𝐨𝐦 @BotFather
✅ 𝟐. 𝐂𝐨𝐩𝐲 𝐭𝐨𝐤𝐞𝐧
✅ 𝟑. 𝐒𝐞𝐧𝐝 𝐭𝐨𝐤𝐞𝐧 𝐡𝐞𝐫𝐞

✅ ═══════════════════════ ✅
"""
    _send_pe(message.chat.id, text)
    bot.register_next_step_handler(message, process_clone_user_token)

def send_clone_payment_qr(chat_id):
    settings = load_settings()
    upi = settings.get("upi", "vanshx111@naviaxis")
    clone_price = settings.get("clone_price", 199)
    
    qr_url = f"https://api.qrserver.com/v1/create-qr-code/?size=300x300&data=upi://pay?pa={upi}&am={clone_price}&cu=INR"
    
    text = f"""
✅ ═══《 💰 𝐂𝐋𝐎𝐍𝐄 𝐏𝐀𝐘𝐌𝐄𝐍𝐓 》═══ ✅

✅ 💳 𝐔𝐏𝐈: {upi}
✅ 💰 𝐀𝐦𝐨𝐮𝐧𝐭: 𝐑𝐬.{clone_price}

✅ ═══════════════════════ ✅

✅ 📱 𝐒𝐜𝐚𝐧 𝐐𝐑 𝐭𝐨 𝐏𝐚𝐲

✅ ═══════════════════════ ✅
"""
    
    keyboard = [
        [make_green_button("𝐈 𝐇𝐀𝐕𝐄 𝐏𝐀𝐈𝐃", callback=f"clone_paid_{chat_id}")],
        [make_blue_button("𝐒𝐔𝐏𝐏𝐎𝐑𝐓", url="https://t.me/iflexzyan")]
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
        _send_pe(message.chat.id, f"❌ 𝐈𝐧𝐯𝐚𝐥𝐢𝐝 𝐁𝐨𝐭 𝐓𝐨𝐤𝐞𝐧!")
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
✅ ═══《 ✅ 𝐁𝐎𝐓 𝐂𝐋𝐎𝐍𝐄𝐃 》═══ ✅

✅ 🤖 𝐁𝐨𝐭 𝐍𝐚𝐦𝐞: {bot_info.first_name}
✅ 👾 𝐔𝐬𝐞𝐫𝐧𝐚𝐦𝐞: @{bot_info.username}
✅ 🆔 𝐁𝐨𝐭 𝐈𝐃: {bot_info.id}

✅ ═══════════════════════ ✅

✅ 👨‍💻 𝐃𝐞𝐯𝐞𝐥𝐨𝐩𝐞𝐫: {clone_data['developer']}
✅ 💰 𝐏𝐫𝐢𝐜𝐞: 𝐑𝐬.{clone_data['price']}
✅ 🏦 𝐔𝐏𝐈: {clone_data['upi']}

✅ ═══════════════════════ ✅

✅ 📌 𝐂𝐥𝐨𝐧𝐞 𝐛𝐨𝐭 𝐢𝐬 𝐫𝐞𝐚𝐝𝐲!
✅ 📌 𝐔𝐬𝐞 /developer 𝐭𝐨 𝐜𝐡𝐚𝐧𝐠𝐞 𝐧𝐚𝐦𝐞

✅ ═══════════════════════ ✅
"""
        _send_pe(message.chat.id, result_text)
        
        try:
            test_bot.send_message(
                user_id,
                f"✅ 𝐖𝐞𝐥𝐜𝐨𝐦𝐞 𝐭𝐨 𝐲𝐨𝐮𝐫 𝐜𝐥𝐨𝐧𝐞𝐝 𝐅𝐅 𝐁𝐀𝐍 𝐁𝐎𝐓!\n\n👨‍💻 𝐃𝐞𝐯𝐞𝐥𝐨𝐩𝐞𝐫: {clone_data['developer']}\n💰 𝐏𝐫𝐢𝐜𝐞: 𝐑𝐬.{clone_data['price']}\n🏦 𝐔𝐏𝐈: {clone_data['upi']}\n\n📌 𝐔𝐬𝐞 /start 𝐭𝐨 𝐛𝐞𝐠𝐢𝐧!"
            )
        except:
            pass
        
        notify_owner(f"✅ 𝐁𝐨𝐭 𝐂𝐥𝐨𝐧𝐞𝐝!\n🤖 {bot_info.first_name}\n👾 @{bot_info.username}\n👤 𝐁𝐲: {user_id}")
        
    except Exception as e:
        _send_pe(message.chat.id, f"❌ 𝐄𝐫𝐫𝐨𝐫: {str(e)}\n\n📌 𝐌𝐚𝐤𝐞 𝐬𝐮𝐫𝐞 𝐭𝐨𝐤𝐞𝐧 𝐢𝐬 𝐜𝐨𝐫𝐫𝐞𝐜𝐭!")

# ============================================================
# ADMIN CLONE COMMAND
# ============================================================

@bot.message_handler(commands=['clone'])
def clone_admin_cmd(message):
    if not is_admin(message.from_user.id):
        _send_pe(message.chat.id, f"❌ 𝐔𝐧𝐚𝐮𝐭𝐡𝐨𝐫𝐢𝐳𝐞𝐝!")
        return
    
    text = f"""
✅ ═══《 📋 𝐂𝐋𝐎𝐍𝐄 𝐁𝐎𝐓 》═══ ✅

✅ 🤖 𝐄𝐧𝐭𝐞𝐫 𝐧𝐞𝐰 𝐛𝐨𝐭 𝐭𝐨𝐤𝐞𝐧 𝐭𝐨 𝐜𝐥𝐨𝐧𝐞:

✅ ═══════════════════════ ✅

✅ 📌 𝐒𝐭𝐞𝐩𝐬:
✅ 𝟏. 𝐂𝐫𝐞𝐚𝐭𝐞 𝐧𝐞𝐰 𝐛𝐨𝐭 𝐟𝐫𝐨𝐦 @BotFather
✅ 𝟐. 𝐂𝐨𝐩𝐲 𝐭𝐨𝐤𝐞𝐧
✅ 𝟑. 𝐒𝐞𝐧𝐝 𝐭𝐨𝐤𝐞𝐧 𝐡𝐞𝐫𝐞

✅ ═══════════════════════ ✅
"""
    _send_pe(message.chat.id, text)
    bot.register_next_step_handler(message, process_clone_admin_token)

def process_clone_admin_token(message):
    if not is_admin(message.from_user.id):
        return
    
    token = message.text.strip()
    
    if not token or ':' not in token:
        _send_pe(message.chat.id, f"❌ 𝐈𝐧𝐯𝐚𝐥𝐢𝐝 𝐁𝐨𝐭 𝐓𝐨𝐤𝐞𝐧!")
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
✅ ═══《 ✅ 𝐁𝐎𝐓 𝐂𝐋𝐎𝐍𝐄𝐃 》═══ ✅

✅ 🤖 𝐁𝐨𝐭 𝐍𝐚𝐦𝐞: {bot_info.first_name}
✅ 👾 𝐔𝐬𝐞𝐫𝐧𝐚𝐦𝐞: @{bot_info.username}
✅ 🆔 𝐁𝐨𝐭 𝐈𝐃: {bot_info.id}

✅ ═══════════════════════ ✅

✅ 👨‍💻 𝐃𝐞𝐯𝐞𝐥𝐨𝐩𝐞𝐫: {clone_data['developer']}
✅ 💰 𝐏𝐫𝐢𝐜𝐞: 𝐑𝐬.{clone_data['price']}
✅ 🏦 𝐔𝐏𝐈: {clone_data['upi']}

✅ ═══════════════════════ ✅
"""
        _send_pe(message.chat.id, result_text)
        
        notify_owner(f"✅ 𝐁𝐨𝐭 𝐂𝐥𝐨𝐧𝐞𝐝 𝐛𝐲 𝐀𝐝𝐦𝐢𝐧!\n🤖 {bot_info.first_name}\n👾 @{bot_info.username}")
        
    except Exception as e:
        _send_pe(message.chat.id, f"❌ 𝐄𝐫𝐫𝐨𝐫: {str(e)}")

# ============================================================
# CALLBACK HANDLERS
# ============================================================

@bot.callback_query_handler(func=lambda c: c.data == "ban_another")
def ban_another_callback(call):
    user_id = call.from_user.id
    user = get_user(user_id)
    
    if not user or user.get("banned", False):
        _send_pe(call.message.chat.id, f"❌ 𝐘𝐨𝐮 𝐚𝐫𝐞 𝐁𝐀𝐍𝐍𝐄𝐃!")
        return
    
    if not user.get("unlimited", False):
        uses = user.get("uses", 0)
        if uses >= 1:
            _send_pe(call.message.chat.id, f"⚠️ 𝐅𝐫𝐞𝐞 𝐓𝐫𝐢𝐚𝐥 𝐔𝐬𝐞𝐝!\n💰 𝐏𝐚𝐲 𝐑𝐬.{load_settings().get('price', 99)} 𝐟𝐨𝐫 𝐔𝐍𝐋𝐈𝐌𝐈𝐓𝐄𝐃")
            send_payment_qr(call.message.chat.id)
            bot.answer_callback_query(call.id)
            return
    
    _send_pe(call.message.chat.id, f"🔑 𝐒𝐞𝐧𝐝 𝐦𝐞 𝐭𝐡𝐞 𝐀𝐜𝐜𝐞𝐬𝐬 𝐓𝐨𝐤𝐞𝐧 𝐭𝐨 𝐁𝐚𝐧!")
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
✅ ═══《 📞 𝐒𝐔𝐏𝐏𝐎𝐑𝐓 》═══ ✅

✅ 👨‍💻 𝐃𝐞𝐯𝐞𝐥𝐨𝐩𝐞𝐫: {settings.get('developer', '@iflexzyan')}

✅ ═══════════════════════ ✅

✅ 📩 𝐂𝐨𝐧𝐭𝐚𝐜𝐭: {support}

✅ ═══════════════════════ ✅
"""
    markup = InlineKeyboardMarkup([
        [make_blue_button("𝐂𝐎𝐍𝐓𝐀𝐂𝐓", url=f"https://t.me/{support.replace('@', '')}")]
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
    
    _send_pe(chat_id, f"📸 𝐒𝐞𝐧𝐝 𝐦𝐞 𝐭𝐡𝐞 𝐂𝐥𝐨𝐧𝐞 𝐏𝐚𝐲𝐦𝐞𝐧𝐭 𝐒𝐜𝐫𝐞𝐞𝐧𝐬𝐡𝐨𝐭!")
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
        
        _send_pe(message.chat.id, f"✅ 𝐒𝐜𝐫𝐞𝐞𝐧𝐬𝐡𝐨𝐭 𝐑𝐞𝐜𝐞𝐢𝐯𝐞𝐝!\n⏳ 𝐖𝐚𝐢𝐭𝐢𝐧𝐠 𝐟𝐨𝐫 𝐀𝐝𝐦𝐢𝐧 𝐀𝐩𝐩𝐫𝐨𝐯𝐚𝐥.")
        
        admin_text = f"""
✅ ═══《 💰 𝐂𝐋𝐎𝐍𝐄 𝐏𝐀𝐘𝐌𝐄𝐍𝐓 》═══ ✅

✅ 👤 𝐔𝐬𝐞𝐫: {message.from_user.first_name}
✅ 🆔 𝐈𝐃: {user_id}
✅ 👾 @{message.from_user.username or 'N/A'}
✅ 📌 𝐓𝐲𝐩𝐞: 𝐂𝐋𝐎𝐍𝐄 𝐁𝐎𝐓

✅ ═══════════════════════ ✅

✅ 📌 𝐔𝐬𝐞: /approveclone {user_id}
✅ 📌 𝐔𝐬𝐞: /disapproveclone {user_id}

✅ ═══════════════════════ ✅
"""
        for admin in ADMIN_IDS:
            try:
                bot.send_photo(admin, photo=file_id, caption=admin_text)
            except:
                bot.send_message(admin, admin_text)
    else:
        _send_pe(message.chat.id, f"❌ 𝐏𝐥𝐞𝐚𝐬𝐞 𝐬𝐞𝐧𝐝 𝐚 𝐏𝐇𝐎𝐓𝐎!")

@bot.message_handler(commands=['approveclone'])
def approve_clone(message):
    if not is_admin(message.from_user.id):
        _send_pe(message.chat.id, f"❌ 𝐔𝐧𝐚𝐮𝐭𝐡𝐨𝐫𝐢𝐳𝐞𝐝!")
        return
    
    parts = message.text.split()
    if len(parts) < 2:
        _send_pe(message.chat.id, f"❌ 𝐔𝐬𝐚𝐠𝐞: /approveclone user_id")
        return
    
    try:
        user_id = int(parts[1])
    except:
        _send_pe(message.chat.id, f"❌ 𝐈𝐧𝐯𝐚𝐥𝐢𝐝 𝐔𝐬𝐞𝐫 𝐈𝐃!")
        return
    
    pending = load_pending()
    if str(user_id) in pending:
        del pending[str(user_id)]
        save_pending(pending)
    
    _send_pe(message.chat.id, f"✅ 𝐔𝐬𝐞𝐫 {user_id} 𝐜𝐥𝐨𝐧𝐞 𝐩𝐚𝐲𝐦𝐞𝐧𝐭 𝐚𝐩𝐩𝐫𝐨𝐯𝐞𝐝!\n📌 𝐍𝐨𝐰 𝐭𝐡𝐞𝐲 𝐜𝐚𝐧 𝐮𝐬𝐞 /clone")
    
    try:
        bot.send_message(user_id, f"✅ 𝐂𝐥𝐨𝐧𝐞 𝐏𝐚𝐲𝐦𝐞𝐧𝐭 𝐀𝐩𝐩𝐫𝐨𝐯𝐞𝐝!\n📌 𝐔𝐬𝐞 /clone 𝐭𝐨 𝐠𝐞𝐭 𝐲𝐨𝐮𝐫 𝐛𝐨𝐭!")
    except:
        pass

# ============================================================
# BOT ON/OFF
# ============================================================

@bot.message_handler(func=lambda m: m.text and "𝐁𝐎𝐓 𝐎𝐍" in m.text)
def bot_on_cmd(message):
    if not is_admin(message.from_user.id):
        _send_pe(message.chat.id, f"❌ 𝐔𝐧𝐚𝐮𝐭𝐡𝐨𝐫𝐢𝐳𝐞𝐝!")
        return
    
    global bot_active
    bot_active = True
    _send_pe(message.chat.id, f"✅ 🟢 𝐁𝐨𝐭 𝐢𝐬 𝐧𝐨𝐰 𝐎𝐍𝐋𝐈𝐍𝐄!")

@bot.message_handler(func=lambda m: m.text and "𝐁𝐎𝐓 𝐎𝐅𝐅" in m.text)
def bot_off_cmd(message):
    if not is_admin(message.from_user.id):
        _send_pe(message.chat.id, f"❌ 𝐔𝐧𝐚𝐮𝐭𝐡𝐨𝐫𝐢𝐳𝐞𝐝!")
        return
    
    global bot_active
    bot_active = False
    _send_pe(message.chat.id, f"✅ 🔴 𝐁𝐨𝐭 𝐢𝐬 𝐧𝐨𝐰 𝐎𝐅𝐅𝐋𝐈𝐍𝐄!")

# ============================================================
# STATS & ADMIN PANEL
# ============================================================

@bot.message_handler(func=lambda m: m.text and "𝐒𝐓𝐀𝐓𝐒" in m.text)
def stats_cmd(message):
    if not is_admin(message.from_user.id):
        _send_pe(message.chat.id, f"❌ 𝐔𝐧𝐚𝐮𝐭𝐡𝐨𝐫𝐢𝐳𝐞𝐝!")
        return
    
    users = load_users()
    orders = load_orders()
    pending = load_pending()
    settings = load_settings()
    
    text = f"""
✅ ═══《 📊 𝐒𝐓𝐀𝐓𝐒 》═══ ✅

✅ 👥 𝐓𝐨𝐭𝐚𝐥 𝐔𝐬𝐞𝐫𝐬: {len(users)}
✅ 🔫 𝐓𝐨𝐭𝐚𝐥 𝐁𝐚𝐧𝐬: {len(orders)}
✅ 💰 𝐏𝐞𝐧𝐝𝐢𝐧𝐠 𝐏𝐚𝐲𝐦𝐞𝐧𝐭𝐬: {len(pending)}
✅ 💎 𝐔𝐧𝐥𝐢𝐦𝐢𝐭𝐞𝐝: {sum(1 for u in users.values() if u.get('unlimited', False))}

✅ ═══════════════════════ ✅

✅ 💳 𝐏𝐫𝐢𝐜𝐞: 𝐑𝐬.{settings.get('price', 99)}
✅ 🏦 𝐔𝐏𝐈: {settings.get('upi', 'vanshx111@naviaxis')}
✅ 👨‍💻 𝐃𝐞𝐯𝐞𝐥𝐨𝐩𝐞𝐫: {settings.get('developer', '@iflexzyan')}

✅ ═══════════════════════ ✅
"""
    _send_pe(message.chat.id, text)

@bot.message_handler(func=lambda m: m.text and "𝐀𝐃𝐌𝐈𝐍 𝐏𝐀𝐍𝐄𝐋" in m.text)
def admin_panel_cmd(message):
    if not is_admin(message.from_user.id):
        _send_pe(message.chat.id, f"❌ 𝐔𝐧𝐚𝐮𝐭𝐡𝐨𝐫𝐢𝐳𝐞𝐝!")
        return
    
    text = f"""
✅ ═══《 👑 𝐀𝐃𝐌𝐈𝐍 𝐏𝐀𝐍𝐄𝐋 》═══ ✅

✅ 📌 𝐂𝐨𝐦𝐦𝐚𝐧𝐝𝐬:

✅ /approve user_id - Approve payment
✅ /disapprove user_id - Reject payment
✅ /ban user_id - Ban user
✅ /unban user_id - Unban user
✅ /users - Show all users
✅ /data - Download all data
✅ /price <amount> - Change price
✅ /upi <upi> - Change UPI
✅ /developer <name> - Change developer
✅ /addadmin user_id - Add admin
✅ /clone - Clone bot (Admin)
✅ /prcclone <amount> - Clone price
✅ /approveclone user_id - Approve clone
✅ /disapproveclone user_id - Reject clone

✅ ═══════════════════════ ✅
"""
    _send_pe(message.chat.id, text)

# ============================================================
# HELP COMMAND
# ============================================================

@bot.message_handler(func=lambda m: m.text and "𝐇𝐄𝐋𝐏" in m.text)
def help_menu_cmd(message):
    user_id = message.from_user.id
    markup = get_menu(user_id)
    
    text = f"""
✅ ═══《 ❓ 𝐇𝐄𝐋𝐏 》═══ ✅

✅ 𝐅𝐅 𝐁𝐀𝐍 𝐁𝐎𝐓 - 𝐂𝐨𝐦𝐩𝐥𝐞𝐭𝐞 𝐆𝐮𝐢𝐝𝐞

✅ ═══════════════════════ ✅

✅ 📌 𝐁𝐚𝐬𝐢𝐜 𝐂𝐨𝐦𝐦𝐚𝐧𝐝𝐬:
✅ /start - Start the bot
✅ /help - This menu

✅ ═══════════════════════ ✅

✅ 🔫 𝐁𝐚𝐧 𝐀𝐜𝐜𝐨𝐮𝐧𝐭:
✅ 1. Click BAN ACCOUNT
✅ 2. Send Access Token
✅ 3. Account gets banned!

✅ ═══════════════════════ ✅

✅ 🆓 𝐅𝐫𝐞𝐞 𝐓𝐫𝐢𝐚𝐥:
✅ 1 FREE ban for new users
✅ After that, pay for UNLIMITED

✅ ═══════════════════════ ✅

✅ 💰 𝐔𝐧𝐥𝐢𝐦𝐢𝐭𝐞𝐝:
✅ Pay once, get unlimited bans
✅ Price: Rs.{load_settings().get('price', 99)}

✅ ═══════════════════════ ✅

✅ 👨‍💻 𝐃𝐞𝐯𝐞𝐥𝐨𝐩𝐞𝐫: @iflexzyan
"""
    _send_pe(message.chat.id, text, reply_markup=markup)

# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":
    print("✅ 𝐅𝐅 𝐁𝐀𝐍 𝐁𝐎𝐓 𝐒𝐭𝐚𝐫𝐭𝐞𝐝!")
    print(f"✅ 𝐎𝐰𝐧𝐞𝐫 𝐈𝐃: {OWNER_ID}")
    print(f"✅ 𝐓𝐨𝐭𝐚𝐥 𝐄𝐦𝐨𝐣𝐢𝐬: {len(VERIFIED_EMOJIS)}")
    bot.infinity_polling()