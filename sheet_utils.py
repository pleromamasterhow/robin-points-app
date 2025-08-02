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
creds = Credentials.from_service_account_info(st.secrets["gcp_service_account"], scopes=scope)
client = gspread.authorize(creds)

def get_tasks_and_rewards():
    sheet = client.open(SHEET_NAME)
    data = sheet.worksheet(TASKS_SHEET).get_all_records()
    tasks = [row for row in data if row.get("type", "").lower() == "task"]
    rewards = [row for row in data if row.get("type", "").lower() == "reward"]
    return tasks, rewards

def get_total_points():
    sheet = client.open(SHEET_NAME)
    history = sheet.worksheet(HISTORY_SHEET).get_all_records()
    return sum(int(row.get("points", 0) or 0) for row in history)

def batch_add_points(records):
    sheet = client.open(SHEET_NAME).worksheet(HISTORY_SHEET)
    for rec in records:
        sheet.append_row([rec["date"], rec["type"], rec["name"], rec["points"]])

def get_history_for_date(qdate):
    sheet = client.open(SHEET_NAME)
    history = sheet.worksheet(HISTORY_SHEET).get_all_records()
    q = str(qdate)
    return [row for row in history if row.get("date") == q]

def undo_last_redeem():
    ws = client.open(SHEET_NAME).worksheet(HISTORY_SHEET)
    data = ws.get_all_values()
    for i in range(len(data)-1, 0, -1):
        if data[i][1].lower() == "reward":
            ws.delete_rows(i+1)
            break

def update_tasks_and_rewards(task_rows, reward_rows):
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
