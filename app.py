import streamlit as st
from sheet_utils import get_tasks_and_rewards, batch_add_points, get_total_points
from datetime import date, timedelta

st.set_page_config(page_title="Robin Points Tracker", layout="centered")
st.title("Robin Points Tracker")

today = date.today()
dates = [today - timedelta(days=i) for i in range(3)]
tasks, _ = get_tasks_and_rewards()

if "pending_checks" not in st.session_state:
    st.session_state["pending_checks"] = {}

for d in reversed(dates):
    st.subheader(d.strftime("%A, %Y-%m-%d"))
    for task in tasks:
        task_name = task["name"]
        key = f"{d}-{task_name}"
        default = st.session_state["pending_checks"].get(key, False)
        checked = st.checkbox(f"{task_name} (+{task['points']})", key=key, value=default)
        st.session_state["pending_checks"][key] = checked

if st.button("Confirm"):
    to_add = []
    for d in dates:
        for task in tasks:
            key = f"{d}-{task['name']}"
            if st.session_state["pending_checks"].get(key):
                to_add.append({"date": d.isoformat(), "type": "Task", "name": task["name"], "points": int(task["points"])})
    if to_add:
        batch_add_points(to_add)
        st.success(f"{len(to_add)} records submitted!")
        st.session_state["pending_checks"] = {}
        st.experimental_rerun()
    else:
        st.info("No tasks selected.")

st.metric("Total Points", get_total_points())
