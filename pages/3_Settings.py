import streamlit as st
from sheet_utils import get_tasks_and_rewards, update_tasks_and_rewards, get_total_points, safe_api_message

st.title("Settings (Edit Tasks and Rewards)")
try:
    st.metric("Total Points", get_total_points())
    tasks, rewards = get_tasks_and_rewards()
    st.subheader("Tasks")
    task_data = [{"name": t["name"], "points": t["points"]} for t in tasks]
    edited_tasks = st.data_editor(task_data, num_rows="dynamic", key="tasks")

    st.subheader("Rewards")
    reward_data = [{"name": r["name"], "points": r["points"]} for r in rewards]
    edited_rewards = st.data_editor(reward_data, num_rows="dynamic", key="rewards")

    if st.button("Save Changes"):
        update_tasks_and_rewards(edited_tasks, edited_rewards)
        st.success("Tasks and Rewards updated! Please refresh the page to see updated status.")
except Exception as ex:
    safe_api_message(ex)
