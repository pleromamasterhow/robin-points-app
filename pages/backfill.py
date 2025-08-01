import streamlit as st
from utils import load_data, save_data
from datetime import date, timedelta

def render():
    st.title("Backfill Records")
    password = st.text_input("Enter password:", type="password")
    if password != "robin":
        st.warning("Incorrect password.")
        return

    data = load_data()
    days = st.slider("Select how many past days to show", 1, 30, 7)
    today = date.today()

    for i in range(days):
        d = today - timedelta(days=i)
        d_str = str(d)
        st.subheader(d_str)
        if d_str not in data["history"]:
            data["history"][d_str] = {"tasks": [], "rewards": []}

        with st.expander("Tasks"):
            for task in data["tasks"]:
                key = f"{d_str}_task_{task['name']}"
                checked = task["name"] in data["history"][d_str]["tasks"]
                if st.checkbox(f"{task['name']} (+{task['points']} pts)", value=checked, key=key):
                    if not checked:
                        data["history"][d_str]["tasks"].append(task["name"])
                        data["total_points"] += task["points"]
                else:
                    if checked:
                        data["history"][d_str]["tasks"].remove(task["name"])
                        data["total_points"] -= task["points"]

        with st.expander("Rewards"):
            for reward in data["rewards"]:
                key = f"{d_str}_reward_{reward['name']}"
                amount = reward["points"]
                if reward.get("custom_price"):
                    amount = st.number_input(f"{reward['name']} - Enter points used:", key=key+"_amount", min_value=1, step=1)
                if st.button(f"Redeem {reward['name']} (-{amount} pts)", key=key):
                    if data["total_points"] >= amount:
                        data["total_points"] -= amount
                        data["history"][d_str]["rewards"].append({"name": reward["name"], "points": amount})
                        save_data(data)
                        st.success(f"Backfilled {reward['name']}!")
                    else:
                        st.error("Not enough points")

    save_data(data)