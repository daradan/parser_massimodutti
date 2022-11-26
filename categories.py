import requests
import json
import config


categories_ids = {}


def process_category(category_obj):
    for subcategory in category_obj['subcategories']:
        process_category(subcategory)
    else:
        category_id = category_obj.get('id')
        category_name = formatting_category_name(category_obj['name'])
        categories_ids[category_id] = category_name


def categories_by_market(market):
    global categories_ids
    categories_ids = {}
    session = requests.session()
    response = session.get(config.URL_CATEGORY, headers=config.HEADERS, params=config.PARAMS_CATALOG)
    json_loads = json.loads(response.text)
    sections = json_loads['categories']
    for section in sections:  # woman, man, studio
        section_name = section.get('nameEn', section['name'])
        if market == 'massimodutti_w' and section_name == 'WOMEN':
            process_category(section)
        if market == 'massimodutti_m' and section_name == 'MEN':
            process_category(section)
        if market == 'massimodutti_h' and section_name == 'HIGHLIGHTS':
            process_category(section)
    return categories_ids


def formatting_category_name(name: str):
    name = name.lower()
    if '\xa0' in name:
        name = name.replace('\xa0', ' ')
    if ' | ' in name:
        return ' '.join(name.split(' | '))
    if ' ' in name:
        return name.replace(' ', '_')
    if '-' in name:
        return name.replace('-', '_')
    return name


if __name__ == '__main__':
    res = categories_by_market('massimodutti_m')
    print(res)
