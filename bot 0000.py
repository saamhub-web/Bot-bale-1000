import sqlite3, re, os, time, json, requests, random, threading
from datetime import datetime, timedelta

TOKEN = "1130839868:2vGgvFCQL3nxnK7syWcaZUfg9LzSc1l1Qj4"
BASE_URL = f"https://tapi.bale.ai/bot{TOKEN}"
BOT_USERNAME = "sinw0rldbot"
DB_PATH = "/storage/emulated/0/kod.bot.bale 💯/empire_game.db"
ADMIN_ID = 216681321
CARD_NUMBER = "6219861457082112"

_original_connect = sqlite3.connect
def _new_connect(*args, **kwargs):
    kwargs['timeout'] = 60
    kwargs['check_same_thread'] = False
    conn = _original_connect(*args, **kwargs)
    try:
        conn.execute("PRAGMA journal_mode=WAL")
        conn.execute("PRAGMA synchronous=OFF")
        conn.execute("PRAGMA cache_size=20000")
        conn.execute("PRAGMA temp_store=MEMORY")
    except:
        pass
    return conn
sqlite3.connect = _new_connect

REQUIRED_CHANNELS = [
    {'id': 5805407256, 'name': 'اطلاعیه', 'link': 'https://ble.ir/atlaieye'},
    {'id': 5662167145, 'name': 'بیانیه', 'link': 'https://ble.ir/imper'},
    {'id': 5665223810, 'name': 'خبرگذاری', 'link': 'https://ble.ir/khabariiiiiiiiiii'}
]

CONTINENTS = ['آفریقا', 'آسیا', 'اروپا', 'آمریکا', 'اقیانوسیه']

CONTINENT_ABILITIES = {
    'آمریکا': '+۵٪ مالیات', 'آسیا': '+۵٪ ارتش',
    'آفریقا': '+۵٪ جمعیت', 'اروپا': '+۵٪ امنیت', 'اقیانوسیه': '+۵٪ درآمد'
}

