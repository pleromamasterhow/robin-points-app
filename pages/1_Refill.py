import streamlit as st
from sheet_utils import get_tasks_and_rewards, batch_add_points, get_history_for_date, get_total_points
from datetime import date

st.title("Refill or Edit History")
st.metric("Total Points", get_total_points())

tasks, _ = get_tasks_and_rewards()
selected_date = st.date_input("Select date to refill:", value=date.today())
history = get_history_for_date(selected_date.isoformat())
done_tasks = set([r["name"] for r in history if r["type"].lower() == "task"])

if "refill_checks" not in st.session_state:
    st.session_state["refill_checks"] = {}

for task in tasks:
    key = f"{selected_date}-{task['name']}"
    default = (task["name"] in done_tasks) or st.session_state["refill_checks"].get(key, False)
    checked = st.checkbox(f"{task['name']} (+{task['points']})", key=key, value=default)
    st.session_state["refill_checks"][key] = checked

if st.button("Confirm refill"):
    to_add = []
    for task in tasks:
        key = f"{selected_date}-{task['name']}"
        if st.session_state["refill_checks"].get(key) and task["name"] not in done_tasks:
            to_add.append({"date": selected_date.isoformat(), "type": "Task", "name": task["name"], "points": int(task["points"])})
    if to_add:
        batch_add_points(to_add)
        st.success(f"{len(to_add)} records submitted! Please refresh the page to see updated status.")
    else:
        st.info("No new tasks to refill.")
