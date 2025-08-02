
import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import date
import pandas as pd

scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_dict(st.secrets["gcp_service_account"], scope)
client = gspread.authorize(creds)

SHEET_NAME = "Robin Points Tracker"
TASKS_SHEET = "TasksAndRewards"
HISTORY_SHEET = "History"

def get_tasks_and_rewards():
    sheet = client.open(SHEET_NAME)
    task_ws = sheet.worksheet(TASKS_SHEET)
    data = task_ws.get_all_records()
    tasks = [row for row in data if row.get("Type") == "Task"]
    rewards = [row for row in data if row.get("Type") == "Reward"]
    return tasks, rewards

def get_total_points():
    sheet = client.open(SHEET_NAME)
    history_ws = sheet.worksheet(HISTORY_SHEET)
    history_data = history_ws.get_all_records()
    total = sum([int(row["Points"]) for row in history_data])
    return total

def add_points(name, points, action_date=None):
    if action_date is None:
        action_date = date.today().isoformat()
    elif isinstance(action_date, date):
        action_date = action_date.isoformat()
    sheet = client.open(SHEET_NAME)
    history_ws = sheet.worksheet(HISTORY_SHEET)
    history_ws.append_row([action_date, name, int(points)])

def get_history_for_date(query_date):
    sheet = client.open(SHEET_NAME)
    history_ws = sheet.worksheet(HISTORY_SHEET)
    df = pd.DataFrame(history_ws.get_all_records())
    df["Date"] = pd.to_datetime(df["Date"])
    filtered = df[df["Date"] == pd.to_datetime(query_date)]
    return filtered.to_dict("records")
