import os
from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())

URL = 'https://www.massimodutti.com/'
URL_CATEGORY = f'{URL}itxrest/2/catalog/store/35009503/30359534/category'
URL_PRODUCT = f'{URL}itxrest/3/catalog/store/35009503/30359534/category'
URL_PHOTO = 'https://static.massimodutti.net/3/photos'

LAST_N_PRICES = 10
TG_TOKEN = os.getenv('TG_TOKEN')
TG_CHANNEL = os.getenv('TG_CHANNEL')
TG_CHANNEL_ERROR = os.getenv('TG_CHANNEL_ERROR')

PARAMS_CATALOG = {
    'languageId': '-20',
    'typeCatalog': '1',
    'appId': '1',
}

PARAMS_PRODUCT = {
    'languageId': '-20',
    'appId': '1',
    'showProducts': 'true',
}

HEADERS = {
    'authority': 'www.massimodutti.com',
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'en-US,en;q=0.9',
    'referer': 'https://www.massimodutti.com/',
    'sec-ch-ua': '"Opera";v="93", "Not/A)Brand";v="8", "Chromium";v="107"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Linux"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) '
                  'AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/107.0.0.0 Safari/537.36 '
                  'OPR/93.0.0.0',
}
