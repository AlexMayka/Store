# Модуль для работы с базой данных
# Содержит функцию для подключения к базе данных и функцию для получения товаров по заказам

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
        query = """
            SELECT p.id, p.name, po.quantity, o.id AS order_id, s.name AS shelf_name, sp.is_main
            FROM product_orders po
            JOIN products p 
            ON po.product_id = p.id
            JOIN orders o  
            ON po.order_id = o.id
            JOIN shelves_product sp ON p.id = sp.product_id 
	        JOIN shelves s ON sp.shelf_id = s.id
	        WHERE o.id IN %s
	    """

        logger.info("Executing a request")
        cur.execute(query, (tuple(orders),))
        products = cur.fetchall()
        cur.close()
        conn.close()
        logger.info("Luck request")
        return products

    except Exception as Ex:
        logger.error(f"Not luck request {Ex}")
        cur.close()
        conn.close()
