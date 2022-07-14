import allure

from Lib.base_case import BaseCase
from Lib.assertions import Assertions
from Lib.my_requests import MyRequests

class TestUserDelete(BaseCase):
    @allure.description("Тест на попытку удалить пользователя по ID 2. ")
    def test_user_id2_delete(self):
        # AUTH пользователем с id = 2
        data_login_user2 = self.auth_user_with_id_2()

        #DELETE
        response2 = MyRequests.delete(f"/user/{data_login_user2['user_id']}",headers={"x-csrf-token": data_login_user2['token']},
                                 cookies={"auth_sid": data_login_user2['auth_sid']})
        assert response2.content.decode('utf-8')=='Please, do not delete test users with ID 1, 2, 3, 4 or 5.', "Что-то пошло не так."

    @allure.description("Тест на попытку  Создать пользователя, авторизоваться из-под него, удалить, затем попробовать получить его данные по ID и убедиться, что пользователь действительно удален.")
    def test_delete_same_user(self):
        data_login = self.register_and_auth_new_user()
        user_id_from_auth = data_login['user_id']

        # DELETE
        response2 = MyRequests.delete(f"/user/{user_id_from_auth}", headers={"x-csrf-token": data_login['token']},
                                   cookies={"auth_sid": data_login['auth_sid']})
        Assertions.assert_code_status(response2, 200)

        #GET
        response3 = MyRequests.get(f"/user/{user_id_from_auth}",
                                   headers={"x-csrf-token": data_login['token']},
                                   cookies={"auth_sid": data_login['auth_sid']}
                                   )
        # или просто
        # response3 = MyRequests.get(f"/user/{user_id_from_auth}")
        assert response3.content.decode('utf-8') == 'User not found', "Пользователь не был удален."

    @allure.description("Тест негативный, попробовать удалить пользователя, будучи авторизованными другим пользователем.")
    def test_delete_other_user(self):
        # заведем и авторизуемся 1м пользователем
        data_login_user1 = self.register_and_auth_new_user()
        user_id_for_user1 = data_login_user1['user_id']

        #AUTH пользователем с id = 2
        data_login_user2 = self.auth_user_with_id_2()


        # DELETE
        response2 = MyRequests.delete(f"/user/{user_id_for_user1}", headers={"x-csrf-token": data_login_user2['token']},
                                   cookies={"auth_sid": data_login_user2['auth_sid']})
        Assertions.assert_code_status(response2, 400)
        assert response2.content.decode('utf-8') == 'Please, do not delete test users with ID 1, 2, 3, 4 or 5.', "Что-то пошло не так."


