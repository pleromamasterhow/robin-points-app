import streamlit as st
from utils import load_data, save_data

def render():
    st.title("Settings")
    password = st.text_input("Enter password:", type="password")
    if password != "robin":
        st.warning("Incorrect password.")
        return

    data = load_data()

    st.subheader("Edit Tasks")
    for i, task in enumerate(data["tasks"]):
        name = st.text_input(f"Task {i+1} name", value=task["name"], key=f"task_name_{i}")
        points = st.number_input(f"Task {i+1} points", value=task["points"], key=f"task_points_{i}")
        data["tasks"][i] = {"name": name, "points": points}

    st.subheader("Edit Rewards")
    for i, reward in enumerate(data["rewards"]):
        name = st.text_input(f"Reward {i+1} name", value=reward["name"], key=f"reward_name_{i}")
        custom = st.checkbox("Custom Price?", value=reward.get("custom_price", False), key=f"custom_price_{i}")
        points = 0 if custom else st.number_input(f"Reward {i+1} points", value=reward["points"], key=f"reward_points_{i}")
        data["rewards"][i] = {"name": name, "points": points}
        if custom:
            data["rewards"][i]["custom_price"] = True

    if st.button("Save"):
        save_data(data)
        st.success("Settings saved!")