import streamlit as st
from sheet_utils import get_tasks_and_rewards, update_tasks_and_rewards

st.set_page_config(page_title="Settings", layout="centered")
st.title("Settings")

tasks, rewards = get_tasks_and_rewards()

st.header("Tasks")
edited_tasks = st.data_editor(tasks, num_rows="dynamic", use_container_width=True)

st.header("Rewards")
edited_rewards = st.data_editor(rewards, num_rows="dynamic", use_container_width=True)

if st.button("Save Changes"):
    update_tasks_and_rewards(edited_tasks, edited_rewards)
    st.success("Saved successfully!")
