import streamlit as st
from utils import load_data, save_data

st.title("Settings")
data = load_data()
st.markdown("### 🏆 Total Points: {}".format(data.get("total_points", 0)))

# Task 管理
st.header("Tasks")
for idx, task in enumerate(data["tasks"]):
    st.markdown(f"• {task['name']} ({task['points']} pts)")

st.subheader("➕ Add New Task")
new_task_name = st.text_input("Task Name")
new_task_points = st.number_input("Task Points", step=1, min_value=1)
if st.button("Add Task"):
    if new_task_name:
        data["tasks"].append({"name": new_task_name, "points": int(new_task_points)})
        save_data(data)
        st.success("Task added!")
        st.rerun()

# Reward 管理
st.header("Rewards")
for idx, reward in enumerate(data["rewards"]):
    st.markdown(f"• {reward['name']} ({reward['points']} pts)")

st.subheader("➕ Add New Reward")
new_reward_name = st.text_input("Reward Name")
new_reward_points = st.number_input("Reward Points", step=1, min_value=0)
if st.button("Add Reward"):
    if new_reward_name:
        data["rewards"].append({"name": new_reward_name, "points": int(new_reward_points)})
        save_data(data)
        st.success("Reward added!")
        st.rerun()