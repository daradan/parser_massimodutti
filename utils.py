import config


def make_photo_urls(photos: dict) -> str:
    photos_list = []
    path = photos['path']
    for photo in photos['xmediaItems'][0]['medias']:
        timestamp = photo['timestamp']
        id_media = photo['idMedia']
        photo_str = f"{config.URL_PHOTO}/{path}/{id_media}16.jpg?t={timestamp}"
        photos_list.append(photo_str)
    return ','.join(photos_list)


def get_price(product_id: int, prices: list) -> int | bool:
    for price in prices:
        for price_id in price.get('productIds'):
            if product_id == price_id:
                return int(price.get('price'))
    return False


def get_percentage(price, price_old):
    percent = round(-1 * (100 - (price * 100 / price_old)))
    if percent > 0:
        percent = f'+{percent}'
    return str(percent)


def make_image_caption(product_obj, last_n_prices):
    image_caption = f"<b>{product_obj.name}</b>\n" \
                    f"<b>{product_obj.color}</b>\n" \
                    f"{fix_category(product_obj.category)}\n\n" \
                    f"{fix_last_n_prices(last_n_prices)}\n" \
                    f"<a href='{product_obj.url}{make_utm_tags()}'>Купить на оф.сайте</a>\n\n" \
                    f"{config.TG_CHANNEL}"
    if product_obj.description != '':
        image_caption = image_caption.replace('\n\n', f'\n\n{product_obj.description}\n\n', 1)
    if product_obj.market == 'zara_b':
        image_caption = image_caption.replace('#', f'#beauty #', 1)
    return image_caption


def fix_category(category):
    need_to_replace = [' ', '-', ',', '/']
    category_list = []
    if ' И ' in category:
        category_list += category.split(' И ')
    else:
        for change in need_to_replace:
            if change in category:
                category_list.append(category.replace(change, '_'))
    return f"#{' #'.join(category_list)}"


def fix_last_n_prices(last_n_prices):
    last_n_prices_text = ''
    for data_price in last_n_prices:
        if data_price.discount:
            dscnt = f' ({data_price.discount}%)'
        else:
            dscnt = ''
        last_n_prices_text += f'{data_price.created.year}/{data_price.created.month}/{data_price.created.day}' \
                              f' - {data_price.price} ₸{dscnt}\n'
    return last_n_prices_text


def make_utm_tags() -> str:
    utm_campaign = config.TG_CHANNEL[1:]
    return f"?utm_source=telegram&utm_medium=messenger&utm_campaign={utm_campaign}&utm_term={config.TG_CHANNEL_NAME}"
