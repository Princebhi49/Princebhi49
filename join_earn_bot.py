import logging
import random
import string
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackContext, CallbackQueryHandler

# 🔐 Your Bot Token
BOT_TOKEN = '7983230537:AAEGttGnzOty7xho0tpkIRKjJQaJxToxoCU'

# 📌 Channels to join/public usernames
CHANNELS = [
    '@EarnReward_98',
    '@officialEarn_00',
    '@officalRewardEarn'
]

# 💸 Fake UPI payment message
UPI_MESSAGE = (
    "💸 Payment Successful!\n"
    "UPI ID: prince@upi\n"
    "Amount: ₹10"
)

# 🧩 Function to generate a random redeem code
def generate_code(length: int = 12) -> str:
    chars = string.ascii_uppercase + string.digits
    return ''.join(random.choice(chars) for _ in range(length))

# --- Bot Handlers ---

# /start command
def start(update: Update, context: CallbackContext):
    keyboard = [[InlineKeyboardButton("✅ I've Joined", callback_data='check')]]
    text = "👋 Welcome to the Join & Earn Bot!\n\n"
    text += UPI_MESSAGE + "\n\n"
    text += "🎯 Please join these channels to get your redeem code:\n"
    for c in CHANNELS:
        text += f"👉 {c}\n"
    text += "\nThen press ✅ to verify and receive your code!"
    update.message.reply_text(text, reply_markup=InlineKeyboardMarkup(keyboard))

# Callback when user clicks the button
def check_join(update: Update, context: CallbackContext):
    query = update.callback_query
    user_id = query.from_user.id
    # For simplicity: skip actual API check; assume joined
    code = generate_code()
    reply = (
        "🎉 Congratulations!\n"
        f"Here is your unique redeem code:\n
🔑 {code}"
    )
    query.message.reply_text(reply)
    query.answer()

# /setchannels command (admin-only) to update CHANNELS list
def setchannels(update: Update, context: CallbackContext):
    user = update.effective_user
    if not user or not user.id == int(context.bot.owner_id):
        update.message.reply_text("❌ You are not authorized.")
        return
    args = context.args
    if len(args) < 1:
        update.message.reply_text("Usage: /setchannels @chan1 @chan2 @chan3")
        return
    global CHANNELS
    CHANNELS = args
    update.message.reply_text(f"✅ Channels updated to: {', '.join(CHANNELS)}")

# Entry point
def main():
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    # Replace 'owner_id' with your Telegram user ID for admin commands
    dp.bot.owner_id = 'YOUR_TELEGRAM_ID'

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CallbackQueryHandler(check_join, pattern='check'))
    dp.add_handler(CommandHandler("setchannels", setchannels))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
