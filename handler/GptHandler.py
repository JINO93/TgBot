import json
import openai
import requests
from telegram import Update
from telegram.ext import CommandHandler, ContextTypes

BASE_AI_URL = "https://api.openai.com"
CHAT_URL = f"{BASE_AI_URL}/v1/chat/completions"
DRAW_URL = f"{BASE_AI_URL}/v1/images/generations"

AUTH_KEY = "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"
REQUEST_HEADER = {"Authorization": f"Bearer {AUTH_KEY}"}

ASK_CMD = "ask"
DRAW_CMD = "draw"

completionRecord = {}


async def ask_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    question = context.args[0]
    if update.effective_message.reply_to_message:
        ori_msg = update.effective_message.reply_to_message.text
        completionRecord[update.effective_chat.id].append(
            {
                "role": "system",
                "content": ori_msg
            }
        )
    else:
        data = []
        completionRecord[update.effective_chat.id] = data
    completionRecord[update.effective_chat.id].append(
        {
            "role": "user",
            "content": question
        }
    )
    answer = await askGpt(question, update.effective_chat.id)
    if answer:
        await context.bot.send_message(update.effective_chat.id, answer,
                                       reply_to_message_id=update.effective_message.id)


async def draw_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    answer = await drawGpt(context.args[0])
    if answer:
        await context.bot.send_photo(update.effective_chat.id, answer, reply_to_message_id=update.effective_message.id)


async def drawGpt(desp: str):
    rsp = requests.post(DRAW_URL, headers=REQUEST_HEADER,
                        json={"prompt": desp, "n": 1, "size": "1024x1024"})
    if rsp.status_code == 200:
        try:
            answer = json.loads(rsp.content)["data"][0]["url"]
            return answer
        except Exception as e:
            print(f"parse error msg:{e}")
    else:
        print(f"request error:{rsp.status_code}, msg:{rsp.content}")


async def askGpt(question: str, chat_id: int):
    rsp = requests.post(CHAT_URL, headers=REQUEST_HEADER,
                        json={"model": "gpt-3.5-turbo", "messages": getRequestMessageList(question, chat_id)})
    if rsp.status_code == 200:
        try:
            answer = json.loads(rsp.content)["choices"][0]["message"]["content"]
            return answer
        except Exception as e:
            print(f"parse error msg:{e}")
        # answer = ""
        # print(f"rsp content:{rsp.content} answer:{answer}")

    else:
        print(f"request error:{rsp.status_code}, msg:{rsp.content}")


def getRequestMessageList(question: str, chat_id: int):
    ret = completionRecord[chat_id]
    # if completionRecord[chat_id]:
    #     for idx, msg in enumerate(completionRecord[chat_id]):
    #         ret.append({
    #             "role": "user" if idx % 2 == 0 else "system",
    #             "content": msg
    #         })
    # ret.append({
    #     "role": "user",
    #     "content": question
    # })
    print(f"request message:{ret}")
    return ret


ask_handler = CommandHandler(ASK_CMD, ask_callback)
draw_handler = CommandHandler(DRAW_CMD, draw_callback)
