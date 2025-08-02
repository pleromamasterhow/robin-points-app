import streamlit as st
from sheet_utils import get_tasks_and_rewards, batch_add_points, get_total_points, get_history_for_date
from datetime import date, timedelta

st.set_page_config(page_title="Robin Points Tracker", layout="centered")
st.title("Robin Points Tracker")

total_points = get_total_points()
st.metric("Total Points", total_points)

today = date.today()
yesterday = today - timedelta(days=1)
dates = [today, yesterday]
tasks, _ = get_tasks_and_rewards()

# 获取历史已打卡任务
history_today = get_history_for_date(today.isoformat())
history_yesterday = get_history_for_date(yesterday.isoformat())
done_today = set(r["name"] for r in history_today if r["type"].lower() == "task")
done_yesterday = set(r["name"] for r in history_yesterday if r["type"].lower() == "task")

if "pending_checks" not in st.session_state:
    st.session_state["pending_checks"] = {}

date_labels = ["Today", "Yesterday"]
for i, (d, done_tasks) in enumerate(zip(dates, [done_today, done_yesterday])):
    st.subheader(f"{date_labels[i]} - {d.strftime('%A, %Y-%m-%d')}")
    for task in tasks:
        task_name = task["name"]
        key = f"{d}-{task_name}"
        already_done = task_name in done_tasks
        checked = st.session_state["pending_checks"].get(key, False) or already_done
        st.checkbox(
            f"{task_name} (+{task['points']})",
            key=key,
            value=checked,
            disabled=already_done,
            help="Already completed" if already_done else None
        )
        if already_done:
            st.write(":white_check_mark: Done!")

if st.button("Confirm"):
    to_add = []
    for d, done_tasks in zip(dates, [done_today, done_yesterday]):
        for task in tasks:
            key = f"{d}-{task['name']}"
            # 仅写入尚未完成且新勾选的
            if (st.session_state["pending_checks"].get(key) and task["name"] not in done_tasks):
                to_add.append({"date": d.isoformat(), "type": "Task", "name": task["name"], "points": int(task["points"])})
    if to_add:
        batch_add_points(to_add)
        st.success(f"{len(to_add)} records submitted! Please refresh the page to see updated status.")
    else:
        st.info("No new tasks selected.")
