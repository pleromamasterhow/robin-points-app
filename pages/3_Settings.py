import streamlit as st
from sheet_utils import get_tasks_and_rewards, update_tasks_and_rewards, get_total_points, safe_api_message, clear_caches

st.title("Settings (Edit Tasks and Rewards)")
st.markdown('<style> .stButton button {font-size:22px !important;} </style>', unsafe_allow_html=True)
def load_total_points():
    return get_total_points()

if "total_points" not in st.session_state:
    st.session_state["total_points"] = load_total_points()

try:
    st.metric("Total Points", st.session_state["total_points"])
    tasks, rewards = get_tasks_and_rewards()
    st.subheader("Tasks")
    task_data = [{"name": t["name"], "points": t["points"]} for t in tasks]
    edited_tasks = st.data_editor(task_data, num_rows="dynamic", key="tasks")

    st.subheader("Rewards")
    reward_data = [{"name": r["name"], "points": r["points"]} for r in rewards]
    edited_rewards = st.data_editor(reward_data, num_rows="dynamic", key="rewards")

    if st.button("Save Changes", use_container_width=True):
        update_tasks_and_rewards(edited_tasks, edited_rewards)
        clear_caches()
        st.session_state["total_points"] = load_total_points()
        st.success("Tasks and Rewards updated! Total Points refreshed.")
except Exception as ex:
    safe_api_message(ex)
