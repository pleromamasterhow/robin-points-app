import streamlit as st
from datetime import date
from utils import load_data, save_data

data = load_data()
if "total_points" not in st.session_state:
    st.session_state["total_points"] = data["total_points"]
if "history" not in st.session_state:
    st.session_state["history"] = data["history"]

st.title("Backfill Check-in")
st.markdown(f"### 🏆 Total Points: {st.session_state.total_points}")

selected_date = st.date_input("Select a date", date.today())
selected_str = str(selected_date)

if selected_str not in st.session_state["history"]:
    st.session_state["history"][selected_str] = {"completed_tasks": [], "redeemed_rewards": []}

st.subheader(f"Tasks on {selected_str}")
for task in data["tasks"]:
    task_id = f"{selected_str}_{task['name']}"
    if task["name"] not in st.session_state["history"][selected_str]["completed_tasks"]:
        if st.button(f"✅ {task['name']} (+{task['points']} pts)", key=task_id):
            st.session_state["history"][selected_str]["completed_tasks"].append(task["name"])
            st.session_state["total_points"] += task["points"]
            data["history"] = st.session_state["history"]
            data["total_points"] = st.session_state["total_points"]
            save_data(data)
            st.rerun()
    else:
        st.markdown(f"✔️ {task['name']} (+{task['points']} pts) - Completed")