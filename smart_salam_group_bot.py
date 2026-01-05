from telegram.ext import Updater, MessageHandler, Filters, CommandHandler
from telegram.error import TelegramError
from langdetect import detect
import time

TOKEN = "8384209825:AAEmMwmbLGUl85pjFhI6-dgzVcRlOXfBpjM"

# وضعیت ربات
bot_active = True

# محدودیت پاسخ (ثانیه)
REPLY_COOLDOWN = 20
last_reply_time = {}

# جواب سلام به زبان‌ها
replies = {
    "fa": "سلام 👋 خوش اومدی",
    "en": "Hello 👋 Welcome",
    "tr": "Merhaba 👋 Hoş geldin",
    "ar": "مرحبا 👋 أهلاً",
    "fr": "Bonjour 👋 Bienvenue",
    "de": "Hallo 👋 Willkommen",
    "es": "Hola 👋 Bienvenido",
    "ru": "Привет 👋 Добро пожаловать",
    "it": "Ciao 👋 Benvenuto",
}

# کلمات سلام (فیلتر اولیه)
hello_words = [
    "سلام", "hello", "hi", "hey", "hola", "bonjour",
    "merhaba", "ciao", "hallo", "привет", "مرحبا"
]

def is_admin(update, context):
    try:
        user_id = update.effective_user.id
        chat_id = update.effective_chat.id
        admins = context.bot.get_chat_administrators(chat_id)
        return any(admin.user.id == user_id for admin in admins)
    except TelegramError:
        return False

def anti_spam(chat_id):
    now = time.time()
    last_time = last_reply_time.get(chat_id, 0)
    if now - last_time < REPLY_COOLDOWN:
        return True
    last_reply_time[chat_id] = now
    return False

def check_greeting(update, context):
    if not bot_active:
        return

    chat_id = update.effective_chat.id
    text = update.message.text.lower()

    # ضد فلود
    if anti_spam(chat_id):
        return

    # اگر سلام نبود کاری نکن
    if not any(word in text for word in hello_words):
        return

    try:
        lang = detect(text)
    except:
        lang = "en"

    reply = replies.get(lang, "Hello 👋")

    update.message.reply_text(reply)

def bot_on(update, context):
    global bot_active
    if not is_admin(update, context):
        update.message.reply_text("⛔️ فقط ادمین‌ها اجازه دارند")
        return
    bot_active = True
    update.message.reply_text("✅ ربات روشن شد")

def bot_off(update, context):
    global bot_active
    if not is_admin(update, context):
        update.message.reply_text("⛔️ فقط ادمین‌ها اجازه دارند")
        return
    bot_active = False
    update.message.reply_text("⛔️ ربات خاموش شد")

def start(update, context):
    update.message.reply_text(
        "🤖 ربات سلام‌ده هوشمند گروه\n"
        "🌍 تشخیص زبان خودکار\n"
        "🛡 ضد اسپم و فلود\n\n"
        "/on\n"
        "/off"
    )

updater = Updater(TOKEN, use_context=True)
dp = updater.dispatcher

dp.add_handler(CommandHandler("start", start))
dp.add_handler(CommandHandler("on", bot_on))
dp.add_handler(CommandHandler("off", bot_off))
dp.add_handler(MessageHandler(Filters.text & ~Filters.command, check_greeting))

updater.start_polling()
updater.idle()
