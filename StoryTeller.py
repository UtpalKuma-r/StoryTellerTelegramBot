import telebot  #pip install pyTelegramBotAPI
from telebot import types
import logging
import random

logging.basicConfig(filename='storyTellerLog.log', level=logging.INFO, format='[%(asctime)s] %(levelname)s:%(message)s/n', datefmt='%m/%d/%Y %I:%M:%S %p')


#reading API key from important.txt file
file = open("important.txt", 'r')
API = file.readline()
file.close()


import json
f = open("stories.json")
data = json.load(f)
f.close()

bot = telebot.TeleBot(API)

user_dict = {}

@bot.message_handler(commands=['start'])
def bigin_conversation(message):
    markup = types.ReplyKeyboardMarkup(row_width=2)
    itembtn1 = types.KeyboardButton(r"yes! let's goo")
    markup.add(itembtn1)
    reply_message = "Welcome,\nHere we have some stories waiting for you to be completed. If you would like to go through them you can bigin now."
    bot.send_message(message.chat.id, reply_message, reply_markup=markup)
    user_dict[message.chat.id] = {"status":"talking"}
    # bot.reply_to(message.chat.id, "message logged")

@bot.message_handler(func=lambda message: True)
def masterFunc(message):

    if message.chat.id in user_dict.keys():

        reply = message.text


        if user_dict[message.chat.id]["status"] == "playing":

            if reply in data["topics"]:

                user_dict[message.chat.id]["selected_topic"] = reply

                selected_story = random.choice(list(data[reply].keys()))

                user_dict[message.chat.id]["selected_story"] = selected_story

                index_required = len(user_dict[message.chat.id]["inputs"])

                required_input = data[reply][selected_story]["data_required"][index_required]

                input_options = random.sample(data["words"][required_input], 5)

                markup = types.ReplyKeyboardMarkup(row_width=3)
                for option in input_options:
                    itembtn = types.KeyboardButton(option)
                    markup.add(itembtn)

                reply_message = "Your selected topic is: {}\nLets write some stories. Provide me with a {}".format(reply, required_input)

                bot.send_message(message.chat.id, reply_message, reply_markup=markup)

            
            elif "selected_topic" not in user_dict[message.chat.id]:
                bot.reply_to(message, "Sorry, I am littel dumb. Did not understood it. Try /start.")

            else:

                user_dict[message.chat.id]["inputs"].append(reply)

                index_required = len(user_dict[message.chat.id]["inputs"])
                required_input_category = data[user_dict[message.chat.id]["selected_topic"]][user_dict[message.chat.id]["selected_story"]]["data_required"]

                if index_required != len(required_input_category):

                    required_input = required_input_category[index_required]

                    input_options = random.sample(data["words"][required_input], 5)

                    markup = types.ReplyKeyboardMarkup(row_width=3)
                    for option in input_options:
                        itembtn = types.KeyboardButton(option)
                        markup.add(itembtn)

                    reply_message = "Great Selection! Now could you provide me with a {}".format(required_input)

                    bot.send_message(message.chat.id, reply_message, reply_markup=markup)

                
                else:
                    story = data[user_dict[message.chat.id]["selected_topic"]][user_dict[message.chat.id]["selected_story"]]["story"]

                    story_formed = story.format(*user_dict[message.chat.id]["inputs"])

                    markup = types.ReplyKeyboardRemove(selective=False)

                    bot.send_message(message.chat.id, "Hurray! Your story is complete. Lets Check it out.")
                    bot.send_message(message.chat.id, story_formed, reply_markup=markup)

                    del user_dict[message.chat.id]
                    

        elif reply in ["yes! let's goo", "yes", "let's go"]:

            reply_message = "Please select a topic from generated keypad"
            markup = types.ReplyKeyboardMarkup(row_width=3)

            for topic in data["topics"]:
                itembtn = types.KeyboardButton(topic)
                markup.add(itembtn)
            
            bot.send_message(message.chat.id, reply_message, reply_markup=markup)
            user_dict[message.chat.id]["status"] = "playing"
            user_dict[message.chat.id]["inputs"] = []




        else:
            bot.reply_to(message, "Sorry, I am littel dumb. Did not understood it. Try /start.")


    else:
        bot.reply_to(message, "Sorry, I am littel dumb. Did not understood it. Try /start.")

bot.polling()