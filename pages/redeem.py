import streamlit as st
from utils import load_data, save_data
from datetime import date

def render():
    st.title("Redeem Rewards")
    password = st.text_input("Enter password:", type="password")
    if password != "robin":
        st.warning("Incorrect password.")
        return

    data = load_data()
    today = str(date.today())
    if today not in data["history"]:
        data["history"][today] = {"tasks": [], "rewards": []}

    st.subheader("Available Rewards")
    for reward in data["rewards"]:
        if reward.get("custom_price"):
            amount = st.number_input(f"{reward['name']} - Enter cost in points:", min_value=1, step=1)
        else:
            amount = reward["points"]
        if st.button(f"Redeem {reward['name']} (-{amount} pts)"):
            if data["total_points"] >= amount:
                data["total_points"] -= amount
                data["history"][today]["rewards"].append({"name": reward["name"], "points": amount})
                save_data(data)
                st.success(f"Redeemed {reward['name']}!")
            else:
                st.error("Not enough points.")
    st.info(f"Total Points: {data['total_points']}")