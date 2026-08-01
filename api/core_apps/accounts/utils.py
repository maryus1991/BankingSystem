import secrets
from functools import partial
from os import getenv
from django.db import transaction
from loguru import logger

from .emails import send_account_creation_email
from .models import BankAccount
from typing import  Union, List

def calculate_len_check_digits(number : str) -> int :
    try:
        def split_into_digit(n: Union[str, int])-> List[int]:
            return [int(digit) for digit in str(n)]

        digits = split_into_digit(number)
        odd_digits = digits[-1::-2]
        even_digits = digits[-2::-2]
        total = sum(odd_digits)

        for d in even_digits:
            doubled = d*2
            total += sum(split_into_digit(doubled))


        return (10-(total % 10)) % 10

    except Exception as E:
        print(E)
        logger.error(E)


def generate_account_number(currency: str) -> str:
    try:
        bank_code = getenv("BANK_CODE")
        branch_code = getenv("BANK_BRANCH_CODE")

        currency_codes = {
            "toman": getenv("CURRENCY_CODE_TOM"),
            "us_dollar": getenv("CURRENCY_CODE_USD"),
            "pound_sterling": getenv("CURRENCY_CODE_GBP"),
            "euro": getenv("CURRENCY_CODE_EURO"),
        }

        currency_codes = currency_codes.get(currency)

        if not currency_codes:
            raise ValueError(f"Invalid Currency : {currency}")

        prefix = f"{bank_code}{branch_code}{currency_codes}"

        remaining_digits = 16 - len(prefix) - 1
        random_digits = "".join(secrets.choice("0123456789") for _ in range(remaining_digits) )
        partial_account_number = f"{prefix}{random_digits}"

        check_digit = calculate_len_check_digits(partial_account_number)
        return f"{partial_account_number}{check_digit}"
    except Exception as E:
        print(E)
        logger.error(E)


def create_bank_account(user, currency:str, account_type:str) -> str:
    try:
        with transaction.atomic():

            while True:

                account_number = generate_account_number(currency)

                if not BankAccount.objects.filter(account_number=account_number).exists():

                    break


            is_primary = not BankAccount.objects.filter(user=user).exists()

            bank_account = BankAccount.objects.create(
                user = user,
                account_number=account_number,
                currency = currency,
                is_primary = is_primary
            )

            send_account_creation_email(user, bank_account)


        return bank_account

    except Exception as E:
        print(E)
        logger.error(E)







