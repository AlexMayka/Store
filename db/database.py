# Модуль для работы с базой данных
# Содержит функцию для подключения к базе данных и функции для получения товаров по заказам

import sqlalchemy
import pandas as pd
from config.config import Config
from loggingApp.loggingApp import logger


def connect_db(config: Config) -> sqlalchemy.Engine:
    """
    Функция для подключения к базе данных
    :param config: Объект конфигурации
    :return: Объект соединения с базой данных
    :raises ValueError: Если возникает ошибка при подключении к базе данных
    """
    try:
        logger.info("Попытка подключения к базе данных")
        engine = sqlalchemy.create_engine(
            f'postgresql://{config.db.name}:'
            f'{config.db.password}@'
            f'{config.db.host}:'
            f'{config.db.port}/'
            f'{config.db.database}'
        )
        return engine

    except Exception as ex:
        logger.error(f"Ошибка подключения к базе данных: {ex}")
        raise ValueError("Ошибка подключения к базе данных")


def get_product_order_by_id(connection: sqlalchemy.Connection, id_orders: tuple) -> list:
    """
    Функция для получения товаров в заказах по ID заказов
    :param connection: Объект соединения с базой данных
    :param id_orders: Кортеж ID заказов
    :return: Список кортежей, содержащих product_id, quantity и order_id
    """
    query = sqlalchemy.text("""
                SELECT po.product_id, po.quantity, po.order_id
                FROM product_orders po
                WHERE po.order_id IN :id_orders
                """)
    result = connection.execute(query, {"id_orders": id_orders}).fetchall()
    return result


def get_products_by_id(connection: sqlalchemy.Connection, id_products: tuple) -> list:
    """
    Функция для получения товаров по ID товаров
    :param connection: Объект соединения с базой данных
    :param id_products: Кортеж ID товаров
    :return: Список кортежей, содержащих id и name товаров
    """
    query = sqlalchemy.text("""
                SELECT id, name
                FROM products
                WHERE id IN :id_products
            """)
    result = connection.execute(query, {"id_products": id_products}).fetchall()
    return result


def get_shelves_product_by_id(connection: sqlalchemy.Connection, id_products: tuple) -> list:
    """
    Функция для получения полок для товаров по ID товаров
    :param connection: Объект соединения с базой данных
    :param id_products: Кортеж ID товаров
    :return: Список кортежей, содержащих product_id, shelf_id и is_main
    """
    query = sqlalchemy.text("""
            SELECT product_id, shelf_id, is_main
            FROM shelves_product
            WHERE product_id IN :id_products
            """)
    result = connection.execute(query, {"id_products": id_products}).fetchall()
    return result


def get_shelves_by_id(connection: sqlalchemy.Connection, id_shelf: tuple) -> list:
    """
    Функция для получения полок по ID полок
    :param connection: Объект соединения с базой данных
    :param id_shelf: Кортеж ID полок
    :return: Список кортежей, содержащих id и name полок
    """
    query = sqlalchemy.text("""
            SELECT id, name
            FROM shelves
            WHERE id IN :id_shelf
            """)
    result = connection.execute(query, {"id_shelf": id_shelf}).fetchall()
    return result


def get_product_by_orders(orders: list, config: Config) -> list:
    """
    Функция для получения товаров по списку заказов
    :param orders: Список заказов
    :param config: Объект конфигурации
    :return: Список кортежей, содержащих информацию о товарах
    """
    engine = connect_db(config)
    with engine.connect() as connection:
        df_product_orders = pd.DataFrame(
            data=get_product_order_by_id(connection, tuple(orders)),
            columns=["product_id", "quantity", "order_id"]
        )

        df_products = pd.DataFrame(
            data=get_products_by_id(connection, tuple(df_product_orders["product_id"])),
            columns=["product_id", "product_name"]
        )

        df_product_shelves = pd.DataFrame(
            data=get_shelves_product_by_id(connection, tuple(df_product_orders["product_id"])),
            columns=["product_id", "shelf_id", "os_main"]
        )

        df_shelves = pd.DataFrame(
            data=get_shelves_by_id(connection, tuple(df_product_shelves["shelf_id"])),
            columns=["shelf_id", "shelf_name"]
        )

        logger.info("Успешное выполнение запросов к базе данных")

    df_product_by_orders = df_product_orders
    df_product_by_orders = df_product_by_orders.merge(df_products, left_on='product_id', right_on='product_id',how='inner')
    df_product_by_orders = df_product_by_orders.merge(df_product_shelves, left_on='product_id', right_on='product_id',how='inner')
    df_product_by_orders = df_product_by_orders.merge(df_shelves, left_on='shelf_id', right_on='shelf_id', how='inner')
    df_product_by_orders = df_product_by_orders.drop('shelf_id', axis=1)

    result = df_product_by_orders.values.tolist()

    logger.info("Успешное получение данных")
    return result
