import requests
from lxml import html

def get_psw_from_wiki():
    list = []
    response = requests.get("https://en.wikipedia.org/wiki/List_of_the_most_common_passwords")

    tree = html.fromstring(response.text)

    locator = '//*[contains(text(),"Top 25 most common passwords by year according to SplashData")]//..//td[@align="left"]/text()'
    passwords = tree.xpath(locator)

    for password in passwords:
        password = str(password).strip()
        if password!='':
            list.append(password)
        # print(password)
    return list