import requests
from bs4 import BeautifulSoup

if __name__ == "__main__":
    # url = "https://example.com"
    # response = requests.get(url)
    # if response.status_code == 200:
    #     print(f"Your request to {url} came back successful")
    #     print(f"Content: {response.text}")
    # else:
    #     print(f"Your request to {url} came back with status code {response.status_code}")

    html_text = """
<html>
    <body>
        <div class="course">
            <a href="lecture1.pdf" class="lecture">Lecture 1</a>
            <a href="lecture2.pdf" class="lecture">Lecture 2</a>
            <a href="tutorial1.pdf" class="tutorial">Tutorial 1</a>
        </div>
    </body>
</html>
"""
    soup = BeautifulSoup(html_text, "html.parser")

    print(soup.prettify())
    lectures = soup.find_all("a", {"class": "lecture"})
    for lecture in lectures:
        print(type(lecture))
        print(f"lecture: {lecture}")
        link = lecture.get("href")
        print(f"link: {link}")
