import requests
from Lib.base_case import BaseCase

class TestHomeWorkCookie(BaseCase):
    def test_homework_cookie(self):
        response = requests.get("https://playground.learnqa.ru/api/homework_cookie")
        cookies = dict(response.cookies)
        print(cookies)#  {'HomeWork': 'hw_value'}
        cookie_value = self.get_cookie(response, "HomeWork")
        assert cookie_value == 'hw_value', f"У ключа 'HomeWork' значение не равно 'hw_value'"

        # cookie_name = list(cookies)
        # print(cookie_name)
        # for i in range(len(cookie_name)):
        #     cookie_value = self.get_cookie(response, cookie_name[i])
        #     print(f"for key {cookie_name} value: {cookie_value}")

