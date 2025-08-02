import streamlit as st
from datetime import date
from sheet_utils import get_tasks_and_rewards, add_points, get_history_for_date, get_total_points

st.set_page_config(page_title="Refill", layout="centered")
st.title("Backfill Check-ins")

selected_date = st.date_input("Select Date", value=date.today())
task_data, _ = get_tasks_and_rewards()
history = get_history_for_date(selected_date)

st.markdown(f"### Total Points: {get_total_points()}")
for task in task_data:
    if st.button(f"{task['Task']} (+{task['Points']})", key=f"refill-{task['Task']}"):
        add_points(task["Task"], task["Points"], selected_date)
        st.rerun()
