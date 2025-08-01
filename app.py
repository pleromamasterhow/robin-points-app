import streamlit as st
from utils import load_data, save_data
from datetime import date, timedelta

st.set_page_config(page_title="Robin Points Tracker", layout="centered")

# Initial session_state
if "total_points" not in st.session_state:
    st.session_state.total_points = None

data = load_data()
if st.session_state.total_points is None:
    st.session_state.total_points = data["total_points"]

st.title("Daily Check-in")
st.markdown(f"### 🏆 Total Points: {st.session_state.total_points}")

# Show tasks for Today, Yesterday, and 2 Days Ago
for offset in [0, -1, -2]:
    day = date.today() + timedelta(days=offset)
    day_str = str(day)
    label = "Today" if offset == 0 else ("Yesterday" if offset == -1 else "2 Days Ago")
    st.subheader(f"{label} - {day_str}")

    if day_str not in data["history"]:
        data["history"][day_str] = {"completed_tasks": [], "redeemed_rewards": []}

    for task in data["tasks"]:
        task_key = f"{day_str}_{task['name']}"
        checked = task["name"] in data["history"][day_str]["completed_tasks"]
        user_input = st.checkbox(f"{task['name']} (+{task['points']} pts)", value=checked, key=task_key)

        if user_input != checked:
            if user_input:
                data["history"][day_str]["completed_tasks"].append(task["name"])
                data["total_points"] += task["points"]
                st.session_state.total_points = data["total_points"]
            else:
                data["history"][day_str]["completed_tasks"].remove(task["name"])
                data["total_points"] -= task["points"]
                st.session_state.total_points = data["total_points"]
            save_data(data)
            st.experimental_rerun()