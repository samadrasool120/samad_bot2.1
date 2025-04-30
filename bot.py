import random
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, CallbackContext, MessageHandler, filters

# ✅ Env Variables
TOKEN = "7786155773:AAG5d5FYhqNXsdNXqZ21umJyhkKXxq_J6-g"  # Your API token
WHATSAPP_LINK = "https://whatsapp.com/channel/0029VbAknvc9sBIFbzgeCT2V"  # WhatsApp channel link
YOUTUBE_LINK = "https://youtube.com/@samadcolortradingvip?si=1copsO7FRkOpnPYh"  # YouTube channel link
TELEGRAM_LINK = "https://t.me/samadcolortradindvip"  # Telegram channel link

# 🎲 Prediction Logic
def get_signal(time_frame, period):
    signal_color = random.choice(["GREEN", "RED"])
    signal_size = random.choice(["BIG", "SMALL"])
    win_rate = random.randint(75, 95)
    
    return f"""🎯 PREMIUM SIGNAL  
━━━━━━━━━━━━━━  
📊 SIGNAL: {signal_color} / {signal_size}  
⏳ TIME: {time_frame}  
🔢 PERIOD: {period}  
📈 WIN RATE: {win_rate}%"""

# 🚀 Start Command
async def start(update: Update, context: CallbackContext):
    user = update.message.from_user
    keyboard = [
        [InlineKeyboardButton("✅ Join WhatsApp Channel", url=WHATSAPP_LINK)],
        [InlineKeyboardButton("📺 Subscribe on YouTube", url=YOUTUBE_LINK)],
        [InlineKeyboardButton("📱 Join Telegram Channel", url=TELEGRAM_LINK)],
        [InlineKeyboardButton("🔄 Check & Continue", callback_data="check_join")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        f"👋 Welcome {user.first_name}!\n\n📌 To continue, please join the WhatsApp channel first:", 
        reply_markup=reply_markup
    )

# 🔄 Check Subscription
async def check_join(update: Update, context: CallbackContext):
    query = update.callback_query
    await query.answer()  # Acknowledge the callback

    keyboard = [
        [InlineKeyboardButton("⚡ Wingo 30 Seconds", callback_data="wingo_30s")],
        [InlineKeyboardButton("⏳ Wingo 1 Minute", callback_data="wingo_1m")],
        [InlineKeyboardButton("⏲️ Wingo 3 Minutes", callback_data="wingo_3m")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.message.reply_text("✅ You have joined WhatsApp!\n\n🎮 Choose a game:", reply_markup=reply_markup)

# 🎮 Handle Wingo Mode Selection & Ask for Period
async def wingo(update: Update, context: CallbackContext):
    query = update.callback_query
    await query.answer()  # Acknowledge the callback
    
    time_frame_mapping = {
        "wingo_30s": "30 SEC",
        "wingo_1m": "1 MIN",
        "wingo_3m": "3 MIN"
    }

    time_frame = time_frame_mapping.get(query.data, "Unknown")
    context.user_data["time_frame"] = time_frame  # Store time frame in user data

    await query.message.reply_text(
        f"""⏱ MODE SELECTED  
Time Frame: {time_frame}  
━━━━━━━━━━━━━━  
Enter last 3 digits of period:"""
    )

# 🎯 Receive 3-Digit Period and Generate Signal
async def receive_period(update: Update, context: CallbackContext):
    period = update.message.text.strip()
    
    # ✅ Check if input is exactly 3 digits
    if not period.isdigit() or len(period) != 3:
        await update.message.reply_text("❌ Please enter exactly 3 digits.")
        return
    
    time_frame = context.user_data.get("time_frame", "Unknown")  # Retrieve time frame

    # Generate Signal
    signal = get_signal(time_frame, period)

    keyboard = [
        [InlineKeyboardButton("NEXT 30 SEC", callback_data="wingo_30s")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(signal, reply_markup=reply_markup)

# 🔥 Main Function
def main():
    app = Application.builder().token(TOKEN).build()

    # ✅ Handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(check_join, pattern="check_join"))
    app.add_handler(CallbackQueryHandler(wingo, pattern="wingo_30s|wingo_1m|wingo_3m"))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, receive_period))

    # 🚀 Start Bot
    print("Bot is running...")
    app.run_polling()

if name == "main":
    main()
