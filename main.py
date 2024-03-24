# Точка входа в программу
# Считывает аргументы командной строки, читает конфигурацию, получает товары по заказам и выводит их на консоль

from sys import argv
from config.config import read_config
from db.database import get_product_by_orders
from console.console import output_product
from loggingApp.loggingApp import logger


def main():
    logger.info("Начало работы программы")
    orders = argv[1:]

    if orders:
        try:
            config = read_config(r"config/config.json")
            products = get_product_by_orders(orders, config)
            if products:
                output_product(orders, products)
            else:
                print("Не найдено")
        except Exception as e:
            logger.error(f"Ошибка при выполнении программы: {e}")
    else:
        print("Не получено входных данных")


if __name__ == "__main__":
    main()
