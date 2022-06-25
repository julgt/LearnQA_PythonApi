import json

json_text = '{"messages":[{"message":"This is the first message","timestamp":"2021-06-04 16:40:53"},{"message":"And this is a second message","timestamp":"2021-06-04 16:41:01"}]}'
js = json.loads(json_text)
# second_message = js['messages'][1]['message'] # или сразу так, или как ниже с проверками

second_message = ''
length = len(js['messages'])
if length >=2:
    try:
        if 'message' in dict(js['messages']):
            second_message = js['messages'][1]['message']
            print(f"Текст второго сообщения: '{second_message}'")
    except:
        print("Ошибка при парсинге Json")
else:
    print("в списке сообщений нет второго")