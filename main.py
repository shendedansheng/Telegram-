import sys
from telegram.ext import Application, CommandHandler, MessageHandler, filters
from telegram import Update
from google_sheets import initialize_connection
from config import config
from bot_handlers import start, handle_search, handle_record, handle_add, handle_message

def main():
    if not config["TG_BOT_TOKEN"]:
        print("❌ 错误：缺少Telegram Token")
        sys.exit(1)
    
    if not initialize_connection():
        print("❌ 错误：无法连接谷歌表格")
        sys.exit(1)
    
    app = Application.builder().token(config["TG_BOT_TOKEN"]).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.Regex("^🔍 搜索$"), handle_search))
    app.add_handler(MessageHandler(filters.Regex("^📝 记录$"), handle_record))
    app.add_handler(MessageHandler(filters.Regex("^➕ 添加$"), handle_add))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    print("✅ 机器人已启动")
    app.run_polling()

if __name__ == "__main__":
    main()
