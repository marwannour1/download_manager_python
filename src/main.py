from login import LoginSession
import requests


def main():

    session = requests.Session()
    login = LoginSession(session)
    print(login.login())


if __name__ == "__main__":
    main()
