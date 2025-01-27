import requests
from bs4 import BeautifulSoup
import schedule
import time
import logging
import os
from pathlib import Path
import configparser
import hashlib
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from getpass import getpass  # For secure password input

Path("logs").mkdir(parents=True, exist_ok=True)
logging.basicConfig(filename="logs/scraper.log", level=logging.INFO, format="%(asctime)s - [%(levelname)s] - %(message)s")

def load_config():
    """
    Loads configuration settings from a config file and environment variables.
    This function reads the configuration settings from a file named 'config.ini' located in the 'config' directory.
    It retrieves the base URL, download path, and courses file from the 'SETTINGS' and 'COURSES' sections of the config file.
    Additionally, it attempts to get the university email and password from environment variables. If the environment variables
    are not set, it falls back to the values in the 'CREDENTIALS' section of the config file. If the email or password is still
    not available, it prompts the user to input them.
    Returns:
        tuple: A tuple containing the following configuration settings:
            - BASE_URL (str): The base URL for downloads.
            - DOWNLOAD_PATH (str): The path where downloads will be saved.
            - EMAIL (str): The university email address.
            - PASSWORD (str): The university password.
            - COURSE_FILE (str): The file containing course information.
    """
    config = configparser.ConfigParser()
    config.read("config/config.ini")


    BASE_URL = config["SETTINGS"]["base_url"]
    DOWNLOAD_PATH = config["SETTINGS"]["download_path"]
    COURSE_FILE = config["COURSES"]["courses_file"]


    EMAIL = os.getenv("UNIVERSITY_EMAIL") or config["CREDENTIALS"]["email"]
    PASSWORD = os.getenv("UNIVERSITY_PASSWORD") or config["CREDENTIALS"]["password"]

    if not EMAIL:
        EMAIL = input("Enter your university email: ")

    if not PASSWORD:
        PASSWORD = getpass("Enter your university password: ")

    return BASE_URL, DOWNLOAD_PATH, EMAIL, PASSWORD, COURSE_FILE


def load_courses(course_file):
    """
    Load a list of courses from a given file.

    Args:
        course_file (str): The path to the file containing the list of courses.

    Returns:
        list: A list of course names as strings, with leading and trailing whitespace removed.
    """
    with open(course_file, "r") as f:
        courses = [line.strip() for line in f if line.strip()]
    return courses


def create_directories(courses, download_path):
    """
    Creates a directory structure for each course in the specified download path.

    Args:
        courses (list of str): A list of course names for which directories will be created.
        download_path (str): The base path where the course directories will be created.

    The function creates the following subdirectories for each course:
        - lecture_slides
        - section_slides
        - assignments
        - labs
        - other

    If the directories already exist, they will not be recreated.
    """
    base_path = Path(download_path)
    sub_paths = ["lecture_slides", "section_slides", "assignments", "labs", "other"]
    for course in courses:
        for sub_path in sub_paths:
            path = base_path / course / sub_path
            path.mkdir(parents=True, exist_ok=True)


def get_token(session, base_url):
    """
    Retrieves a login token from the specified URL.

    Args:
        session (requests.Session): The session object used to make the HTTP request.
        base_url (str): The URL from which to retrieve the login token.

    Returns:
        str or None: The login token if found, otherwise None.
    """
    response = session.get(base_url)
    soup = BeautifulSoup(response.content, "html.parser")
    token = soup.find("input", {"name": "logintoken"})
    token = token["value"] if token else None
    return token


def login(session, login_url, email, password):
    """
    Logs into a website using the provided session, login URL, email, and password.
    Args:
        session (requests.Session): The session object to maintain the login session.
        login_url (str): The URL to send the login request to.
        email (str): The email address used for login.
        password (str): The password used for login.
    Returns:
        bool: True if login is successful, False otherwise.
    Raises:
        requests.RequestException: If there is an issue with the network request.
    """
    token = get_token(session, login_url)

    payload = {
        "username": email,
        "password": password,
        "logintoken": token,
        "rememberusername": "1"

    }

    response = session.post(login_url, data=payload)
    if response.ok and response.url == "https://lms.eng.asu.edu.eg/my/":
        logging.info("Login Successful")
        return True
    else:
        logging.error("Login Failed")
        return False


if __name__ == "__main__":
    BASE_URL, DOWNLOAD_PATH, EMAIL, PASSWORD, COURSE_FILE = load_config()
    courses = load_courses(COURSE_FILE)
    create_directories(courses, DOWNLOAD_PATH)


    session = requests.Session()


    if login(session, BASE_URL, EMAIL, PASSWORD):
        logging.info("Starting the scraper")
        # Start the scraper
    else:
        logging.error("Exiting the scraper")
        exit(1)