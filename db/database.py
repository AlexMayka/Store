# Модуль для работы с базой данных
# Содержит функцию для подключения к базе данных и функцию для получения товаров по заказам
import time

import psycopg2
from config.config import Config
from loggingApp.loggingApp import logger


def _connectDb(config: Config):
    try:
        """
        Функция для подключения к базе данных
        :param config: Объект конфигурации
        :return: Объект соединения с базой данных
        """
        logger.info("Connect db")
        conn = psycopg2.connect(
            host=config.db.host,
            port=config.db.port,
            dbname=config.db.database,
            user=config.db.name,
            password=config.db.password
        )
        return conn
    except Exception as Ex:
        logger.error(f"Connect db {Ex}")
        raise ValueError("Error connect DB")


def getProductByOrders(orders: list, config: Config) -> list[tuple]:
    """
    Функция для получения товаров по списку заказов
    :param orders: Список заказов
    :param config: Объект конфигурации
    :return: Список кортежей с информацией о товарах
    """
    conn = _connectDb(config)
    cur = conn.cursor()

    try:
        # Получаем список id и количества товаров для каждого заказа
        query = """
            SELECT po.product_id, po.quantity, po.order_id
            FROM product_orders po
            WHERE order_id in %s
        """
        cur.execute(query, (tuple(orders),))
        order_products = cur.fetchall()
        # print(order_products)

        # Получаем информацию о товарах
        query = """
            SELECT id, name
            FROM products
            WHERE id IN %s
        """
        cur.execute(query, (tuple([order[0] for order in order_products]),))
        products = cur.fetchall()
        # print(products)

        # Получаем информацию о полках и главном флаге для каждого товара
        query = """
            SELECT product_id, shelf_id, is_main
            FROM shelves_product
            WHERE product_id IN %s
        """
        cur.execute(query, (tuple([order[0] for order in order_products]),))
        shelves_products = cur.fetchall()


        # Получаем имена полок
        query = """
            SELECT id, name
            FROM shelves
            WHERE id IN %s
        """
        cur.execute(query, (tuple([shelves_product[1] for shelves_product in shelves_products]), ))
        shelves = cur.fetchall()

        result = []

        order_products_dict = dict()
        for order in order_products:
            idProductOp, quantityOp, idOrderOp = order
            if idProductOp not in order_products_dict.keys():
                order_products_dict[idProductOp] = []
            order_products_dict[idProductOp].append({"quantity": quantityOp, "idOrder": idOrderOp})

        shelves_products_dict = dict()
        for product in shelves_products:
            idProductSp, idShelvesSp, isMainSp = product
            if idProductSp not in shelves_products_dict.keys():
                shelves_products_dict[idProductSp] = []
            shelves_products_dict[idProductSp].append({"idShelves": idShelvesSp, "isMain": isMainSp})

        products_dict = {p[0]: p[1] for p in products}
        shelves_dict = {s[0]: s[1] for s in shelves}

        result = []
        for product_id, product_data in order_products_dict.items():
            for data in product_data:
                quantity = data['quantity']
                order_id = data['idOrder']
                product_name = products_dict[product_id]
                shelves_data = shelves_products_dict.get(product_id, [{"idShelves": None, "isMain": False}])
                for shelf_data in shelves_data:
                    is_main = shelf_data['isMain']
                    shelf_name = shelves_dict.get(shelf_data['idShelves'], None)
                    result.append((product_id, product_name, quantity, order_id, shelf_name, is_main))


        cur.close()
        conn.close()
        logger.info("Luck request")

        return result

    except Exception as Ex:
        logger.error(f"Not luck request {Ex}")
        cur.close()
        conn.close()
