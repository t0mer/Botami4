import Tami4EdgeAPI
import os, requests, phonenumbers, pathlib
from os.path import exists
from warnings import catch_warnings
from pypasser import reCaptchaV3
from loguru import logger
from telebot import types, TeleBot
from telebot.custom_filters import AdvancedCustomFilter
from telebot.callback_data import CallbackData, CallbackDataFilter

PHONE_NUMBER =""
CHAT_ID = os.getenv('CHAT_ID')
BOT_TOKEN = os.getenv('BOT_TOKEN')
ENDPOINT = "https://swelcustomers.strauss-water.com"
ANCHOR_URL = "https://www.google.com/recaptcha/enterprise/anchor?ar=1&k=6Lf-jYgUAAAAAEQiRRXezC9dfIQoxofIhqBnGisq&co=aHR0cHM6Ly93d3cudGFtaTQuY28uaWw6NDQz&hl=en&v=gWN_U6xTIPevg0vuq7g1hct0&size=invisible&cb=ji0lh9higcza"
TOKEN_DIRECTORY = os.getcwd()
TOKEN_DIRECTORY = TOKEN_DIRECTORY + "/tokens"
TOKEN_FILE = TOKEN_DIRECTORY + "/token.txt"
#Init bot
bot = TeleBot(BOT_TOKEN)

# ---------------- Save token to file --------------------
def save_refresh_token(refresh_token):
    global TOKEN_FILE
    try:
      with open(TOKEN_FILE, 'w') as f:
        f.write(refresh_token)
    except Exception as e:
        logger.error(str(e))

# ---------------- Read token from file --------------------
def read_refresh_token():
    global TOKEN_FILE
    with open(TOKEN_FILE) as f:
      return f.read()

# ---------------- Bypass the recaptcha --------------------
def recaptcha_token():
    return reCaptchaV3(ANCHOR_URL)

# ---------------- Request OTP --------------------
def request_otp(phone_number):
    requests.post(
        f"{ENDPOINT}/public/phone/generateOTP",
        json={
            "phoneNumber": phone_number,
            "reCaptchaToken": recaptcha_token(),
        },
    )

# ---------------- Submit OTP --------------------
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

# ---------------- Handle the phone number validation --------------------
def phonenumber_validation(message):
    global PHONE_NUMBER
    if(is_valid_phone_number(message.text)):
        request_otp(message.text)
        PHONE_NUMBER = message.text
        msg = bot.send_message(message.chat.id, "Please enter your 6 digits otp (xxxxx):", reply_markup=types.ForceReply(selective=False))
        bot.register_next_step_handler(msg, get_token)
    else:
        msg = bot.send_message(message.chat.id, "Invalid Phone number, please enter valid one (+972xxxxxxxxx):", reply_markup=types.ForceReply(selective=False))
        bot.register_next_step_handler(msg, phonenumber_validation) 

# ---------------- Handle the token generation --------------------
def get_token(message):
    try:
        logger.info("Getting Token")
        if message.text.isnumeric() and len(message.text)>3:
            response = submit_otp(PHONE_NUMBER, message.text)
            save_refresh_token(response['refresh_token'])
            bot.send_message(message.chat.id, "refresh token was successfully generated")
        else:
            msg = bot.send_message(message.chat.id, "Please enter valid otp (xxxx):", reply_markup=types.ForceReply(selective=False))
            bot.register_next_step_handler(msg, get_token)

    except Exception as e:
        logger.error(str(e))
        bot.send_message(message.chat.id, "Error generating token, see error in log file")



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

# ---------------- Validate phone number --------------------
def is_valid_phone_number(my_number):
    if(my_number.startswith('+')):
        my_number = phonenumbers.parse(my_number)
        return phonenumbers.is_possible_number(my_number)
    else:
        return False

# ---------------- Handle the start menu --------------------
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    global TOKEN_FILE
    if(not exists(TOKEN_FILE)):
        bot.send_message(message.chat.id, text="Token file does not exixts, pleas generate new token")
    else
        if not read_refresh_token():
            bot.send_message(message.chat.id, text="Token file is empty, pleas generate new token")

    bot.send_message(message.chat.id, text="welcome", reply_markup=command_keyboard(), parse_mode='Markdown')

# ---------------- Handle the config button --------------------
@bot.callback_query_handler(func=lambda c: c.data == 'config')
def back_callback(call: types.CallbackQuery):
   msg = bot.send_message(call.message.chat.id, "Please enter your phone number with country code (+972xxxxxxxxx):", reply_markup=types.ForceReply(selective=False))
   bot.register_next_step_handler(msg, phonenumber_validation) 



if __name__ == "__main__":
    if not os.path.exists(TOKEN_DIRECTORY):
        os.makedirs(TOKEN_DIRECTORY)
    bot.infinity_polling()
    