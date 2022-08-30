# import Tami4EdgeAPI
import os
# from pypasser import reCaptchaV3
import requests
import phonenumbers
from loguru import logger
from telebot import types, TeleBot
from telebot.custom_filters import AdvancedCustomFilter
from telebot.callback_data import CallbackData, CallbackDataFilter

PHONE_NUMBER = os.getenv('PHONE_NUMBER')
CHAT_ID = os.getenv('CHAT_ID')
BOT_TOKEN = os.getenv('BOT_TOKEN')
ENDPOINT = "https://swelcustomers.strauss-water.com"
ANCHOR_URL = "https://www.google.com/recaptcha/enterprise/anchor?ar=1&k=6Lf-jYgUAAAAAEQiRRXezC9dfIQoxofIhqBnGisq&co=aHR0cHM6Ly93d3cudGFtaTQuY28uaWw6NDQz&hl=en&v=gWN_U6xTIPevg0vuq7g1hct0&size=invisible&cb=ji0lh9higcza"

#Init bot
bot = TeleBot(BOT_TOKEN)



def recaptcha_token():
    return reCaptchaV3(ANCHOR_URL)

def request_otp(phone_number):
    requests.post(
        f"{ENDPOINT}/public/phone/generateOTP",
        json={
            "phoneNumber": phone_number,
            "reCaptchaToken": recaptcha_token(),
        },
    )

def submit_otp(phone_number, otp):
    response = requests.post(
        f"{ENDPOINT}/public/phone/submitOTP",
        json={
            "phoneNumber": phone_number,
            "code": otp,
            "reCaptchaToken": recaptcha_token(),
        },
    ).json()
    return response


# -------------- Set command list -------------------------------------
commands = [{"text": " חידוש / יצירת טוקן", "callback_data": "config"},
            {"text": "רשימת משקאות", "callback_data": "drinks_list"},
            {"text": "סטטיסטיקת שימוש", "callback_data": "statistics"},
            {"text": "הרתחה", "callback_data": "boiling"},
            {"text": "תחזוקה", "callback_data": "status"}, 
            {"text": "ביטול", "callback_data": "exit"},  ]

# ------------- Build command keyboard -----------------
def command_keyboard():
    return types.InlineKeyboardMarkup(
        keyboard=[
            [
                types.InlineKeyboardButton(
                    text=command['text'],
                    callback_data=command["callback_data"]
                )
            ]
            for command in commands
        ], row_width=1
    )

def is_valid_phone_number(my_number):
    if(my_number.startswith('+')):
        my_number = phonenumbers.parse(my_number)
        return phonenumbers.is_possible_number(my_number)
    else:
        return False


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
	  bot.send_message(CHAT_ID, text="welcome", reply_markup=command_keyboard(), parse_mode='Markdown')



# ---------------- Handle the configf button --------------------
@bot.callback_query_handler(func=lambda c: c.data == 'config')
def back_callback(call: types.CallbackQuery):
   bot.send_message(CHAT_ID, "Please enter your phone number with country code (+972xxxxxxxxx):", reply_markup=types.ForceReply(selective=False),callback_data="phone_validation")
    


@bot.callback_query_handler(func=lambda c: c.data == 'phone_validation')
def back_callback(call: types.CallbackQuery):
   bot.send_message(CHAT_ID, "Please enter your phone number with country code (+972xxxxxxxxx):", reply_markup=types.ForceReply(selective=False),callback_data="phone_validation")
    


@bot.message_handler(func=lambda message: True)
def echo_all(message):
    if(is_valid_phone_number(message.text)):
        bot.reply_to(message, message.text)
    else:
        bot.send_message(CHAT_ID, "Invalid Phone number, please enter valid one (+972xxxxxxxxx):", reply_markup=types.ForceReply(selective=False))



# @bot.message_handler(commands=['setalarm'])
# def setalarmcmd(message):
#     alarmMessage = "Let's start with setting up alarm.\n\n" \
#                    "First of all, provide the pair you want to observe."
#     msg = bot.send_message(message.chat.id, alarmMessage)
#     bot.register_next_step_handler(msg, setalarmcryptopair)


def setalarmcryptopair(pair):
    print(pair.text)



if __name__ == "__main__":
    bot.infinity_polling()
    

    # phone_number = PHONE_NUMBER
    # request_otp(phone_number)
    # while(True):
    #     i=i+1

    
    
# otp = input("OTP: ")
# response = submit_otp(phone_number, otp)
# logger.info(response['refresh_token'])

