import streamlit as st
from sheet_utils import get_tasks_and_rewards, update_tasks_and_rewards

st.title("⚙️ Settings")
tasks, rewards = get_tasks_and_rewards()
combined = [{"type": "task", **t} for t in tasks] + [{"type": "reward", **r} for r in rewards]

st.markdown("### Edit Tasks & Rewards")
edited = []
for i, item in enumerate(combined):
    cols = st.columns([3, 2, 1])
    with cols[0]:
        name = st.text_input("Name", value=item["name"], key=f"name_{i}")
    with cols[1]:
        points = st.number_input("Points", value=int(item["points"]), step=1, key=f"points_{i}")
    with cols[2]:
        remove = st.checkbox("❌ Remove", key=f"remove_{i}")
    if not remove:
        edited.append({"type": item["type"], "name": name, "points": points})

st.markdown("### ➕ Add New Entry")
col1, col2, col3 = st.columns(3)
new_type = col1.selectbox("Type", ["task", "reward"])
new_name = col2.text_input("New Name")
new_points = col3.number_input("New Points", step=1)
if st.button("Add Entry"):
    edited.append({"type": new_type, "name": new_name, "points": int(new_points)})
    st.success("Added successfully!")

if st.button("💾 Save All Changes"):
    update_tasks_and_rewards(edited)
    st.success("Settings updated!")
    st.experimental_rerun()