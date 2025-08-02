import streamlit as st
from datetime import datetime, timedelta
from sheet_utils import get_tasks_and_rewards, get_history, add_history_entry, remove_history_entry

st.title("📆 Backfill")
tasks, _ = get_tasks_and_rewards()
history_df = get_history()

selected_date = st.date_input("Select date", value=datetime.today().date())
filtered = history_df[history_df["date"] == str(selected_date)]
total = filtered["points"].sum()
st.markdown(f"### ✅ Score on {selected_date}: {total}")

st.markdown("#### ✅ Fill Tasks")
for task in tasks:
    exists = filtered[(filtered["type"] == "task") & (filtered["name"] == task["name"])]
    if exists.empty:
        if st.button(f"{task['name']} (+{task['points']})", key=f"fill_{task['name']}"):
            add_history_entry(str(selected_date), "task", task["name"], int(task["points"]))
            st.experimental_rerun()
    else:
        if st.button(f"Undo {task['name']}", key=f"undo_fill_{task['name']}"):
            remove_history_entry(str(selected_date), "task", task["name"])
            st.experimental_rerun()