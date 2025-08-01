import streamlit as st
import calendar
from datetime import datetime
from utils import load_data, save_data

st.title("Backfill Check-in")
data = load_data()

selected_date = st.date_input("Select a date to backfill")
date_str = str(selected_date)
if date_str not in data["history"]:
    data["history"][date_str] = {"completed_tasks": [], "redeemed_rewards": []}

st.subheader(f"Tasks on {date_str}")
for task in data["tasks"]:
    checked = task["name"] in data["history"][date_str]["completed_tasks"]
    if st.checkbox(f'{task["name"]} (+{task["points"]} pts)', value=checked, key=date_str+task["name"]):
        if not checked:
            data["history"][date_str]["completed_tasks"].append(task["name"])
            data["total_points"] += task["points"]
            save_data(data)
            st.experimental_rerun()