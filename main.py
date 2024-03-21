# Точка входа в программу
# Считывает аргументы командной строки, читает конфигурацию, получает товары по заказам и выводит их на консоль

from sys import argv
from config.config import readConfig
from db.database import getProductByOrders
from console.console import outputProduct
from loggingApp.loggingApp import logger

if __name__ == "__main__":
    logger.info("Start work")
    orders = argv[1:]

    if len(orders):
        config = readConfig(r"config/config.json")
        products = getProductByOrders(orders, config)
        outputProduct(orders, products) if len(products) else print("Не найдено")