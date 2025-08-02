import streamlit as st
from datetime import date, timedelta
from sheet_utils import get_tasks_and_rewards, add_points, get_total_points, get_history_for_date

st.set_page_config(page_title="Robin Points", layout="centered")
st.title("Robin Points Tracker")

today = date.today()
for delta, label in zip([0, 1, 2], ["Today", "Yesterday", "2 Days Ago"]):
    st.subheader(label)
    task_data, _ = get_tasks_and_rewards()
    history = get_history_for_date(today - timedelta(days=delta))
    cols = st.columns(len(task_data))
    for idx, task in enumerate(task_data):
        with cols[idx]:
            if st.button(f"{task['Task']} (+{task['Points']})", key=f"{label}-{task['Task']}"):
                add_points(task['Task'], task['Points'], today - timedelta(days=delta))
                st.rerun()

st.markdown(f"### Total Points: {get_total_points()}")
