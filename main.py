import logging

from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

from handler.GptHandler import ask_handler, askGpt, draw_handler
from handler.newGptHandler import gpt_ask_handler, gpt_new_chat_handler, gpt_handlers

TOKEN = "6272334621:AAGR-wc-UgjsU3ew5KJCErYo_e7g_2RFz4E"

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id,
                                   text="I'm a bot, please talk to me!")


if __name__ == '__main__':
    application = ApplicationBuilder().token(TOKEN).build()

    start_handler = CommandHandler('start', start)
    application.add_handler(start_handler)
    # application.add_handler(ask_handler)
    # application.add_handler(draw_handler)
    application.add_handlers(gpt_handlers)

    application.run_polling()
    # askGpt("1+1=")
