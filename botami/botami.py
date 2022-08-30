import Tami4EdgeAPI
import os
from pypasser import reCaptchaV3
import requests
from loguru import logger

PHONE_NUMBER = os.getenv('PHONE_NUMBER')
ENDPOINT = "https://swelcustomers.strauss-water.com"
ANCHOR_URL = "https://www.google.com/recaptcha/enterprise/anchor?ar=1&k=6Lf-jYgUAAAAAEQiRRXezC9dfIQoxofIhqBnGisq&co=aHR0cHM6Ly93d3cudGFtaTQuY28uaWw6NDQz&hl=en&v=gWN_U6xTIPevg0vuq7g1hct0&size=invisible&cb=ji0lh9higcza"
i=0

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

if __name__ == "__main__":
    phone_number = PHONE_NUMBER
    request_otp(phone_number)
    while(True):
        i=i+1

    
    
# otp = input("OTP: ")
# response = submit_otp(phone_number, otp)
# logger.info(response['refresh_token'])

