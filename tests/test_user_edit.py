import allure

from Lib.base_case import BaseCase
from Lib.assertions import Assertions
from Lib.my_requests import MyRequests

class TestUserEdit(BaseCase):

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.epic("Тестирование пользователей")
    @allure.feature("Редактирование пользователя")
    @allure.story("Редактирование авторизованного пользователя")
    @allure.description("Редактируем только что зарегистрированного и авторизованного пользователя")
    def test_edit_just_created_user(self):
        with allure.step("1. Зарегистрируем  пользователя и авторизуемся"):
            data = self.register_and_auth_new_user()

        with allure.step("2. Пробуем отредактировать firstName авторизованного пользователя"):
            new_name = "Changed name"
            response3 = MyRequests.put(f"/user/{data['user_id']}",
                                     headers={"x-csrf-token": data['token']},
                                     cookies={"auth_sid": data['auth_sid']},
                                     data= {"firstName": new_name})
            Assertions.assert_code_status(response3, 200)

        with allure.step("3. Убеждаемся, что редактирование прошло успешно."):
            response4 = MyRequests.get(f"/user/{data['user_id']}",
                                     headers={"x-csrf-token": data['token']},
                                     cookies={"auth_sid": data['auth_sid']}
                                     )
            Assertions.assert_code_status(response4, 200)
            Assertions.assert_json_value_by_name(
                response4,
                "firstName",
                new_name,
                "Wrong name of the user after edit"
            )

    @allure.epic("Тестирование пользователей")
    @allure.feature("Редактирование пользователя")
    @allure.story("Редактирование другого пользователя будучи авторизованным в сисиетме")
    @allure.description("Пытаемся изменить данные пользователя, будучи авторизованным другим пользователем (д/з)")
    def test_edit_other_user(self):
        with allure.step("1. Зарегистрируем  пользователя и авторизуемся"):
            data = self.register_and_auth_new_user()

        with allure.step("2. Пытаемся изменить инфу у другого пользователя c id=2 после своей авторизации (со своими headers и cookies)"):
            new_name = "Changed name"
            response2 = MyRequests.put(f"/user/2",
                                     headers={"x-csrf-token": data['token']},
                                     cookies={"auth_sid": data['auth_sid']},
                                     data= {"firstName": new_name}
                                       )
            Assertions.assert_code_status(response2, 200)

        with allure.step("3. Авторизуемся под тем пользователем, которого хотели отредактировать, и проверим firstName"):
            data_id_2 = self.auth_user_with_id_2()
            response4 = MyRequests.get(f"/user/{data_id_2['user_id']}",
                                       headers={"x-csrf-token": data_id_2['token']},
                                       cookies={"auth_sid": data_id_2['auth_sid']})

            Assertions.assert_code_status(response4, 200)
            Assertions.assert_json_value_by_name(
                response4,
                'firstName',
                'Vitalii',
                f"Error! Сменили данные другого пользователя. (Must be 'Vitalii', not '{new_name}')"
            )

    @allure.epic("Тестирование пользователей")
    @allure.feature("Редактирование пользователя")
    @allure.story("Редактирование без авторизации в сисиетме")
    @allure.description("Пытаемся изменить данные пользователя, будучи неавторизованным (д/з)")
    def test_edit_without_auth(self):
        new_name = "Changed name"
        response3 = MyRequests.put(f"/user/2",
                                   data={"firstName": new_name})
        assert response3.content.decode("utf-8") == "Auth token not supplied",  f"Регистрация прошла с некорректным email: {email}"
        Assertions.assert_code_status(response3, 400)


    @allure.epic("Тестирование пользователей")
    @allure.feature("Редактирование пользователя")
    @allure.story("Изменение email и firstName на некорректные, будучи авторизованным в системе")
    @allure.description("Пытаемся изменить email авторизованного пользователя на email без символа @ + FirstName на очень короткий (д/з)")
    def test_edit_incorrect_details_user(self):
        with allure.step("1. Зарегистрируем  пользователя и авторизуемся"):
            data_login = self.register_and_auth_new_user()

        with allure.step("2. Попытаемся изменить email авторизованного пользователя на некорректный"):
            new_email = "ivanovexample.com"
            response2 = MyRequests.put(f"/user/{data_login['user_id']}",
                                       headers={"x-csrf-token": data_login['token']},
                                       cookies={"auth_sid": data_login['auth_sid']},
                                       data={"email": new_email}
                                       )
            Assertions.assert_code_status(response2, 400)
            assert response2.content.decode("utf-8") == "Invalid email format",  f"Редактирование email прошло с некорректным email без символа @: {new_email}"

        with allure.step("3. Попытаемся изменить firstName авторизованного пользователя на очень короткий"):
            new_firstName = "f"
            response3 = MyRequests.put(f"/user/{data_login['user_id']}",
                                       headers={"x-csrf-token": data_login['token']},
                                       cookies={"auth_sid": data_login['auth_sid']},
                                       data={"firstName": new_firstName}
                                       )
            Assertions.assert_code_status(response3, 400)
            assert response3.content.decode(
                "utf-8") == "{\"error\":\"Too short value for field firstName\"}", f"Редактирование firstName прошло с очень коротким значением в один символ: {new_firstName}"