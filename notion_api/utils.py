import json
import re

def get_page_id_from_json(file_path='db.json'):
    try:
        with open(file_path, 'r', encoding='utf8') as f:
            data = json.load(f)
            if data and "results" in data and len(data["results"]) > 0:
                return [page["id"] for page in data["results"]]
            else:
                print("Файл пуст или не содержит результатов.")
                return []
    except FileNotFoundError:
        print("Файл не найден.")
        return []

def is_valid_page_id(page_id):
    return re.match(r'^[0-9a-fA-F-]{36}$', page_id) is not None
