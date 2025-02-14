"""
Handles authentication with the university website using provided credentials.
"""

from typing import Any
from dotenv import load_dotenv
import os
import configparser
from bs4 import BeautifulSoup as bs, NavigableString, Tag
import requests
import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path


from configManager import ConfigManager
from appLogger import AppLogger

load_dotenv()


class LoginSession:
    """
    Handles authentication with the university website using provided credentials.
    """

    def __init__(self, session: requests.Session) -> None:
        """
        Initialize login handler with credentials and configuration.

        Args:
            session: Requests session object to persist cookies
        """
        # Validate credentials before initialization
        self.__username: str | None = os.getenv("UNIVERSITY_USERNAME")
        self.__password: str | None = os.getenv("UNIVERSITY_PASSWORD")
        if not self.__username or not self.__password:
            raise ValueError("Missing credentials in environment variables")

        self.__session: requests.Session = session
        self.__logger: logging.Logger = AppLogger(__name__)
        self.__config: ConfigManager = ConfigManager()
        self.__login_url: str = self.__config.get_config_value("URLS", "university_url")
        self.__success_url: str = self.__config.get_config_value("URLS", "university_next_url")



    def __get_token(self) -> str:
        """Extract CSRF token from login page

        Returns:
            str: CSRF token value
        """
        try:
            response: requests.Response = self.__session.get(self.__login_url)
            response.raise_for_status()  # Check HTTP errors
            soup = bs(response.content, "html.parser")
            token: Tag | NavigableString | None = soup.find("input", {"name": "logintoken"})

            if not token or "value" not in token.attrs:
                raise ValueError("CSRF token not found in login page")

            return token["value"]
        except requests.RequestException as e:
            self.__logger.error(f"Token retrieval failed: {str(e)}")
            raise e

    def login(self) -> bool:
        """Execute login sequence with credentials and CSRF token

        Raises:
            requests.RequestException: If network error occurs during login
        Returns:
            bool: True if login successful, False otherwise
        """
        try:
            self.__logger.info("Initiating login process")
            token: str = self.__get_token()
            payload: dict[str, Any] = {
                "username": self.__username,
                "password": self.__password,
                "logintoken": token,
                "rememberusername": 1,
            }

            response = self.__session.post(
                self.__login_url,
                data=payload,
            )

            # Check for successful authentication patterns
            if response.status_code == 200 and response.url == self.__success_url:
                self.__logger.info("Login and redirected successful")
                return True

            self.__logger.error(f"Login failed. Status: {response.status_code}")
            return False

        except requests.RequestException as e:
            self.__logger.error(f"Network error during login: {str(e)}")
            raise e
        except Exception as e:
            self.__logger.error(f"Unexpected login error: {str(e)}", exc_info=False)
            raise e
