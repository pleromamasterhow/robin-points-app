import streamlit as st
from sheet_utils import get_tasks_and_rewards, add_points, get_total_points, get_history_for_date

st.set_page_config(page_title="Robin Points Tracker", layout="wide")

st.title("Robin Points Tracker")
st.markdown("Track daily tasks and points for Robin.")

tasks, rewards = get_tasks_and_rewards()
today_points = get_history_for_date("today")
total_points = get_total_points()

st.metric(label="Total Points", value=total_points)

for task in tasks:
    if st.button(f"Add {task['points']} pts for {task['task']}", key=task['task']):
        add_points(task['task'], task['points'])
        st.experimental_rerun()