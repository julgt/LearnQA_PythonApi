import requests
from Lib.base_case import BaseCase

class TestHomeWorkHeader(BaseCase):
    def test_homework_header(self):
        response = requests.get("https://playground.learnqa.ru/api/homework_header")
        headers = dict(response.headers)
        print(headers)  # {'HomeWork': 'hw_value'}
        headers_name = list(headers)
        print(headers_name)
        headers_values = [*headers.values()]
        print(headers_values)

        for i in range(len(headers_name)):
            headers_val = self.get_header(response, headers_name[i])
            assert headers_values[i] == headers_val, f"У ключа '{headers_name[i]}' значение не равно '{headers_values[i]}'"
            print(f"for key '{headers_name[i]}' value: '{headers_values[i]}'")