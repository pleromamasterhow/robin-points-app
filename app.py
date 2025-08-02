import streamlit as st
from datetime import date, timedelta
from sheet_utils import get_tasks_and_rewards, get_history, add_history_entry, remove_history_entry

st.set_page_config(page_title="Robin Points", layout="centered")
st.title("🏠 Daily Check-in")

tasks, _ = get_tasks_and_rewards()
history_df = get_history()
today = date.today()
for offset in [0, -1, -2]:
    check_date = today + timedelta(days=offset)
    st.subheader(f"✅ Tasks for {check_date}")
    for task in tasks:
        matched = history_df[(history_df["date"] == str(check_date)) & 
                             (history_df["type"] == "task") & 
                             (history_df["name"] == task["name"])]
        if matched.empty:
            if st.button(f"{task['name']} (+{task['points']})", key=f"{check_date}_{task['name']}"):
                add_history_entry(str(check_date), "task", task["name"], int(task["points"]))
                st.experimental_rerun()
        else:
            if st.button(f"Undo {task['name']} ({check_date})", key=f"undo_{check_date}_{task['name']}"):
                remove_history_entry(str(check_date), "task", task["name"])
                st.experimental_rerun()

# 显示当前总分
history_df = get_history()
total_points = history_df["points"].sum()
st.sidebar.markdown(f"### 🏆 Total Points: {total_points}")