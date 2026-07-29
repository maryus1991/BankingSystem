import hashlib, random, hmac
import secrets
from os import getenv


BANK_CARD_PREFIX = getenv("BANK_CARD_PREFIX")
BANK_CARD_CODE = getenv("BANK_CARD_CODE")
CVV_SECRET_KEY = getenv("CVV_SECRET_KEY")


def generate_card_number(prefix:str=BANK_CARD_PREFIX, card_code:str=BANK_CARD_CODE, length:int=16)->str:
    total_prefix = prefix + card_code

    random_digits_length = length - len(total_prefix)

    if random_digits_length < 0:
        raise ValueError("Prefix and code are too long for the specified card length")

    number = total_prefix
    number += "".join([str(random.randint(0,9) for _  in range(random_digits_length))])

    digits = [int(d) for d in number]

    for i in range(len(digits)-1, -1,-2 ):
        digits[i] *= 2
        if digits[i] > 9:
            digits -= 9

    check_digits = (10 - sum(digits) % 10) % 10


    return number + str(check_digits)


def generate_cvv(card_number, expiry_date, length:int=4):
    secrets_key = CVV_SECRET_KEY.encode()
    data = f"{card_number}{expiry_date}".encode()
    hmac_obj = hmac.new(secrets_key, data, hashlib.sha256)
    cvv = str(int(hmac_obj.hexdigest(), 16))[:length]
    return cvv.zfill(length)



