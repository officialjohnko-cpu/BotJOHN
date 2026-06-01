# -*- coding: utf-8 -*-

# ===============================
# TELEGRAM VIP SHOP BOT
# Developer : @paing07709
# ===============================

# INSTALL:
# pip install pyTelegramBotAPI flask

import telebot
from telebot import types
import json
import os

from flask import Flask
from threading import Thread

# ================= CONFIG =================

BOT_TOKEN = "8897320866:AAEvGILDD3Mt2eTiv4paAHZyqsoJBe_AdmE"
ADMIN_ID = 8404894106 

bot = telebot.TeleBot(BOT_TOKEN)

USERS_FILE = "users.json"

broadcast_mode = {}

# ================= WEB SERVER =================

app = Flask(__name__)

@app.route('/')
def home():
    return "BOT RUNNING"

def run_web():
    app.run(host="0.0.0.0", port=10000)

Thread(target=run_web).start()

# ================= DATABASE =================

def load_users():

    if not os.path.exists(USERS_FILE):
        return []

    with open(USERS_FILE, "r") as f:

        try:
            return json.load(f)

        except:
            return []

def save_user(user_id):

    users = load_users()

    if user_id not in users:

        users.append(user_id)

        with open(USERS_FILE, "w") as f:
            json.dump(users, f)

# ================= START =================

@bot.message_handler(commands=['start'])
def start(message):

    user = message.from_user

    save_user(message.chat.id)

    keyboard = types.ReplyKeyboardMarkup(
        resize_keyboard=True
    )

    keyboard.row("📞 Contact Admin")
    keyboard.row("💎 Vip ဈေးနှုန်း")
    keyboard.row("💸 ငွေလွှဲရန်")

    # ADMIN PANEL
    if message.chat.id == ADMIN_ID:

        keyboard.row("/broadcast")
        keyboard.row("/users")

    bot.send_message(
        message.chat.id,
        f"""
👋 Welcome {user.first_name}

VIP Channel ဝယ်ယူရန် Menu ကို အသုံးပြုပါ။
""",
        reply_markup=keyboard
    )

# ================= CONTACT ADMIN =================

@bot.message_handler(
    func=lambda m: m.text == "📞 Contact Admin"
)
def contact_admin(message):

    keyboard = types.InlineKeyboardMarkup()

    btn = types.InlineKeyboardButton(
        "📩 Contact Admin",
        url="https://t.me/Videozone781"
    )

    keyboard.add(btn)

    bot.send_message(
        message.chat.id,
        "Admin ကို ဆက်သွယ်ရန် Button ကိုနှိပ်ပါ",
        reply_markup=keyboard
    )

# ================= VIP PRICE =================

@bot.message_handler(
    func=lambda m: m.text == "💎 Vip ဈေးနှုန်း"
)
def vip_price(message):

    bot.send_message(
        message.chat.id,
        """
💎 Vip Channel 34ကျော်
Premium VIP (34 Channels) 🥇
Local & Asian Collections 🌏
(1) 🇲🇲 Myanmar Local

(2) 💃 Myanmar Model

(3) 📼 Myanmar Old Service

(4) 🎬 Myanmar Inset

(5) 🎥 Myanmar Camera

(6) 🇲🇲 Hanti MM

(7) 💎 Myanmar Exclusive Models

(8) 📽️ Myanmar Old School
Hits

(9) 🔓 Share ဖြုတ်တဲ့မမလေး

(10) 🇨🇳🇲🇲 Chinese +

MyanmarInternational & Regional 🌐

(11) 🇬🇧 English 18+

(12) 🇰🇷 Korean 18+

(13) 🇹🇭 Thailand 18+

(14) 🇨🇳 Chinese 18+

(15) 🇯🇵 Japanese 18+

(16) 🔞 Jav 21+

(17) 💎 Jav Premium 21+

(18) 🇮🇳 India 184

(19) 🌏 Asian 18+

(20) ⭐ Asian Elite

Collection(21) 🌍 Global Mix 18+

Social Media & Trends 📱

(22) 📱 Tiktok Pron

(23) ✨ Tiktok Cele

(24) 📈 Tiktok Viral Trends

(25) 🌟 Only Fan + 18+

(26) 🔒 OnlyFans Premium Vault

(27) 📸 Candid Camera Files

Special & Hanti Series 🔥

(28) 🔥 Hanti 18+

(29) 🎬 Hanti Special Editions

(30) 🍼 Baby 1500+ Channel

(31) 🚶 Walking Pots

(32) 👬 BL 18+

(33) ⛓️ BDSM

(34) 🎭 BDSM & Unique Tastes

ရာသက်ပန် တစ်သက်စာ

💰 20000 ကျပ်
"""
    )

# ================= PAYMENT =================

@bot.message_handler(
    func=lambda m: m.text == "💸 ငွေလွှဲရန်"
)
def payment(message):

    bot.send_message(
        message.chat.id,
        """
💸 Kpay - Wave ဖြင့်၀ယ်ယူနိုင်သည်

📱 Ph - 09795763632

name - Thu Htet Lin 

📝 Note မှာ Shop လို့ရေးပေးပါ

📸 ပြီးပါက Screenshot ပို့ပေးပါ။
"""
    )

