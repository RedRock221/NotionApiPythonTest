# main.py
from notion_api.notion_client import get_pages, create_page, update_page, delete_page
from notion_api.utils import get_page_id_from_json, is_valid_page_id
from datetime import datetime, timezone

def main():
    pages = get_pages()
    if not pages:
        print("Нет записей для редактирования.")
        return

    for i, page in enumerate(pages, start=1):
        page_id = page["id"]
        props = page["properties"]
        url = props["URL"]["title"][0]["text"]["content"]
        title = props["Title"]["rich_text"][0]["text"]["content"]
        published = props["Published"]["date"]["start"]
        text = props["Text1"]["rich_text"][0]["text"]["content"]

        published = datetime.fromisoformat(published)
        print(f"{i}. {url} | {title} | {published} | {text}")

    print("\nВыберите вариант:")
    print("1. Добавить данные")
    print("2. Изменить данные")
    print("3. Удалить данные")

    choice = input("Введите номер варианта: ")
    if choice == "1":
        url = input("Введите URL: ")
        title = input("Введите заголовок: ")
        text1 = input("Введите текст: ")
        published_date = datetime.now().astimezone(timezone.utc).isoformat()
        data = {
            "URL": {"title": [{"text": {"content": url}}]},
            "Title": {"rich_text": [{"text": {"content": title}}]},
            "Published": {"date": {"start": published_date}},
            "Text1": {"rich_text": [{"text": {"content": text1}}]}
        }
        create_page(data)
    elif choice == "2":
        page_number = int(input("Введите номер записи для редактирования: ")) - 1
        if 0 <= page_number < len(pages):
            page_id = pages[page_number]["id"]
            field = input("Введите название поля для изменения (Title, URL, Text1, Published): ")
            new_value = input("Введите новое значение: ")
            update_page(page_id, field, new_value)
        else:
            print("Некорректный номер записи.")
    elif choice == "3":
        page_number = int(input("Введите номер записи для удаления: ")) - 1
        if 0 <= page_number < len(pages):
            page_id = pages[page_number]["id"]
            confirm = input("Вы уверены, что хотите удалить эту запись? (y/n): ")
            if confirm.lower() == 'y':
                delete_page(page_id)
            else:
                print("Удаление отменено.")
        else:
            print("Некорректный номер записи.")
    else:
        print("Некорректный выбор.")

if __name__ == "__main__":
    main()
