import json

import requests

dict = ['POST', 'GET', 'PUT', 'DELETE']


def print_result(response):
    print("\n")
    print(f"Тип запроса {response.request.method}, @method = {dict[i]}, ответ - {response.text}")
    try:
        if (dict[i] != response.request.method and 'success' in json.loads(response.text)):
            print("Реальный тип запроса не совпадает со значением параметра, но сервер отвечает так, словно все ок.")
    except:
        pass
    try:
        if (dict[i] == response.request.method and response.text=='Wrong method provided'):
            print("Типы совпадают, но сервер считает, что это не так")
    except:
        pass

print("-------------------")
print("1. Запросы всех типов без параметров:")
print("-------------------")

response = requests.delete("https://playground.learnqa.ru/ajax/api/compare_query_type")
print(f"Ответ для типа запроса {response.request.method} - {response.text}")
response2 = requests.put("https://playground.learnqa.ru/ajax/api/compare_query_type")
print(f"Ответ для типа запроса {response2.request.method} - {response2.text}")
response3 = requests.post("https://playground.learnqa.ru/ajax/api/compare_query_type")
print(f"Ответ для типа запроса {response3.request.method} - {response3.text}")
response4 = requests.get("https://playground.learnqa.ru/ajax/api/compare_query_type")
print(f"Ответ для типа запроса {response4.request.method} - {response4.text}")

print("-------------------")
print("2. Запрос не из списка:")
print("-------------------")
response = requests.head("https://playground.learnqa.ru/ajax/api/compare_query_type")
print(f"Ответ для типа запроса {response.request.method} без параметров - {response.text}")
for i in range(len(dict)):
    response = requests.head("https://playground.learnqa.ru/ajax/api/compare_query_type", data={"method":""+dict[i]+""})
    print(f"Ответ для типа запроса {response.request.method} и @method = '{dict[i]}' - {response.text}")

print("-------------------")
print("3/4. Перебор всех возможных сочетаний типов запросов и передаваемого значения в method:")
print("-------------------")
for i in range(len(dict)):
    if dict[i] != 'GET':
        response = requests.get("https://playground.learnqa.ru/ajax/api/compare_query_type", data={"method":""+dict[i]+""})
        print_result(response)
        response2 = requests.post("https://playground.learnqa.ru/ajax/api/compare_query_type", data={"method":""+dict[i]+""})
        print_result(response2)
        response3 = requests.put("https://playground.learnqa.ru/ajax/api/compare_query_type", data={"method":""+dict[i]+""})
        print_result(response3)
        response4 = requests.delete("https://playground.learnqa.ru/ajax/api/compare_query_type", data={"method":""+dict[i]+""})
        print_result(response4)
    else:
        response = requests.get("https://playground.learnqa.ru/ajax/api/compare_query_type", params={"method":""+dict[i]+""})
        print_result(response)
        response2 = requests.post("https://playground.learnqa.ru/ajax/api/compare_query_type", params={"method":""+dict[i]+""})
        print_result(response2)
        response3 = requests.put("https://playground.learnqa.ru/ajax/api/compare_query_type", params={"method":""+dict[i]+""})
        print_result(response3)
        response4 = requests.delete("https://playground.learnqa.ru/ajax/api/compare_query_type", params={"method":""+dict[i]+""})
        print_result(response4)