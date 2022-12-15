import json
import logging
from logging.handlers import RotatingFileHandler
import requests

import categories
import config
import utils
import send_to_telegram
from crud import WomanProductsCrud, WomanPricesCrud, ManProductsCrud, ManPricesCrud, \
    HighlightsProductsCrud, HighlightsPricesCrud
from database import SessionLocal
from schemas import ProductSchema, PriceSchema


class MassimoDuttiParser:
    def __init__(self):
        self.db_session = SessionLocal()
        self.urls_category_id = None
        self.market = None
        self.products_crud = None
        self.prices_crud = None
        self.items_count = 0

    def start(self):
        logging.info(f"Massimo Dutti Parser Start: {self.market}")
        for url in self.make_urls():
            self.get_data_from_json_loads(url)

    def make_urls(self) -> list:
        urls = []
        for category_id, url_category in self.urls_category_id.items():
            urls.append(f"{config.URL_PRODUCT}/{category_id}/product")
        logging.info(f"{len(urls)} urls created")
        return urls

    def get_data_from_json_loads(self, url: str):
        logging.info(f"Start URL: {url}")
        session = requests.Session()
        response = session.get(url, params=config.PARAMS_PRODUCT, headers=config.HEADERS)
        json_loads = json.loads(response.text)
        if not json_loads.get('products') or len(json_loads['products']) <= 0 or not json_loads['filters']:
            return

        products = json_loads['products']
        for product in products.values():
            try:
                if not product.get('bundleProductSummaries') or len(product.get('bundleProductSummaries')) <= 0:
                    continue
                product_id = product.get('id')
                prices = json_loads['filters']['maxPriceFilter']
                price = utils.get_price(product_id, prices)
                if not price:
                    continue
                product = product['bundleProductSummaries'][0]
                if not product.get('id') \
                        or not product.get('name') \
                        or not product.get('familyName', product.get('subFamilyName')) \
                        or not product.get('detail') \
                        or not product['detail'].get('colors') \
                        or len(product['detail'].get('colors')) <= 0:
                    continue
                product_img = product['detail']['xmedia'][0]
                product_obj = {
                    'market': self.market,
                    'url': f"{config.URL}kz/{product.get('productUrl')}",
                    'store_id': product_id,
                    'category': product.get('familyName', product.get('subFamilyName')),
                    'name': product.get('name'),
                    'color': product['detail']['colors'][0]['name'],
                    'description': product['detail']['description'],
                    'image': utils.make_photo_urls(product_img)
                }
                product_obj = ProductSchema(**product_obj)
                price_obj = PriceSchema(price=price // 100)
                self.check_data_from_db(product_obj, price_obj)
            except Exception as e:
                logging.exception(f"{self.market} product: {e}")
                send_to_telegram.send_error(f"{self.market} product: {e}")
                continue

    def check_data_from_db(self, product_obj: ProductSchema, price_obj: PriceSchema):
        self.items_count += 1
        logging.info(f"Check From DB: {self.items_count}")
        product = self.products_crud.get_or_create(product_obj)
        price_obj.product_id = product.id
        last_price = self.prices_crud.get_last_price(product.id)
        if last_price:
            discount = utils.get_percentage(price_obj.price, last_price.price)
            price_obj.discount = discount
        if not last_price or price_obj.discount != '0':
            self.prices_crud.insert(price_obj)
            logging.info(f"New Price: {price_obj.price} for product: {product.id}")
            if int(price_obj.discount) <= -15:
                image_caption = utils.make_image_caption(product_obj, self.prices_crud.get_last_n_prices(product.id))
                send_tg = send_to_telegram.send_as_media_group(image_caption, product_obj)
                logging.info(f"Send to telegram status code: {send_tg}")

    def __del__(self):
        logging.info(f"Total Parsed: {self.market}, {self.items_count}")


class MassimoDuttiWomanParser(MassimoDuttiParser):
    def __init__(self):
        super().__init__()
        self.market = 'massimodutti_w'
        try:
            self.urls_category_id = categories.categories_by_market(self.market)
        except Exception as e:
            logging.exception(f"{self.market} category: {e}")
            send_to_telegram.send_error(f"{self.market} category: {e}")
        self.products_crud: WomanProductsCrud = WomanProductsCrud(session=self.db_session)
        self.prices_crud: WomanPricesCrud = WomanPricesCrud(session=self.db_session)


class MassimoDuttiManParser(MassimoDuttiParser):
    def __init__(self):
        super().__init__()
        self.market = 'massimodutti_m'
        try:
            self.urls_category_id = categories.categories_by_market(self.market)
        except Exception as e:
            logging.exception(f"{self.market} category: {e}")
            send_to_telegram.send_error(f"{self.market} category: {e}")
        self.products_crud: ManProductsCrud = ManProductsCrud(session=self.db_session)
        self.prices_crud: ManPricesCrud = ManPricesCrud(session=self.db_session)


class MassimoDuttiHighlightsParser(MassimoDuttiParser):
    def __init__(self):
        super().__init__()
        self.market = 'massimodutti_h'
        try:
            self.urls_category_id = categories.categories_by_market(self.market)
        except Exception as e:
            logging.exception(f"{self.market} category: {e}")
            send_to_telegram.send_error(f"{self.market} category: {e}")
        self.products_crud: HighlightsProductsCrud = HighlightsProductsCrud(session=self.db_session)
        self.prices_crud: HighlightsPricesCrud = HighlightsPricesCrud(session=self.db_session)


if __name__ == '__main__':
    logging.basicConfig(
        handlers=[RotatingFileHandler('massimodutti_parser.log', mode='a+', maxBytes=10485760, backupCount=2, encoding='utf-8')],
        format="%(asctime)s %(levelname)s:%(message)s",
        level=logging.INFO,
    )
    MassimoDuttiWomanParser().start()
    MassimoDuttiManParser().start()
    MassimoDuttiHighlightsParser().start()
