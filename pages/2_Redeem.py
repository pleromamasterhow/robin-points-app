import streamlit as st
from sheet_utils import get_tasks_and_rewards, batch_add_points, undo_last_redeem, get_total_points, safe_api_message
from datetime import date

st.title("Redeem Rewards")
try:
    st.metric("Total Points", get_total_points())
    _, rewards = get_tasks_and_rewards()
    selected_reward = st.selectbox("Select reward to redeem:", [r["name"] for r in rewards])

    if selected_reward == "Buy Toy":
        amount = st.number_input("Enter points for Buy Toy:", min_value=1, value=10)
        points = -abs(amount)
    else:
        points = -abs(int([r["points"] for r in rewards if r["name"] == selected_reward][0]))

    if st.button("Confirm Redeem"):
        to_add = [{"date": date.today().isoformat(), "type": "Reward", "name": selected_reward, "points": points}]
        batch_add_points(to_add)
        st.success(f"Redeemed: {selected_reward} ({-points} points). Please refresh the page to see updated status.")

    if st.button("Undo last redemption"):
        undo_last_redeem()
        st.success("Last redeem record undone. Please refresh the page to see updated status.")
except Exception as ex:
    safe_api_message(ex)
