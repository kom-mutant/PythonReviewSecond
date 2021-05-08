#!/usr/bin/env python
# pylint: disable=C0116
# This program is dedicated to the public domain under the CC0 license.

"""
Simple Bot to reply to Telegram messages.
First, a few handler functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.
"""

import logging
import datetime

from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from sqlalchemy import create_engine, Column, Integer, String, DateTime, select
from sqlalchemy.orm import declarative_base, Session

Base = declarative_base()


class Document(Base):
    __tablename__ = 'documents'

    id = Column(Integer, primary_key=True)
    title = Column(String)
    url = Column(String)
    last_updated = Column(DateTime)
    text = Column(String)
    # todo: storing tags, probably as a comma separated list of tags?
    tags = Column(String)


class Theme(Base):
    __tablename__ = 'themes'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    url = Column(String)
    description = Column(String)
    # todo: storing list of documents, probably as a comma separated list of ids?
    list_of_documents = Column(String)


# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments update and
# context.
def start(update: Update, _: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    update.message.reply_markdown_v2(
        fr'Hi {user.mention_markdown_v2()}\!',
        reply_markup=ForceReply(selective=True),
    )


def help_command(update: Update, _: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    update.message.reply_text("Используйте команды /new_docs, /new_topics, /topic, /doc, /words, "
                              "/describe_doc, /describe_topic")


def echo(update: Update, context: CallbackContext) -> None:
    """Echo the user message."""
    update.message.reply_text(context.args[0])


def new_docs(update: Update, context: CallbackContext) -> None:
    """показать N самых свежих новостей"""
    amount_to_show = context.args[0]
    update.message.reply_text(f"Запрошено {amount_to_show} свежих нововстей")


def new_topics(update: Update, context: CallbackContext) -> None:
    """показать N самых свежих тем"""
    amount_to_show = context.args[0]
    update.message.reply_text(f"Запрошено {amount_to_show} свежих тем")


def topic(update: Update, context: CallbackContext) -> None:
    """показать описание темы и заголовки 5 самых свежих новостей в этой теме"""
    topic_name = ' '.join(context.args)
    update.message.reply_text(f"Запрошен показ описания темы {topic_name} и 5 свежих нововстей по этой теме")


def doc(update: Update, context: CallbackContext) -> None:
    """показать текст документа с заданным заголовком"""
    doc_title = ' '.join(context.args)
    update.message.reply_text(f"Запрошено текст документа с заголовком {doc_title}")


def words(update: Update, context: CallbackContext) -> None:
    """показать 5 слов, лучше всего характеризующих тему"""
    topic_name = ' '.join(context.args)
    update.message.reply_text(f"Запрошены 5 слов лучше всего характерезующих тему {topic_name}")


def describe_doc(update: Update, context: CallbackContext) -> None:
    """вывести статистику по документу"""
    doc_title = ' '.join(context.args)
    update.message.reply_text(f"Запрошена статистика по документу: {doc_title}")


def describe_topic(update: Update, context: CallbackContext) -> None:
    """вывести статистику по теме"""
    topic_name = ' '.join(context.args)
    update.message.reply_text(f"Запрошена статистика по теме: {topic_name}")


def main() -> None:

    engine = create_engine("sqlite://", echo=True)
    Base.metadata.create_all(engine)
    session = Session(engine)
    document1 = Document(title="Заголовок", url="https://example.com", last_updated=datetime.datetime.utcnow(),
                         text="lorem ipsum bla bla bla", tags="яблоки, груши, абрикосы")
    document2 = Document(title="Заголовок2", url="https://example.com/2", last_updated=datetime.datetime.utcnow(),
                         text="lorem ipsum bla bla bla2", tags="яблоки, груши, абрикосы2")
    session.add(document1)
    session.add(document2)
    session.commit()
    print("now let's select")
    documents = Document.query.all()
    for document in documents:
        print(document.title)

    # session.close()

    # Create the Updater and pass it your bot's token.
    updater = Updater("1729021146:AAF6RPtBZnvmniwpsayFzrcjVsxQ7J2yZ8k")

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler('new_docs', new_docs))
    dispatcher.add_handler(CommandHandler('new_topics', new_topics))
    dispatcher.add_handler(CommandHandler('topic', topic))
    dispatcher.add_handler(CommandHandler('doc', doc))
    dispatcher.add_handler(CommandHandler('words', words))
    dispatcher.add_handler(CommandHandler('describe_doc', describe_doc))
    dispatcher.add_handler(CommandHandler('describe_topic', describe_topic))
    dispatcher.add_handler(CommandHandler("help", help_command))

    # on non command i.e message - echo the message on Telegram
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, help_command))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
