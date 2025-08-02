import streamlit as st
from sheet_utils import get_tasks_and_rewards, get_total_points, get_history_for_dates, sync_points_for_dates, safe_api_message, clear_caches
from datetime import date, timedelta

st.set_page_config(page_title="Robin Points Tracker", layout="wide")
st.markdown('<style> .stButton button, .stCheckbox>div {font-size:22px !important;} .stMetricValue {font-size: 36px;} </style>', unsafe_allow_html=True)
st.title("Robin Points Tracker")

def load_total_points():
    return get_total_points()

if "total_points" not in st.session_state:
    st.session_state["total_points"] = load_total_points()

today = date.today()
yesterday = today - timedelta(days=1)
dates = [today, yesterday]
date_labels = ["Today", "Yesterday"]

try:
    tasks, _ = get_tasks_and_rewards()
    histories = get_history_for_dates([d.isoformat() for d in dates])
    history_map = {d: set(r["name"] for r in histories.get(d.isoformat(), []) if r["type"].lower() == "task") for d in dates}

    if "pending_checks" not in st.session_state:
        st.session_state["pending_checks"] = {}

    st.metric("Total Points", st.session_state["total_points"])

    for i, d in enumerate(dates):
        st.subheader(f"{date_labels[i]} - {d.strftime('%a, %Y-%m-%d')}")
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

    if st.button("Confirm", use_container_width=True):
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
            clear_caches()
            st.session_state["total_points"] = load_total_points()
            st.success("Updated! Total Points refreshed.")
        else:
            st.info("No changes detected.")
except Exception as ex:
    safe_api_message(ex)
