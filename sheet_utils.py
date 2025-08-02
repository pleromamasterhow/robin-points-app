import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
import pandas as pd

SHEET_NAME = "Robin Points Tracker"
TASKS_SHEET = "TasksAndRewards"
HISTORY_SHEET = "History"
CREDS_FILE = "robintracker-5ffca9f369ad.json"

def get_client():
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name(CREDS_FILE, scope)
    client = gspread.authorize(creds)
    return client

def get_tasks_and_rewards():
    client = get_client()
    sheet = client.open(SHEET_NAME).worksheet(TASKS_SHEET)
    records = sheet.get_all_records()
    tasks = [r for r in records if r["type"] == "task"]
    rewards = [r for r in records if r["type"] == "reward"]
    return tasks, rewards

def add_task(name, points):
    client = get_client()
    sheet = client.open(SHEET_NAME).worksheet(TASKS_SHEET)
    sheet.append_row(["task", name, points])

def add_reward(name, points):
    client = get_client()
    sheet = client.open(SHEET_NAME).worksheet(TASKS_SHEET)
    sheet.append_row(["reward", name, points])

def update_tasks_and_rewards(new_data):
    client = get_client()
    sheet = client.open(SHEET_NAME).worksheet(TASKS_SHEET)
    sheet.clear()
    sheet.append_row(["type", "name", "points"])
    for row in new_data:
        sheet.append_row([row["type"], row["name"], row["points"]])

def get_history():
    client = get_client()
    sheet = client.open(SHEET_NAME).worksheet(HISTORY_SHEET)
    data = sheet.get_all_records()
    return pd.DataFrame(data)

def add_history_entry(date, type_, name, points):
    client = get_client()
    sheet = client.open(SHEET_NAME).worksheet(HISTORY_SHEET)
    sheet.append_row([date, type_, name, points])

def remove_history_entry(date, type_, name):
    df = get_history()
    idx = df[(df["date"] == date) & (df["type"] == type_) & (df["name"] == name)].index
    if not idx.empty:
        df = df.drop(idx[0])
        client = get_client()
        sheet = client.open(SHEET_NAME).worksheet(HISTORY_SHEET)
        sheet.clear()
        sheet.append_row(["date", "type", "name", "points"])
        for _, row in df.iterrows():
            sheet.append_row([row["date"], row["type"], row["name"], row["points"]])