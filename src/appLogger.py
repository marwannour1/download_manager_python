import logging
from logging.handlers import RotatingFileHandler
import os


class AppLogger:
    def __init__(self, name: str, log_file: str = "logs/app.log") -> None:
        self.__logger: logging.Logger= logging.getLogger(name)
        self.__logger.setLevel(logging.INFO)

        os.makedirs(os.path.dirname(log_file), exist_ok=True)

        if not self.__logger.handlers:
            handler = RotatingFileHandler(
                filename=log_file,
                maxBytes=1024 * 1024,
                backupCount=5,
                encoding="utf-8"
            )

            formatter = logging.Formatter(
                "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
            )
            handler.setFormatter(formatter)
            self.__logger.addHandler(handler)

    def info(self, message: str) -> None:
        self.__logger.info(message)

    def error(self, message: str) -> None:
        self.__logger.error(message)

    def exception(self, message: str) -> None:
        self.__logger.exception(message)
