import streamlit as st
from datetime import date
from utils import load_data, save_data

st.title("Backfill Check-in")
data = load_data()
st.markdown(f"### 🏆 Total Points: {data['total_points']}")

selected_date = st.date_input("Select a date", date.today())
selected_str = str(selected_date)
if selected_str not in data["history"]:
    data["history"][selected_str] = {"completed_tasks": [], "redeemed_rewards": []}

st.subheader(f"Tasks on {selected_str}")
for task in data["tasks"]:
    checked = task["name"] in data["history"][selected_str]["completed_tasks"]
    if st.checkbox(f"{task['name']} (+{task['points']} pts)", value=checked, key=selected_str + task["name"]):
        if not checked:
            data["history"][selected_str]["completed_tasks"].append(task["name"])
            data["total_points"] += task["points"]
        else:
            data["history"][selected_str]["completed_tasks"].remove(task["name"])
            data["total_points"] -= task["points"]
        save_data(data)