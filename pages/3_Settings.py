import streamlit as st
from utils import load_data, save_data

st.title("Settings")
data = load_data()
st.markdown("### 🏆 Total Points: {}".format(data.get("total_points", 0)))

# Task 管理
st.header("Tasks")
for idx, task in enumerate(data["tasks"]):
    col1, col2, col3 = st.columns([3, 2, 1])
    with col1:
        new_name = st.text_input(f"Task Name {idx}", value=task["name"], key=f"task_name_{idx}")
    with col2:
        new_points = st.number_input(f"Points {idx}", value=task["points"], step=1, key=f"task_points_{idx}")
    with col3:
        if st.button("🗑 Delete", key=f"delete_task_{idx}"):
            data["tasks"].pop(idx)
            save_data(data)
            st.experimental_rerun()

if st.button("Save Task Changes"):
    for idx in range(len(data["tasks"])):
        data["tasks"][idx]["name"] = st.session_state[f"task_name_{idx}"]
        data["tasks"][idx]["points"] = st.session_state[f"task_points_{idx}"]
    save_data(data)
    st.success("Tasks updated!")

st.subheader("➕ Add New Task")
new_task_name = st.text_input("New Task Name")
new_task_points = st.number_input("New Task Points", step=1, min_value=1)
if st.button("Add Task"):
    if new_task_name:
        data["tasks"].append({"name": new_task_name, "points": int(new_task_points)})
        save_data(data)
        st.success("Task added!")
        st.experimental_rerun()

# Reward 管理
st.header("Rewards")
for idx, reward in enumerate(data["rewards"]):
    col1, col2, col3 = st.columns([3, 2, 1])
    with col1:
        new_rname = st.text_input(f"Reward Name {idx}", value=reward["name"], key=f"reward_name_{idx}")
    with col2:
        new_rpoints = st.number_input(f"Reward Points {idx}", value=reward["points"], step=1, key=f"reward_points_{idx}")
    with col3:
        if st.button("🗑 Delete", key=f"delete_reward_{idx}"):
            data["rewards"].pop(idx)
            save_data(data)
            st.experimental_rerun()

if st.button("Save Reward Changes"):
    for idx in range(len(data["rewards"])):
        data["rewards"][idx]["name"] = st.session_state[f"reward_name_{idx}"]
        data["rewards"][idx]["points"] = st.session_state[f"reward_points_{idx}"]
    save_data(data)
    st.success("Rewards updated!")

st.subheader("➕ Add New Reward")
new_reward_name = st.text_input("New Reward Name")
new_reward_points = st.number_input("New Reward Points", step=1, min_value=0)
if st.button("Add Reward"):
    if new_reward_name:
        data["rewards"].append({"name": new_reward_name, "points": int(new_reward_points)})
        save_data(data)
        st.success("Reward added!")
        st.experimental_rerun()