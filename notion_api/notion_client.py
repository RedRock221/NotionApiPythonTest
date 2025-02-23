import requests
import json
from .config import headers, DATABASE_ID
from datetime import datetime, timezone


def get_pages():
    url = f"https://api.notion.com/v1/databases/{DATABASE_ID}/query"
    response = requests.post(url, headers=headers)
    data = response.json()
    return data.get("results", [])  # <- возвращает записи

def create_page(data: dict):
    create_url = "https://api.notion.com/v1/pages"
    payload = {"parent": {"database_id": DATABASE_ID}, "properties": data}
    res = requests.post(create_url, headers=headers, json=payload)
    return res

def update_page(page_id, field_name, new_value):
    url = f"https://api.notion.com/v1/pages/{page_id}"
    field_types = {
        "Title": {"rich_text": [{"text": {"content": new_value}}]},
        "URL": {"title": [{"text": {"content": new_value}}]},
        "Text1": {"rich_text": [{"text": {"content": new_value}}]},
        "Published": {"date": {"start": new_value}}
    }
    payload = {"properties": {field_name: field_types[field_name]}}
    response = requests.patch(url, json=payload, headers=headers)
    return response

def delete_page(page_id: str):
    url = f"https://api.notion.com/v1/pages/{page_id}"
    payload = {"archived": True}
    res = requests.patch(url, headers=headers, json=payload)
    return res
