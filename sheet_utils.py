import streamlit as st
import gspread
from google.oauth2.service_account import Credentials

SHEET_NAME = "Robin Points Tracker"
TASKS_SHEET = "TasksAndRewards"
HISTORY_SHEET = "History"

scope = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

def safe_api_message(ex):
    st.error(f"Google Sheets API Error: {str(ex)}\nPlease check if your Google Sheet is shared with the service account and tables exist with correct headers.")

def get_gspread_client():
    creds = Credentials.from_service_account_info(st.secrets["gcp_service_account"], scopes=scope)
    return gspread.authorize(creds)

def get_tasks_and_rewards():
    try:
        client = get_gspread_client()
        sheet = client.open(SHEET_NAME)
        ws = sheet.worksheet(TASKS_SHEET)
        data = ws.get_all_records()
        tasks = [row for row in data if row.get("type", "").lower() == "task"]
        rewards = [row for row in data if row.get("type", "").lower() == "reward"]
        return tasks, rewards
    except Exception as ex:
        safe_api_message(ex)
        return [], []

def get_total_points():
    try:
        client = get_gspread_client()
        sheet = client.open(SHEET_NAME)
        ws = sheet.worksheet(HISTORY_SHEET)
        history = ws.get_all_records()
        return sum(int(row.get("points", 0) or 0) for row in history)
    except Exception as ex:
        safe_api_message(ex)
        return 0

def get_history_for_date(qdate):
    try:
        client = get_gspread_client()
        sheet = client.open(SHEET_NAME)
        ws = sheet.worksheet(HISTORY_SHEET)
        history = ws.get_all_records()
        q = str(qdate)
        return [row for row in history if row.get("date") == q]
    except Exception as ex:
        safe_api_message(ex)
        return []

def get_history_for_dates(date_list):
    try:
        client = get_gspread_client()
        sheet = client.open(SHEET_NAME)
        ws = sheet.worksheet(HISTORY_SHEET)
        history = ws.get_all_records()
        result = {}
        for d in date_list:
            result[d] = [row for row in history if row.get("date") == d]
        return result
    except Exception as ex:
        safe_api_message(ex)
        return {d: [] for d in date_list}

def batch_add_points(records):
    try:
        client = get_gspread_client()
        ws = client.open(SHEET_NAME).worksheet(HISTORY_SHEET)
        for rec in records:
            ws.append_row([rec["date"], rec["type"], rec["name"], rec["points"]])
    except Exception as ex:
        safe_api_message(ex)

def undo_last_redeem():
    try:
        client = get_gspread_client()
        ws = client.open(SHEET_NAME).worksheet(HISTORY_SHEET)
        data = ws.get_all_values()
        for i in range(len(data)-1, 0, -1):
            if data[i][1].lower() == "reward":
                ws.delete_rows(i+1)
                break
    except Exception as ex:
        safe_api_message(ex)

def update_tasks_and_rewards(task_rows, reward_rows):
    try:
        client = get_gspread_client()
        ws = client.open(SHEET_NAME).worksheet(TASKS_SHEET)
        new_data = []
        for t in task_rows:
            new_data.append(["Task", t["name"], t["points"]])
        for r in reward_rows:
            new_data.append(["Reward", r["name"], r["points"]])
        ws.clear()
        ws.append_row(["type", "name", "points"])
        for row in new_data:
            ws.append_row(row)
    except Exception as ex:
        safe_api_message(ex)

def sync_points_for_dates(update_list):
    try:
        client = get_gspread_client()
        ws = client.open(SHEET_NAME).worksheet(HISTORY_SHEET)
        all_data = ws.get_all_values()
        header = all_data[0] if all_data else ["date", "type", "name", "points"]
        records = all_data[1:] if len(all_data) > 1 else []
        # 删除所有撤销的
        for upd in update_list:
            if not upd["add"]:
                for i in range(len(records)):
                    if records[i][0] == upd["date"] and records[i][1].lower() == "task" and records[i][2] == upd["task"]:
                        ws.delete_rows(i+2)
                        records.pop(i)
                        break
        # 新增所有新打卡的
        for upd in update_list:
            if upd["add"]:
                ws.append_row([upd["date"], "Task", upd["task"], upd["points"]])
    except Exception as ex:
        safe_api_message(ex)
