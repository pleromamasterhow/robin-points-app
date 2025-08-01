import streamlit as st
from utils import load_data, save_data
from datetime import date

def render():
    st.title("Daily Check-in")
    password = st.text_input("Enter password:", type="password")
    if password != "robin":
        st.warning("Incorrect password.")
        return

    data = load_data()
    today = str(date.today())
    if today not in data["history"]:
        data["history"][today] = {"tasks": [], "rewards": []}

    st.subheader(f"Today's Tasks ({today})")
    for task in data["tasks"]:
        checked = task["name"] in data["history"][today]["tasks"]
        if st.checkbox(f"{task['name']} (+{task['points']} pts)", value=checked):
            if not checked:
                data["history"][today]["tasks"].append(task["name"])
                data["total_points"] += task["points"]
        else:
            if checked:
                data["history"][today]["tasks"].remove(task["name"])
                data["total_points"] -= task["points"]

    save_data(data)
    st.success(f"Total Points: {data['total_points']}")