# Точка входа в программу
# Считывает аргументы командной строки, читает конфигурацию, получает товары по заказам и выводит их на консоль

from sys import argv
from db.database import get_product_by_orders
from console.console import output_product
from loggingApp.loggingApp import logger


def main():
    logger.info("Начало работы программы")
    orders = argv[1:]

    if orders:
        try:
            products = get_product_by_orders(orders)
            if products:
                output_product(orders, products)
            else:
                print("Не найдено")
        except Exception as e:
            logger.error(f"Ошибка при выполнении программы: {e}")
            print("Ошибка выполнения программы")
    else:
        print("Не получено входных данных")


if __name__ == "__main__":
    main()