COLUMNS = [
    'user_id','username','first_name','display_name','country','cabinet','leader',
    'president','pm','step','budget','coin','tax','other_income','population',
    'satisfaction','status','war','rank','xp','security','strike','army','spy',
    'spy_attack','awax1','awax2','wizard','coin_maker','bank_central','bank_world',
    'leader_shield','leader_double','last_income_time','leader_alive',
    'attack_block_time','explorer','expedition_time','admin_step','admin_gift_type',
    'is_banned','ban_reason','shield_end_time','pending_shop_item','is_reporter',
    'reporter_until','news_count','last_news_date','total_likes','total_attacks',
    'total_wins','total_losses','total_defenses','total_ghonaimat','alliance_id',
    'invite_code','invited_by','invite_count','rules_accepted',
    'war_alliance_id','war_start_time','war_end_time','war_target_id',
    'land','hp','workers','continent','map_piece','last_attack_time',
    'last_expedition_count','last_login_date','consecutive_login',
    'daily_statements','last_statement_date','voted_news','last_statement_time',
    'daily_missions','last_mission_date','daily_purchases','statements_unlimited',
    'npcs_disabled','shop_pending_count','total_purchases','xp_purchase_counter'
]

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY, username TEXT DEFAULT '', first_name TEXT DEFAULT '',
        display_name TEXT DEFAULT '', country TEXT DEFAULT '', cabinet TEXT DEFAULT '',
        leader TEXT DEFAULT '', president TEXT DEFAULT '', pm TEXT DEFAULT '',
        step INTEGER DEFAULT 0, budget INTEGER DEFAULT 200000, coin INTEGER DEFAULT 0,
        tax INTEGER DEFAULT 0, other_income INTEGER DEFAULT 0, population INTEGER DEFAULT 1000,
        satisfaction INTEGER DEFAULT 100, status TEXT DEFAULT 'آرام', war TEXT DEFAULT 'صلح',
        rank INTEGER DEFAULT 1, xp INTEGER DEFAULT 0, security INTEGER DEFAULT 0,
        strike INTEGER DEFAULT 0, army INTEGER DEFAULT 0, spy INTEGER DEFAULT 0,
        spy_attack INTEGER DEFAULT 0, awax1 INTEGER DEFAULT 0, awax2 INTEGER DEFAULT 0,
        wizard INTEGER DEFAULT 0, coin_maker INTEGER DEFAULT 0, bank_central INTEGER DEFAULT 0,
        bank_world INTEGER DEFAULT 0, leader_shield INTEGER DEFAULT 0,
        leader_double INTEGER DEFAULT 0, last_income_time TEXT DEFAULT '',
        leader_alive INTEGER DEFAULT 1, attack_block_time TEXT DEFAULT '',
        explorer INTEGER DEFAULT 0, expedition_time TEXT DEFAULT '',
        admin_step INTEGER DEFAULT 0, admin_gift_type TEXT DEFAULT '',
        is_banned INTEGER DEFAULT 0, ban_reason TEXT DEFAULT '', shield_end_time TEXT DEFAULT '',
        pending_shop_item TEXT DEFAULT '', is_reporter INTEGER DEFAULT 0,
        reporter_until TEXT DEFAULT '', news_count INTEGER DEFAULT 0,
        last_news_date TEXT DEFAULT '', total_likes INTEGER DEFAULT 0,
        total_attacks INTEGER DEFAULT 0, total_wins INTEGER DEFAULT 0,
        total_losses INTEGER DEFAULT 0, total_defenses INTEGER DEFAULT 0,
        total_ghonaimat INTEGER DEFAULT 0, alliance_id INTEGER DEFAULT 0,
        invite_code TEXT DEFAULT '', invited_by TEXT DEFAULT '', invite_count INTEGER DEFAULT 0,
        rules_accepted INTEGER DEFAULT 0, war_alliance_id INTEGER DEFAULT 0,
        war_start_time TEXT DEFAULT '', war_end_time TEXT DEFAULT '',
        war_target_id INTEGER DEFAULT 0, land INTEGER DEFAULT 500, hp INTEGER DEFAULT 100,
        workers INTEGER DEFAULT 0, continent TEXT DEFAULT '', map_piece INTEGER DEFAULT 0,
        last_attack_time TEXT DEFAULT '', last_expedition_count INTEGER DEFAULT 0,
        last_login_date TEXT DEFAULT '', consecutive_login INTEGER DEFAULT 1,
        daily_statements INTEGER DEFAULT 0, last_statement_date TEXT DEFAULT '',
        voted_news TEXT DEFAULT '', last_statement_time TEXT DEFAULT '',
        daily_missions INTEGER DEFAULT 1, last_mission_date TEXT DEFAULT '',
        daily_purchases INTEGER DEFAULT 0, statements_unlimited INTEGER DEFAULT 0,
        npcs_disabled INTEGER DEFAULT 0, shop_pending_count INTEGER DEFAULT 0,
        total_purchases INTEGER DEFAULT 0, xp_purchase_counter INTEGER DEFAULT 0
    )''')
    c.execute('''CREATE TABLE IF NOT EXISTS settings (key TEXT PRIMARY KEY, value TEXT DEFAULT '')''')
    c.execute('''CREATE TABLE IF NOT EXISTS attack_logs (id INTEGER PRIMARY KEY AUTOINCREMENT, attacker_id INTEGER, target_id INTEGER, result TEXT, time TEXT, loot_budget INTEGER DEFAULT 0, loot_army INTEGER DEFAULT 0)''')
    c.execute('''CREATE TABLE IF NOT EXISTS news (id INTEGER PRIMARY KEY AUTOINCREMENT, author_id INTEGER, text TEXT, likes INTEGER DEFAULT 0, dislikes INTEGER DEFAULT 0, date TEXT, message_id INTEGER DEFAULT 0)''')
    c.execute('''CREATE TABLE IF NOT EXISTS statements (id INTEGER PRIMARY KEY AUTOINCREMENT, author_id INTEGER, text TEXT, date TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS alliances (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, leader_id INTEGER, treasury INTEGER DEFAULT 0, is_private INTEGER DEFAULT 0, created_at TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS alliance_members (id INTEGER PRIMARY KEY AUTOINCREMENT, alliance_id INTEGER, user_id INTEGER, joined_at TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS war_history (id INTEGER PRIMARY KEY AUTOINCREMENT, attacker_id INTEGER, target_id INTEGER, attacker_country TEXT, target_country TEXT, result TEXT, time TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS loans (id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER, amount INTEGER, interest INTEGER, remaining INTEGER, next_payment TEXT, status TEXT DEFAULT 'active')''')
    c.execute('''CREATE TABLE IF NOT EXISTS map_pieces (id INTEGER PRIMARY KEY, x INTEGER, y INTEGER, w INTEGER, h INTEGER, owner_id INTEGER DEFAULT 0, color TEXT DEFAULT 'gray')''')
    conn.commit()
    conn.close()

def get_user(uid):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT * FROM users WHERE user_id = ?', (uid,))
    row = c.fetchone()
    conn.close()
    return row

def F(user, field, default=0):
    if not user:
        return default
    try:
        idx = COLUMNS.index(field)
        val = user[idx]
        if val is None or val == '':
            return default
        return val
    except:
        return default

def FI(user, field, default=0):
    try:
        return int(F(user, field, default))
    except:
        return default

def save_user(data):
    if 'user_id' not in data:
        return
    uid = data['user_id']
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT user_id FROM users WHERE user_id = ?', (uid,))
    if c.fetchone():
        fields, values = [], []
        for k, v in data.items():
            if k == 'user_id': continue
            if k in COLUMNS:
                fields.append(f"{k} = ?")
                values.append(v)
        if fields:
            values.append(uid)
            c.execute(f"UPDATE users SET {', '.join(fields)} WHERE user_id = ?", values)
    else:
        cols, vals = [], []
        for k, v in data.items():
            if k in COLUMNS:
                cols.append(k)
                vals.append(v)
        if cols:
            ph = ','.join(['?'] * len(cols))
            c.execute(f"INSERT INTO users ({','.join(cols)}) VALUES ({ph})", vals)
    conn.commit()
    conn.close()

_session = requests.Session()

def send(chat_id, text, reply_markup=None):
    def _s():
        try:
            data = {"chat_id": chat_id, "text": text, "parse_mode": "Markdown"}
            if reply_markup:
                data["reply_markup"] = json.dumps(reply_markup)
            _session.post(f"{BASE_URL}/sendMessage", data=data, timeout=15)
        except Exception as e:
            print(f"send err: {e}")
    threading.Thread(target=_s, daemon=True).start()

def send_photo(chat_id, photo_url, caption="", reply_markup=None):
    def _s():
        try:
            data = {"chat_id": chat_id, "photo": photo_url, "caption": caption, "parse_mode": "Markdown"}
            if reply_markup:
                data["reply_markup"] = json.dumps(reply_markup)
            _session.post(f"{BASE_URL}/sendPhoto", data=data, timeout=15)
        except:
            pass
    threading.Thread(target=_s, daemon=True).start()

def edit(chat_id, message_id, text, reply_markup=None):
    try:
        data = {"chat_id": chat_id, "message_id": message_id, "text": text, "parse_mode": "Markdown"}
        if reply_markup:
            data["reply_markup"] = json.dumps(reply_markup)
        _session.post(f"{BASE_URL}/editMessageText", data=data, timeout=15)
    except:
        pass

def answer_cb(cb_id):
    def _a():
        try:
            _session.post(f"{BASE_URL}/answerCallbackQuery", data={"callback_query_id": cb_id}, timeout=5)
        except:
            pass
    threading.Thread(target=_a, daemon=True).start()

def kb(buttons):
    return {"inline_keyboard": buttons}

def get_updates(offset):
    try:
        return _session.get(f"{BASE_URL}/getUpdates", params={"offset": offset, "timeout": 10}, timeout=15).json()
    except:
        return {}

def get_chat_member(chat_id, user_id):
    try:
        r = _session.get(f"{BASE_URL}/getChatMember", params={"chat_id": chat_id, "user_id": user_id}, timeout=5).json()
        if r.get('ok'): return r['result'].get('status', '')
        return ''
    except:
        return ''

def check_channels(uid):
    not_member = []
    for ch in REQUIRED_CHANNELS:
        st = get_chat_member(ch['id'], uid)
        if st not in ['member', 'administrator', 'creator']:
            not_member.append(ch)
    return not_member

def get_setting(key, default=''):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT value FROM settings WHERE key = ?', (key,))
    r = c.fetchone()
    conn.close()
    return r[0] if r else default

def set_setting(key, value):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('INSERT OR REPLACE INTO settings (key, value) VALUES (?, ?)', (key, str(value)))
    conn.commit()
    conn.close()

def rank_name(lv):
    ranks = ['Bronze','Silver','Gold','Platinum','Diamond','Emerald','Ruby','Sapphire','Master','Grand Master','Challenger','Elite','Legendary','Mythic','Apex']
    try:
        lv = int(lv)
        return ranks[lv-1] if 1 <= lv <= 15 else 'Bronze'
    except:
        return 'Bronze'

def valid_name(name, mn=3, mx=21):
    if not name or not isinstance(name, str): return False
    name = name.strip()
    if len(name) < mn or len(name) > mx: return False
    if re.search(r'[\U0001F300-\U0001FFFF]', name): return False
    return True

def country_exists(name):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT user_id FROM users WHERE country = ?', (name,))
    r = c.fetchone()
    conn.close()
    return r is not None

def alliance_name_exists(name):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT id FROM alliances WHERE name = ?', (name,))
    r = c.fetchone()
    conn.close()
    return r is not None

def get_iran_hour():
    return datetime.now()

def get_free_map_piece():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT id FROM map_pieces WHERE owner_id = 0 LIMIT 1')
    r = c.fetchone()
    conn.close()
    return r[0] if r else None

def display_name(user):
    if not user: return "ناشناس"
    fn = F(user, 'first_name', '')
    if fn: return fn
    un = F(user, 'username', '')
    if un: return un
    return "ناشناس"

# ==================== ماموریت‌های روزانه (۶۰ روز - پول) ====================
DAILY_MISSIONS = {
    1: {'title': '🌅 روز اول: آغاز سفر', 'reward': 10000, 'label': '۱ اکسپدیشن'},
    2: {'title': '🌅 روز دوم: رفاه', 'reward': 20000, 'label': 'از رفاه خرید کن'},
    3: {'title': '🌅 روز سوم: کاوش', 'reward': 40000, 'label': '۳ اکسپدیشن'},
    4: {'title': '🌅 روز چهارم: ارتش', 'reward': 50000, 'label': '۵ ارتش بخر'},
    5: {'title': '🌅 روز پنجم: امنیت', 'reward': 60000, 'label': '۳ امنیت بخر'},
    6: {'title': '🌅 روز ششم: اقتصاد', 'reward': 70000, 'label': '۳ اقتصاد بخر'},
    7: {'title': '🌅 روز هفتم: دیپلماسی', 'reward': 80000, 'label': '۱ بیانیه'},
    8: {'title': '🌅 روز هشتم: خبر', 'reward': 90000, 'label': '۱ خبر'},
    9: {'title': '🌅 روز نهم: دعوت', 'reward': 100000, 'label': '۱ دعوت'},
    10: {'title': '🌅 روز دهم: قدرت', 'reward': 120000, 'label': '۱۰ خرید'},
    11: {'title': '🌅 روز یازدهم: جنگ', 'reward': 130000, 'label': '۱ حمله'},
    12: {'title': '🌅 روز دوازدهم: فتح', 'reward': 150000, 'label': '۱ برد'},
}
for d in range(13, 61):
    DAILY_MISSIONS[d] = {'title': f'🌅 روز {d}', 'reward': 150000 + (d - 12) * 50000, 'label': f'{5 + d//10} خرید + ۱ حمله'}

# ==================== ماموریت‌های رنک (XP - ۱۰۰ تا) ====================
RANK_MISSIONS = {
    1: {'title': '🥉 Bronze', 'buy': 10, 'attack': 5, 'login': 3},
    2: {'title': '🥈 Silver', 'buy': 25, 'attack': 15, 'login': 7},
    3: {'title': '🥇 Gold', 'buy': 50, 'attack': 30, 'login': 14},
    4: {'title': '💎 Platinum', 'buy': 100, 'attack': 50, 'login': 21},
    5: {'title': '💠 Diamond', 'buy': 200, 'attack': 100, 'login': 30},
    6: {'title': '💚 Emerald', 'buy': 400, 'attack': 200, 'login': 45},
    7: {'title': '❤️ Ruby', 'buy': 700, 'attack': 350, 'login': 60},
    8: {'title': '💙 Sapphire', 'buy': 1000, 'attack': 500, 'login': 90},
}
for r in range(9, 16):
    RANK_MISSIONS[r] = {'title': f'👑 رنک {r}', 'buy': 1000 + (r - 8) * 500, 'attack': 500 + (r - 8) * 250, 'login': 90 + (r - 8) * 10}

NPC_LIST = [
    {'name': 'نیوزیلند', 'budget': 50000000, 'army': 5000},
    {'name': 'اکبرآباد کتول', 'budget': 40000000, 'army': 4000},
    {'name': 'بات‌کش', 'budget': 30000000, 'army': 3000},
    {'name': 'رونالسه', 'budget': 80000000, 'army': 8000},
    {'name': 'استانبول', 'budget': 70000000, 'army': 7000},
    {'name': 'توکسوپلاسموز', 'budget': 60000000, 'army': 6000},
    {'name': 'توکیو', 'budget': 90000000, 'army': 9000},
    {'name': 'اینگلیس', 'budget': 100000000, 'army': 10000},
    {'name': 'هندوستان', 'budget': 150000000, 'army': 15000},
    {'name': 'دورقوزآباد', 'budget': 120000000, 'army': 12000},
    {'name': 'ژاپن', 'budget': 200000000, 'army': 20000},
    {'name': 'بروکن', 'budget': 300000000, 'army': 30000},
    {'name': 'دیسک‌کمر', 'budget': 500000000, 'army': 50000}
]
# ==================== متن‌های فانتزی ====================

def get_help_text(page=0):
    pages = [
        (
            "📖 ═══ *راهنمای عصر امپراطوری* ═══ 📖\n"
            "━━━━━━━━━━━━━━━━━━\n\n"
            "🏛️ *به سرزمین قدرت خوش آمدی، فرمانده!*\n\n"
            "اینجا جاییه که هر تصمیمت، سرنوشت یک\n"
            "امپراطوری رو رقم می‌زنه. تو از یه کشور\n"
            "کوچیک شروع می‌کنی و می‌تونی تا فتح\n"
            "تمام قاره‌ها پیش بری.\n\n"
            "━━━━━━━━━━━━━━━━━━\n"
            "📝 *ثبت‌نام و شروع*\n"
            "━━━━━━━━━━━━━━━━━━\n"
            "• نام کشور: ۳ تا ۲۱ کاراکتر\n"
            "• انتخاب قاره (هر کدوم یه ابیلیتی)\n"
            "• کابینه، رهبر، رئیس‌جمهور، نخست‌وزیر\n"
            "• قبول قوانین امپراطوری\n\n"
            "🎁 *هدیه شروع:*\n"
            "💰 ۲۰۰,۰۰۰ دلار\n"
            "👥 ۱,۰۰۰ جمعیت\n"
            "🏞️ ۵۰۰ کیلومتر مربع\n"
            "❤️ ۱۰۰٪ HP\n\n"
            "📄 صفحه ۱ از ۵"
        ),
        (
            "📖 ═══ *راهنمای عصر امپراطوری* ═══ 📖\n"
            "━━━━━━━━━━━━━━━━━━\n\n"
            "🌍 *قاره‌ها و ابیلیتی‌هاشون*\n"
            "━━━━━━━━━━━━━━━━━━\n"
            "🇺🇸 *آمریکا* — +۵٪ مالیات\n"
            "🌏 *آسیا* — +۵٪ ارتش\n"
            "🌍 *آفریقا* — +۵٪ جمعیت\n"
            "🌍 *اروپا* — +۵٪ امنیت\n"
            "🌊 *اقیانوسیه* — +۵٪ درآمد\n\n"
            "━━━━━━━━━━━━━━━━━━\n"
            "💰 *اقتصاد امپراطوری*\n"
            "━━━━━━━━━━━━━━━━━━\n"
            "• مالیات: جمعیت × (رضایت ÷ ۱۰۰)\n"
            "• هر ثانیه به خزانه‌ات اضافه می‌شه\n"
            "• درآمد جانبی از اقتصادها\n"
            "• بانک مرکزی/جهانی سود روزانه\n"
            "• کوین‌ساز: روزانه ۱ کوین\n\n"
            "🫂 *رضایت مردم*\n"
            "• هر ۲ ساعت ۱٪ کم می‌شه\n"
            "• زیر ۵۰٪: هشدار\n"
            "• زیر ۲۰٪: خطر\n"
            "• زیر ۱۰٪: شورش!\n\n"
            "📄 صفحه ۲ از ۵"
        ),
        (
            "📖 ═══ *راهنمای عصر امپراطوری* ═══ 📖\n"
            "━━━━━━━━━━━━━━━━━━\n\n"
            "⚔️ *ارتش و امنیت*\n"
            "━━━━━━━━━━━━━━━━━━\n"
            "• ۱۹ آیتم ارتش (بمب استراتژیکی → بمب زیستی)\n"
            "• ۶ آیتم امنیت (سپر وایکینگ → نیرو پیشش)\n"
            "• ⚠️ قانون: ارتش ≤ امنیت + ۵۰,۰۰۰\n\n"
            "🎯 *۷ نوع حمله*\n"
            "• 🎲 رندوم — هدف تصادفی\n"
            "• 🔁 انتقام — از مهاجم قبلی\n"
            "• 🕵️ جاسوسی — فقط Diamond+\n"
            "• 🕶️ مخفی — بدون شناسایی (۱۵©)\n"
            "• 🔍 جستجو — هدف خاص\n"
            "• 💰 جایزه — ثروتمندترین‌ها\n"
            "• 🔥 آشوب — کشورهای ویران\n\n"
            "🛡️ *آواکس:*\n"
            "• آواکس ۱: ۲۵٪ شناسایی\n"
            "• آواکس ۲: ۵۰٪ شناسایی\n"
            "• هر دو: ۷۵٪ شناسایی\n\n"
            "📄 صفحه ۳ از ۵"
        ),
        (
            "📖 ═══ *راهنمای عصر امپراطوری* ═══ 📖\n"
            "━━━━━━━━━━━━━━━━━━\n\n"
            "🗺️ *اکسپدیشن*\n"
            "━━━━━━━━━━━━━━━━━━\n"
            "• انتخاب تعداد کاوشگر\n"
            "• هر کاوشگر یه نتیجه جدا\n"
            "• ۳ ساعت طول می‌کشه\n"
            "• هزینه: ۵۰,۰۰۰$ برای هر کاوشگر\n"
            "• جوایز: گنج، معدن، اسلحه، الماس، زمین\n\n"
            "🌑 *بازار سیاه*\n"
            "━━━━━━━━━━━━━━━━━━\n"
            "• جاسوس (۱۰©)\n"
            "• نیروی ضربت (۵©)\n"
            "• آواکس ۱ و ۲\n"
            "• بانک مرکزی (۵۰۰K)\n"
            "• بانک جهانی (۲.۵M)\n"
            "• کوین‌ساز (۱M)\n"
            "• نیروی کاوش (۵۰K)\n\n"
            "📄 صفحه ۴ از ۵"
        ),
        (
            "📖 ═══ *راهنمای عصر امپراطوری* ═══ 📖\n"
            "━━━━━━━━━━━━━━━━━━\n\n"
            "🎗️ *رنک‌ها (۱۵ سطح)*\n"
            "━━━━━━━━━━━━━━━━━━\n"
            "🥉 Bronze → Silver → Gold → Platinum\n"
            "💎 Diamond → Emerald → Ruby → Sapphire\n"
            "👑 Master → Grand Master → Challenger\n"
            "🏆 Elite → Legendary → Mythic → Apex\n\n"
            "📋 *ماموریت‌های رنک:*\n"
            "• هر رنک ماموریت خاص داره\n"
            "• با انجام ماموریت، XP می‌گیری\n"
            "• XP = پیشرفت رنک (۱۰۰ = رنک‌آپ)\n\n"
            "📅 *ماموریت‌های روزانه:*\n"
            "• هر روز ماموریت جدید (پول جایزه)\n"
            "• ۶۰ روز ماموریت متوالی\n"
            "• اگه یه روز نیای، ریست می‌شه\n\n"
            "📟 *اتحاد:*\n"
            "• ساخت با ۵M یا ۵۰©\n"
            "• عضویت، خزانه، تنظیمات\n\n"
            "📰 *خبرنگاری:*\n"
            "• روزانه ۱ خبر\n"
            "• خبر به کانال می‌ره\n"
            "• رای کاربران روی خبر\n\n"
            "📜 *بیانیه:*\n"
            "• روزانه ۱۲ بیانیه\n"
            "• کول‌داون ۳۰ ثانیه\n"
            "• به کانال بیانیه می‌ره\n\n"
            "📄 صفحه ۵ از ۵"
        ),
    ]
    page = max(0, min(4, page))
    return pages[page]

def get_rules_text():
    return (
        "📜 ═══ *قوانین امپراطوری* ═══ 📜\n"
        "━━━━━━━━━━━━━━━━━━\n\n"
        "🏛️ *فرمانده گرامی،*\n\n"
        "پیش از ورود به سرزمین قدرت، باید قوانین\n"
        "امپراطوری رو بپذیری. این قوانین برای\n"
        "حفظ نظم و عدالت بین تمام فرماندهان است.\n\n"
        "━━━━━━━━━━━━━━━━━━\n"
        "⚖️ *قوانین اساسی*\n"
        "━━━━━━━━━━━━━━━━━━\n\n"
        "۱️⃣ *احترام به دیگران:*\n"
        "   به هیچ فرمانده‌ای توهین نکنید.\n"
        "   هرگونه توهین = بن فوری\n\n"
        "۲️⃣ *ممنوعیت اسپم:*\n"
        "   از ربات به صورت اسپم استفاده نکنید.\n"
        "   ارسال پیام‌های تکراری = اخطار\n\n"
        "۳️⃣ *ممنوعیت تقلب:*\n"
        "   سوء استفاده از باگ‌ها = بن دائم\n"
        "   گزارش باگ = پاداش ویژه\n\n"
        "۴️⃣ *درخواست‌های مالی:*\n"
        "   فقط از طریق پشتیبانی رسمی\n"
        "   درخواست از دیگران = بن\n\n"
        "۵️⃣ *مسئولیت امنیت:*\n"
        "   امنیت کشورت بر عهده خودته\n"
        "   اگه سقوط کردی، تقصیر خودته\n\n"
        "۶️⃣ *احترام به کانال‌ها:*\n"
        "   در کانال‌ها فقط پیام رسمی\n"
        "   تبلیغات = بن دائم\n\n"
        "۷️⃣ *ممنوعیت چند حساب:*\n"
        "   هر پلیر فقط یک حساب\n"
        "   چند حساب = بن همه\n\n"
        "━━━━━━━━━━━━━━━━━━\n"
        "🖋️ *با قبول این قوانین، تو رسماً فرمانده\n"
        "   امپراطوری خودت می‌شی!*\n\n"
        "👇 اگه قبول داری، دکمه زیر رو بزن:"
    )

# ==================== منوها ====================

def menu_main():
    return kb([
        [{"text":"🗺️ اکسپدیشن","callback_data":"expedition"},{"text":"🌑 بازار سیاه","callback_data":"black_market"}],
        [{"text":"🛒 فروشگاه","callback_data":"shop"},{"text":"💸 خرید","callback_data":"buy"}],
        [{"text":"💰 بانک","callback_data":"bank"},{"text":"⚔️ جنگ","callback_data":"attack"}],
        [{"text":"🎖️ رده‌بندی","callback_data":"ranking"},{"text":"🧺 تجهیزات","callback_data":"equipment"}],
        [{"text":"👠 رفاه","callback_data":"welfare"},{"text":"📟 اتحاد","callback_data":"alliance"}],
        [{"text":"📜 بیانیه","callback_data":"statement"},{"text":"🎗️ رنک","callback_data":"rank"}],
        [{"text":"🧾 پشتیبانی","callback_data":"support"},{"text":"🎭 دعوت","callback_data":"invite"}],
        [{"text":"📋 مأموریت‌ها","callback_data":"missions"},{"text":"🗺️ نقشه","callback_data":"map"}],
        [{"text":"📜 تاریخچه","callback_data":"war_history"},{"text":"📰 خبرنگاری","callback_data":"news"}]
    ])

def menu_shop():
    return kb([
        [{"text":"🛡️ سپر ۶ ساعته — ۲۰ت","callback_data":"shop_shield_6h"}],
        [{"text":"🛡️ سپر ۱۲ ساعته — ۳۵ت","callback_data":"shop_shield_12h"}],
        [{"text":"🛡️ سپر ۱ روزه — ۵۰ت","callback_data":"shop_shield_1d"}],
        [{"text":"💵 ۵۰۰K پول — ۲۵ت","callback_data":"shop_money_500k"}],
        [{"text":"💵 ۱.۵M پول — ۵۵ت","callback_data":"shop_money_1.5m"}],
        [{"text":"💵 ۳.۵M پول — ۸۵ت","callback_data":"shop_money_3.5m"}],
        [{"text":"© ۲۵ کوین — ۱۲ت","callback_data":"shop_coin_25"}],
        [{"text":"© ۴۵ کوین — ۲۱ت","callback_data":"shop_coin_45"}],
        [{"text":"© ۱۰۰ کوین — ۳۵ت","callback_data":"shop_coin_100"}],
        [{"text":"🎗️ رنک آپ — ۵۵ت","callback_data":"shop_rankup"}],
        [{"text":"✏️ تغییر نام — ۳۵ت","callback_data":"shop_rename"}],
        [{"text":"📜 بیانیه نامحدود — ۱۵ت","callback_data":"shop_unlimited_statement"}],
        [{"text":"🔙 بازگشت","callback_data":"back_to_menu"}]
    ])

def menu_black_market():
    return kb([
        [{"text":"🕵️ جاسوس (۱۰©)","callback_data":"bm_spy"}],
        [{"text":"🗡️ نیروی ضربت (۵©)","callback_data":"bm_strike"}],
        [{"text":"👑 محافظ رهبر (۵۰K)","callback_data":"bm_leader_shield"}],
        [{"text":"👥 بدل رهبر (۱۰۰K)","callback_data":"bm_leader_double"}],
        [{"text":"📡 آواکس ۱ (۲۰©)","callback_data":"bm_awax1"}],
        [{"text":"📡 آواکس ۲ (۴۰©)","callback_data":"bm_awax2"}],
        [{"text":"🏦 بانک مرکزی (۵۰۰K)","callback_data":"bm_bank_central"}],
        [{"text":"🌍 بانک جهانی (۲.۵M)","callback_data":"bm_bank_world"}],
        [{"text":"🧙 جادوگر (۱۵©)","callback_data":"bm_wizard"}],
        [{"text":"💰 کوین ساز (۱M)","callback_data":"bm_coin_maker"}],
        [{"text":"🔍 نیروی کاوش (۵۰K)","callback_data":"bm_explorer"}],
        [{"text":"🔙 بازگشت","callback_data":"back_to_menu"}]
    ])

def menu_welfare():
    return kb([
        [{"text":"👥 جمعیت","callback_data":"welfare_pop"}],
        [{"text":"🫂 رضایت","callback_data":"welfare_sat"}],
        [{"text":"🔙 بازگشت","callback_data":"back_to_menu"}]
    ])

def menu_pop():
    return kb([
        [{"text":"🏫 مدرسه (۶۰۰K) — +۳۰","callback_data":"pop_0"}],
        [{"text":"🎓 دبیرستان (۱M) — +۵۰","callback_data":"pop_1"}],
        [{"text":"🔬 پژوهشگاه (۱.۶M) — +۸۰","callback_data":"pop_2"}],
        [{"text":"🏥 بیمارستان (۴.۶M) — +۲۳۰","callback_data":"pop_3"}],
        [{"text":"💉 بهداری (۵M) — +۲۵۰","callback_data":"pop_4"}],
        [{"text":"🔙 بازگشت","callback_data":"welfare"}]
    ])

def menu_sat():
    return kb([
        [{"text":"🏋️ باشگاه (۲۵۰K) — +۱","callback_data":"sat_0"}],
        [{"text":"🌳 پارک (۵۰۰K) — +۲","callback_data":"sat_1"}],
        [{"text":"🌿 فضای سبز (۷۵۰K) — +۵","callback_data":"sat_2"}],
        [{"text":"🎵 دیسکو پولو (۲M) — +۸","callback_data":"sat_3"}],
        [{"text":"🚜 مزرعه (۲.۵M) — +۱۰","callback_data":"sat_4"}],
        [{"text":"🔙 بازگشت","callback_data":"welfare"}]
    ])

def menu_buy():
    return kb([
        [{"text":"💰 اقتصاد","callback_data":"buy_econ"}],
        [{"text":"⚔️ ارتش","callback_data":"buy_army"}],
        [{"text":"🛡️ امنیت","callback_data":"buy_sec"}],
        [{"text":"👷 کارگر","callback_data":"buy_worker"}],
        [{"text":"🔙 بازگشت","callback_data":"back_to_menu"}]
    ])

def menu_econ():
    btns = []
    for i, it in enumerate(ECON_ITEMS):
        btns.append([{"text": f"{it['name']} — {it['price']:,}$", "callback_data": f"econ_{i}"}])
    btns.append([{"text":"🔙 بازگشت","callback_data":"buy"}])
    return kb(btns)

def menu_army():
    btns = []
    for i, it in enumerate(ARMY_ITEMS):
        btns.append([{"text": f"{it['name']} — dmg {it['damage']:,} — {it['price']:,}$", "callback_data": f"army_{i}"}])
    btns.append([{"text":"🔙 بازگشت","callback_data":"buy"}])
    return kb(btns)

def menu_sec():
    btns = []
    for i, it in enumerate(SEC_ITEMS):
        btns.append([{"text": f"{it['name']} — res {it['res']:,} — {it['price']:,}$", "callback_data": f"sec_{i}"}])
    btns.append([{"text":"🔙 بازگشت","callback_data":"buy"}])
    return kb(btns)

def menu_continents():
    btns = []
    for c in CONTINENTS:
        ab = CONTINENT_ABILITIES.get(c, '')
        btns.append([{"text": f"{c} — {ab}", "callback_data": f"cont_{c}"}])
    return kb(btns)

def menu_help_pages(current=0):
    nav = []
    if current > 0:
        nav.append({"text":"◀️ صفحه قبل","callback_data":f"help_page_{current-1}"})
    if current < 4:
        nav.append({"text":"صفحه بعد ▶️","callback_data":f"help_page_{current+1}"})
    return kb([
        nav,
        [{"text":"📝 ثبت نام","callback_data":"register"}]
    ])

def menu_admin():
    return kb([
        [{"text":"👥 لیست بازیکنان","callback_data":"admin_players_0"}],
        [{"text":"🔍 جستجوی بازیکن","callback_data":"admin_search"}],
        [{"text":"📊 آمار کلی","callback_data":"admin_stats"}],
        [{"text":"💸 کمک به همه","callback_data":"admin_help_all"}],
        [{"text":"👤 کمک به یک نفر","callback_data":"admin_help_one"}],
        [{"text":"📢 پیام همگانی","callback_data":"admin_broadcast"}],
        [{"text":"🚫 بن/آنبن","callback_data":"admin_ban_menu"}],
        [{"text":"⚙️ تنظیمات ربات","callback_data":"admin_settings"}]
    ])

def menu_admin_player(target_uid, page=0):
    return kb([
        [{"text":"💸 ارسال پول","callback_data":f"admin_send_money_{target_uid}"}],
        [{"text":"© ارسال کوین","callback_data":f"admin_send_coin_{target_uid}"}],
        [{"text":"🎗️ رنک آپ","callback_data":f"admin_rankup_{target_uid}"}],
        [{"text":"🚫 بن کردن","callback_data":f"admin_ban_{target_uid}"}],
        [{"text":"✅ آنبن","callback_data":f"admin_unban_{target_uid}"}],
        [{"text":"✏️ ویرایش فیلد","callback_data":f"admin_edit_{target_uid}"}],
        [{"text":"🔄 ریست اکانت","callback_data":f"admin_reset_{target_uid}"}],
        [{"text":"🔙 بازگشت به لیست","callback_data":f"admin_players_{page}"}]
    ])

def menu_attack():
    return kb([
        [{"text":"🎲 حمله سریع","callback_data":"atk_random"}],
        [{"text":"🔁 انتقام","callback_data":"atk_revenge"}],
        [{"text":"🕵️ جاسوسی (Diamond+)","callback_data":"atk_spy"}],
        [{"text":"🕶️ مخفی (۱۵©)","callback_data":"atk_hidden"}],
        [{"text":"🔍 جستجو","callback_data":"atk_search"}],
        [{"text":"💰 شکار جایزه","callback_data":"atk_bounty"}],
        [{"text":"🔥 شکار آشوب","callback_data":"atk_unstable"}],
        [{"text":"🔙 بازگشت","callback_data":"back_to_menu"}]
    ])

def menu_alliance_main():
    return kb([
        [{"text":"📋 لیست اتحادها","callback_data":"alliance_list"}],
        [{"text":"➕ ساخت اتحاد","callback_data":"alliance_create"}],
        [{"text":"🔍 جستجو","callback_data":"alliance_search"}],
        [{"text":"🔙 بازگشت","callback_data":"back_to_menu"}]
    ])

def menu_alliance_panel(aid, is_leader=False):
    btns = [
        [{"text":"👥 اعضا","callback_data":"alliance_members"}],
        [{"text":"💰 خزانه","callback_data":"alliance_treasury"}],
    ]
    if is_leader:
        btns.append([{"text":"⚙️ تنظیمات","callback_data":"alliance_settings"}])
        btns.append([{"text":"👑 انتقال رهبری","callback_data":"alliance_transfer"}])
    else:
        btns.append([{"text":"❌ خروج","callback_data":"alliance_leave"}])
    btns.append([{"text":"🔙 بازگشت","callback_data":"back_to_menu"}])
    return kb(btns)

# ==================== آیتم‌ها ====================

ECON_ITEMS = [
    {'name':'⛏️ معدن الماس','price':24000,'profit':10500},
    {'name':'🥇 معدن طلا','price':48000,'profit':21000},
    {'name':'💠 معدن کریستال','price':96000,'profit':42000},
    {'name':'🏨 کاروانسرا','price':150000,'profit':75000},
    {'name':'🏪 بازار بزرگ','price':240000,'profit':10000},
    {'name':'⚓ بندر تجاری','price':480000,'profit':21000},
    {'name':'🚢 بندر اقتصادی','price':960000,'profit':420000},
    {'name':'🛢️ پالایشگاه نفت','price':2400000,'profit':1050000}
]

ARMY_ITEMS = [
    {'name':'💣 بمب استراتژیکی','damage':2500,'price':25000},
    {'name':'🚙 تانک سبک','damage':2600,'price':26000},
    {'name':'🛡️ تانک سنگین','damage':3100,'price':31000},
    {'name':'🏹 منجنیق','damage':4500,'price':45000},
    {'name':'🏹 کماندار','damage':4750,'price':47500},
    {'name':'🚤 قایق تندرو','damage':5150,'price':51500},
    {'name':'✈️ جنگنده F14','damage':5500,'price':55000},
    {'name':'🛩️ جنگنده B2','damage':6000,'price':60000},
    {'name':'🪖 تکاور','damage':6400,'price':64000},
    {'name':'⚔️ شوالیه','damage':6700,'price':67000},
    {'name':'🚢 ناو جنگی','damage':7500,'price':75000},
    {'name':'🚔 خودرو زرهی','damage':9000,'price':90000},
    {'name':'🔫 مسلسل‌چی','damage':9500,'price':95000},
    {'name':'🔫 تفنگدار','damage':11500,'price':115000},
    {'name':'🚀 موشک هایپرسونیک','damage':14500,'price':145000},
    {'name':'🎯 موشک کروز','damage':21000,'price':210000},
    {'name':'☢️ بمب شیمیایی','damage':51500,'price':515000},
    {'name':'💥 بمب اتم','damage':75000,'price':750000},
    {'name':'🧬 بمب زیستی','damage':110000,'price':1100000}
]

SEC_ITEMS = [
    {'name':'🛡️ سپر وایکینگ','res':13300,'price':180000},
    {'name':'🔰 گنبد آهنین','res':18000,'price':240000},
    {'name':'🛡️ پدافند سراج','res':23250,'price':310000},
    {'name':'🛡️ پدافند غیرعامل','res':45000,'price':600000},
    {'name':'🚀 پدافند هوایی','res':55500,'price':740000},
    {'name':'⚔️ نیرو پیشش','res':150000,'price':2000000}
]

POP_ITEMS = [
    {'name':'🏫 مدرسه','pop':30,'price':600000},
    {'name':'🎓 دبیرستان','pop':50,'price':1000000},
    {'name':'🔬 پژوهشگاه','pop':80,'price':1600000},
    {'name':'🏥 بیمارستان','pop':230,'price':4600000},
    {'name':'💉 بهداری','pop':250,'price':5000000}
]

SAT_ITEMS = [
    {'name':'🏋️ باشگاه','sat':1,'price':250000},
    {'name':'🌳 پارک','sat':2,'price':500000},
    {'name':'🌿 فضای سبز','sat':5,'price':750000},
    {'name':'🎵 دیسکو پولو','sat':8,'price':2000000},
    {'name':'🚜 مزرعه','sat':10,'price':2500000}
]

BM_ITEMS = {
    'spy': {'cost':10,'type':'coin','name':'🕵️ جاسوس','field':'spy'},
    'strike': {'cost':5,'type':'coin','name':'🗡️ نیروی ضربت','field':'strike'},
    'leader_shield': {'cost':50000,'type':'budget','name':'👑 محافظ رهبر','field':'leader_shield','max':1},
    'leader_double': {'cost':100000,'type':'budget','name':'👥 بدل رهبر','field':'leader_double','max':1},
    'awax1': {'cost':20,'type':'coin','name':'📡 آواکس ۱','field':'awax1','max':1},
    'awax2': {'cost':40,'type':'coin','name':'📡 آواکس ۲','field':'awax2','max':1},
    'bank_central': {'cost':500000,'type':'budget','name':'🏦 بانک مرکزی','field':'bank_central'},
    'bank_world': {'cost':2500000,'type':'budget','name':'🌍 بانک جهانی','field':'bank_world'},
    'wizard': {'cost':15,'type':'coin','name':'🧙 جادوگر','field':'wizard','max':1},
    'coin_maker': {'cost':1000000,'type':'budget','name':'💰 کوین‌ساز','field':'coin_maker','max':15},
    'explorer': {'cost':50000,'type':'budget','name':'🔍 نیروی کاوش','field':'explorer'}
}

LOAN_TYPES = [
    {'name':'🥉 برنز','amount':20000000,'interest':20,'rank':1},
    {'name':'🥈 سیلور','amount':30000000,'interest':20,'rank':2},
    {'name':'🥇 گلد','amount':50000000,'interest':20,'rank':3},
    {'name':'💎 پلاتینیوم','amount':70000000,'interest':20,'rank':4},
    {'name':'💠 کریستالی','amount':100000000,'interest':20,'rank':5}
]

EXP_RESULTS = [
    {'name':'🔮 پیدا کردن گنج باستانی','budget':200000,'coin':0,'army':0,'land':0},
    {'name':'💰 کشف معدن طلا','budget':500000,'coin':0,'army':0,'land':0},
    {'name':'⚔️ پیدا کردن اسلحه قدیمی','budget':0,'coin':0,'army':200,'land':0},
    {'name':'💎 کشف الماس درخشان','budget':0,'coin':20,'army':0,'land':0},
    {'name':'📦 محموله جنگی رهاشده','budget':0,'coin':0,'army':500,'land':0},
    {'name':'🏞️ کشف سرزمین حاصلخیز','budget':0,'coin':0,'army':0,'land':'random'},
    {'name':'🏴‍☠️ حمله دزدان دریایی','budget':-100000,'coin':0,'army':-50,'land':0},
    {'name':'🌪️ طوفان ناگهانی','budget':-150000,'coin':0,'army':-100,'land':0},
    {'name':'🍀 هیچی پیدا نشد','budget':0,'coin':0,'army':0,'land':0}
]
# ==================== درآمد هر ثانیه ====================

def calculate_income_per_second(u):
    pop = FI(u, 'population', 1000)
    sat = FI(u, 'satisfaction', 100)
    other = FI(u, 'other_income')
    bc = FI(u, 'bank_central')
    bw = FI(u, 'bank_world')
    tax_income = pop * (sat / 100)
    bank_income = (bc * 200000) + (bw * 1100000)
    total_per_hour = tax_income + other + bank_income
    return total_per_hour / 3600

def check_income_all():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT user_id FROM users WHERE step >= 5 AND is_banned = 0")
    uids = [r[0] for r in c.fetchall()]
    conn.close()
    now = get_iran_hour()
    
    for uid in uids:
        u = get_user(uid)
        if not u:
            continue
        last = F(u, 'last_income_time', '')
        if not last:
            save_user({'user_id': uid, 'last_income_time': now.isoformat()})
            continue
        try:
            last_dt = datetime.fromisoformat(last)
        except:
            save_user({'user_id': uid, 'last_income_time': now.isoformat()})
            continue
        seconds = (now - last_dt).total_seconds()
        if seconds >= 1:
            inc_per_sec = calculate_income_per_second(u)
            earned = int(inc_per_sec * seconds)
            if earned > 0:
                new_budget = FI(u, 'budget') + earned
                sat = FI(u, 'satisfaction', 100)
                new_sat = sat
                if seconds >= 7200:
                    new_sat = max(0, sat - int(seconds // 7200))
                hp = FI(u, 'hp', 100)
                workers = FI(u, 'workers')
                new_hp = hp
                if seconds >= 3600:
                    new_hp = min(100, hp + (1 + 5 * workers) * int(seconds // 3600))
                pop = FI(u, 'population', 1000)
                new_pop = pop
                if new_sat >= 50 and seconds >= 86400:
                    new_pop = int(pop * (1.01 ** int(seconds // 86400)))
                cm = FI(u, 'coin_maker')
                new_coin = FI(u, 'coin')
                if seconds >= 86400 and cm > 0:
                    new_coin += cm * int(seconds // 86400)
                status = F(u, 'status', 'آرام')
                new_status = status
                if status == 'سقوط' and new_hp >= 50:
                    new_status = 'آرام'
                save_user({
                    'user_id': uid, 'budget': new_budget, 'satisfaction': new_sat,
                    'hp': new_hp, 'population': new_pop, 'coin': new_coin,
                    'tax': int(new_pop * (new_sat / 100)),
                    'status': new_status, 'last_income_time': now.isoformat()
                })
        check_login_streak(uid, u)
        check_satisfaction_warning(uid, u)

def check_login_streak(uid, u):
    today = get_iran_hour().strftime('%Y-%m-%d')
    last = F(u, 'last_login_date', '')
    if last == today:
        return
    yesterday = (get_iran_hour() - timedelta(days=1)).strftime('%Y-%m-%d')
    new_streak = FI(u, 'consecutive_login', 1) + 1 if last == yesterday else 1
    save_user({'user_id': uid, 'last_login_date': today, 'consecutive_login': new_streak, 'xp': FI(u, 'xp', 0) + 5})

def check_satisfaction_warning(uid, u):
    sat = FI(u, 'satisfaction', 100)
    if sat >= 50:
        return
    last_warn = get_setting(f"sat_warn_{uid}", "")
    now = get_iran_hour()
    interval = 6 * 3600
    if sat < 20: interval = 3 * 3600
    if sat < 10: interval = 1 * 3600
    if last_warn:
        try:
            if (now - datetime.fromisoformat(last_warn)).total_seconds() < interval:
                return
        except:
            pass
    set_setting(f"sat_warn_{uid}", now.isoformat())
    if sat < 10:
        warn_msg = f"🚨🚨🚨 ═══ *شورش!* ═══ 🚨🚨🚨\n\n🫂 رضایت به *{sat}%* سقوط کرد!\n🔥 مردم شورش کردن!\n⚠️ کشورت در خطره!\n\n🏛️ فوراً رضایت رو بالا ببر!"
    elif sat < 20:
        warn_msg = f"⚠️⚠️ ═══ *هشدار جدی* ═══ ⚠️⚠️\n\n🫂 رضایت به *{sat}%* رسید!\n📉 کشور در آستانه شورشته!"
    else:
        warn_msg = f"⚠️ ═══ *هشدار رضایت* ═══ ⚠️\n\n🫂 رضایت فقط *{sat}%*\n📉 مردم ناراضیان"
    send(uid, warn_msg, reply_markup=kb([
        [{"text":"👠 رفاه","callback_data":"welfare"}],
        [{"text":"🔙 بازگشت","callback_data":"back_to_menu"}]
    ]))

def show_dashboard(uid):
    u = get_user(uid)
    if not u:
        return "❌"
    country = F(u, 'country', '')
    fn = F(u, 'first_name', '')
    cab = F(u, 'cabinet', '')
    land = FI(u, 'land', 500)
    hp = FI(u, 'hp', 100)
    budget = FI(u, 'budget')
    coin = FI(u, 'coin')
    tax = FI(u, 'tax')
    other = FI(u, 'other_income')
    pop = FI(u, 'population', 1000)
    sat = FI(u, 'satisfaction', 100)
    status = F(u, 'status', 'آرام')
    war = F(u, 'war', 'صلح')
    rank = FI(u, 'rank', 1)
    xp = FI(u, 'xp')
    sec = FI(u, 'security')
    strike = FI(u, 'strike')
    army = FI(u, 'army')
    inc_sec = calculate_income_per_second(u)
    hourly = int(inc_sec * 3600)
    war_icon = "🔥 در حال جنگ" if war == 'جنگ' else "خاموش ❌"
    return (
        f"📝 *لیست کشور* 📝\n\n"
        f"🌏 کشور : {country}\n"
        f"🚸 پلیر : {fn}\n"
        f"⚕️ نام کابینه : {cab}\n"
        f"🌤️ آب و هوا : آفتابی ☀️\n"
        f"🏞️ مساحت کشور : {land:,} km\n"
        f"Hp: {hp}%✨\n"
        f"ــــــــــــــــــــــــــــــــــ\n"
        f"💵 بودجه  : {budget:,}$\n"
        f"© کوین  : {coin}\n"
        f"💸 مالیات  : {tax:,}$\n"
        f"💴 سایر درآمد ها : {other:,}$\n"
        f"💵 درآمد ساعتی : {hourly:,}$\n"
        f"ــــــــــــــــــــــــــــــــــ\n"
        f"👥 جمعیت کشور  : {pop:,}\n"
        f"🫂 درصد رضایت مردم  : {sat}%\n"
        f"ــــــــــــــــــــــــــــــــــ\n"
        f"✨ وضعیت کشور  : {status}\n"
        f"🔫 وضعیت جنگ  : {war_icon}\n"
        f"ــــــــــــــــــــــــــــــــــ\n"
        f"🎗️ رنک  : {rank_name(rank)} | XP : {xp}\n"
        f"ــــــــــــــــــــــــــــــــــ\n"
        f"🛡️ امنیت   : {sec:,}\n"
        f"🗡️ ضربت  : {strike:,}\n"
        f"⚔️ ارتش  : {army:,}\n"
        f"🛠️ *منوی مدیریت امپراطوری:*"
    )

# ==================== XP خرید ====================

def add_xp_for_purchase(uid, u):
    counter = FI(u, 'xp_purchase_counter', 0) + 1
    total_p = FI(u, 'total_purchases', 0) + 1
    daily_p = FI(u, 'daily_purchases', 0) + 1
    if counter >= 10:
        save_user({'user_id': uid, 'xp': FI(u, 'xp', 0) + 1, 'xp_purchase_counter': 0, 'total_purchases': total_p, 'daily_purchases': daily_p})
    else:
        save_user({'user_id': uid, 'xp_purchase_counter': counter, 'total_purchases': total_p, 'daily_purchases': daily_p})

# ==================== process_message ====================

def process_message(message):
    chat = message.get('chat', {})
    if chat.get('type') == 'channel':
        return
    uid = chat.get('id')
    txt = message.get('text', '') or ''
    first_name = chat.get('first_name', '') or ''
    username = chat.get('username', '') or ''
    u = get_user(uid)

    if uid == ADMIN_ID:
        if txt == "/start":
            send(uid, "👑 *پنل مدیریت*", reply_markup=menu_admin())
            return
        if u and process_admin_message(uid, txt, u):
            return

    not_member = check_channels(uid)
    if not_member:
        buttons = []
        for ch in not_member:
            buttons.append([{"text": f"📢 {ch['name']}", "url": ch['link']}])
        buttons.append([{"text":"🔄 بررسی مجدد","callback_data":"check"}])
        send(uid, "❌ برای استفاده از ربات عضو کانال‌های زیر شوید:", reply_markup=kb(buttons))
        return

    if not u:
        if txt.startswith("/start inv_"):
            code = txt.replace("/start ", "").strip()
            inviter = None
            conn = sqlite3.connect(DB_PATH)
            c = conn.cursor()
            c.execute('SELECT user_id FROM users WHERE invite_code = ?', (code,))
            r = c.fetchone()
            conn.close()
            if r:
                inviter = r[0]
            save_user({
                'user_id': uid, 'username': username, 'first_name': first_name,
                'step': 0, 'invited_by': code, 'last_income_time': get_iran_hour().isoformat(),
                'last_login_date': get_iran_hour().strftime('%Y-%m-%d'), 'consecutive_login': 1
            })
            if inviter:
                iu = get_user(inviter)
                new_inv = FI(iu, 'invite_count') + 1
                save_user({'user_id': inviter, 'invite_count': new_inv, 'budget': FI(iu, 'budget') + 120000, 'xp': FI(iu, 'xp', 0) + 20})
                send(inviter, f"🎭 یه نفر با کد تو ثبت‌نام کرد!\n💰 +۱۲۰,۰۰۰$\n⭐ +۲۰ XP\n👥 تعداد دعوت: {new_inv}")
        elif txt == "/start":
            save_user({
                'user_id': uid, 'username': username, 'first_name': first_name,
                'step': 0, 'last_income_time': get_iran_hour().isoformat(),
                'last_login_date': get_iran_hour().strftime('%Y-%m-%d'), 'consecutive_login': 1
            })
            welcome = (
                "🛑 ═══ *درود فرمانده* ═══ 🛑\n"
                "━━━━━━━━━━━━━━━━━━\n\n"
                "🏛️ به *عصر امپراطوری* خوش آمدی!\n\n"
                "اینجا سرزمینی‌ست که قدرت، شکوه و افتخار\n"
                "در انتظار توئه. برای شروع این سفر بزرگ،\n"
                "دکمه *ثبت‌نام* رو بزن.\n\n"
                "💰 بعد از ثبت‌نام، سرمایه‌ای برای\n"
                "   اداره کشورت دریافت می‌کنی.\n\n"
                "━━━━━━━━━━━━━━━━━━\n"
                "👇 یکی رو انتخاب کن:"
            )
            send(uid, welcome, reply_markup=kb([
                [{"text":"📖 مشاهده راهنما","callback_data":"show_help_0"}],
                [{"text":"📝 ثبت نام","callback_data":"register"}]
            ]))
            return
        else:
            send(uid, "❌ /start")
            return

    step = FI(u, 'step')
    if step < 7:
        if txt == "/start":
            send(uid, "برای ادامه، نام کشور خود را بفرستید:")
            return
        if step == 0:
            if not valid_name(txt, 3, 21):
                send(uid, "❌ نام کشور باید بین ۳ تا ۲۱ کاراکتر و بدون ایموجی باشه:")
                return
            if country_exists(txt):
                send(uid, "❌ این نام قبلاً استفاده شده! یه اسم دیگه بفرست:")
                return
            save_user({'user_id': uid, 'country': txt, 'step': 1, 'invite_code': f"inv_{uid}"})
            send(uid, (
                "🌍 ═══ *انتخاب قاره* ═══ 🌍\n"
                "━━━━━━━━━━━━━━━━━━\n\n"
                "فرمانده، کشورت رو در کدوم قاره بنا کنی؟\n"
                "هر قاره یه ابیلیتی خاص داره:\n\n"
                "👇 انتخاب کن:"
            ), reply_markup=menu_continents())
            return
        if step == 2:
            if not valid_name(txt, 2, 21):
                send(uid, "❌ نام کابینه باید ۲ تا ۲۱ کاراکتر باشه:")
                return
            save_user({'user_id': uid, 'cabinet': txt, 'step': 3})
            send(uid, f"🏛️ *کابینه سیاسی*\n━━━━━━━━━━━━━━━━━━\n✅ کابینه: *{txt}*\n⏳ رهبر: انتخاب نشده\n⏳ رئیس جمهور: انتخاب نشده\n⏳ نخست وزیر: انتخاب نشده\n\n🖋️ حالا نام *رهبر* رو بنویس:")
            return
        if step == 3:
            if not valid_name(txt, 2, 21):
                send(uid, "❌ نام رهبر باید ۲ تا ۲۱ کاراکتر باشه:")
                return
            save_user({'user_id': uid, 'leader': txt, 'step': 4})
            cab = F(u, 'cabinet', '')
            send(uid, f"🏛️ *کابینه*\n✅ کابینه: *{cab}*\n✅ رهبر: *{txt}*\n⏳ رئیس: انتخاب نشده\n⏳ نخست‌وزیر: انتخاب نشده\n\n🖋️ حالا نام *رئیس جمهور* رو بنویس:")
            return
        if step == 4:
            if not valid_name(txt, 2, 21):
                send(uid, "❌ نام رئیس جمهور باید ۲ تا ۲۱ کاراکتر باشه:")
                return
            save_user({'user_id': uid, 'president': txt, 'step': 5})
            cab = F(u, 'cabinet', '')
            ld = F(u, 'leader', '')
            send(uid, f"🏛️ *کابینه*\n✅ کابینه: *{cab}*\n✅ رهبر: *{ld}*\n✅ رئیس: *{txt}*\n⏳ نخست‌وزیر: انتخاب نشده\n\n🖋️ حالا نام *نخست وزیر* رو بنویس:")
            return
        if step == 5:
            if not valid_name(txt, 2, 21):
                send(uid, "❌ نام نخست وزیر باید ۲ تا ۲۱ کاراکتر باشه:")
                return
            save_user({'user_id': uid, 'pm': txt, 'step': 6})
            send(uid, get_rules_text(), reply_markup=kb([[{"text":"✅ قبول قوانین","callback_data":"accept_rules"}]]))
            return
        return

    if FI(u, 'is_banned') == 1:
        send(uid, "🚫 شما بن شدید!")
        return

    if not F(u, 'first_name', '') and first_name:
        save_user({'user_id': uid, 'first_name': first_name})

    pending = F(u, 'pending_shop_item', '')
    if pending and not pending.startswith('waiting') and not pending.startswith(str(uid)):
        admin_msg = (
            f"🧾 ═══ *رسید جدید* ═══\n"
            f"━━━━━━━━━━━━━━━━━━\n\n"
            f"👤 {display_name(u)}\n"
            f"🆔 `{uid}`\n"
            f"🌏 کشور: {F(u, 'country', '')}\n"
            f"📦 {pending}\n"
            f"📸 پیام: {txt[:50]}\n\n"
            f"👇 تایید یا رد کن:"
        )
        send(ADMIN_ID, admin_msg, reply_markup=kb([
            [{"text":"✅ تایید","callback_data":f"confirm_shop_{uid}_{pending}"}],
            [{"text":"❌ رد","callback_data":f"cancel_shop_{uid}"}]
        ]))
        send(uid, "✅ رسید تو برای ادمین ارسال شد. منتظر تایید باش.")
        save_user({'user_id': uid, 'pending_shop_item': ''})
        return

    astep = F(u, 'admin_step', '')

    if astep == 500:
        try:
            cnt = int(txt)
            if cnt < 1: raise
        except:
            send(uid, "❌ عدد نامعتبر!")
            save_user({'user_id': uid, 'admin_step': 0})
            return
        item_type = F(u, 'admin_gift_type', '')
        it = BM_ITEMS.get(item_type)
        if not it:
            save_user({'user_id': uid, 'admin_step': 0})
            return
        field = it['field']
        cur = FI(u, field)
        if 'max' in it and cur + cnt > it['max']:
            send(uid, f"❌ حداکثر {it['max']} عدد")
            save_user({'user_id': uid, 'admin_step': 0})
            return
        total_cost = it['cost'] * cnt
        if it['type'] == 'coin':
            if FI(u, 'coin') < total_cost:
                send(uid, "❌ کوین کافی نیست!")
                save_user({'user_id': uid, 'admin_step': 0})
                return
            save_user({'user_id': uid, 'coin': FI(u, 'coin') - total_cost})
        else:
            if FI(u, 'budget') < total_cost:
                send(uid, "❌ بودجه کافی نیست!")
                save_user({'user_id': uid, 'admin_step': 0})
                return
            save_user({'user_id': uid, 'budget': FI(u, 'budget') - total_cost})
        add_xp_for_purchase(uid, u)
        save_user({'user_id': uid, field: cur + cnt, 'admin_step': 0})
        send(uid, f"✅ {cnt} عدد {it['name']} خریدی!")
        return

    if astep == 501:
        try: cnt = int(txt)
        except:
            save_user({'user_id': uid, 'admin_step': 0})
            return
        idx = FI(u, 'war_target_id')
        if 0 <= idx < len(ECON_ITEMS):
            it = ECON_ITEMS[idx]
            total = it['price'] * cnt
            if FI(u, 'budget') < total:
                send(uid, "❌ بودجه کافی نیست")
            else:
                save_user({'user_id': uid, 'budget': FI(u, 'budget') - total, 'other_income': FI(u, 'other_income') + it['profit'] * cnt})
                add_xp_for_purchase(uid, u)
                send(uid, f"✅ {cnt} عدد {it['name']} خریدی! سود: +{it['profit']*cnt:,}$")
        save_user({'user_id': uid, 'admin_step': 0})
        return

    if astep == 502:
        try: cnt = int(txt)
        except:
            save_user({'user_id': uid, 'admin_step': 0})
            return
        idx = FI(u, 'war_target_id')
        if 0 <= idx < len(ARMY_ITEMS):
            it = ARMY_ITEMS[idx]
            total = it['price'] * cnt
            new_army = FI(u, 'army') + it['damage'] * cnt
            if new_army > FI(u, 'security') + 50000:
                send(uid, "❌ ارتش نمی‌تونه ۵۰,۰۰۰ بیشتر از امنیت باشه!")
                save_user({'user_id': uid, 'admin_step': 0})
                return
            if FI(u, 'budget') < total:
                send(uid, "❌ بودجه کافی نیست")
            else:
                save_user({'user_id': uid, 'budget': FI(u, 'budget') - total, 'army': new_army})
                add_xp_for_purchase(uid, u)
                send(uid, f"✅ {cnt} عدد {it['name']} خریدی! ⚔️ +{it['damage']*cnt:,}")
        save_user({'user_id': uid, 'admin_step': 0})
        return

    if astep == 503:
        try: cnt = int(txt)
        except:
            save_user({'user_id': uid, 'admin_step': 0})
            return
        idx = FI(u, 'war_target_id')
        if 0 <= idx < len(SEC_ITEMS):
            it = SEC_ITEMS[idx]
            total = it['price'] * cnt
            if FI(u, 'budget') < total:
                send(uid, "❌ بودجه کافی نیست")
            else:
                save_user({'user_id': uid, 'budget': FI(u, 'budget') - total, 'security': FI(u, 'security') + it['res'] * cnt})
                add_xp_for_purchase(uid, u)
                send(uid, f"✅ {cnt} عدد {it['name']} خریدی! 🛡️ +{it['res']*cnt:,}")
        save_user({'user_id': uid, 'admin_step': 0})
        return

    if astep == 504:
        try: cnt = int(txt)
        except:
            save_user({'user_id': uid, 'admin_step': 0})
            return
        cost = 50000 * cnt
        if FI(u, 'budget') < cost:
            send(uid, "❌ بودجه کافی نیست")
        else:
            save_user({'user_id': uid, 'budget': FI(u, 'budget') - cost, 'workers': FI(u, 'workers') + cnt})
            add_xp_for_purchase(uid, u)
            send(uid, f"✅ {cnt} کارگر استخدام کردی!")
        save_user({'user_id': uid, 'admin_step': 0})
        return

    if astep == 200:
        today = get_iran_hour().strftime('%Y-%m-%d')
        daily = FI(u, 'daily_statements', 0)
        if F(u, 'last_statement_date', '') != today:
            daily = 0
        if daily >= 12 and FI(u, 'statements_unlimited', 0) == 0:
            send(uid, "❌ امروز به حد مجاز رسیدی (۱۲ بیانیه)")
            save_user({'user_id': uid, 'admin_step': 0})
            return
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute('INSERT INTO statements (author_id, text, date) VALUES (?, ?, ?)', (uid, txt, get_iran_hour().isoformat()))
        conn.commit()
        conn.close()
        save_user({'user_id': uid, 'admin_step': 0, 'daily_statements': daily + 1, 'last_statement_date': today, 'last_statement_time': get_iran_hour().isoformat()})
        try:
            sc = REQUIRED_CHANNELS[1]['id']
            cn = F(u, 'country', 'ناشناس')
            send(sc, f"📜 *بیانیه‌ی امپراطوری {cn}*\n━━━━━━━━━━━━━━━━━━\n\n{txt}\n\n📅 {get_iran_hour().strftime('%Y-%m-%d | %H:%M')}")
        except:
            pass
        send(uid, f"📜 بیانیه صادر شد! ({daily + 1}/12)")
        return

    if astep == 201:
        admin_msg = f"🧾 *پشتیبانی جدید*\n\n👤 {display_name(u)}\n🆔 `{uid}`\n🌏 {F(u, 'country', '')}\n💬 {txt}"
        send(ADMIN_ID, admin_msg, reply_markup=kb([[{"text":"📩 پاسخ","callback_data":f"reply_support_{uid}"},{"text":"✅ بستن","callback_data":f"close_support_{uid}"}]]))
        save_user({'user_id': uid, 'admin_step': 0})
        send(uid, "✅ پیامت به پشتیبانی ارسال شد!")
        return

    if astep == 100:
        if not valid_name(txt, 3, 21):
            send(uid, "❌ نام باید ۳ تا ۲۱ کاراکتر باشه")
            return
        if country_exists(txt):
            send(uid, "❌ تکراریه")
            return
        save_user({'user_id': uid, 'country': txt, 'admin_step': 0})
        send(uid, f"✅ نام کشور شد: {txt}")
        return

    if astep == 300:
        if not valid_name(txt, 3, 21):
            send(uid, "❌ نام اتحاد باید ۳ تا ۲۱ باشه")
        elif alliance_name_exists(txt):
            send(uid, "❌ تکراریه")
        else:
            conn = sqlite3.connect(DB_PATH)
            c = conn.cursor()
            c.execute('INSERT INTO alliances (name, leader_id, treasury, created_at) VALUES (?, ?, 0, ?)', (txt, uid, get_iran_hour().isoformat()))
            aid = c.lastrowid
            c.execute('INSERT INTO alliance_members (alliance_id, user_id, joined_at) VALUES (?, ?, ?)', (aid, uid, get_iran_hour().isoformat()))
            conn.commit()
            conn.close()
            save_user({'user_id': uid, 'alliance_id': aid, 'admin_step': 0, 'xp': FI(u, 'xp', 0) + 5})
            send(uid, f"🎉 اتحاد «{txt}» ساخته شد!")
            return
        save_user({'user_id': uid, 'admin_step': 0})
        return

    if astep == 600:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("SELECT user_id FROM users WHERE country LIKE ? AND step >= 5", (f"%{txt}%",))
        rows = c.fetchall()
        conn.close()
        if not rows:
            send(uid, "❌ پیدا نشد")
        else:
            for r in rows[:10]:
                send(uid, show_profile(r[0]), reply_markup=kb([[{"text":"⚔️ حمله","callback_data":f"do_attack_{r[0]}"}]]))
        save_user({'user_id': uid, 'admin_step': 0})
        return

    if astep == 601:
        show_country_search_results(uid, txt)
        save_user({'user_id': uid, 'admin_step': 0})
        return

    if astep == 610:
        try:
            cnt = int(txt)
            if cnt < 1: raise
            do_expedition_start(uid, u, cnt)
        except:
            send(uid, "❌ عدد نامعتبر!")
        save_user({'user_id': uid, 'admin_step': 0})
        return

    if astep == 620:
        try:
            cnt = int(txt)
            if cnt < 1: raise
        except:
            send(uid, "❌ عدد نامعتبر!")
            save_user({'user_id': uid, 'admin_step': 0})
            return
        target = FI(u, 'war_target_id')
        is_hidden = F(u, 'admin_gift_type', '') == 'hidden'
        do_attack_with_count(uid, target, u, cnt, is_hidden=is_hidden)
        save_user({'user_id': uid, 'admin_step': 0, 'admin_gift_type': ''})
        return

    if astep == 700:
        today = get_iran_hour().strftime('%Y-%m-%d')
        if F(u, 'last_news_date', '') == today and FI(u, 'news_count', 0) >= 1:
            send(uid, "❌ امروز یه خبرت رو ثبت کردی")
            save_user({'user_id': uid, 'admin_step': 0})
            return
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute('INSERT INTO news (author_id, text, date) VALUES (?, ?, ?)', (uid, txt, get_iran_hour().isoformat()))
        nid = c.lastrowid
        conn.commit()
        conn.close()
        save_user({'user_id': uid, 'admin_step': 0, 'news_count': 1, 'last_news_date': today})
        try:
            nc = REQUIRED_CHANNELS[2]['id']
            cn = F(u, 'country', 'ناشناس')
            channel_msg = f"📰 *خبر {cn}*\n━━━━━━━━━━━━━━━━━━\n\n{txt}\n\n━━━━━━━━━━━━━━━━━━\n👍 رای: 0\n👎 رای: 0\n\n🆔 `news_{nid}`"
            resp = _session.post(f"{BASE_URL}/sendMessage", data={"chat_id": nc, "text": channel_msg, "parse_mode": "Markdown", "reply_markup": json.dumps(kb([[{"text":"👍","callback_data":f"news_like_{nid}"},{"text":"👎","callback_data":f"news_dislike_{nid}"}]]))}, timeout=15).json()
            if resp.get('ok'):
                mid = resp['result']['message_id']
                conn = sqlite3.connect(DB_PATH)
                c = conn.cursor()
                c.execute('UPDATE news SET message_id = ? WHERE id = ?', (mid, nid))
                conn.commit()
                conn.close()
        except Exception as e:
            print(f"news err: {e}")
        send(uid, "✅ خبرت به کانال رفت!")
        return

    send(uid, show_dashboard(uid), reply_markup=menu_main())
def process_callback(callback):
    uid = callback['from']['id']
    data = callback['data']
    cb_id = callback['id']
    u = get_user(uid)
    answer_cb(cb_id)

    if uid == ADMIN_ID and data.startswith("admin_"):
        process_admin_callback(uid, data, cb_id)
        return

    if data == "check":
        not_member = check_channels(uid)
        if not_member:
            return
        if not u or FI(u, 'step', 0) < 1:
            send(uid, "🛑 به عصر امپراطوری خوش آمدی!", reply_markup=kb([
                [{"text":"📖 راهنما","callback_data":"show_help_0"}],
                [{"text":"📝 ثبت نام","callback_data":"register"}]
            ]))
        else:
            send(uid, show_dashboard(uid), menu_main())
        return

    if data == "noop":
        return

    if data == "back_to_menu":
        send(uid, show_dashboard(uid), menu_main())
        return

    if data.startswith("show_help_") or data.startswith("help_page_"):
        page = int(data.replace("show_help_", "").replace("help_page_", ""))
        send(uid, get_help_text(page), reply_markup=menu_help_pages(page))
        return

    if data == "register":
        save_user({'user_id': uid, 'step': 0})
        send(uid, (
            "📝 ═══ *ثبت‌نام* ═══ 📝\n"
            "━━━━━━━━━━━━━━━━━━\n\n"
            "درود فرمانده\n"
            "برای شروع بازی نام کشور خود را تایپ کنید و بفرستید\n\n"
            "🛑 توجه:\n"
            "  • بین ۳ تا ۲۱ کاراکتر\n"
            "  • بدون ایموجی\n"
            "  • بدون کلمات رکیک"
        ))
        return

    if data.startswith("cont_"):
        cont = data.replace("cont_", "")
        if cont not in CONTINENTS:
            return
        save_user({'user_id': uid, 'continent': cont, 'step': 2})
        send(uid, (
            "🏛️ ═══ *کابینه سیاسی* ═══ 🏛️\n"
            "━━━━━━━━━━━━━━━━━━\n\n"
            "⏳ کابینه: انتخاب نشده\n"
            "⏳ رهبر: انتخاب نشده\n"
            "⏳ رئیس جمهور: انتخاب نشده\n"
            "⏳ نخست وزیر: انتخاب نشده\n\n"
            "🖋️ ابتدا نام *کابینه* رو بنویس:"
        ))
        return

    if data == "accept_rules":
        save_user({'user_id': uid, 'rules_accepted': 1, 'step': 7, 'tax': 100, 'last_income_time': get_iran_hour().isoformat()})
        send(uid, "🎉 به امپراطوری خوش آمدی!")
        send(uid, show_dashboard(uid), menu_main())
        return

    if data == "missions":
        show_missions(uid, u)
        return
    if data == "rank_missions":
        show_rank_missions(uid, u)
        return
    if data == "complete_daily_mission":
        complete_daily_mission(uid, u)
        return
    if data == "complete_rank_mission":
        complete_rank_mission(uid, u)
        return

    if data == "welfare":
        send(uid, "👠 *رفاه*\n👇 کدوم؟", reply_markup=menu_welfare())
        return
    if data == "welfare_pop":
        send(uid, "👥 *جمعیت*", reply_markup=menu_pop())
        return
    if data == "welfare_sat":
        send(uid, "🫂 *رضایت*", reply_markup=menu_sat())
        return
    if data.startswith("pop_"):
        idx = int(data.replace("pop_", ""))
        if 0 <= idx < len(POP_ITEMS):
            it = POP_ITEMS[idx]
            if FI(u, 'budget') < it['price']:
                send(uid, "❌ بودجه کافی نیست!")
                return
            save_user({'user_id': uid, 'budget': FI(u, 'budget') - it['price'], 'population': FI(u, 'population') + it['pop']})
            add_xp_for_purchase(uid, u)
            send(uid, f"✅ {it['name']} خریدی! 👥 +{it['pop']:,}")
        return
    if data.startswith("sat_"):
        idx = int(data.replace("sat_", ""))
        if 0 <= idx < len(SAT_ITEMS):
            it = SAT_ITEMS[idx]
            if FI(u, 'budget') < it['price']:
                send(uid, "❌ بودجه کافی نیست!")
                return
            new_sat = min(100, FI(u, 'satisfaction') + it['sat'])
            save_user({'user_id': uid, 'budget': FI(u, 'budget') - it['price'], 'satisfaction': new_sat})
            add_xp_for_purchase(uid, u)
            send(uid, f"✅ {it['name']} خریدی! 🫂 +{it['sat']}%")
        return

    if data == "black_market":
        send(uid, "🌑 *بازار سیاه*\n👇 انتخاب کن:", reply_markup=menu_black_market())
        return
    if data.startswith("bm_"):
        buy_bm(uid, data.replace("bm_", ""), u)
        return

    if data == "shop":
        send(uid, f"🛒 *فروشگاه*\n💳 کارت: `{CARD_NUMBER}`", reply_markup=menu_shop())
        return
    if data.startswith("shop_"):
        item_key = data.replace("shop_", "")
        save_user({'user_id': uid, 'pending_shop_item': item_key})
        send(uid, f"🧾 خرید *{item_key}*\n\n💳 کارت: `{CARD_NUMBER}`\n💰 مبلغ رو واریز کن و رسید رو بفرست.")
        return

    if data == "equipment":
        send(uid, (
            f"🧺 ═══ *تجهیزات* ═══ 🧺\n━━━━━━━━━━━━━━━━━━\n\n"
            f"🕵️ جاسوس: *{FI(u,'spy'):,}*\n"
            f"🗡️ ضربت: *{FI(u,'strike'):,}*\n"
            f"📡 آواکس ۱: *{FI(u,'awax1')}*\n"
            f"📡 آواکس ۲: *{FI(u,'awax2')}*\n"
            f"🧙 جادوگر: *{FI(u,'wizard')}*\n"
            f"👑 محافظ رهبر: *{FI(u,'leader_shield')}*\n"
            f"👥 بدل رهبر: *{FI(u,'leader_double')}*\n"
            f"🔍 کاوش: *{FI(u,'explorer'):,}*\n"
            f"👷 کارگر: *{FI(u,'workers'):,}*\n"
            f"🏦 بانک مرکزی: *{FI(u,'bank_central'):,}*\n"
            f"🌍 بانک جهانی: *{FI(u,'bank_world'):,}*\n"
            f"💰 کوین‌ساز: *{FI(u,'coin_maker'):,}*\n\n"
            f"━━━━━━━━━━━━━━━━━━\n"
            f"⚔️ ارتش: *{FI(u,'army'):,}*\n"
            f"🛡️ امنیت: *{FI(u,'security'):,}*"
        ), reply_markup=kb([[{"text":"🔙","callback_data":"back_to_menu"}]]))
        return

    if data == "buy":
        send(uid, "💸 *بازار* \n👇", reply_markup=menu_buy())
        return
    if data == "buy_econ":
        send(uid, "💰 *اقتصاد*", reply_markup=menu_econ())
        return
    if data == "buy_army":
        send(uid, "⚔️ *ارتش*", reply_markup=menu_army())
        return
    if data == "buy_sec":
        send(uid, "🛡️ *امنیت*", reply_markup=menu_sec())
        return
    if data == "buy_worker":
        send(uid, "👷 کارگر (۵۰K هر کدوم) — چند تا؟")
        save_user({'user_id': uid, 'admin_step': 504})
        return
    if data.startswith("econ_"):
        idx = int(data.replace("econ_", ""))
        if 0 <= idx < len(ECON_ITEMS):
            it = ECON_ITEMS[idx]
            save_user({'user_id': uid, 'admin_step': 501, 'war_target_id': idx})
            send(uid, f"🏭 *{it['name']}* — {it['price']:,}$ — سود {it['profit']:,}$\n🔢 چند تا؟")
        return
    if data.startswith("army_"):
        idx = int(data.replace("army_", ""))
        if 0 <= idx < len(ARMY_ITEMS):
            it = ARMY_ITEMS[idx]
            save_user({'user_id': uid, 'admin_step': 502, 'war_target_id': idx})
            send(uid, f"⚔️ *{it['name']}* — dmg {it['damage']:,} — {it['price']:,}$\n🔢 چند تا؟")
        return
    if data.startswith("sec_"):
        idx = int(data.replace("sec_", ""))
        if 0 <= idx < len(SEC_ITEMS):
            it = SEC_ITEMS[idx]
            save_user({'user_id': uid, 'admin_step': 503, 'war_target_id': idx})
            send(uid, f"🛡️ *{it['name']}* — res {it['res']:,} — {it['price']:,}$\n🔢 چند تا؟")
        return

    if data == "statement":
        today = get_iran_hour().strftime('%Y-%m-%d')
        daily = FI(u, 'daily_statements', 0)
        if F(u, 'last_statement_date', '') != today:
            daily = 0
        limit = 12
        lim_txt = "♾️" if FI(u, 'statements_unlimited', 0) == 1 else f"{daily}/{limit}"
        send(uid, f"📜 *دیوان بیانیه*\n\n📊 امروز: *{lim_txt}*\n⏳ کول‌داون: ۳۰ ثانیه", reply_markup=kb([
            [{"text":"✍️ نوشتن بیانیه","callback_data":"write_statement"}],
            [{"text":"🔙","callback_data":"back_to_menu"}]
        ]))
        return
    if data == "write_statement":
        today = get_iran_hour().strftime('%Y-%m-%d')
        daily = FI(u, 'daily_statements', 0)
        if F(u, 'last_statement_date', '') != today:
            daily = 0
        if daily >= 12 and FI(u, 'statements_unlimited', 0) == 0:
            send(uid, "❌ امروز به حد مجاز رسیدی")
            return
        last_st = F(u, 'last_statement_time', '')
        if last_st:
            try:
                if (get_iran_hour() - datetime.fromisoformat(last_st)).total_seconds() < 30:
                    send(uid, "⏳ ۳۰ ثانیه صبر کن")
                    return
            except:
                pass
        send(uid, "🖋️ بیانیه‌ات رو بنویس:")
        save_user({'user_id': uid, 'admin_step': 200})
        return

    if data == "invite":
        inv_cnt = FI(u,'invite_count')
        send(uid, f"🎭 *دعوت دوستان*\n\n👥 دعوت‌های تو: *{inv_cnt}*\n💰 هر دعوت: ۱۲۰,۰۰۰$", reply_markup=kb([
            [{"text":"🔗 دریافت لینک","callback_data":"get_invite_link"}],
            [{"text":"🔙","callback_data":"back_to_menu"}]
        ]))
        return
    if data == "get_invite_link":
        code = F(u,'invite_code', f'inv_{uid}')
        link = f"https://ble.ir/{BOT_USERNAME}?start={code}"
        send(uid, f"🔗 *لینک اختصاصی شما*\n\n`{link}`\n\n📌 روی لینک نگه دار و کپی کن")
        return

    if data == "support":
        send(uid, "🧾 *پشتیبانی*\n👇", reply_markup=kb([
            [{"text":"✍️ ارسال","callback_data":"write_support"}],
            [{"text":"🔙","callback_data":"back_to_menu"}]
        ]))
        return
    if data == "write_support":
        send(uid, "📝 پیامت رو بنویس:")
        save_user({'user_id': uid, 'admin_step': 201})
        return

    if data == "bank":
        if FI(u, 'rank', 1) < 5:
            send(uid, f"🏦 *بانک* — 🔒 فقط Diamond+\n\n🎗️ رنک تو: *{rank_name(FI(u, 'rank', 1))}*", reply_markup=kb([[{"text":"🔙","callback_data":"back_to_menu"}]]))
            return
        show_bank(uid, u)
        return
    if data.startswith("loan_"):
        handle_loan(uid, data)
        return
    if data == "pay_loan":
        handle_pay_loan(uid, u)
        return

    if data == "news":
        send(uid, "📰 *خبرگذاری*\n👇", reply_markup=kb([
            [{"text":"✍️ نوشتن","callback_data":"write_news"}],
            [{"text":"🔙","callback_data":"back_to_menu"}]
        ]))
        return
    if data == "write_news":
        today = get_iran_hour().strftime('%Y-%m-%d')
        if F(u, 'last_news_date', '') == today and FI(u, 'news_count', 0) >= 1:
            send(uid, "❌ امروز یه خبرت رو ثبت کردی")
            return
        send(uid, "📰 خبرت رو بنویس:")
        save_user({'user_id': uid, 'admin_step': 700})
        return
    if data.startswith("news_like_") or data.startswith("news_dislike_"):
        handle_news_vote(uid, u, data)
        return

    if data == "war_history":
        show_war_history(uid)
        return
    if data == "ranking":
        send(uid, show_ranking(), reply_markup=kb([[{"text":"🔙","callback_data":"back_to_menu"}]]))
        return
    if data == "rank":
        show_rank_info(uid, u)
        return

    if data == "map":
        mt, tp, tot = get_map_page(0, uid)
        if mt:
            btns = []
            if tp > 1:
                btns.append([{"text":"➡️","callback_data":"map_page_2"}])
            btns.append([{"text":"🔍 جستجو","callback_data":"map_search_input"}])
            btns.append([{"text":"🔙","callback_data":"back_to_menu"}])
            send(uid, mt, reply_markup=kb(btns))
        return
    if data.startswith("map_page_"):
        page = int(data.replace("map_page_", "")) - 1
        mt, tp, tot = get_map_page(page, uid)
        if mt:
            btns = []
            nav = []
            if page > 0:
                nav.append({"text":"⬅️","callback_data":f"map_page_{page}"})
            if page < tp - 1:
                nav.append({"text":"➡️","callback_data":f"map_page_{page+2}"})
            if nav:
                btns.append(nav)
            btns.append([{"text":"🔍 جستجو","callback_data":"map_search_input"}])
            btns.append([{"text":"🔙","callback_data":"back_to_menu"}])
            send(uid, mt, reply_markup=kb(btns))
        return
    if data == "map_search_input":
        send(uid, "🔍 اسم کشور رو بنویس (یا بخشی از اسم):")
        save_user({'user_id': uid, 'admin_step': 601})
        return
    if data.startswith("profile_"):
        target = int(data.replace("profile_", ""))
        send(uid, show_profile(target), reply_markup=kb([
            [{"text":"⚔️ حمله","callback_data":f"do_attack_{target}"}],
            [{"text":"🔙","callback_data":"map"}]
        ]))
        return

    if data == "attack":
        if F(u, 'war', 'صلح') == 'جنگ':
            send(uid, "⚔️ در حال جنگ هستی!")
            return
        if FI(u, 'security') < 15000:
            send(uid, "🛡️ امنیتت کمتر از ۱۵,۰۰۰ هست! اول امنیت بخر.", reply_markup=kb([
                [{"text":"🛡️ خرید امنیت","callback_data":"buy_sec"}],
                [{"text":"🔙","callback_data":"back_to_menu"}]
            ]))
            return
        if FI(u, 'army') < 1:
            send(uid, "❌ ارتش نداری!")
            return
        send(uid, "⚔️ *ستاد فرماندهی*\n👇 نوع حمله:", reply_markup=menu_attack())
        return
    if data == "atk_random":
        show_random_target(uid, u)
        return
    if data == "atk_revenge":
        show_revenge(uid, u)
        return
    if data == "atk_hidden":
        show_hidden(uid, u)
        return
    if data == "atk_spy":
        show_spy_menu(uid, u)
        return
    if data == "atk_search":
        send(uid, "🔍 اسم کشور رو بنویس:")
        save_user({'user_id': uid, 'admin_step': 600})
        return
    if data == "atk_bounty":
        show_bounty(uid, u)
        return
    if data == "atk_unstable":
        show_unstable(uid, u)
        return
    if data.startswith("do_attack_") or data.startswith("do_hidden_"):
        is_hidden = data.startswith("do_hidden_")
        target = int(data.replace("do_hidden_" if is_hidden else "do_attack_", ""))
        tu = get_user(target)
        if not tu:
            return
        max_army = FI(u, 'army')
        if max_army < 1:
            send(uid, "❌ ارتش نداری!")
            return
        send(uid, f"⚔️ *حمله*\n\n🎯 {F(tu,'country','')}\n⚔️ ارتش تو: {max_army:,}\n🛡️ دفاع دشمن: {FI(tu,'security'):,}\n\n🔢 چند تا ارتش بفرستی؟ (۱ تا {max_army})")
        save_user({'user_id': uid, 'admin_step': 620, 'war_target_id': target, 'admin_gift_type': 'hidden' if is_hidden else 'normal'})
        return
    if data.startswith("spy_target_"):
        target = int(data.replace("spy_target_", ""))
        save_user({'user_id': uid, 'admin_step': 601, 'war_target_id': target})
        send(uid, "🕵️ چند تا جاسوس؟")
        return

    if data == "expedition":
        do_expedition_prompt(uid, u)
        return

    if data == "alliance":
        aid = FI(u, 'alliance_id')
        if aid:
            show_alliance_panel(uid, u, aid)
        else:
            send(uid, "📟 *اتحاد*\nعضو هیچ اتحادی نیستی.", reply_markup=menu_alliance_main())
        return
    if data == "alliance_list":
        show_all_alliances(uid)
        return
    if data.startswith("alliance_view_"):
        aid = int(data.replace("alliance_view_", ""))
        show_alliance_info(uid, aid)
        return
    if data == "alliance_create":
        send(uid, "➕ *ساخت اتحاد*\n💰 ۵M$ یا ۵۰©", reply_markup=kb([
            [{"text":"💰 با پول","callback_data":"create_alliance_money"}],
            [{"text":"© با کوین","callback_data":"create_alliance_coin"}],
            [{"text":"🔙","callback_data":"alliance"}]
        ]))
        return
    if data == "create_alliance_money":
        if FI(u, 'budget') < 5000000:
            send(uid, "❌ بودجه کافی نیست")
            return
        save_user({'user_id': uid, 'budget': FI(u,'budget') - 5000000})
        send(uid, "✅ نام اتحاد رو بفرست:")
        save_user({'user_id': uid, 'admin_step': 300})
        return
    if data == "create_alliance_coin":
        if FI(u, 'coin') < 50:
            send(uid, "❌ کوین کافی نیست")
            return
        save_user({'user_id': uid, 'coin': FI(u,'coin') - 50})
        send(uid, "✅ نام اتحاد رو بفرست:")
        save_user({'user_id': uid, 'admin_step': 300})
        return
    if data.startswith("join_alliance_"):
        aid = int(data.replace("join_alliance_", ""))
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute('SELECT is_private FROM alliances WHERE id = ?', (aid,))
        r = c.fetchone()
        if not r:
            conn.close()
            return
        if r[0] == 1:
            send(uid, "❌ خصوصی")
            conn.close()
            return
        c.execute('INSERT INTO alliance_members (alliance_id, user_id, joined_at) VALUES (?, ?, ?)', (aid, uid, get_iran_hour().isoformat()))
        conn.commit()
        conn.close()
        save_user({'user_id': uid, 'alliance_id': aid})
        send(uid, "✅ عضو اتحاد شدی!")
        return
    if data == "alliance_members":
        aid = FI(u, 'alliance_id')
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute('SELECT user_id FROM alliance_members WHERE alliance_id = ?', (aid,))
        rows = c.fetchall()
        conn.close()
        msg = "👥 *اعضا*\n\n"
        for r in rows:
            tu = get_user(r[0])
            if tu:
                msg += f"• {F(tu,'country','')}\n"
        send(uid, msg, reply_markup=kb([[{"text":"🔙","callback_data":"alliance"}]]))
        return
    if data == "alliance_leave":
        aid = FI(u, 'alliance_id')
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute('SELECT leader_id FROM alliances WHERE id = ?', (aid,))
        r = c.fetchone()
        if r and r[0] == uid:
            send(uid, "❌ لیدر نمی‌تونه خارج بشه! اول یکی رو رهبر کن.", reply_markup=kb([[{"text":"👑 انتقال رهبری","callback_data":"alliance_transfer"}]]))
            conn.close()
            return
        conn.close()
        save_user({'user_id': uid, 'alliance_id': 0})
        send(uid, "❌ از اتحاد خارج شدی")
        return
    if data == "alliance_treasury":
        aid = FI(u, 'alliance_id')
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute('SELECT treasury FROM alliances WHERE id = ?', (aid,))
        r = c.fetchone()
        conn.close()
        tr = r[0] if r else 0
        send(uid, f"💰 خزانه: *{tr:,}$*", reply_markup=kb([
            [{"text":"💵 واریز ۱۰۰K","callback_data":"treasury_dep_100000"}],
            [{"text":"🔙","callback_data":"alliance"}]
        ]))
        return
    if data.startswith("treasury_dep_"):
        amount = int(data.replace("treasury_dep_", ""))
        if FI(u, 'budget') < amount:
            send(uid, "❌ بودجه کافی نیست")
            return
        aid = FI(u, 'alliance_id')
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute('UPDATE alliances SET treasury = treasury + ? WHERE id = ?', (amount, aid))
        conn.commit()
        conn.close()
        save_user({'user_id': uid, 'budget': FI(u,'budget') - amount})
        send(uid, f"✅ {amount:,}$ واریز شد")
        return
    if data == "alliance_transfer":
        aid = FI(u, 'alliance_id')
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute('SELECT leader_id FROM alliances WHERE id = ?', (aid,))
        r = c.fetchone()
        conn.close()
        if not r or r[0] != uid:
            send(uid, "❌ فقط لیدر")
            return
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute('SELECT user_id FROM alliance_members WHERE alliance_id = ? AND user_id != ?', (aid, uid))
        rows = c.fetchall()
        conn.close()
        if not rows:
            send(uid, "❌ عضو دیگه‌ای نیست")
            return
        btns = []
        for r in rows[:10]:
            tu = get_user(r[0])
            if tu:
                btns.append([{"text": F(tu,'country',''), "callback_data": f"transfer_{r[0]}"}])
        btns.append([{"text":"🔙","callback_data":"alliance"}])
        send(uid, "👑 رهبری رو به کی بدی؟", reply_markup=kb(btns))
        return
    if data.startswith("transfer_"):
        new_leader = int(data.replace("transfer_", ""))
        aid = FI(u, 'alliance_id')
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute('UPDATE alliances SET leader_id = ? WHERE id = ?', (new_leader, aid))
        conn.commit()
        conn.close()
        send(uid, "✅ رهبری منتقل شد")
        send(new_leader, "👑 تو رهبر جدید اتحاد شدی!")
        return

    # پیش‌فرض
    send(uid, show_dashboard(uid), menu_main())
# ==================== پنل ادمین ====================

def process_admin_callback(uid, data, cb_id):
    if data.startswith("admin_players_"):
        page = int(data.replace("admin_players_", ""))
        show_admin_players(uid, page)
        return
    if data.startswith("admin_view_"):
        target = int(data.replace("admin_view_", ""))
        tu = get_user(target)
        if not tu:
            send(uid, "❌ یافت نشد")
            return
        send(uid, show_dashboard(target))
        send(uid, f"👆 داشبورد *{F(tu,'country','')}*\n👇 عملیات:", reply_markup=menu_admin_player(target))
        return
    if data == "admin_search":
        send(uid, "🔍 اسم کشور رو بفرست:")
        save_user({'user_id': uid, 'admin_step': 'search'})
        return
    if data == "admin_stats":
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute('SELECT COUNT(*) FROM users WHERE step >= 5')
        total = c.fetchone()[0]
        c.execute('SELECT COUNT(*) FROM users WHERE step >= 5 AND is_banned = 0')
        active = c.fetchone()[0]
        c.execute('SELECT COUNT(*) FROM users WHERE step >= 5 AND is_banned = 1')
        banned = c.fetchone()[0]
        conn.close()
        send(uid, f"📊 *آمار*\n\n👥 کل: *{total}*\n✅ فعال: *{active}*\n🚫 بن: *{banned}*", reply_markup=kb([[{"text":"🔙","callback_data":"admin_back"}]]))
        return
    if data == "admin_help_all":
        send(uid, "💸 نوع کمک:", reply_markup=kb([
            [{"text":"💵 پول","callback_data":"admin_help_all_money"}],
            [{"text":"© کوین","callback_data":"admin_help_all_coin"}],
            [{"text":"⭐ XP","callback_data":"admin_help_all_xp"}],
            [{"text":"🔙","callback_data":"admin_back"}]
        ]))
        return
    if data.startswith("admin_help_all_"):
        gift = data.replace("admin_help_all_", "")
        send(uid, f"🔢 مقدار {gift} رو بفرست:")
        save_user({'user_id': uid, 'admin_step': f'help_all_{gift}'})
        return
    if data == "admin_help_one":
        send(uid, "🆔 اسم کشور رو بفرست:")
        save_user({'user_id': uid, 'admin_step': 'help_one_find'})
        return
    if data == "admin_ban_menu":
        send(uid, "🚫 *مدیریت بن*", reply_markup=kb([
            [{"text":"📋 لیست بازیکنان","callback_data":"admin_players_0"}],
            [{"text":"🔍 جستجو","callback_data":"admin_search_ban"}],
            [{"text":"🔙","callback_data":"admin_back"}]
        ]))
        return
    if data == "admin_search_ban":
        send(uid, "🔍 اسم کشور رو بفرست:")
        save_user({'user_id': uid, 'admin_step': 'search_ban'})
        return
    if data.startswith("admin_ban_") and data != "admin_ban_menu":
        target = int(data.replace("admin_ban_", ""))
        save_user({'user_id': target, 'is_banned': 1})
        tu = get_user(target)
        send(uid, f"✅ {F(tu,'country','')} بن شد")
        send(target, "🚫 شما بن شدید!")
        return
    if data.startswith("admin_unban_"):
        target = int(data.replace("admin_unban_", ""))
        save_user({'user_id': target, 'is_banned': 0})
        tu = get_user(target)
        send(uid, f"✅ {F(tu,'country','')} آنبن شد")
        send(target, "✅ آنبن شدی!")
        return
    if data.startswith("admin_rankup_"):
        target = int(data.replace("admin_rankup_", ""))
        tu = get_user(target)
        new_rank = min(15, FI(tu, 'rank', 1) + 1)
        save_user({'user_id': target, 'rank': new_rank})
        send(uid, f"✅ {F(tu,'country','')} → {rank_name(new_rank)}")
        send(target, f"🎉 رنک شما شد: {rank_name(new_rank)}")
        return
    if data.startswith("admin_send_money_"):
        target = int(data.replace("admin_send_money_", ""))
        send(uid, "💵 مقدار پول رو بفرست:")
        save_user({'user_id': uid, 'admin_step': f'send_money_{target}'})
        return
    if data.startswith("admin_send_coin_"):
        target = int(data.replace("admin_send_coin_", ""))
        send(uid, "© مقدار کوین رو بفرست:")
        save_user({'user_id': uid, 'admin_step': f'send_coin_{target}'})
        return
    if data.startswith("admin_edit_"):
        target = int(data.replace("admin_edit_", ""))
        send(uid, "✏️ فرمت: `field value`\nمثال: `budget 1000000`\n\nمجاز: budget, coin, population, satisfaction, army, security, land, hp, rank, xp")
        save_user({'user_id': uid, 'admin_step': f'edit_{target}'})
        return
    if data.startswith("admin_reset_"):
        target = int(data.replace("admin_reset_", ""))
        save_user({'user_id': target, 'budget': 200000, 'coin': 0, 'tax': 100, 'population': 1000, 'satisfaction': 100, 'army': 0, 'security': 0, 'land': 500, 'hp': 100, 'rank': 1, 'xp': 0, 'status': 'آرام', 'war': 'صلح'})
        send(uid, "✅ ریست شد")
        send(target, "🔄 اکانتت ریست شد")
        return
    if data == "admin_broadcast":
        send(uid, "📢 پیام همگانی:", reply_markup=kb([
            [{"text":"📷 با عکس","callback_data":"admin_bc_with_photo"}],
            [{"text":"💬 بدون عکس","callback_data":"admin_bc_no_photo"}],
            [{"text":"🔙","callback_data":"admin_back"}]
        ]))
        return
    if data == "admin_bc_no_photo":
        send(uid, "📝 متن پیام رو بفرست:")
        save_user({'user_id': uid, 'admin_step': 'broadcast_text'})
        return
    if data == "admin_bc_with_photo":
        send(uid, "📷 لینک عکس رو بفرست (اول عکس، بعد متن):")
        save_user({'user_id': uid, 'admin_step': 'broadcast_photo'})
        return
    if data == "admin_settings":
        war_status = get_setting("war_global", "صلح")
        send(uid, f"⚙️ *تنظیمات*\n\n🔫 وضعیت جنگ: *{war_status}*", reply_markup=kb([
            [{"text":"🔫 تغییر جنگ","callback_data":"admin_toggle_war"}],
            [{"text":"🔙","callback_data":"admin_back"}]
        ]))
        return
    if data == "admin_toggle_war":
        war_status = get_setting("war_global", "صلح")
        new_war = "جنگ" if war_status == "صلح" else "صلح"
        set_setting("war_global", new_war)
        send(uid, f"✅ وضعیت جنگ شد: *{new_war}*")
        return
    if data.startswith("reply_support_"):
        target = int(data.replace("reply_support_", ""))
        send(uid, "📩 پاسخ رو بنویس:")
        save_user({'user_id': uid, 'admin_step': f'reply_support_{target}'})
        return
    if data.startswith("close_support_"):
        send(uid, "✅ تیکت بسته شد")
        return
    if data.startswith("confirm_shop_"):
        parts = data.replace("confirm_shop_", "").split("_")
        target = int(parts[0])
        item_key = "_".join(parts[1:])
        apply_shop_item(target, item_key)
        send(uid, f"✅ خرید {item_key} اعمال شد")
        return
    if data.startswith("cancel_shop_"):
        target = int(data.replace("cancel_shop_", ""))
        send(uid, "❌ رد شد")
        send(target, "❌ خریدت رد شد")
        return
    if data == "admin_back":
        send(uid, "👑 *پنل مدیریت*", reply_markup=menu_admin())
        return

def show_admin_players(admin_uid, page):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT user_id, country, rank, budget, is_banned FROM users WHERE step >= 5 ORDER BY user_id LIMIT 20 OFFSET ?', (page * 20,))
    rows = c.fetchall()
    c.execute('SELECT COUNT(*) FROM users WHERE step >= 5')
    total = c.fetchone()[0]
    conn.close()
    if not rows:
        send(admin_uid, "❌ خالی")
        return
    btns = []
    for r in rows:
        banned = "🚫 " if r[4] else ""
        btns.append([{"text": f"{banned}{r[1]} — {rank_name(r[2])}", "callback_data": f"admin_view_{r[0]}"}])
    nav = []
    if page > 0:
        nav.append({"text":"⬅️","callback_data":f"admin_players_{page-1}"})
    if (page + 1) * 20 < total:
        nav.append({"text":"➡️","callback_data":f"admin_players_{page+1}"})
    if nav:
        btns.append(nav)
    btns.append([{"text":"🔙","callback_data":"admin_back"}])
    send(admin_uid, f"👥 *بازیکنان* ({page+1}/{(total+19)//20}) — کل: {total}", reply_markup=kb(btns))

def show_admin_search_results(admin_uid, query):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT user_id, country, rank FROM users WHERE country LIKE ? AND step >= 5 LIMIT 20", (f"%{query}%",))
    rows = c.fetchall()
    conn.close()
    if not rows:
        send(admin_uid, f"❌ نتیجه‌ای برای «{query}» پیدا نشد")
        return
    btns = []
    for r in rows:
        btns.append([{"text": f"{r[1]} — {rank_name(r[2])}", "callback_data": f"admin_view_{r[0]}"}])
    btns.append([{"text":"🔙","callback_data":"admin_back"}])
    send(admin_uid, f"🔍 نتایج «{query}»:", reply_markup=kb(btns))

def apply_shop_item(target, item_key):
    tu = get_user(target)
    if not tu:
        return
    if item_key == "unlimited_statement":
        save_user({'user_id': target, 'statements_unlimited': 1})
        send(target, "📜 بیانیه نامحدود فعال شد!")
    elif item_key == "rename":
        send(target, "✏️ اسم جدید رو بفرست:")
        save_user({'user_id': target, 'admin_step': 100})
    elif item_key == "rankup":
        new_rank = min(15, FI(tu, 'rank', 1) + 1)
        save_user({'user_id': target, 'rank': new_rank})
        send(target, f"🎉 رنک شد: {rank_name(new_rank)}")
    elif item_key == "shield_6h":
        save_user({'user_id': target, 'shield_end_time': (get_iran_hour() + timedelta(hours=6)).isoformat()})
        send(target, "🛡️ سپر ۶ ساعته فعال!")
    elif item_key == "shield_12h":
        save_user({'user_id': target, 'shield_end_time': (get_iran_hour() + timedelta(hours=12)).isoformat()})
        send(target, "🛡️ سپر ۱۲ ساعته فعال!")
    elif item_key == "shield_1d":
        save_user({'user_id': target, 'shield_end_time': (get_iran_hour() + timedelta(days=1)).isoformat()})
        send(target, "🛡️ سپر ۱ روزه فعال!")
    elif item_key == "money_500k":
        save_user({'user_id': target, 'budget': FI(tu, 'budget') + 500000})
        send(target, "💰 +۵۰۰,۰۰۰$")
    elif item_key == "money_1.5m":
        save_user({'user_id': target, 'budget': FI(tu, 'budget') + 1500000})
        send(target, "💰 +۱,۵۰۰,۰۰۰$")
    elif item_key == "money_3.5m":
        save_user({'user_id': target, 'budget': FI(tu, 'budget') + 3500000})
        send(target, "💰 +۳,۵۰۰,۰۰۰$")
    elif item_key == "coin_25":
        save_user({'user_id': target, 'coin': FI(tu, 'coin') + 25})
        send(target, "© +۲۵ کوین")
    elif item_key == "coin_45":
        save_user({'user_id': target, 'coin': FI(tu, 'coin') + 45})
        send(target, "© +۴۵ کوین")
    elif item_key == "coin_100":
        save_user({'user_id': target, 'coin': FI(tu, 'coin') + 100})
        send(target, "© +۱۰۰ کوین")

def process_admin_message(uid, txt, u):
    astep = F(u, 'admin_step', '')
    if not astep:
        return False
    if astep == 'search':
        show_admin_search_results(uid, txt)
        save_user({'user_id': uid, 'admin_step': 0})
        return True
    if astep == 'search_ban':
        show_admin_search_results(uid, txt)
        save_user({'user_id': uid, 'admin_step': 0})
        return True
    if astep.startswith('help_all_'):
        gift = astep.replace('help_all_', '')
        try:
            amount = int(txt)
        except:
            send(uid, "❌ عدد نامعتبر")
            save_user({'user_id': uid, 'admin_step': 0})
            return True
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute('SELECT user_id FROM users WHERE step >= 5')
        all_uids = [r[0] for r in c.fetchall()]
        conn.close()
        for tuid in all_uids:
            tu = get_user(tuid)
            if not tu: continue
            if gift == 'money':
                save_user({'user_id': tuid, 'budget': FI(tu, 'budget') + amount})
            elif gift == 'coin':
                save_user({'user_id': tuid, 'coin': FI(tu, 'coin') + amount})
            elif gift == 'xp':
                save_user({'user_id': tuid, 'xp': FI(tu, 'xp') + amount})
        send(uid, f"✅ {amount:,} {gift} به {len(all_uids)} نفر داده شد")
        save_user({'user_id': uid, 'admin_step': 0})
        return True
    if astep == 'help_one_find':
        show_admin_search_results(uid, txt)
        save_user({'user_id': uid, 'admin_step': 0})
        return True
    if astep.startswith('send_money_'):
        target = int(astep.replace('send_money_', ''))
        try: amount = int(txt)
        except:
            send(uid, "❌")
            save_user({'user_id': uid, 'admin_step': 0})
            return True
        tu = get_user(target)
        if tu:
            save_user({'user_id': target, 'budget': FI(tu, 'budget') + amount})
            send(uid, f"✅ {amount:,}$ به {F(tu,'country','')}")
            send(target, f"💵 +{amount:,}$ از طرف ادمین")
        save_user({'user_id': uid, 'admin_step': 0})
        return True
    if astep.startswith('send_coin_'):
        target = int(astep.replace('send_coin_', ''))
        try: amount = int(txt)
        except:
            send(uid, "❌")
            save_user({'user_id': uid, 'admin_step': 0})
            return True
        tu = get_user(target)
        if tu:
            save_user({'user_id': target, 'coin': FI(tu, 'coin') + amount})
            send(uid, f"✅ {amount} کوین به {F(tu,'country','')}")
            send(target, f"© +{amount} کوین از طرف ادمین")
        save_user({'user_id': uid, 'admin_step': 0})
        return True
    if astep.startswith('edit_'):
        target = int(astep.replace('edit_', ''))
        try:
            parts = txt.split(' ', 1)
            field = parts[0].strip()
            value = int(parts[1].strip())
        except:
            send(uid, "❌ فرمت: field value")
            save_user({'user_id': uid, 'admin_step': 0})
            return True
        allowed = ['budget', 'coin', 'population', 'satisfaction', 'army', 'security', 'land', 'hp', 'rank', 'xp']
        if field not in allowed:
            send(uid, f"❌ مجاز: {', '.join(allowed)}")
            save_user({'user_id': uid, 'admin_step': 0})
            return True
        save_user({'user_id': target, field: value})
        send(uid, f"✅ {field} = {value}")
        save_user({'user_id': uid, 'admin_step': 0})
        return True
    if astep.startswith('reply_support_'):
        target = int(astep.replace('reply_support_', ''))
        send(target, f"📩 *پاسخ پشتیبانی:*\n\n{txt}")
        send(uid, "✅ ارسال شد")
        save_user({'user_id': uid, 'admin_step': 0})
        return True
    if astep == 'broadcast_text':
        send_broadcast(uid, txt)
        save_user({'user_id': uid, 'admin_step': 0})
        return True
    if astep == 'broadcast_photo':
        save_user({'user_id': uid, 'admin_step': 'broadcast_photo_text', 'admin_gift_type': txt.strip()})
        send(uid, "📝 حالا متن پیام رو بفرست:")
        return True
    if astep == 'broadcast_photo_text':
        photo_url = F(u, 'admin_gift_type', '')
        send_broadcast(uid, txt, photo_url)
        save_user({'user_id': uid, 'admin_step': 0, 'admin_gift_type': ''})
        return True
    return False

def send_broadcast(admin_uid, text, photo_url=None):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT user_id FROM users WHERE step >= 5')
    all_uids = [r[0] for r in c.fetchall()]
    conn.close()
    cnt = 0
    for tuid in all_uids:
        try:
            if photo_url:
                send_photo(tuid, photo_url, f"📢 *پیام همگانی:*\n\n{text}")
            else:
                send(tuid, f"📢 *پیام همگانی:*\n\n{text}")
            cnt += 1
        except:
            pass
    send(admin_uid, f"✅ ارسال شد به {cnt} نفر")

# ==================== جنگ ====================

def show_random_target(uid, u):
    if FI(u, 'security') < 15000:
        send(uid, "🛡️ امنیتت کمتر از ۱۵,۰۰۰ هست!")
        return
    if FI(u, 'army') < 1:
        send(uid, "❌ ارتش نداری!")
        return
    last_atk = F(u, 'last_attack_time', '')
    if last_atk:
        try:
            if (get_iran_hour() - datetime.fromisoformat(last_atk)).total_seconds() < 120:
                send(uid, "⏳ صبر کن")
                return
        except: pass
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT user_id FROM users WHERE step >= 5 AND user_id != ? AND is_banned = 0 AND war = "صلح" ORDER BY RANDOM() LIMIT 1', (uid,))
    r = c.fetchone()
    conn.close()
    if not r:
        send(uid, "❌ حریفی نیست")
        return
    show_attack_confirm(uid, r[0])

def show_revenge(uid, u):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT DISTINCT attacker_id FROM attack_logs WHERE target_id = ? ORDER BY id DESC LIMIT 5', (uid,))
    rows = c.fetchall()
    conn.close()
    if not rows:
        send(uid, "❌ کسی بهت حمله نکرده")
        return
    btns = []
    for r in rows:
        tu = get_user(r[0])
        if tu:
            btns.append([{"text": f"⚔️ {F(tu,'country','')}", "callback_data": f"do_attack_{r[0]}"}])
    btns.append([{"text":"🔙","callback_data":"attack"}])
    send(uid, "🔁 *انتقام*", reply_markup=kb(btns))

def show_hidden(uid, u):
    first_hidden = get_setting(f"hidden_first_{uid}", "0")
    if first_hidden == "1":
        if FI(u, 'coin') < 15:
            send(uid, "❌ ۱۵ کوین نیازه")
            return
        save_user({'user_id': uid, 'coin': FI(u,'coin') - 15})
    else:
        set_setting(f"hidden_first_{uid}", "1")
    show_random_target(uid, u)

def show_bounty(uid, u):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT user_id FROM users WHERE step >= 5 AND user_id != ? AND war = "صلح" ORDER BY budget DESC LIMIT 4', (uid,))
    rows = c.fetchall()
    conn.close()
    if not rows:
        send(uid, "❌")
        return
    btns = []
    for r in rows:
        tu = get_user(r[0])
        if tu:
            btns.append([{"text": f"💰 {F(tu,'country','')}", "callback_data": f"do_attack_{r[0]}"}])
    btns.append([{"text":"🔙","callback_data":"attack"}])
    send(uid, "💰 *شکار جایزه*", reply_markup=kb(btns))

def show_spy_menu(uid, u):
    if FI(u, 'rank', 1) < 5:
        send(uid, "❌ فقط Diamond+")
        return
    if FI(u, 'spy') < 1:
        send(uid, "❌ جاسوس نداری!")
        return
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT user_id FROM users WHERE step >= 5 AND user_id != ? ORDER BY RANDOM() LIMIT 5', (uid,))
    rows = c.fetchall()
    conn.close()
    btns = []
    for r in rows:
        tu = get_user(r[0])
        if tu:
            btns.append([{"text": f"🕵️ {F(tu,'country','')}", "callback_data": f"spy_target_{r[0]}"}])
    btns.append([{"text":"🔙","callback_data":"attack"}])
    send(uid, "🕵️ *جاسوسی*", reply_markup=kb(btns))

def show_unstable(uid, u):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT user_id FROM users WHERE step >= 5 AND user_id != ? AND status = 'آشوب' ORDER BY RANDOM() LIMIT 5", (uid,))
    rows = c.fetchall()
    conn.close()
    if not rows:
        send(uid, "❌ آشوبی نیست")
        return
    btns = []
    for r in rows:
        tu = get_user(r[0])
        if tu:
            btns.append([{"text": f"🔥 {F(tu,'country','')}", "callback_data": f"do_attack_{r[0]}"}])
    btns.append([{"text":"🔙","callback_data":"attack"}])
    send(uid, "🔥 *شکار آشوب*", reply_markup=kb(btns))

def show_attack_confirm(uid, target_uid, is_hidden=False):
    u = get_user(uid)
    tu = get_user(target_uid)
    if not tu or not u:
        return
    if F(tu, 'war', 'صلح') == 'جنگ':
    send(uid, (
        f"⚔️ *تأیید حمله*\n\n"
        f"🎯 {F(tu,'country','')}\n"
        f"⚔️ ارتش دشمن: *{FI(tu,'army'):,}*\n"
        f"🛡️ دفاع دشمن: *{FI(tu,'security'):,}*\n"
        f"⚔️ ارتش تو: *{max_army:,}*\n\n"
        f"👇 حمله کن؟"
    ), reply_markup=kb([
        [{"text":"⚔️ حمله","callback_data":cb_data}],
        [{"text":"🔙","callback_data":"attack"}]
    ]))

def do_attack_with_count(uid, target_uid, u, count, is_hidden=False):
    last_atk = F(u, 'last_attack_time', '')
    if last_atk:
        try:
            if (get_iran_hour() - datetime.fromisoformat(last_atk)).total_seconds() < 120:
                send(uid, "⏳ صبر کن")
                return
        except: pass
    tu = get_user(target_uid)
    if not tu:
        send(uid, "❌")
        return
    if F(tu, 'war', 'صلح') == 'جنگ':
        send(uid, "🛡️ این کشور در حال جنگه!")
        return
    if count > FI(u, 'army'):
        send(uid, f"❌ فقط {FI(u,'army'):,} ارتش داری!")
        return
    t_block = F(tu, 'attack_block_time', '')
    if t_block:
        try:
            if datetime.fromisoformat(t_block) > get_iran_hour():
                send(uid, "🛡️ گارد داره")
                return
        except: pass
    t_shield = F(tu, 'shield_end_time', '')
    if t_shield:
        try:
            if datetime.fromisoformat(t_shield) > get_iran_hour():
                send(uid, "🛡️ شیلد داره")
                return
        except: pass
    
    my_power = count + FI(u,'strike')
    t_power = FI(tu,'army') + FI(tu,'security')
    
    if not is_hidden:
        awax = FI(tu, 'awax1') + FI(tu, 'awax2') * 2
        chance = {0:0, 1:25, 2:50, 3:75}.get(awax, 0)
        if chance > 0 and random.randint(1, 100) <= chance:
            send(target_uid, f"📡 آواکس: مهاجم: {F(u,'country','')}")
    
    now_iso = get_iran_hour().isoformat()
    save_user({'user_id': uid, 'last_attack_time': now_iso})
    ac = F(u, 'country', '')
    tc = F(tu, 'country', '')
    
    # سقوط کامل: power > 2x
    if my_power > t_power * 2:
        lb = int(FI(tu, 'budget') * 0.5)
        la = FI(tu, 'army')
        lp = int(FI(tu, 'population') * 0.05)
        lt = random.randint(1, 10)
        save_user({'user_id': uid, 'budget': FI(u,'budget') + lb, 'army': FI(u,'army') - count + la, 'population': FI(u,'population') + lp, 'land': FI(u,'land',500) + lt, 'total_attacks': FI(u,'total_attacks') + 1, 'total_wins': FI(u,'total_wins') + 1, 'total_ghonaimat': FI(u,'total_ghonaimat') + la, 'xp': FI(u, 'xp', 0) + 10})
        save_user({'user_id': target_uid, 'budget': FI(tu,'budget') - lb, 'army': 0, 'security': 0, 'population': max(0, FI(tu,'population') - lp), 'satisfaction': max(0, FI(tu,'satisfaction') - 20), 'hp': max(0, FI(tu,'hp',100) - 5), 'land': max(100, FI(tu,'land',500) - lt), 'status': 'سقوط', 'attack_block_time': (get_iran_hour() + timedelta(minutes=10)).isoformat(), 'total_losses': FI(tu,'total_losses') + 1})
        send(uid, f"✨ *سقوط!*\n\n🏴 {tc} سقوط کرد!\n🪤 غنیمت: {la:,}\n💰 {lb:,}$\n🧑 {lp:,}\n🏞️ +{lt} km\n⭐ +۱۰ XP")
        send(target_uid, f"⚠️ *سقوط!*\n\n{tc} توسط {ac} سقوط کرد!\n💰 -{lb:,}$\n🛡️ گارد ۱۰ دقیقه")
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute('INSERT INTO attack_logs (attacker_id, target_id, result, time, loot_budget, loot_army) VALUES (?, ?, ?, ?, ?, ?)', (uid, target_uid, 'win', now_iso, lb, la))
        c.execute('INSERT INTO war_history (attacker_id, target_id, attacker_country, target_country, result, time) VALUES (?, ?, ?, ?, ?, ?)', (uid, target_uid, ac, tc, 'win', now_iso))
        conn.commit()
        conn.close()
    elif my_power > t_power:
        lb = int(FI(tu, 'budget') * 0.15)
        la = int(FI(tu, 'army') * 0.3)
        save_user({'user_id': uid, 'budget': FI(u,'budget') + lb, 'army': FI(u,'army') - count + la, 'land': FI(u,'land',500) + 1, 'total_attacks': FI(u,'total_attacks') + 1, 'total_wins': FI(u,'total_wins') + 1, 'total_ghonaimat': FI(u,'total_ghonaimat') + la, 'xp': FI(u, 'xp', 0) + 5})
        save_user({'user_id': target_uid, 'budget': FI(tu,'budget') - lb, 'army': max(0, FI(tu,'army') - la), 'security': max(0, FI(tu,'security') - count), 'hp': max(0, FI(tu,'hp',100) - 5)})
        send(uid, f"⚔️ *پیروزی نسبی!*\n💰 {lb:,}$\n⚔️ {la:,}\n🏞️ +۱ km\n⭐ +۵ XP")
        send(target_uid, f"⚔️ *حمله!*\nاز {ac}\n❤️ -۵\n🛡️ دفاع -{count}")
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute('INSERT INTO attack_logs (attacker_id, target_id, result, time, loot_budget, loot_army) VALUES (?, ?, ?, ?, ?, ?)', (uid, target_uid, 'partial', now_iso, lb, la))
        conn.commit()
        conn.close()
    else:
        save_user({'user_id': uid, 'army': max(0, FI(u,'army') - count), 'hp': max(0, FI(u,'hp',100) - 5), 'total_attacks': FI(u,'total_attacks') + 1, 'total_losses': FI(u,'total_losses') + 1, 'xp': FI(u, 'xp', 0) + 2})
        save_user({'user_id': target_uid, 'security': max(0, FI(tu,'security') - count)})
        send(uid, f"💔 *شکست!*\n⚔️ -{count:,}\n❤️ -۵\n⭐ +۲ XP")
        send(target_uid, f"🛡️ *دفع شد!*\nاز {ac}\n🛡️ -{count}")
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute('INSERT INTO attack_logs (attacker_id, target_id, result, time) VALUES (?, ?, ?, ?)', (uid, target_uid, 'lose', now_iso))
        conn.commit()
        conn.close()

# ==================== NPC ====================

def init_npc():
    set_setting("npc_last_attack", get_iran_hour().isoformat())

def check_npc_attack():
    if get_iran_hour().weekday() == 4:
        return
    war_global = get_setting("war_global", "صلح")
    if war_global == "صلح":
        return
    last = get_setting("npc_last_attack", "")
    if not last:
        set_setting("npc_last_attack", get_iran_hour().isoformat())
        return
    try:
        last_dt = datetime.fromisoformat(last)
    except:
        set_setting("npc_last_attack", get_iran_hour().isoformat())
        return
    if (get_iran_hour() - last_dt).total_seconds() < 10800:
        return
    set_setting("npc_last_attack", get_iran_hour().isoformat())
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT user_id FROM users WHERE step >= 5 AND is_banned = 0 AND war = "صلح" AND npcs_disabled = 0 ORDER BY RANDOM() LIMIT 4')
    targets = [r[0] for r in c.fetchall()]
    conn.close()
    for tuid in targets:
        tu = get_user(tuid)
        if not tu: continue
        npc = random.choice(NPC_LIST)
        pp = FI(tu, 'army') + FI(tu, 'security')
        np = npc['army']
        if pp >= np:
            save_user({'user_id': tuid, 'budget': FI(tu, 'budget') + 50000, 'army': FI(tu, 'army') + 200, 'xp': FI(tu, 'xp', 0) + 3})
            send(tuid, "🛡️ *دفاع موفق!*\n💰 +۵۰K\n⚔️ +۲۰۰\n⭐ +۳ XP")
        else:
            al = int(FI(tu, 'army') * 0.3)
            bl = int(FI(tu, 'budget') * 0.1)
            ll = random.randint(1, 5)
            pl = int(FI(tu, 'population') * 0.02)
            save_user({'user_id': tuid, 'army': max(0, FI(tu, 'army') - al), 'budget': max(0, FI(tu, 'budget') - bl), 'population': max(0, FI(tu, 'population') - pl), 'land': max(100, FI(tu, 'land', 500) - ll), 'satisfaction': max(0, FI(tu, 'satisfaction', 100) - 5), 'hp': max(0, FI(tu, 'hp', 100) - random.randint(10, 30))})
            send(tuid, f"⚠️ *حمله!*\n\n⚔️ -{al:,}\n💰 -{bl:,}$\n👥 -{pl:,}\n🏞️ -{ll} km\n😁 -۵٪\n❤️ کم")

# ==================== توابع کمکی ====================

def show_profile(target_uid):
    u = get_user(target_uid)
    if not u: return "❌"
    country = F(u, 'country', '')
    fn = F(u, 'first_name', '')
    rank = FI(u, 'rank', 1)
    status = F(u, 'status', 'آرام')
    land = FI(u, 'land', 500)
    hp = FI(u, 'hp', 100)
    return f"👤 *{country}*\n\n👑 {fn}\n🎗️ {rank_name(rank)}\n📊 {status}\n🏞️ {land:,} km\n❤️ {hp}%"

def get_map_page(page, my_uid):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT user_id, country, rank, status, alliance_id FROM users WHERE step >= 5 ORDER BY country LIMIT 20 OFFSET ?', (page * 20,))
    users = c.fetchall()
    c.execute('SELECT COUNT(*) FROM users WHERE step >= 5')
    total = c.fetchone()[0]
    conn.close()
    if not users:
        return None, 0, 0
    icons = []
    for ud in users:
        if ud[0] == my_uid: icons.append("🔵")
        elif ud[3] == 'آشوب': icons.append("🟠")
        elif ud[3] == 'سقوط': icons.append("⚫")
        elif ud[3] == 'آرام':
            if ud[4] == 0: icons.append("🔴")
            elif ud[2] >= 10: icons.append("🟡")
            else: icons.append("🟢")
        else: icons.append("⚫")
    lines = []
    pos = 0
    for count in [4,3,5,2,4,3,5,4,3,4]:
        if pos >= len(icons): break
        row = icons[pos:pos+count]
        lines.append("|" + " " * random.randint(0,2) + "      ".join(row))
        pos += count
    while pos < len(icons):
        lines.append("|" + "      ".join(icons[pos:pos+4]))
        pos += 4
    map_text = "🗺️ *نقشه*\n━━━━━━━━━━━━━━━━━━\n" + "\n".join(lines) + "\n━━━━━━━━━━━━━━━━━━\n"
    map_text += "🟢آرام 🔵شما 🟡قدرتمند 🔴بدون اتحاد 🟠ویران ⚫سقوط\n"
    tp = (total + 19) // 20
    map_text += f"📊 کل: {total} | صفحه {page+1}/{tp}"
    return map_text, tp, total

def show_ranking():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT country, rank, army, land, hp, total_ghonaimat FROM users WHERE step >= 5 ORDER BY rank DESC, army DESC LIMIT 10')
    rows = c.fetchall()
    conn.close()
    msg = "🎖️ *۱۰ برتر*\n━━━━━━━━━━━━━━━━━━\n"
    medals = ["🥇","🥈","🥉"]
    for i, r in enumerate(rows, 1):
        m = medals[i-1] if i <= 3 else f"{i}."
        msg += f"\n{m} *{r[0]}*\n🎗️{rank_name(r[1])} | 🏞️{r[3]:,} | ❤️{r[4]}% | ⚔️{r[2]:,} | 💰{r[5]:,}\n"
    return msg

def show_rank_info(uid, u):
    rl = FI(u, 'rank', 1)
    xp = FI(u, 'xp')
    send(uid, f"🎗️ *رنک شما*\n\n📊 {rank_name(rl)}\n✨ XP: {xp}/100", reply_markup=kb([
        [{"text":"📋 ماموریت‌های رنک","callback_data":"rank_missions"}],
        [{"text":"🔙","callback_data":"back_to_menu"}]
    ]))

def show_missions(uid, u):
    today = get_iran_hour().strftime('%Y-%m-%d')
    last = F(u, 'last_mission_date', '')
    if not last:
        day = 1
    elif last == today:
        day = FI(u, 'daily_missions', 1)
    else:
        yest = (get_iran_hour() - timedelta(days=1)).strftime('%Y-%m-%d')
        day = FI(u, 'daily_missions', 1) + 1 if last == yest else 1
    if day > 60: day = 60
    save_user({'user_id': uid, 'daily_missions': day, 'last_mission_date': today})
    m = DAILY_MISSIONS.get(day, DAILY_MISSIONS[1])
    msg = f"📋 *ماموریت روزانه*\n\n📅 {m['title']}\n📊 روز {day}/60\n\n🎯 {m['label']}\n💰 پاداش: *{m['reward']:,}$*\n\n⚠️ اگه یه روز نیای ریست می‌شه"
    send(uid, msg, reply_markup=kb([
        [{"text":"✅ تکمیل","callback_data":"complete_daily_mission"}],
        [{"text":"🔙","callback_data":"back_to_menu"}]
    ]))

def complete_daily_mission(uid, u):
    today = get_iran_hour().strftime('%Y-%m-%d')
    if get_setting(f"mission_complete_{uid}", "") == today:
        send(uid, "❌ امروز تکمیل کردی!")
        return
    day = FI(u, 'daily_missions', 1)
    m = DAILY_MISSIONS.get(day, DAILY_MISSIONS[1])
    save_user({'user_id': uid, 'budget': FI(u, 'budget') + m['reward']})
    set_setting(f"mission_complete_{uid}", today)
    send(uid, f"✅ ماموریت روز {day}!\n💰 +{m['reward']:,}$")

def show_rank_missions(uid, u):
    rl = FI(u, 'rank', 1)
    m = RANK_MISSIONS.get(rl, RANK_MISSIONS[1])
    msg = f"🎗️ *ماموریت‌های رنک*\n\n🏆 {m['title']}\n\n📋 خرید: {FI(u,'total_purchases')}/{m['buy']}\n⚔️ حمله: {FI(u,'total_attacks')}/{m['attack']}\n📅 لاگین: {FI(u,'consecutive_login')}/{m['login']}\n\n⭐ با تکمیل همه = ۱۰۰ XP = رنک‌آپ"
    send(uid, msg, reply_markup=kb([
        [{"text":"✅ تکمیل","callback_data":"complete_rank_mission"}],
        [{"text":"🔙","callback_data":"back_to_menu"}]
    ]))

def complete_rank_mission(uid, u):
    rl = FI(u, 'rank', 1)
    m = RANK_MISSIONS.get(rl, RANK_MISSIONS[1])
    if FI(u,'total_purchases') < m['buy'] or FI(u,'total_attacks') < m['attack'] or FI(u,'consecutive_login') < m['login']:
        send(uid, "❌ هنوز همه وظایف انجام نشده")
        return
    new_rank = min(15, rl + 1)
    save_user({'user_id': uid, 'rank': new_rank, 'xp': 0})
    send(uid, f"🎉 *رنک‌آپ!*\n\n🎗️ {rank_name(new_rank)}\n⭐ +۱۰۰ XP")

def show_war_history(uid):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT attacker_country, target_country, result, time FROM war_history WHERE attacker_id = ? OR target_id = ? ORDER BY id DESC LIMIT 10', (uid, uid))
    rows = c.fetchall()
    conn.close()
    if not rows:
        send(uid, "📜 *تاریخچه*\n❌ خالی", reply_markup=kb([[{"text":"🔙","callback_data":"back_to_menu"}]]))
        return
    msg = "📜 *تاریخچه*\n\n"
    for r in rows:
        i = "✅" if r[2] == 'win' else "❌"
        msg += f"{i} {r[0]} → {r[1]}\n"
    send(uid, msg, reply_markup=kb([[{"text":"🔙","callback_data":"back_to_menu"}]]))

def show_bank(uid, u):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT amount, interest, remaining FROM loans WHERE user_id = ? AND status = "active"', (uid,))
    r = c.fetchone()
    conn.close()
    if r:
        btns = [[{"text":"💳 پرداخت","callback_data":"pay_loan"}],[{"text":"🔙","callback_data":"back_to_menu"}]]
        send(uid, f"💰 *بانک*\n\n💵 {r[0]:,}$\n📈 {r[1]}%\n💳 {r[2]:,}$", reply_markup=kb(btns))
    else:
        btns = []
        for i, lt in enumerate(LOAN_TYPES):
            if FI(u, 'rank', 1) >= lt['rank']:
                btns.append([{"text": f"{lt['name']} — {lt['amount']:,}$", "callback_data": f"loan_{i}"}])
        btns.append([{"text":"🔙","callback_data":"back_to_menu"}])
        send(uid, "💰 *بانک*", reply_markup=kb(btns))

def handle_loan(uid, data):
    try: idx = int(data.replace("loan_", ""))
    except: return
    if not (0 <= idx < len(LOAN_TYPES)): return
    lt = LOAN_TYPES[idx]
    u = get_user(uid)
    if FI(u, 'rank', 1) < lt['rank']:
        send(uid, "❌ رنک کافی نیست")
        return
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT id FROM loans WHERE user_id = ? AND status = "active"', (uid,))
    if c.fetchone():
        conn.close()
        send(uid, "❌ وام فعال داری")
        return
    total = int(lt['amount'] * 1.2)
    c.execute('INSERT INTO loans (user_id, amount, interest, remaining, next_payment, status) VALUES (?, ?, ?, ?, ?, "active")', (uid, lt['amount'], lt['interest'], total, get_iran_hour().isoformat()))
    conn.commit()
    conn.close()
    save_user({'user_id': uid, 'budget': FI(u, 'budget') + lt['amount']})
    send(uid, f"✅ وام {lt['name']}! {lt['amount']:,}$")

def handle_pay_loan(uid, u):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT id, remaining FROM loans WHERE user_id = ? AND status = "active"', (uid,))
    r = c.fetchone()
    if not r:
        conn.close()
        send(uid, "❌ وام نداری")
        return
    pay = int(r[1] * 0.2)
    if FI(u, 'budget') < pay:
        conn.close()
        send(uid, f"❌ {pay:,}$ نیازه")
        return
    rem = r[1] - pay
    if rem <= 0:
        c.execute('UPDATE loans SET remaining = 0, status = "paid" WHERE id = ?', (r[0],))
        save_user({'user_id': uid, 'budget': FI(u,'budget') - r[1]})
        send(uid, "✅ تسویه شد!")
    else:
        c.execute('UPDATE loans SET remaining = ? WHERE id = ?', (rem, r[0]))
        save_user({'user_id': uid, 'budget': FI(u,'budget') - pay})
        send(uid, f"✅ {pay:,}$ پرداخت شد. باقی: {rem:,}$")
    conn.commit()
    conn.close()

def show_all_alliances(uid):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT id, name, is_private FROM alliances LIMIT 20')
    rows = c.fetchall()
    conn.close()
    if not rows:
        send(uid, "❌ اتحادی نیست", reply_markup=kb([[{"text":"🔙","callback_data":"alliance"}]]))
        return
    btns = []
    for r in rows:
        lock = "🔒" if r[2] else "🔓"
        btns.append([{"text": f"{lock} {r[1]}", "callback_data": f"alliance_view_{r[0]}"}])
    btns.append([{"text":"🔙","callback_data":"alliance"}])
    send(uid, "📋 *اتحادها*", reply_markup=kb(btns))

def show_alliance_info(uid, aid):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT name, leader_id, treasury, is_private FROM alliances WHERE id = ?', (aid,))
    r = c.fetchone()
    c.execute('SELECT COUNT(*) FROM alliance_members WHERE alliance_id = ?', (aid,))
    cnt = c.fetchone()[0]
    conn.close()
    if not r: return
    lu = get_user(r[1])
    ln = F(lu, 'country', '') if lu else '?'
    btns = []
    u_aid = FI(get_user(uid), 'alliance_id')
    if u_aid != aid and not r[3]:
        btns.append([{"text":"➕ عضویت","callback_data":f"join_alliance_{aid}"}])
    btns.append([{"text":"🔙","callback_data":"alliance_list"}])
    send(uid, f"📟 *{r[0]}*\n👑 {ln}\n👥 {cnt}\n💰 {r[2]:,}$", reply_markup=kb(btns))

def show_alliance_panel(uid, u, aid):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT name, leader_id, treasury FROM alliances WHERE id = ?', (aid,))
    r = c.fetchone()
    conn.close()
    if not r: return
    is_leader = r[1] == uid
    send(uid, f"📟 *{r[0]}*\n💰 {r[2]:,}$", reply_markup=menu_alliance_panel(aid, is_leader))

def show_country_search_results(uid, query):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT user_id, country, rank FROM users WHERE country LIKE ? AND step >= 5 LIMIT 10", (f"%{query}%",))
    rows = c.fetchall()
    conn.close()
    if not rows:
        send(uid, f"❌ «{query}» پیدا نشد")
        return
    btns = []
    for r in rows:
        btns.append([{"text": f"{r[1]} — {rank_name(r[2])}", "callback_data": f"profile_{r[0]}"}])
    btns.append([{"text":"🔙","callback_data":"map"}])
    send(uid, f"🔍 «{query}»:", reply_markup=kb(btns))

def handle_news_vote(uid, u, data):
    is_like = data.startswith("news_like_")
    try: nid = int(data.split("_")[-1])
    except: return
    voted = F(u, 'voted_news', '')
    if str(nid) in voted.split(','):
        send(uid, "❌ قبلا رای دادی!")
        return
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT likes, dislikes, author_id, text, message_id FROM news WHERE id = ?', (nid,))
    row = c.fetchone()
    if not row:
        conn.close()
        return
    likes, dislikes, author_id, text, msg_id = row
    if is_like:
        likes += 1
        c.execute('UPDATE news SET likes = ? WHERE id = ?', (likes, nid))
    else:
        dislikes += 1
        c.execute('UPDATE news SET dislikes = ? WHERE id = ?', (dislikes, nid))
    conn.commit()
    conn.close()
    new_voted = voted + "," + str(nid) if voted else str(nid)
    save_user({'user_id': uid, 'voted_news': new_voted})
    au = get_user(author_id)
    an = F(au, 'country', '') if au else '?'
    channel_msg = f"📰 *خبر {an}*\n━━━━━━━━━━━━━━━━━━\n\n{text}\n\n━━━━━━━━━━━━━━━━━━\n👍 {likes}\n👎 {dislikes}\n\n🆔 `news_{nid}`"
    if msg_id:
        try:
            edit(REQUIRED_CHANNELS[2]['id'], msg_id, channel_msg, kb([[{"text":"👍","callback_data":f"news_like_{nid}"},{"text":"👎","callback_data":f"news_dislike_{nid}"}]]))
        except: pass
    send(uid, "✅ رای ثبت شد")

def buy_bm(uid, item_type, u):
    if item_type not in BM_ITEMS: return
    it = BM_ITEMS[item_type]
    field = it['field']
    cur = FI(u, field)
    if 'max' in it and cur >= it['max']:
        send(uid, f"❌ حداکثر {it['max']}")
        return
    if it['type'] == 'coin':
        if FI(u, 'coin') < it['cost']:
            send(uid, "❌ کوین کافی نیست!")
            return
    else:
        if FI(u, 'budget') < it['cost']:
            send(uid, "❌ بودجه کافی نیست!")
            return
    save_user({'user_id': uid, 'admin_step': 500, 'admin_gift_type': item_type})
    send(uid, f"🛒 *{it['name']}*\n💰 {it['cost']:,}\n📦 {cur}\n\n🔢 چند تا؟")

def do_expedition_prompt(uid, u):
    if FI(u, 'explorer') < 1:
        send(uid, "❌ کاوشگر نداری!")
        return
    exp_time = F(u, 'expedition_time', '')
    if exp_time:
        try:
            t = datetime.fromisoformat(exp_time)
            if t > get_iran_hour():
                rem = int((t - get_iran_hour()).total_seconds())
                send(uid, f"⏳ *اکسپدیشن فعال*\n🕐 {rem//3600}s {rem%3600//60}m\n📦 {FI(u, 'last_expedition_count')} کاوشگر")
                return
        except: pass
    send(uid, f"🗺️ *اکسپدیشن*\n📦 کاوشگر: {FI(u,'explorer')}\n💰 ۵۰K هر کدوم\n🕐 ۳ ساعت\n\n🔢 چند تا؟")
    save_user({'user_id': uid, 'admin_step': 610})

def do_expedition_start(uid, u, count):
    if count < 1 or count > FI(u, 'explorer'):
        send(uid, "❌ عدد نامعتبر")
        return
    cost = 50000 * count
    if FI(u, 'budget') < cost:
        send(uid, f"❌ {cost:,}$ نیازه")
        return
    now = get_iran_hour()
    save_user({'user_id': uid, 'budget': FI(u, 'budget') - cost, 'explorer': FI(u, 'explorer') - count, 'expedition_time': (now + timedelta(hours=3)).isoformat(), 'last_expedition_count': count})
    send(uid, f"🗺️ *اکسپدیشن شروع شد!*\n👥 {count}\n💰 {cost:,}$\n🕐 ۳ ساعت")

def check_exp():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT user_id FROM users WHERE expedition_time != '' AND step >= 5")
    uids = [r[0] for r in c.fetchall()]
    conn.close()
    now = get_iran_hour()
    for uid in uids:
        u = get_user(uid)
        if not u: continue
        try:
            t = datetime.fromisoformat(F(u, 'expedition_time', ''))
        except: continue
        if t <= now:
            count = FI(u, 'last_expedition_count', 1)
            if count < 1: count = 1
            tb = tc = ta = tl = 0
            results = []
            for i in range(count):
                res = random.choice(EXP_RESULTS)
                b = res['budget']; co = res['coin']; ar = res['army']; la = res['land']
                if la == 'random': la = random.randint(10, 100)
                if isinstance(b, int): tb += b
                if isinstance(co, int): tc += co
                if isinstance(ar, int): ta += ar
                if isinstance(l, int): tl += la
                results.append(res['name'])
            save_user({'user_id': uid, 'budget': max(0, FI(u, 'budget') + tb), 'coin': max(0, FI(u, 'coin') + tc), 'army': max(0, FI(u, 'army') + ta), 'land': FI(u, 'land', 500) + tl, 'expedition_time': '', 'last_expedition_count': 0, 'xp': FI(u, 'xp', 0) + (3 * count)})
            summary = f"🗺️ *نتیجه اکسپدیشن*\n👥 {count} کاوشگر\n\n"
            for i, r in enumerate(results, 1):
                summary += f"{i}. {r}\n"
            summary += f"\n🎁\n"
            if tb: summary += f"💰 {tb:+,}$\n"
            if tc: summary += f"© {tc:+}\n"
            if ta: summary += f"⚔️ {ta:+}\n"
            if tl: summary += f"🏞️ {tl:+}\n"
            summary += f"⭐ +{3*count} XP"
            send(uid, summary)
def main():
    init_db()
    init_npc()
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT COUNT(*) FROM map_pieces')
    if c.fetchone()[0] == 0:
        for i in range(250):
            c.execute('INSERT INTO map_pieces (id, x, y, w, h, owner_id, color) VALUES (?, ?, ?, ?, ?, 0, "gray")', (i, (i % 25) * 40, (i // 25) * 40, 40, 40))
        conn.commit()
    conn.close()
    
    offset = 0
    last_income = time.time()
    last_exp = time.time()
    last_npc = time.time()
    
    print("🚀 ربات عصر امپراطوری در حال اجراست...")
    
    while True:
        try:
            now = time.time()
            
            if now - last_income >= 5:
                try:
                    check_income_all()
                except Exception as e:
                    print(f"income err: {e}")
                last_income = now
                
            if now - last_exp >= 5:
                try:
                    check_exp()
                except Exception as e:
                    print(f"exp err: {e}")
                last_exp = now
                
            if now - last_npc >= 30:
                try:
                    check_npc_attack()
                except Exception as e:
                    print(f"npc err: {e}")
                last_npc = now
                
            updates = get_updates(offset)
            if updates.get('result'):
                for update in updates['result']:
                    offset = update['update_id'] + 1
                    try:
                        if 'message' in update:
                            threading.Thread(target=process_message, args=(update['message'],), daemon=True).start()
                        elif 'callback_query' in update:
                            threading.Thread(target=process_callback, args=(update['callback_query'],), daemon=True).start()
                    except Exception as e:
                        print(f"process err: {e}")
                        
            time.sleep(0.03)
            
        except Exception as e:
            print(f"❌ {e}")
            time.sleep(1)

if __name__ == "__main__":
    main()