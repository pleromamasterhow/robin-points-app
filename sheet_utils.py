import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

scope = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_dict(st.secrets["gcp_service_account"], scope)
client = gspread.authorize(creds)

SHEET_NAME = "RobinPoints"
TASKS_SHEET = "TasksAndRewards"
HISTORY_SHEET = "History"

def get_tasks_and_rewards():
    sheet = client.open(SHEET_NAME)
    data = sheet.worksheet(TASKS_SHEET).get_all_records()
    tasks = [row for row in data if row["Type"] == "Task"]
    rewards = [row for row in data if row["Type"] == "Reward"]
    return tasks, rewards

def get_total_points():
    records = client.open(SHEET_NAME).worksheet(HISTORY_SHEET).get_all_records()
    return 1000 + sum(int(r["Points"]) for r in records)

def add_points(task, points, day):
    sheet = client.open(SHEET_NAME).worksheet(HISTORY_SHEET)
    sheet.append_row([str(day), task, int(points)])

def redeem_reward(reward, cost):
    sheet = client.open(SHEET_NAME).worksheet(HISTORY_SHEET)
    sheet.append_row([str(datetime.today().date()), reward, -int(cost)])

def undo_last_action():
    sheet = client.open(SHEET_NAME).worksheet(HISTORY_SHEET)
    data = sheet.get_all_values()
    if len(data) > 1:
        sheet.delete_rows(len(data))

def get_history_for_date(day):
    records = client.open(SHEET_NAME).worksheet(HISTORY_SHEET).get_all_records()
    return [r for r in records if r["Date"] == str(day)]

def update_tasks_and_rewards(tasks, rewards):
    worksheet = client.open(SHEET_NAME).worksheet(TASKS_SHEET)
    worksheet.clear()
    worksheet.append_row(["Type", "Task", "Points", "Reward"])
    for t in tasks:
        worksheet.append_row(["Task", t["Task"], t["Points"], ""])
    for r in rewards:
        worksheet.append_row(["Reward", "", r["Points"], r["Reward"]])
