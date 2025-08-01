import streamlit as st
from utils import load_data, save_data, get_today_date

st.set_page_config(page_title="Robin's Points Tracker", layout="centered")
st.title("Daily Check-in")

data = load_data()
today = get_today_date()

if today not in data["history"]:
    data["history"][today] = {"completed_tasks": [], "redeemed_rewards": []}

st.subheader(f"Today's Tasks ({today})")
for task in data["tasks"]:
    if st.checkbox(f'{task["name"]} (+{task["points"]} pts)', key=task["name"]):
        if task["name"] not in data["history"][today]["completed_tasks"]:
            data["history"][today]["completed_tasks"].append(task["name"])
            data["total_points"] += task["points"]
            save_data(data)
            st.experimental_rerun()

st.success(f"Total Points: {data['total_points']}")