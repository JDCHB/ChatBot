import logging
import aiohttp
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext


API_KEY = "7686083232:AAG91hoA6McKm0PnDkF2uxcSy6O7kIiF_Q8"


# configura el inicio de sesion
logging.basicConfig(
    format='%(asctime)s -%(name)s -%(levelname)s -%(message)s', level=logging.INFO)
logging.info('Starting Bot...')


async def start_command(update: Update, content: CallbackContext):
    await update.message.reply_text('Hola! yo soy Tonyo, tu asistente virtual')


async def help_command(update: Update, content: CallbackContext):
    await update.message.reply_text('Oí un sonido de angustia, ¿Tienes algun problema?')


async def custom_command(update: Update, content: CallbackContext):
    await update.message.reply_text('Hola! si')


async def mensaje_chatbox(update: Update, content: CallbackContext):
    text = str(update.message.text).lower()
    user_id = update.message.chat.id  # --
    logging.info(f'User ({update.message.chat.id}) says: {text}')

    # -----------------------------------------------------------
    payload = {
        "sender": str(user_id),
        "message": text
    }

    async with aiohttp.ClientSession() as session:
        async with session.post("http://localhost:5005/webhooks/rest/webhook", json=payload) as response:
            rasa_response = await response.json()

    if rasa_response:
        for mensaje in rasa_response:

            if "text" in mensaje:
                await update.message.reply_text(mensaje["text"])

            if "image" in mensaje:
                await update.message.reply_photo(mensaje["image"])
    else:
        respuesta_rasa = "Lo siento, no entendí tu mensaje."
    # -----------------------------------------------------------

    # bot responde:
    await update.message.reply_text(respuesta_rasa)


async def error(update: Update, content: CallbackContext):
    logging.error(f'Update {update} causado por el error {content.error}')


"""if __name__ =='telegrambotci':
    updater=Updater(API_KEY, use_content=True)
    dp= updater.dispatcher"""
# Configuración principal del bot


def main():
    app = Application.builder().token(API_KEY).build()

    # Commands
    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('help', help_command))
    app.add_handler(CommandHandler('custom', custom_command))

    # Messages
    app.add_handler(MessageHandler(filters.TEXT, mensaje_chatbox))

    # Registrar todos los errores
    app.add_error_handler(error)

    # correr el bot
    logging.info("Bot iniciado...")
    app.run_polling()


"""updater.start_polling(2.0)
updater.idle()
"""
# Ejecutar el bot
if __name__ == "__main__":
    main()
