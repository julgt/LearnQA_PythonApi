import allure

from Lib.base_case import BaseCase
from Lib.assertions import Assertions
from Lib.my_requests import MyRequests

class TestUserGet(BaseCase):
    def test_user_details_not_auth(self):
        response = MyRequests.get("/user/2")
        Assertions.assert_json_has_key(response,"username")
        Assertions.assert_json_has_not_key(response,"email")
        Assertions.assert_json_has_not_key(response,"firstName")
        Assertions.assert_json_has_not_key(response,"lastName")

    def test_user_details_auth_as_same_user(self):
        data = {
            'email': 'vinkotov@example.com',
            'password': '1234'
        }

        response1 = MyRequests.post("/user/login", data=data)
        auth_sid = self.get_cookie(response1, "auth_sid")
        token = self.get_header(response1, "x-csrf-token")
        user_id_from_auth_method = self.get_json_value(response1, "user_id")

        response2 = MyRequests.get(f"/user/{user_id_from_auth_method}",
                                 headers={"x-csrf-token": token},
                                 cookies={"auth_sid": auth_sid})

        expected_fields = ["username", "email", "firstName", "lastName"]
        Assertions.assert_json_has_keys(response2, expected_fields )

    @allure.description("Запрос данных другого пользователя (д/з)")
    def test_user_details_auth_as_other_user(self):
        #зарегистрируем второго пользователя и получим его email, id после авторизации
        data = self.prepare_registration_data()
        response = MyRequests.post("/user", data=data)
        Assertions.assert_code_status(response, 200)
        Assertions.assert_json_has_key(response, "id")
        email = data['email']
        psw = data['password']

        # получим его cookie/headers после авторизации, используя данные при регистрации
        data1 = {
            'email': email,
            'password': psw
        }
        response1 = MyRequests.post("/user/login", data=data1)
        self.user_id_from_auth_method = self.get_json_value(response1, "user_id")
        auth_sid = self.get_cookie(response1, "auth_sid")
        token = self.get_header(response1, "x-csrf-token")

        # получим инфу по другому юзеру после своей авторизации (со своими headers и cookies)
        response2 = MyRequests.get(f"/user/2"
                                 ,headers={"x-csrf-token": token},
                                 cookies={"auth_sid": auth_sid}
                                   )
        # response2 = MyRequests.get(f"/user/2") # или так просто?

        Assertions.assert_json_has_key(response2, "username")
        Assertions.assert_json_has_not_key(response2, "email")
        Assertions.assert_json_has_not_key(response2, "firstName")
        Assertions.assert_json_has_not_key(response2, "lastName")