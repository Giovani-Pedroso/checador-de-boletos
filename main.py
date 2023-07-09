from telegram import Update, Bot
import time
import os
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from dotenv import load_dotenv
from reconhecimento import test, getTextImage, cleanData, getHeaderInfo
load_dotenv()

BOT_TOKEN = os.getenv('TOKEN_TELEGRAM')

NOME_DA_ASSISTENTE = "Jade"
# Commands
async def start_command(update, context):
    await update.message.reply_text(f"Olá, eu sou a {NOME_DA_ASSISTENTE}, estou aqui para te ajudar")
    await update.message.reply_text(f"Para testar um boleto tire uma foto da parte de baixo ou envie o arquvo PDF")

async def help_command(update, context):
    await update.message.reply_text("Tirre uma foto da parte de baixo do boleto para identificar se é um boleto valido")

async def test_command(update, context):
    await update.message.reply_text("comando de teste")

async def handle_message(update, context):
    await update.message.reply_text("Envie uma foto ou arquivo pdf para analize")

#Se ocorrer um error
async def error(update, context):
    print(f'\n\n--------------------------------------------------------\n\n')
    print(f'Update {update}')
    print(f' caused error {context.error}')

#Roda o comando quando quando o usuariio envia uma foto
async def photo_handler(update, context):
    
    await update.message.reply_text("Analizando a imagem")
    
    #print (update.message.photo[-1].file_id)

    #Pega o id da imagem com a maior resolucao
    file_id = update.message.photo[-1].file_id

    #Se remover a linha abaixo o codigo para de funcionar
    print (type(update.message.photo))

    #Salva a imagem para a analize
    file = await context.bot.getFile(file_id)
    file_path = f'./tmp/{file_id}.jpg'
    await file.download_to_drive(file_path)
    # await update.message.reply_text("Desculpe não consegui analizar a imagem")

    #Pega o texto da imagem
    texto_boleto = getTextImage(file_path)
    texto_boleto = cleanData(texto_boleto)
    heater_info = getHeaderInfo(texto_boleto)

    #Teste de checagem de boleto
    #Checa se codigo é da linha digitavel corresponde ao
    if header_info['bankCodeReal'] !=header_info['bankCodeReal']:
        await update.message.reply_text(f'O diz ser do banco {heater_info["bankName"]} porem essa informação não com o codigo {heater_info["bankCodeReal"]}')

#Analize um pdf
async def document_handler(update, context):
    file_id = update.message.document.file_id
    print("a PDF was sent")
    await update.message.reply_text("PDF recievied")
    file = await context.bot.getFile(file_id)
    await file.download_to_drive(f'./tmp/{file_id}.pdf')
    # await update.message.reply_text("Desculpe não consegui analizar o documento")

#Inicia o bot
if __name__ == '__main__':
    print("The bot is running")
    app = Application.builder().token(BOT_TOKEN).build()

    #Commands do bot
    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('help', help_command))
    app.add_handler(CommandHandler('test', test_command))
    
    #Messages
    app.add_handler(MessageHandler(filters.TEXT, handle_message))

    #Images
    app.add_handler(MessageHandler(filters.PHOTO, photo_handler))

    #Documents
    app.add_handler(MessageHandler(filters.Document.PDF, document_handler))
    
    #Erros
    app.add_error_handler(error)

    #Coloca o bot para rodar
    print('Polling...')
    app.run_polling(poll_interval=1)

