import configparser
from appLogger import AppLogger
from pathlib import Path


class ConfigManager:
    def __init__(self) -> None:
        self.__config: configparser.ConfigParser = self.__load_config()
        self.__logger: AppLogger = AppLogger(__name__)



    def __load_config(self) -> configparser.ConfigParser:
        config_path: Path = Path(__file__).parent.parent / "config/config.ini"
        config = configparser.ConfigParser()
        if not config_path.exists():
            self.__logger.error("Config file not found")
            raise FileNotFoundError("Config file not found")

        config.read(config_path)
        return config

    def get_config_value(self, section: str, key: str | None = None) -> str | dict:
        try:
            if key == None:
                return self.__config[section]
            else:
                return self.__config[section][key]
        except KeyError as e:
            self.__logger.error(f"Missing config entry: [{section}] {key}")
            raise e



