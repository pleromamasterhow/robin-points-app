import json
from datetime import date

DATA_FILE = "data.json"

def load_data():
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return {
            "total_points": 1000,
            "tasks": [
                {"name": "阅读", "points": 2},
                {"name": "书写", "points": 2},
                {"name": "早起", "points": 2},
                {"name": "早睡", "points": 2},
                {"name": "收拾", "points": 2}
            ],
            "rewards": [
                {"name": "买玩具", "points": 0, "date": str(date.today())},
                {"name": "市内旅行", "points": 100, "date": str(date.today())},
                {"name": "跨州旅行", "points": 500, "date": str(date.today())},
                {"name": "跨国旅行", "points": 1000, "date": str(date.today())}
            ],
            "history": {}
        }

def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def get_today_date():
    return str(date.today())