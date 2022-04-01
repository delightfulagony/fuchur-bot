#!/usr/bin/env python

"""
Bot to welcome new members inside Dragonscale Castle Chat
"""

import logging
from apscheduler.schedulers.background import BackgroundScheduler
import datetime
from random import randint
from telegram import Bot, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, Filters, MessageHandler, CommandHandler, CallbackQueryHandler

######
# GLOBAL VARIABLES
# DS Chat Index
with open('dschat.txt', 'r') as file:
    ds_chat_id = file.read()

# Opens tutors file readonly
with open('tutors.txt', 'r') as file:
  tutors = file.read().split() # Open english welcome message readonly
with open('welcome_en.html', 'r') as file:
  welcome_en = file.read()
# Open spanish welcome message readonly
with open('welcome_es.html', 'r') as file:
  welcome_es = file.read()

# Index for tutors list
current_tutor_index = 0

# Open fuchur quotes
with open('scratch_responses.txt', 'r') as file:
    scratch_responses = file.read().split('\n')

# Start the scheduler
scheduler = BackgroundScheduler()

## Bot init
with open('token.txt', 'r') as file: # Get bot token from file
    TOKEN = file.read().rstrip()

updater = Updater(TOKEN, use_context=True) # Init the updater
dp = updater.dispatcher # Start the dispatcher
##
######

####
# Welcome message for chat
def welcome_message(update, context):
  global current_tutor_index
  global last_welcome_message

  # Set language of the message
  welcome = welcome_en

  ##
  # Configure Inline Keyboard
  tutor_button = InlineKeyboardButton(
    "To join, talk to a tutor!",
    url=tutors[current_tutor_index]
    ) # Button for contacting a tutor

  welcome_button = InlineKeyboardButton(
    "Español",
    callback_data='welcome_es'
    ) # Button for switching language to spanish

  welcome_keyboard = InlineKeyboardMarkup([
    [welcome_button],
    [tutor_button]
    ]) # Welcome message Inline Keyboard
  ##

  current_tutor_index = (current_tutor_index+1)%len(tutors) # Set next tutor index

  try:
    last_welcome_message.delete() # Deletes last welcome message
  except:
    pass # Nothing to do if unsuccessful

  last_welcome_message = update.message.reply_html(
    welcome, 
    disable_web_page_preview=True, 
    reply_markup=welcome_keyboard
    ) # Sends welcome message
####

####
# Translates welcome message to spanish
def translate_welcome_to_es(update, context):
  global current_tutor_index

  # Set language of the message
  welcome = welcome_es

  ##
  # Configure Inline Keyboard
  tutor_button = InlineKeyboardButton(
    "Para unirte, contacta con un tutor!", 
    url=tutors[current_tutor_index]
    ) # Button for contacting a tutor

  welcome_button = InlineKeyboardButton(
    "English", 
    callback_data='welcome_en'
    ) # Button for switching language to english

  welcome_keyboard = InlineKeyboardMarkup([
    [welcome_button],
    [tutor_button]
    ]) # Welcome message Inline Keyboard
  ##

  current_tutor_index = (current_tutor_index+1)%len(tutors) # Set next tutor index

  update.callback_query.edit_message_text(
    welcome, 
    parse_mode='HTML', 
    disable_web_page_preview=True
    ) # Edits message language
  update.callback_query.edit_message_reply_markup(
    reply_markup=welcome_keyboard
    ) # Edits Inline Keyboard language
####

####
# Translates welcome message back to english
def translate_welcome_to_en(update, context):
  global current_tutor_index

  # Set language of the message
  welcome = welcome_en

  ##
  # Configure Inline Keyboard
  tutor_button = InlineKeyboardButton(
    "To join, talk to a tutor!", 
    url=tutors[current_tutor_index]
    ) # Button for contacting a tutor

  welcome_button = InlineKeyboardButton(
    "Español", 
    callback_data='welcome_es'
    ) # Button for switching language to spanish

  welcome_keyboard = InlineKeyboardMarkup([
    [welcome_button],
    [tutor_button]
    ]) # Welcome message Inline Keyboard
  ##
  
  current_tutor_index = (current_tutor_index+1)%len(tutors) # Set next tutor index

  update.callback_query.edit_message_text(
    welcome,
    parse_mode='HTML', 
    disable_web_page_preview=True
    ) # Edits message language
  update.callback_query.edit_message_reply_markup(
    reply_markup=welcome_keyboard
    ) # Edits Inline Keyboard language
####

####
# Message requesting to be scratched
def scratch_request():
  scratch_message="Can you scratch my ear? I always have so much trouble reaching there."

  scratch_button = InlineKeyboardButton("Scratch Fuchur's ear", callback_data='scratch')
  scratch_keyboard = InlineKeyboardMarkup([[scratch_button]])

  updater.bot.send_message(ds_chat_id, scratch_message, reply_markup=scratch_keyboard)

  days = randint(2,4)
  hours = randint(0,23)
  minutes = randint(0,59)
  seconds = randint(0,59)
  scratch_date = datetime.datetime.now() + datetime.timedelta(hours=hours, minutes=minutes, seconds=seconds)
  with open('scratch_date.txt', 'w') as file:
    file.write(scratch_date.isoformat())
      
  scheduler.add_job(scratch_request, trigger='date', run_date=scratch_date, id='fuchur_request', misfire_grace_time=2**30)
####


####
# Response to scratches
def scratch_response(update, context):
  update.callback_query.message.edit_text(
    scratch_responses[randint(0,len(scratch_responses)-1)].replace("username",update.callback_query.from_user.username)
    )

def main():
  try:
    with open('scratch_date.txt', 'r') as file:
      scratch_date = file.read()
    if scratch_date == '':
      scratch_date = datetime.datetime.now() + datetime.timedelta(minutes = randint(0,59))
    else:
      scratch_date = datetime.datetime.fromisoformat(scratch_date)
  except IOError:
    scratch_date = datetime.datetime.now() + datetime.timedelta(minutes = randint(0,59))
    with open('scratch_date.txt', 'w') as file:
      file.write(scratch_date.isoformat())

  ## Add handlers
  dp.add_handler(
    MessageHandler(Filters.status_update.new_chat_members, welcome_message)
    ) # New group member handler
  dp.add_handler(
    CallbackQueryHandler(translate_welcome_to_es, pattern='welcome_es')
    ) # Translate to spanish welcome button handler
  dp.add_handler(
    CallbackQueryHandler(translate_welcome_to_en, pattern='welcome_en')
    ) # Translate to english welcome button handler
  dp.add_handler(
    CallbackQueryHandler(scratch_response, pattern='scratch')
    ) 
  ##

  scheduler.start()
  scheduler.add_job(scratch_request, trigger='date', run_date=scratch_date, id='fuchur_request', misfire_grace_time=2**30)

  # Start the updater
  updater.start_polling()
  updater.idle()


if __name__ == '__main__':
  main()
