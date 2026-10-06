import base64
import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = os.environ.get("BOT_TOKEN")
DB = {}

def encode(t):
    return base64.urlsafe_b64encode(t.encode()).decode().rstrip("=")

def decode(c):
    try:
        return base64.urlsafe_b64decode(c + "=" * (-len(c) % 4)).decode()
    except Exception:
        return None

async def simpan(update: Update, context: ContextTypes.DEFAULT_TYPE):
    fid = update.message.video.file_id if update.message.video else update.message.document.file_id
    rid = f"id-{len(DB)+1}{update.message.message_id}15248"
    DB[rid] = fid
    code = encode(rid)
    botname = (await context.bot.get_me()).username
    link = f"https://t.me/{botname}?start={code}"
    await update.message.reply_text(f"LINK JADI:\n{link}")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Kirim video/dokumen dulu untuk buat link.")
        return
    
    key = decode(context.args[0])
    fid = DB.get(key) if key else None
    
    if fid:
        await context.bot.send_video(update.effective_chat.id, fid, supports_streaming=True, protect_content=True)
    else:
        await update.message.reply_text("File tidak ditemukan atau link salah!")

if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.VIDEO | filters.Document.ALL, simpan))
    app.run_polling()
