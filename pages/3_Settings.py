import streamlit as st
from utils import load_data, save_data

st.title("Settings")
data = load_data()
st.markdown(f"### 🏆 Total Points: {data['total_points']}")

st.subheader("Edit Tasks")
for task in data["tasks"]:
    task["name"] = st.text_input("Task name", task["name"], key=task["name"] + "_name")
    task["points"] = st.number_input("Points", value=task["points"], step=1, key=task["name"] + "_points")

if st.button("Save Tasks"):
    save_data(data)
    st.success("Tasks updated!")

st.subheader("Edit Rewards")
for reward in data["rewards"]:
    reward["name"] = st.text_input("Reward name", reward["name"], key=reward["name"] + "_rname")
    reward["points"] = st.number_input("Points", value=reward["points"], step=1, key=reward["name"] + "_rpoints")

if st.button("Save Rewards"):
    save_data(data)
    st.success("Rewards updated!")