# ================= RECEIVE PHOTO =================

@bot.message_handler(content_types=['photo'])
def receive_photo(message):

    user = message.from_user

    username = user.username

    if username is None:
        username = "No Username"

    caption = f"""
📥 NEW PAYMENT

👤 Name : {user.first_name}

🔰 Username : @{username}

🆔 Chat ID : {message.chat.id}
"""

    keyboard = types.InlineKeyboardMarkup()

    done_btn = types.InlineKeyboardButton(
        "✅ Done",
        callback_data=f"done_{message.chat.id}"
    )

    not_btn = types.InlineKeyboardButton(
        "❌ Not Done",
        callback_data=f"not_{message.chat.id}"
    )

    keyboard.add(done_btn, not_btn)

    # SEND TO ADMIN
    bot.send_photo(
        ADMIN_ID,
        message.photo[-1].file_id,
        caption=caption,
        reply_markup=keyboard
    )

    # USER MESSAGE
    bot.send_message(
        message.chat.id,
        "✅ Screenshot ပို့ပြီးပါပြီ Admin စစ်ဆေးနေပါသည်။"
    )

# ================= CALLBACK =================

@bot.callback_query_handler(func=lambda call: True)
def callback(call):

    data = call.data

    # ================= DONE =================

    if data.startswith("done_"):

        user_id = int(data.split("_")[1])

        # SEND VIP LINK
        bot.send_message(
            user_id,
            """
✅ Payment Confirmed

🔗 Vip Channel Join Link

https://t.me/+86_9WwF1Fy85Nzk1
"""
        )

        # REMOVE BUTTON
        try:

            bot.edit_message_reply_markup(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                reply_markup=None
            )

        except:
            pass

        # UPDATE CAPTION
        try:

            bot.edit_message_caption(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                caption=call.message.caption + "\n\n✅ DONE"
            )

        except:
            pass

        bot.answer_callback_query(
            call.id,
            "DONE SUCCESS"
        )

    # ================= NOT DONE =================

    elif data.startswith("not_"):

        user_id = int(data.split("_")[1])

        # SEND ERROR
        bot.send_message(
            user_id,
            "❌ မအောင်မြင်ပါ ငွေလွှဲပြေစာ မှူးယွင်းနေသည်"
        )

        # REMOVE BUTTON
        try:

            bot.edit_message_reply_markup(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                reply_markup=None
            )

        except:
            pass

        # UPDATE CAPTION
        try:

            bot.edit_message_caption(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                caption=call.message.caption + "\n\n❌ NOT DONE"
            )

        except:
            pass

        bot.answer_callback_query(
            call.id,
            "NOT DONE SUCCESS"
        )

# ================= BROADCAST =================

@bot.message_handler(commands=['broadcast'])
def broadcast(message):

    if message.chat.id != ADMIN_ID:
        return

    broadcast_mode[message.chat.id] = True

    bot.send_message(
        ADMIN_ID,
        """
📢 Broadcast Mode ON

စာ / ပုံ / Video ပို့နိုင်သည်
"""
    )

# ================= SEND BROADCAST =================

@bot.message_handler(
    func=lambda message: message.chat.id in broadcast_mode,
    content_types=['text', 'photo', 'video']
)
def send_broadcast(message):

    users = load_users()

    success = 0
    failed = 0

    # ================= TEXT =================

    if message.content_type == "text":

        for user_id in users:

            try:

                bot.send_message(
                    user_id,
                    message.text
                )

                success += 1

            except:

                failed += 1

    # ================= PHOTO =================

    elif message.content_type == "photo":

        photo = message.photo[-1].file_id

        caption = message.caption if message.caption else ""

        for user_id in users:

            try:

                bot.send_photo(
                    user_id,
                    photo,
                    caption=caption
                )

                success += 1

            except:

                failed += 1

    # ================= VIDEO =================

    elif message.content_type == "video":

        video = message.video.file_id

        caption = message.caption if message.caption else ""

        for user_id in users:

            try:

                bot.send_video(
                    user_id,
                    video,
                    caption=caption
                )

                success += 1

            except:

                failed += 1

    # ================= RESULT =================

    bot.send_message(
        ADMIN_ID,
        f"""
📢 Broadcast Complete

✅ Success : {success}
❌ Failed : {failed}
"""
    )

    del broadcast_mode[message.chat.id]

# ================= USERS =================

@bot.message_handler(commands=['users'])
def users_list(message):

    if message.chat.id != ADMIN_ID:
        return

    users = load_users()

    text = f"👥 Total Users : {len(users)}\n\n"

    for user in users:

        text += f"{user}\n"

    bot.send_message(
        ADMIN_ID,
        text
    )

# ================= RUN =================

print("BOT RUNNING...")

bot.infinity_polling()
