import streamlit as st
from sheet_utils import get_tasks_and_rewards, get_total_points, get_history_for_dates, sync_points_for_dates, safe_api_message
from datetime import date, timedelta

st.set_page_config(page_title="Robin Points Tracker", layout="centered")
st.title("Robin Points Tracker")
try:
    total_points = get_total_points()
    st.metric("Total Points", total_points)

    today = date.today()
    yesterday = today - timedelta(days=1)
    dates = [today, yesterday]
    date_labels = ["Today", "Yesterday"]
    tasks, _ = get_tasks_and_rewards()

    # 获取历史已打卡任务（健壮处理）
    histories = get_history_for_dates([d.isoformat() for d in dates])
    history_map = {d: set(r["name"] for r in histories.get(d.isoformat(), []) if r["type"].lower() == "task") for d in dates}

    if "pending_checks" not in st.session_state:
        st.session_state["pending_checks"] = {}

    for i, d in enumerate(dates):
        st.subheader(f"{date_labels[i]} - {d.strftime('%A, %Y-%m-%d')}")
        for task in tasks:
            task_name = task["name"]
            key = f"{d}-{task_name}"
            default_checked = (task_name in history_map[d])
            checked = st.session_state["pending_checks"].get(key, default_checked)
            st.session_state["pending_checks"][key] = st.checkbox(
                f"{task_name} (+{task['points']})",
                key=key,
                value=checked
            )

    if st.button("Confirm"):
        update_list = []
        for i, d in enumerate(dates):
            for task in tasks:
                task_name = task["name"]
                key = f"{d}-{task_name}"
                checked = st.session_state["pending_checks"][key]
                if checked != (task_name in history_map[d]):
                    update_list.append({"date": d.isoformat(), "task": task_name, "add": checked, "points": int(task["points"])})
        if update_list:
            sync_points_for_dates(update_list)
            st.success("Updated! Please refresh the page to see the latest status.")
        else:
            st.info("No changes detected.")
except Exception as ex:
    safe_api_message(ex)
