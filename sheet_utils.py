import gspread
from datetime import date
from oauth2client.service_account import ServiceAccountCredentials
import streamlit as st

scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_dict(st.secrets["gcp_service_account"], scope)
client = gspread.authorize(creds)

SHEET_NAME = "Robin Points Tracker"
TASKS_SHEET = "TasksAndRewards"
HISTORY_SHEET = "History"

def get_tasks_and_rewards():
    sheet = client.open(SHEET_NAME)
    tasks_data = sheet.worksheet(TASKS_SHEET).get_all_records()
    return tasks_data, []

def add_points(task_name, points):
    sheet = client.open(SHEET_NAME).worksheet(HISTORY_SHEET)
    today = str(date.today())
    sheet.append_row([today, task_name, points])

def get_total_points():
    sheet = client.open(SHEET_NAME).worksheet(HISTORY_SHEET)
    data = sheet.get_all_records()
    return sum(int(row["Points"]) for row in data)

def get_history_for_date(day):
    return 0  # Placeholder