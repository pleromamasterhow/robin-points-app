import streamlit as st
from sheet_utils import get_tasks_and_rewards, add_points, get_total_points, get_history_for_date
from datetime import date, timedelta

st.set_page_config(page_title="Robin Points Tracker", layout="centered")
st.title("Robin Points Tracker")

today = date.today()
dates = [today - timedelta(days=i) for i in range(3)]
tasks, rewards = get_tasks_and_rewards()
total_points = get_total_points()

st.metric("Total Points", total_points)
for d in reversed(dates):
    st.header(d.strftime("%A, %Y-%m-%d"))
    for task in tasks:
        task_name = task["Task"]
        task_points = int(task["Points"])
        if st.button(f"{task_name} (+{task_points})", key=f"{d}-{task_name}"):
            add_points(task_name, task_points, d)
            st.experimental_rerun()
