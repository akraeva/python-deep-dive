# Stepick.org — Углублённый Python
# 2. Метапрограммирование

import logging
import tracemalloc
import time
import functools
import types
import io


# 2.2 Дескрипторы


class UsernameValidator:

    def __get__(self, obj, objtype=None):
        return obj.__dict__.get("username")

    def __set__(self, obj, value):
        if not isinstance(value, str):
            raise ValueError("Username must be a string")
        if not (3 <= len(value) <= 20):
            raise ValueError("Username must be between 3 and 20 characters")
        if not value[0].isalpha():
            raise ValueError("Username must start with a letter")
        if not all(ch.isalnum() or ch == "_" for ch in value):
            raise ValueError(
                "Username can contain only letters, digits, and underscores"
            )
        obj.__dict__["username"] = value


class PasswordValidator:
    def __get__(self, obj, objtype=None):
        return obj.__dict__.get("password")

    def __set__(self, obj, value):
        if not isinstance(value, str):
            raise ValueError("Password must be a string")
        if len(value) < 8:
            raise ValueError("Password must be at least 8 characters long")
        if not any(ch.isupper() for ch in value):
            raise ValueError("Password must contain at least one uppercase letter")
        if not any(ch.islower() for ch in value):
            raise ValueError("Password must contain at least one lowercase letter")
        if not any(ch.isdigit() for ch in value):
            raise ValueError("Password must contain at least one digit")
        obj.__dict__["password"] = value


class User:
    username = UsernameValidator()
    password = PasswordValidator()

    def __init__(self, username, password):
        self.username = username
        self.password = password


# 2.3 Метаклассы


logging.basicConfig(
    level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger(__name__)

tracemalloc.start()


class LoggingMeta(type):
    def __new__(cls, name, bases, class_dict):
        new_class = super().__new__(cls, name, bases, class_dict)

        for attr_name, attr_value in class_dict.items():
            if callable(attr_value) and not attr_name.startswith("__"):
                setattr(new_class, attr_name, cls._wrap_method(attr_name, attr_value))
        return new_class

    def __call__(cls, *args, **kwargs):
        logger.info(f"Создание экземпляра класса: {cls.__name__}")
        obj = super().__call__(*args, **kwargs)
        obj.__call_stats__ = {}
        return obj

    @staticmethod
    def _wrap_method(name, func):
        @functools.wraps(func)
        def wrapper(self, *args, **kwargs):
            logger.info(f"Вызов метода: {name} объекта {self.__class__.__name__}")

            start_time = time.perf_counter()
            mem_before, _ = tracemalloc.get_traced_memory()

            result = func(self, *args, **kwargs)

            mem_after, _ = tracemalloc.get_traced_memory()
            elapsed = (time.perf_counter() - start_time) * 1000

            logger.info(f"Время выполнения метода {name}: {elapsed:.2f} мс")
            logger.info(
                f"Использование памяти: до = {mem_before} байт, после = {mem_after} байт, "
                f"разница = {mem_after - mem_before:+} байт"
            )
            stats = getattr(self, "__call_stats__", {})
            stats[name] = stats.get(name, 0) + 1
            self.__call_stats__ = stats

            return result

        return wrapper

    @staticmethod
    def get_statistics(obj):
        logger.info("Статистика вызовов методов:")
        for method, count in obj.__call_stats__.items():
            logger.info(f"{method} - {count} раз(а)")


class HttpClient(metaclass=LoggingMeta):
    def __init__(self):
        pass

    def __str__(self):
        return "HttpClient"

    def request_handler(self):
        return "OK, Status code: 200"


# 2.4 Синглтон


class SingletonMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]


class DBSettings(metaclass=SingletonMeta):
    def __init__(self, host, port, user, password, database):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.database = database

    def get_connection(self):
        return f"{self.user}:{self.password}@{self.host}:{self.port}/{self.database}"
