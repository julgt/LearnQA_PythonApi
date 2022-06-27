import requests

response = requests.post('https://playground.learnqa.ru/api/long_redirect', allow_redirects=True)
count_url = len(response.history)
print(f"Число редиректов: {count_url}")

for i in range(count_url):
    print(response.history[i].url)
    if i == count_url-1:
        print(f"Итоговый URL: {response.history[i].url}")
