from ctypes.wintypes import PUSHORT
from errno import EDEADLK
from Tami4EdgeAPI import Tami4EdgeAPI
import os, requests, phonenumbers, pathlib
from os.path import exists
from warnings import catch_warnings
from pypasser import reCaptchaV3
from loguru import logger
from telebot import types, TeleBot
from telebot.custom_filters import AdvancedCustomFilter
from telebot.callback_data import CallbackData, CallbackDataFilter
from datetime import datetime

PHONE_NUMBER =""
ALLOWD_IDS = os.getenv('ALLOWED_IDS')
BOT_TOKEN = os.getenv('BOT_TOKEN')
ENDPOINT = "https://swelcustomers.strauss-water.com"
ANCHOR_URL = "https://www.google.com/recaptcha/enterprise/anchor?ar=1&k=6Lf-jYgUAAAAAEQiRRXezC9dfIQoxofIhqBnGisq&co=aHR0cHM6Ly93d3cudGFtaTQuY28uaWw6NDQz&hl=en&v=gWN_U6xTIPevg0vuq7g1hct0&size=invisible&cb=ji0lh9higcza"
edge = None
# ----------------Set token file path --------------------
TOKEN_DIRECTORY = os.getcwd()
TOKEN_DIRECTORY = TOKEN_DIRECTORY + "/tokens"
TOKEN_FILE = TOKEN_DIRECTORY + "/token.txt"

#Init bot
bot = TeleBot(BOT_TOKEN)

# ---------------- Save token to file --------------------
def save_refresh_token(refresh_token):
    global TOKEN_FILE
    try:
      if exists(TOKEN_FILE):
        os.remove(exists(TOKEN_FILE))
      with open(TOKEN_FILE, 'w') as f:
        f.write(refresh_token)
    except Exception as e:
        logger.error(str(e))

# ---------------- Read token from file --------------------
def read_refresh_token():
    global TOKEN_FILE
    try:
        with open(TOKEN_FILE) as f:
            return f.read()
    except Exception as e:
        logger.error(str(e))
        return ""

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
            init_edge_device(message)
        else:
            msg = bot.send_message(message.chat.id, "Please enter valid otp (xxxx):", reply_markup=types.ForceReply(selective=False))
            bot.register_next_step_handler(msg, get_token)
        
    except Exception as e:
        logger.error(str(e))
        bot.send_message(message.chat.id, "Error generating token, see error in log file")

# -------------- Set command list -------------------------------------
commands = [{"text": " חידוש / יצירת טוקן", "callback_data": "config"},
            {"text": "רשימת משקאות", "callback_data": "drinks_list"},
            {"text": "סטטיסטיקה ותחזוקה", "callback_data": "statistics"},
            {"text": "הרתחה", "callback_data": "boil"},
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
    init_edge_device(message)
    # if(not exists(TOKEN_FILE)):
    #     bot.send_message(message.chat.id, text="Token file does not exixts, pleas generate new token")
    # else:
    #     if not read_refresh_token():
    #         bot.send_message(message.chat.id, text="Token file is empty, pleas generate new token")

    msg=bot.send_message(message.chat.id, text="welcome", reply_markup=command_keyboard(), parse_mode='Markdown')
    print(msg.id)
# ---------------- Handle the config button --------------------
@bot.callback_query_handler(func=lambda c: c.data == 'config')
def config_callback(call: types.CallbackQuery):
   msg = bot.send_message(call.message.chat.id, "Please enter your phone number with country code (+972xxxxxxxxx):", reply_markup=types.ForceReply(selective=False))
   bot.register_next_step_handler(msg, phonenumber_validation) 


# ---------------- Handle the boil command --------------------
@bot.callback_query_handler(func=lambda c: c.data == 'boil')
def boil_callback(call: types.CallbackQuery):
    global edge
    init_edge_device(call.message)
    logger.info("Boiling water")
    edge.boil_water()

@bot.callback_query_handler(func=lambda c: c.data == 'drinks_list')
def drinks_list_callback(call: types.CallbackQuery):
    global edge
    init_edge_device(call.message)
    logger.info("Getting drinks list")
    # edge.boil_water()
    drinks = edge.get_drinks()
    for drink in drinks:
        print(drink)


@bot.callback_query_handler(func=lambda c: c.data == 'statistics')
def boil_callback(call: types.CallbackQuery):
    global edge
    init_edge_device(call.message)
    logger.info("Getting statistics")
    # edge.boil_water()
    statistics = edge.get_water_quality()
    stats = f"""
    *Usage Statistics:* \n
    *Filter*:
            Last Replacemnt: {statistics.filter.last_replacement.strftime("%d/%m/%Y")}
            Next Replacement: {statistics.filter.upcoming_replacement.strftime("%d/%m/%Y")}
            Status: {statistics.filter.status}
            Liters Passed: {int(statistics.filter.milli_litters_passed)/1000}

*UV*:
            Last Replacemnt: {statistics.uv.last_replacement.strftime("%d/%m/%Y")}
            Next Replacement: {statistics.uv.upcoming_replacement.strftime("%d/%m/%Y")}
            Status: {statistics.uv.status}            
    """
    msg = bot.send_message(call.message.chat.id, text=stats,parse_mode='Markdown')
    print(msg.id)
# 
def init_edge_device(message):
    global edge
    try:
        token = read_refresh_token()
        if token:
            if  edge is None:
                edge = Tami4EdgeAPI(token)
                # bot.send_message(message.chat.id, text=f"Bar Name: {edge.device.name}, Firmware Version: {edge.device.device_firmware}")
        else:
            pass
            # bot.send_message(message.chat.id, text="Token file does not exixts or the file is empty, pleas generate new token")
    except Exception as e:
        # bot.send_message(message.chat.id, text="Error occurred when initializing edge device, see details in log file")
        logger.error(str(e))

if __name__ == "__main__":
    if not os.path.exists(TOKEN_DIRECTORY):
        os.makedirs(TOKEN_DIRECTORY)
    bot.infinity_polling()
    