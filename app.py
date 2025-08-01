import streamlit as st
from utils import load_data, save_data
from datetime import date, timedelta

st.set_page_config(page_title="Robin Points Tracker", layout="centered")

data = load_data()
if "total_points" not in st.session_state:
    st.session_state["total_points"] = data["total_points"]
if "history" not in st.session_state:
    st.session_state["history"] = data["history"]

st.title("Daily Check-in")
st.markdown(f"### 🏆 Total Points: {st.session_state.total_points}")

for offset in [0, -1, -2]:
    day = date.today() + timedelta(days=offset)
    day_str = str(day)
    label = "Today" if offset == 0 else ("Yesterday" if offset == -1 else "2 Days Ago")
    st.subheader(f"{label} - {day_str}")

    if day_str not in st.session_state["history"]:
        st.session_state["history"][day_str] = {"completed_tasks": [], "redeemed_rewards": []}

    for task in data["tasks"]:
        key = f"{day_str}_{task['name']}"
        checked = task["name"] in st.session_state["history"][day_str]["completed_tasks"]
        new_checked = st.checkbox(f"{task['name']} (+{task['points']} pts)", value=checked, key=key)
        if new_checked != checked:
            if new_checked:
                st.session_state["history"][day_str]["completed_tasks"].append(task["name"])
                st.session_state["total_points"] += task["points"]
            else:
                st.session_state["history"][day_str]["completed_tasks"].remove(task["name"])
                st.session_state["total_points"] -= task["points"]
            data["history"] = st.session_state["history"]
            data["total_points"] = st.session_state["total_points"]
            save_data(data)