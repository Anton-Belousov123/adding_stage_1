import json
import time
import dotenv
import requests
import os

dotenv.load_dotenv()  # Загружаем .env файл

# Подгружаем Headers для запросов
headers_test_shop = {
    'Client-Id': os.getenv('TEST_CLIENT_ID'),
    'Api-Key': os.getenv('TEST_API_KEY')
}

headers_oleg_shop = {
    'Client-Id': os.getenv('OLEG_CLIENT_ID'),
    'Api-Key': os.getenv('OLEG_API_KEY')
}

headers_kamran_shop = {
    'Client-Id': os.getenv('KAMRAN_CLIENT_ID'),
    'Api-Key': os.getenv('KAMRAN_API_KEY')
}


def test_upload_is_ok(article, name, sku) -> bool:
    """Функция предназначенная для проверки ситуации: сможет ли товар, загрузится без ошибок"""
    response = _upload_item(sku=sku, name=name, article=article, headers=headers_test_shop)
    time.sleep(90)
    status = _get_upload_status(response['result']['task_id'])
    print(status)
    return 'errors' not in status['result']['items'][0].keys()


def upload_to_main(article, name, sku, table_name):
    """Функция предназначена для загрузки товара на основной аккаунт"""
    if table_name == 'oleg':
        headers = headers_oleg_shop
    else:
        headers = headers_kamran_shop
    _upload_item(sku=sku, name=name, article=article, headers=headers)


def _upload_item(sku, name, article, headers):
    """Функция предназначена для загрузки товара на аккаунт, который передается в headers"""
    url = 'https://api-seller.ozon.ru/v1/product/import-by-sku'
    data = {
        "items": [
            {
                "sku": sku,
                "name": name,
                "offer_id": "РСВ-" + str(article) + "РСВ-" + str(article),
                "currency_code": "RUB",
                "old_price": "10000",
                "price": "10000",
                "premium_price": "10000",
                "vat": "0"
            }
        ]
    }
    response = requests.post(url, headers=headers_test_shop, data=json.dumps(data)).json()
    return response


def _get_upload_status(task_id):
    """Функция создана для получения статуса загрузки товара"""
    url = 'https://api-seller.ozon.ru/v1/product/import/info'
    data = {
        'task_id': task_id
    }
    return requests.post(url=url, headers=headers_test_shop, data=json.dumps(data)).json()
