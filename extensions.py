import requests
import json

from config import keys

class APIException(Exception):
    pass

class Converter:
    @staticmethod
    def get_price(base, quote, amount):

        try:
            base_key = keys[base.lower()]
        except KeyError:
            raise APIException(f"Валюта {base} не найдена!")

        try:
            quote_key = keys[quote.lower()]
        except KeyError:
            raise APIException(f"Валюта {quote} не найдена!")

        if base_key == quote_key:
            raise APIException(f'Невозможно перевести одинаковые валюты {base}!')

        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f'Не верно указано количество {amount}!')

        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={keys[base]}&tsyms={keys[quote]}')
        total = json.loads(r.content)[keys[quote]] * float(amount)
        return total
