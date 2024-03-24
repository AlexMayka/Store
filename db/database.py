# Модуль для работы с базой данных
# Содержит функцию для подключения к базе данных и функции для получения товаров по заказам
# Способ 1 (более читабельным и удобным для работы, также при смене СУБД не требует переработок SQL-запросов)

from pandas import DataFrame
from sqlalchemy.orm import Session

from config.config import Config
from loggingApp.loggingApp import logger
from db.models import Product, ProductOrder, ShelfProduct, Shelf
from sqlalchemy import create_engine, Engine


def connect_db(config: Config) -> Engine:
    """
    Функция для подключения к базе данных
    :param config: Объект конфигурации
    :return: Объект соединения с базой данных
    :raises ValueError: Если возникает ошибка при подключении к базе данных
    """
    try:
        logger.info("Попытка подключения к базе данных")
        engine = create_engine(
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


def get_product_order_by_id(session: Session, id_orders: list) -> list:
    """
    Функция для получения товаров в заказах по ID заказов
    :param session: Объект сессии SQLAlchemy
    :param id_orders: Кортеж ID заказов
    :return: Список кортежей, содержащих product_id, quantity и order_id
    """
    result = session.query(ProductOrder.product_id, ProductOrder.quantity, ProductOrder.order_id) \
        .filter(ProductOrder.order_id.in_(id_orders)).all()
    return result


def get_products_by_id(session: Session, id_products: list) -> list:
    """
    Функция для получения товаров по ID товаров
    :param session: Объект сессии SQLAlchemy
    :param id_products: Кортеж ID товаров
    :return: Список кортежей, содержащих id и name товаров
    """
    result = session.query(Product.id, Product.name).filter(Product.id.in_(id_products)).all()
    return result


def get_shelves_product_by_id(session: Session, id_products: list) -> list:
    """
    Функция для получения полок для товаров по ID товаров
    :param session: Объект сессии SQLAlchemy
    :param id_products: Кортеж ID товаров
    :return: Список кортежей, содержащих product_id, shelf_id и is_main
    """
    result = session.query(ShelfProduct.product_id, ShelfProduct.shelf_id, ShelfProduct.is_main) \
        .filter(ShelfProduct.product_id.in_(id_products)).all()
    return result


def get_shelves_by_id(session: Session, id_shelf: list) -> list:
    """
    Функция для получения полок по ID полок
    :param session: Объект сессии SQLAlchemy
    :param id_shelf: Кортеж ID полок
    :return: Список кортежей, содержащих id и name полок
    """
    result = session.query(Shelf.id, Shelf.name).filter(Shelf.id.in_(id_shelf)).all()
    return result


def get_product_by_orders(orders: list, config: Config) -> list:
    """
    Функция для получения товаров по списку заказов
    :param orders: Список заказов
    :param config: Объект конфигурации
    :return: Список кортежей, содержащих информацию о товарах
    """

    engine = connect_db(config)
    with Session(engine) as session:
        product_orders = get_product_order_by_id(session, orders)
        products = get_products_by_id(session, [order[0] for order in product_orders])
        product_shelves = get_shelves_product_by_id(session, [order[0] for order in product_orders])
        shelves = get_shelves_by_id(session, [shelf[1] for shelf in product_shelves])

    df_product_orders = DataFrame(data=product_orders, columns=["product_id", "quantity", "order_id"])
    df_products = DataFrame(data=products, columns=["product_id", "product_name"])
    df_product_shelves = DataFrame(data=product_shelves, columns=["product_id", "shelf_id", "os_main"])
    df_shelves = DataFrame(data=shelves, columns=["shelf_id", "shelf_name"])
    del product_orders, products, product_shelves, shelves

    logger.info("Успешное выполнение запросов к базе данных")

    df_product_by_orders = df_product_orders.merge(df_products, left_on='product_id', right_on='product_id', how='inner')
    df_product_by_orders = df_product_by_orders.merge(df_product_shelves, left_on='product_id', right_on='product_id', how='inner')
    df_product_by_orders = df_product_by_orders.merge(df_shelves, left_on='shelf_id', right_on='shelf_id', how='inner')
    df_product_by_orders = df_product_by_orders.drop('shelf_id', axis=1)
    del df_product_orders, df_products, df_product_shelves, df_shelves

    result = df_product_by_orders.values.tolist()

    logger.info("Успешное получение данных")
    return result
