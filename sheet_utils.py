import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
from datetime import date

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
    tasks = [row for row in data if row.get("type") == "Task"]
    rewards = [row for row in data if row.get("type") == "Reward"]
    return tasks, rewards

def get_total_points():
    sheet = client.open(SHEET_NAME)
    history = sheet.worksheet(HISTORY_SHEET).get_all_records()
    return sum(int(row.get("points", 0) or 0) for row in history)

def add_points(task, points, action_date=None):
    if action_date is None:
        action_date = date.today().isoformat()
    elif isinstance(action_date, date):
        action_date = action_date.isoformat()
    sheet = client.open(SHEET_NAME).worksheet(HISTORY_SHEET)
    sheet.append_row([action_date, "Task", task, int(points)])

def get_history_for_date(query_date):
    sheet = client.open(SHEET_NAME)
    history = sheet.worksheet(HISTORY_SHEET).get_all_records()
    q = str(query_date)
    return [row for row in history if row.get("date") == q]
