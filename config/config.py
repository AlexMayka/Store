# Модуль для работы с конфигурацией
# Содержит функцию для чтения конфигурации из файла JSON

# Можно дописывать классы с дополнительными настройками проекта, к примеру сторонние API, настройка хоста и тп

import json
from dataclasses import dataclass
from loggingApp.loggingApp import logger


@dataclass
class DB:
    """
    Класс для управления настройками подключения к базе данных.
    """
    host: str  # Хост базы данных.
    name: str  # Имя пользователя базы данных
    password: str  # Пароль пользователя базы данных
    database: str  # Имя базы данных
    port: str  # Порт базы данных

    def __init__(self, jsonSetDB: dict):
        """
        Инициализация экземпляра класса DB
        :param jsonSetDB: Словарь с настройками подключения к базе данных
        """
        self.database = jsonSetDB["database"]
        self.name = jsonSetDB["user"]
        self.password = jsonSetDB["password"]
        self.host = jsonSetDB["host"]
        self.port = jsonSetDB["port"]


@dataclass
class Config:
    """
    Класс для хранения конфигурации
    """
    db: DB  # Экземпляр класса DB с настройками подключения к базе данных.

    def __init__(self, path_config_json: str):
        """
        Инициализация экземпляра класса Config
        :param path_config_json: Путь к файлу конфигурации
        """
        with open(path_config_json, "r") as f:
            self.config = json.load(f)

        self.db = DB(self.config["DB"])


def read_config(path_config_json: str) -> Config:
    """
    Функция для чтения конфигурации из файла JSON
    :param path_config_json: Путь к файлу конфигурации
    :return: Экземпляр класса Config
    """
    try:
        config_def = Config(path_config_json)
        logger.info("Успешное чтение конфигурации")
        return config_def
    except Exception as ex:
        logger.error(f"Ошибка при чтении конфигурации: {ex}")


config = read_config(r"config/config.json")

if __name__ == "__main__":
    config_test = Config("config.json")
    print(config_test.db.host)
