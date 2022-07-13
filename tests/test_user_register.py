from datetime import datetime

import pytest

from Lib.base_case import BaseCase
from Lib.assertions import Assertions
from Lib.my_requests import MyRequests

class TestUserRegister(BaseCase):

    random_part = datetime.now().strftime("%m%d%Y%H%M%S")
    email = f"learnqa{random_part}@example.com"
    short_username = 'u'
    long_username = 'qwertyuasdfghjklw3e4r5t6y71w2w3e4r5t5tre3w2q1sdfghqwertyuasdfghjklw3e4r5t6y71w2w3e4r5t5tre3w2q1sdfghqwertyuasdfghjklw3e4r5t6y71w2w3e4r5t5tre3w2q1sdfghqwertyuasdfghjklw3e4r5t6y71w2w3e4r5t5tre3w2q1sdfghqwertyuasdfghjklw3e4r5t6y71w2w3e4r5t5tre3w2q1sdfghqwertyuasdfghjklw3e4r5t6y71w2w3e4r5t5tre3w2q1sdfgh'

    parameters = [  # password, username, firstName, lastName , email
        (None,'learnqa','learnqa','learnqa', email),
        ('123', None, 'learnqa', 'learnqa', email),
        ('123', 'learnqa', None, 'learnqa', email),
        ('123', 'learnqa', 'learnqa', None, email),
        # ('123', 'learnqa', 'learnqa', 'learnqa', None), # 'этот вариант в test_user_create_user_successfully
        ('123', 'learnqa', 'learnqa', 'learnqa', ''),
    ]

    parameters2 = [  # version, username, email
        (1, short_username, email),
        (2, long_username, email),
    ]


    def test_user_create_user_successfully(self):
        data = self.prepare_registration_data()

        response = MyRequests.post("/user", data=data)
        Assertions.assert_code_status(response,200)
        Assertions.assert_json_has_key(response, "id")


    def test_create_user_with_existing_email(self):
        email = 'vinkotov@example.com'
        data = self.prepare_registration_data(None,None,None,None,email)

        response = MyRequests.post("/user", data=data)
        Assertions.assert_code_status(response,400)
        assert response.content.decode("utf-8") == f"Users with email '{email}' already exists", f"Unexpected response content {response.content}"

    def test_create_user_with_incorrect_email(self):
        email = 'ivanovexample.com'
        data = self.prepare_registration_data(None,None,None,None,email)
        response = MyRequests.post("/user", data=data)
        Assertions.assert_code_status(response,400)
        assert response.content.decode("utf-8") == "Invalid email format",  f"Регистрация прошла с некорректным email: {email}"

    @pytest.mark.parametrize('password, username, firstName, lastName , email', parameters)
    def test_create_user_without_one_field(self, password, username, firstName, lastName , email):
        data = self.prepare_registration_data(email)
        response = MyRequests.post("/user", data=data)
        # print('\n----------------------------\n')
        # print(f"{password} {username} {firstName} {lastName} {email}")
        # print(response.content)
        Assertions.assert_code_status(response,400)
        assert response.content.decode("utf-8") == "The following required params are missed: username, firstName, lastName",  f"Регистрация прошла с некорректными данными: {password}-{username}-{firstName}-{lastName}-{email}"

    @pytest.mark.parametrize('version, username, email', parameters2)
    def test_create_user_with_short_or_long_username(self,version, username, email):
        data = {
            'password': '123',
            'username': username,
            'firstName': 'learnqa',
            'lastName': 'learnqa',
            'email': email
        }
        response = MyRequests.post("/user", data=data)
        Assertions.assert_code_status(response,400)
        if version == 1:
            assert response.content.decode("utf-8") == "The value of 'username' field is too short",  f"Регистрация прошла с nameuser в один символ "
        else:
            assert response.content.decode(
                "utf-8") == "The value of 'username' field is too long", f"Регистрация прошла со слишком длинным nameuser"