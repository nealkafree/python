import logging
import os
import shutil

import ffmpeg
import face_recognition
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters


def get_token():
    with open('token', encoding='UTF-8') as file:
        return file.read()


def start_command(update, context):
    text = 'Я сохраняю ваши аудиосообщения и фотографии с лицами.'
    user_id = str(update.message.from_user.id)
    if not os.path.exists(user_id):
        os.mkdir(str(user_id))
    context.bot.send_message(chat_id=update.effective_chat.id, text=text)


def help_command(update, context):
    text = 'Я сохраняю ваши аудиосообщения и фотографии с лицами.\n' \
           'Возможные команды:\n' \
           '/help - помощь\n' \
           '/get_voices - получить ваши аудиоосообщения\n' \
           '/get_photos - получить ваши сохраненные фотографии'
    context.bot.send_message(chat_id=update.effective_chat.id, text=text)


def get_voices(update, context):
    path = os.path.join(str(update.message.from_user.id), 'voices')
    archive_path = os.path.join(path, 'voices_archive')
    shutil.make_archive(archive_path, 'zip', path)

    context.bot.send_document(chat_id=update.effective_chat.id, document=open(archive_path + '.zip', 'rb'))
    os.remove(archive_path + '.zip')


def get_photos(update, context):
    path = os.path.join(str(update.message.from_user.id), 'photos')
    archive_path = os.path.join(path, 'photos_archive')
    shutil.make_archive(archive_path, 'zip', path)

    context.bot.send_document(chat_id=update.effective_chat.id, document=open(archive_path + '.zip', 'rb'))
    os.remove(archive_path + '.zip')


def save_voice(update, context):
    user_id = str(update.message.from_user.id)
    path = os.path.join(user_id, 'voices')
    if not os.path.exists(path):
        os.mkdir(path)

    file_id = update.message.voice.file_id
    new_voice = context.bot.get_file(file_id)
    new_voice.download(os.path.join(path, 'temp'))

    stream = ffmpeg.input(os.path.join(path, 'temp'))
    stream = ffmpeg.output(stream, os.path.join(path, 'audio_message_' + str(len(os.listdir(path)) - 1)), f='wav',
                           ar=16000)
    ffmpeg.run(stream)

    text = 'Голосовое сообщение сохранено.'
    context.bot.send_message(chat_id=update.effective_chat.id, text=text)
    os.remove(os.path.join(path, 'temp'))


def save_photo(update, context):
    user_id = str(update.message.from_user.id)
    path = os.path.join(user_id, 'photos')
    if not os.path.exists(path):
        os.mkdir(path)

    new_photo = context.bot.get_file(update.message.photo[-1].file_id)
    path_to_photo = os.path.join(path, 'photo_' + str(len(os.listdir(path))))
    new_photo.download(path_to_photo)

    image = face_recognition.load_image_file(path_to_photo)
    face_locations = face_recognition.face_locations(image)
    if len(face_locations) == 0:
        os.remove(path_to_photo)
        text = 'Эта фотография не сохранена.'
    else:
        text = 'Эта фотография сохранена.'

    context.bot.send_message(chat_id=update.effective_chat.id, text=text)


def echo(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

REQUEST_KWARGS = {
    'proxy_url': 'socks5h://5.79.83.132:42332/'
}

updater = Updater(token=get_token(), use_context=True, request_kwargs=REQUEST_KWARGS)
dispatcher = updater.dispatcher

dispatcher.add_handler(CommandHandler('start', start_command))
dispatcher.add_handler(CommandHandler('help', help_command))
dispatcher.add_handler(CommandHandler('get_voices', get_voices))
dispatcher.add_handler(CommandHandler('get_photos', get_photos))
dispatcher.add_handler(MessageHandler(Filters.text, echo))
dispatcher.add_handler(MessageHandler(Filters.voice, save_voice))
dispatcher.add_handler(MessageHandler(Filters.photo, save_photo))

print('start pooling')
updater.start_polling()
