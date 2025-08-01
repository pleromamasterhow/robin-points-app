import streamlit as st
from utils import load_data, save_data, get_today_date

st.set_page_config(page_title="Robin Points App", layout="centered")
data = load_data()
today = get_today_date()

st.title("Daily Check-in")
st.markdown(f"### 🏆 Current Points: {data['total_points']}")

if today not in data["history"]:
    data["history"][today] = {"completed_tasks": [], "redeemed_rewards": []}

st.subheader(f"Today's Tasks - {today}")
for task in data["tasks"]:
    key = f"{today}_task_{task['name']}"
    checked = task["name"] in data["history"][today]["completed_tasks"]
    if st.checkbox(f"{task['name']} (+{task['points']} pts)", value=checked, key=key):
        if not checked:
            data["history"][today]["completed_tasks"].append(task["name"])
            data["total_points"] += task["points"]
    else:
        if checked:
            data["history"][today]["completed_tasks"].remove(task["name"])
            data["total_points"] -= task["points"]

save_data(data)