import streamlit as st
from sheet_utils import get_tasks_and_rewards, get_total_points, get_history_for_date, sync_points_for_dates, safe_api_message
from datetime import date

st.title("Refill or Edit History")
try:
    st.metric("Total Points", get_total_points())
    tasks, _ = get_tasks_and_rewards()
    selected_date = st.date_input("Select date to refill:", value=date.today())
    history = get_history_for_date(selected_date.isoformat())
    done_tasks = set([r["name"] for r in history if r["type"].lower() == "task"])

    if "refill_checks" not in st.session_state:
        st.session_state["refill_checks"] = {}

    for task in tasks:
        key = f"{selected_date}-{task['name']}"
        default_checked = (task["name"] in done_tasks)
        checked = st.session_state["refill_checks"].get(key, default_checked)
        st.session_state["refill_checks"][key] = st.checkbox(f"{task['name']} (+{task['points']})", key=key, value=checked)

    if st.button("Confirm refill"):
        update_list = []
        for task in tasks:
            key = f"{selected_date}-{task['name']}"
            checked = st.session_state["refill_checks"][key]
            if checked != (task["name"] in done_tasks):
                update_list.append({"date": selected_date.isoformat(), "task": task["name"], "add": checked, "points": int(task["points"])})
        if update_list:
            sync_points_for_dates(update_list)
            st.success("Updated! Please refresh the page to see the latest status.")
        else:
            st.info("No changes detected.")
except Exception as ex:
    safe_api_message(ex)
