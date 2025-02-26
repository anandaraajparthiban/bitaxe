import json
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from datetime import datetime, timedelta
import time
from app import *


# Get text from PDFs
raw_text = get_pdf_text()

# Split text into chunks
text_chunks = get_text_chunks(raw_text)

# Create vector store
vectorstore = get_vectorstore(text_chunks)

# create conversation chain
chain = get_conversation_chain(vectorstore)


BotToken="7772604841:AAE1vANK35BmlW_Dze_u0VnrQ1GFC-vhBLM"

async def hello(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if context.args:
        arguments = ' '.join(context.args)
        arguments = arguments.replace("@bitaxe_osbot","").strip()
    print(arguments)
    BotToken="7772604841:AAE1vANK35BmlW_Dze_u0VnrQ1GFC-vhBLM"
    url = f"https://api.telegram.org/bot{BotToken}/getUpdates"
    output  = requests.get(url)
    fh = open('bitaxe.log','a')
    fh.write(output.text)
    fh.write('\n')
    fh.close()
    output = main(chain, arguments)
    #output = "test"
    await update.message.reply_text(f'{output}')

app = ApplicationBuilder().token(BotToken).build()

app.add_handler(CommandHandler("query", hello))

app.run_polling()
