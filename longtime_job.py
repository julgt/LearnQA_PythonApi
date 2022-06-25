import time
import requests

# 1) создаем задачу
response = requests.get('https://playground.learnqa.ru/ajax/api/longtime_job')
resp = response.json()
print(resp)

# 2) запрос с token ДО того, как задача готова, убеждаемся в правильности поля status
response2 = requests.get('https://playground.learnqa.ru/ajax/api/longtime_job', params={"token": ""+resp['token']+""} )
print(response2.text)
resp2 = response2.json()
assert resp2['status'] == "Job is NOT ready", "Error. Статус не Job is NOT ready"

# проверяем, что при отправке токена, на который не была заведена задача, приходит ответ error
response22 = requests.get('https://playground.learnqa.ru/ajax/api/longtime_job', params={"token": "dhdfjdjFbhjj"} )
print(response22.text)
resp22 = response22.json()
assert resp22['error'] == "No job linked to this token", "Error. Статус не No job linked to this token"

# ждем завершения создания задачи
time.sleep(resp['seconds'])

# запрос c token ПОСЛЕ того, как задача готова, убеждаемся в правильности поля status и наличии поля result
response3 = requests.get('https://playground.learnqa.ru/ajax/api/longtime_job', params=resp )
print(response3.text)
resp3 = response3.json()
assert resp3['status'] == "Job is ready", "Error. Статус не Job is ready"
assert 'result' in resp3, "Error. В ответе нет ключа result"
