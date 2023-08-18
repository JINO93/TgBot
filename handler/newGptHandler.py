from revChatGPT.V1 import Chatbot
from telegram import Update
from telegram.ext import ContextTypes, CommandHandler

from config import gpt_access_token
from model.chat_info import ChatInfo

chatbot = Chatbot(config={
    "access_token": gpt_access_token
})

chat_info = ChatInfo("", "", "")


async def ask_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    question = context.args[0]
    pre_answer = ""
    c_id = ""
    p_id = ""
    current_conversation_id = chat_info.conversation_id
    for data in chatbot.ask(prompt=question, conversation_id=current_conversation_id):
        message_ = data['message']
        c_id = data['conversation_id']
        p_id = data['parent_id']
        if len(message_) != len(pre_answer):
            pre_answer = message_
    if pre_answer:
        if c_id != chat_info.conversation_id:
            chat_info.conversation_id = c_id
            chat_info.parent_id = p_id
            chat_info.content = pre_answer
        await context.bot.send_message(update.effective_chat.id, pre_answer,
                                       reply_to_message_id=update.effective_message.id)


async def new_chat_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_info.conversation_id = ""
    chat_info.parent_id = ""
    chat_info.content = ""
    await context.bot.send_message(update.effective_chat.id, "已开启新会话，请说出你的问题",
                                   reply_to_message_id=update.effective_message.id)


gpt_ask_handler = CommandHandler("ask", ask_callback)
gpt_new_chat_handler = CommandHandler("new_chat", new_chat_callback)

gpt_handlers = [
    gpt_ask_handler,
    gpt_new_chat_handler
]
