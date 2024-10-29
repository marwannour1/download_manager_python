import requests
from bs4 import BeautifulSoup

session = requests.Session()

login_url = "https://lms.eng.asu.edu.eg/login/index.php"
login_page_response = session.get(login_url)

soup = BeautifulSoup(login_page_response.text, "html.parser")
token_input = soup.find("input", {"name": "logintoken"})

if token_input:
    token = token_input["value"]
    print("Token:", token)
    print("-------------------------------------------------------\n\n")


login_payload = {
    "username": "21P0165@eng.asu.edu.eg",
    "password": "budget@rg023",
    "logintoken": token,
    "rememberusername": "1"
}

login_response = session.post(login_url, data=login_payload)

print(login_response.text)

print("-------------------------------------------------------\n\n\n")

print("Login Status Code:", login_response.status_code)

if login_response.ok and login_response.url == "https://lms.eng.asu.edu.eg/my/":
    print("Login successful")
    print("Login URL:", login_response.url)
else:
    print("Login failed")
    print("Login URL:", login_response.url)
