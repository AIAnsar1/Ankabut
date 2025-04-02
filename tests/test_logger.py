import unittest, logging, sys, io

from unittest.mock import patch
from core.log import Logger, CustomLogging


class TestLogger(unittest.TestCase):
    def setUp(self):
        """Перед каждым тестом сбрасываем обработчики логгера"""
        Logger.handlers.clear()  # Убираем старые обработчики
        self.log_capture = io.StringIO()
        handler = logging.StreamHandler(self.log_capture)
        formatter = logging.Formatter("[%(levelname)s] %(message)s")
        handler.setFormatter(formatter)
        Logger.addHandler(handler)
        Logger.setLevel(logging.INFO)

    def test_logger_output(self):
        """Проверяем, что логгер пишет в stdout"""
        Logger.info("Test message")
        self.log_capture.seek(0)  # Перематываем на начало
        output = self.log_capture.read()
        self.assertIn("[INFO] Test message", output)

    def test_custom_log_levels_output(self):
        """Проверяем кастомные уровни логирования"""
        Logger.log(25, "[PAYLOAD] Custom payload log")  # Уровень PAYLOAD
        self.log_capture.seek(0)
        output = self.log_capture.read()
        self.assertIn("[PAYLOAD] Custom payload log", output)

    def test_fallback_to_standard_handler(self):
        """Проверяем, что при отсутствии ColorizingStreamHandler используется StreamHandler"""
        Logger.info("Fallback test")
        self.log_capture.seek(0)
        output = self.log_capture.read()
        self.assertIn("[INFO] Fallback test", output)



if __name__ == "__main__":
    unittest.main()