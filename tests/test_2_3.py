import pytest
import logging
import io
from module_2 import LoggingMeta, HttpClient


def setup_logger():
    log_stream = io.StringIO()
    handler = logging.StreamHandler(log_stream)
    logger = logging.getLogger()
    logger.handlers = []
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)
    return log_stream, logger


def test_instance_creation_logs():
    log_stream, _ = setup_logger()
    obj = HttpClient()
    logs = log_stream.getvalue()
    assert "Создание экземпляра класса: HttpClient" in logs


def test_methods_not_logged():
    log_stream, _ = setup_logger()
    obj = HttpClient()
    _ = str(obj)
    logs = log_stream.getvalue()
    assert "Вызов метода: __str__" not in logs
    assert "Вызов метода: __init__" not in logs


def test_method_call_logged_and_counted():
    log_stream, _ = setup_logger()
    obj = HttpClient()
    obj.request_handler()
    logs = log_stream.getvalue()
    assert "Вызов метода: request_handler объекта HttpClient" in logs
    assert any(
        "Время выполнения метода request_handler:" in line for line in logs.splitlines()
    )
    assert any("Использование памяти: до" in line for line in logs.splitlines())
    assert obj.__call_stats__["request_handler"] == 1


def test_multiple_method_calls():
    log_stream, _ = setup_logger()
    obj = HttpClient()
    for _ in range(3):
        obj.request_handler()
    logs = log_stream.getvalue()
    assert logs.count("Вызов метода: request_handler объекта HttpClient") == 3
    assert obj.__call_stats__["request_handler"] == 3


def test_get_statistics():
    log_stream, _ = setup_logger()
    obj = HttpClient()
    obj.request_handler()
    HttpClient.get_statistics(obj)
    logs = log_stream.getvalue()
    assert "Статистика вызовов методов:" in logs
    assert "request_handler - 1 раз(а)" in logs
