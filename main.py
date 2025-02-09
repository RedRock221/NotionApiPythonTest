import json, requests
import re
from config import headers, DATABASE_ID, NOTION_TOKEN
from datetime import datetime, timezone

url1 = 'https://api.notion.com/v1/pages'

def get_pages():
    url = f"https://api.notion.com/v1/databases/{DATABASE_ID}/query"

    payload = {"page_size": 100}
    response = requests.post(url, json=payload, headers=headers)

    data = response.json()

    import json
    with open('db.json', 'w', encoding='utf8') as f:
     json.dump(data, f, ensure_ascii=False, indent=4)

    results = data["results"]
    return results


def get_page_id_from_json():
    try:
        with open('db.json', 'r', encoding='utf8') as f:
            data = json.load(f)
            if data and "results" in data and len(data["results"]) > 0:
                # Берем page_id из первой страницы в результатах
                page_id = data["results"][0]["id"]
                return page_id
            else: 
                print("Файл db.json пуст или не содержит результатов.") 
                return None
    except FileNotFoundError:
        print("Файл db.json не найден.")
        return None


def create_page(data: dict):
    create_url = "https://api.notion.com/v1/pages"

    payload = {"parent": {"database_id": DATABASE_ID}, "properties": data}

    res = requests.post(create_url, headers=headers, json=payload)
    if res.status_code == 200:
        print("Готово")
    else:
        print("Ошибка запроса")

    return res


def update_page(page_id, field_name, new_value):
    """Обновляет только одно поле в записи"""
    url = f"https://api.notion.com/v1/pages/{page_id}"

    # Определяем формат данных в зависимости от типа поля
    field_types = {
        "Title": {"rich_text": [{"text": {"content": new_value}}]},
        "URL": {"title": [{"text": {"content": new_value}}]},
        "Text1": {"rich_text": [{"text": {"content": new_value}}]},
        "Published": {"date": {"start": new_value}}
    }
    
    payload = {"properties": {field_name: field_types[field_name]}}
    
    response = requests.patch(url, json=payload, headers=headers)
    return response

n = 1
print("Данные из файла:")
pages = get_pages()
for page in pages:
    page_id = page["id"]
    props = page["properties"]
    url = props["URL"]["title"][0]["text"]["content"]
    title = props["Title"]["rich_text"][0]["text"]["content"]
    published = props["Published"]["date"]["start"]
    text = props["Text1"]["rich_text"][0]["text"]["content"]

    published = datetime.fromisoformat(published)
    print(n, url, title, published, text)
    n = n + 1


pages = get_pages()
if not pages:
    print("Нет записей для редактирования.")
    exit()


page_id = get_page_id_from_json()

def get_page_id_from_json():
    try:
        with open('db.json', 'r', encoding='utf8') as f:
            data = json.load(f)
            if data and "results" in data and len(data["results"]) > 0:
                # Возвращаем id каждой страницы для выбора
                return [page["id"] for page in data["results"]]
            else:
                print("Файл db.json пуст или не содержит результатов.")
                return []
    except FileNotFoundError:
        print("Файл db.json не найден.")
        return []


def is_valid_page_id(page_id):
    # Стандартный формат UUID
    return re.match(r'^[0-9a-fA-F-]{36}$', page_id) is not None


def delete_page(page_id: str):
    """Архивирует (удаляет) страницу в Notion, устанавливая параметр archived в True."""
    url = f"https://api.notion.com/v1/pages/{page_id}"
    payload = {"archived": True}
    
    print(f"Архивирование страницы с ID: {page_id}")
    print(f"URL: {url}")
    
    res = requests.patch(url, headers=headers, json=payload)
    
    if res.status_code == 200:
        print("Запись успешно архивирована!")
    else:
        print(f"Ошибка архивирования: {res.status_code} - {res.text}")

def archive_page(page_id: str):
    url = f"https://api.notion.com/v1/pages/{page_id}"
    payload = {"archived": True}
    
    print(f"Архивирование страницы с ID: {page_id}")
    print(f"URL: {url}")
    
    res = requests.patch(url, headers=headers, json=payload)
    
    if res.status_code == 200:
        print("Запись успешно архивирована!")
    else:
        print(f"Ошибка архивирования: {res.status_code} - {res.text}")




# Получаем все страницы
pages = get_pages()

if not pages:
    print("Нет записей для редактирования.")
    exit()




page_id = get_page_id_from_json()
print("\n Выберите вариант:")
print("1. Добавить данные")
print("2. Изменить данные")
print("3. Удалить данные")


var = input("Выберите вариант: ")
if var == "1":
    url = input("Выберите поле 1: ")
    title = input("Выберите поле 2: ")
    text1 = input("Выберите поле 3: ")
    published_date = datetime.now().astimezone(timezone.utc).isoformat()
    data = {
        "URL": {"title": [{"text": {"content": url}}]},
        "Title": {"rich_text": [{"text": {"content": title}}]},
        "Published": {"date": {"start": published_date, "end": None}},
        "Text1": {"rich_text": [{"text": {"content": text1}}]}
    }
    create_page(data)
elif var == "2":
    while True:
        try:
            choice = int(input("\nВведите номер записи для редактирования: "))
            if 1 <= choice <= len(pages):
                selected_page = pages[choice - 1]
                break
            else:
                print("Неверный номер, попробуйте снова.")
        except ValueError:
            print("Введите число!")

    # Получаем данные выбранной записи
    page_id = selected_page["id"]
    props = selected_page["properties"]

    # Показываем данные записи
    fields = {
        "1": "Title",
        "2": "URL",
        "3": "Text1",
        "4": "Published"
    }

    print("\nВыберите поле для изменения:")
    print(f"1. Заголовок: {props.get('Title', {}).get('rich_text', [{}])[0].get('text', {}).get('content', 'Нет данных')}")
    print(f"2. URL: {props.get('URL', {}).get('title', [{}])[0].get('text', {}).get('content', 'Нет данных')}")
    print(f"3. Текст: {props.get('Text1', {}).get('rich_text', [{}])[0].get('text', {}).get('content', 'Нет данных')}")
    print(f"4. Дата публикации: {props.get('Published', {}).get('date', {}).get('start', 'Нет данных')}")

    # Пользователь выбирает ячейку
    while True:
        field_choice = input("\nВведите номер поля для изменения: ")
        if field_choice in fields:
            field_name = fields[field_choice]
            break
        else:
            print("Неверный номер, попробуйте снова.")

    # Ввод нового значения
    new_value = input(f"Введите новое значение для {field_name}: ")

    # Отправляем обновление
    update_page(page_id, field_name, new_value)
    print("\nЯчейка обновлена!")
elif var == "3":
    try:
        choice = int(input("\nВведите номер записи для удаления: ")) - 1
        if 0 <= choice < len(pages):
            page_id = pages[choice]["id"]
            confirm = input(f"Вы уверены, что хотите удалить '{pages[choice]['properties']['Title']['rich_text'][0]['text']['content']}'? (y/n): ")
            if confirm.lower() == "y":
                print(f"Удаляемая запись: {page_id}")
                print(f"Запрос будет отправлен на: https://api.notion.com/v1/pages/{page_id}")
                delete_page(page_id)
            else:
                print("Удаление отменено.")
        else:
            print("Некорректный номер.")
    except ValueError:
        print("Введите число.")
else:
    print("Некорректный ввод. Попробуйте ещё раз.")