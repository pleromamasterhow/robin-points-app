import streamlit as st
from utils import load_data, save_data
from datetime import date, timedelta

st.set_page_config(page_title="Robin Points App", layout="centered")
if "refresh" not in st.session_state:
    st.session_state["refresh"] = False

data = load_data()
st.title("Daily Check-in")
st.markdown(f"### 🏆 Current Points: {data['total_points']}")

if st.session_state["refresh"]:
    st.session_state["refresh"] = False
    st.experimental_rerun()

# 支持三天打卡
for offset in [0, -1, -2]:
    day = date.today() + timedelta(days=offset)
    day_str = str(day)
    label = "Today" if offset == 0 else ("Yesterday" if offset == -1 else "2 Days Ago")
    st.subheader(f"{label} - {day_str}")

    if day_str not in data["history"]:
        data["history"][day_str] = {"completed_tasks": [], "redeemed_rewards": []}

    for task in data["tasks"]:
        key = f"{day_str}_{task['name']}"
        checked = task["name"] in data["history"][day_str]["completed_tasks"]
        new_checked = st.checkbox(f"{task['name']} (+{task['points']} pts)", value=checked, key=key)
        if new_checked != checked:
            if new_checked:
                data["history"][day_str]["completed_tasks"].append(task["name"])
                data["total_points"] += task["points"]
            else:
                data["history"][day_str]["completed_tasks"].remove(task["name"])
                data["total_points"] -= task["points"]
            save_data(data)
            st.session_state["refresh"] = True