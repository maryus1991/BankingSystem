import random
import string

def generate_otp(length=6) -> str:
    return ''.join(random.choice(string.digits, k=length))
