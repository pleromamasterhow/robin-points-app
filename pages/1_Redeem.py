import streamlit as st
from sheet_utils import get_tasks_and_rewards, redeem_reward, get_total_points

st.set_page_config(page_title="Redeem", layout="centered")
st.title("Redeem a Reward")

_, rewards = get_tasks_and_rewards()

st.markdown(f"### Total Points: {get_total_points()}")

for reward in rewards:
    if reward["Reward"] == "Buy Toy":
        amount = st.number_input("Enter amount for Buy Toy", min_value=1, step=1)
        if st.button(f"Buy Toy (-{amount})"):
            redeem_reward("Buy Toy", amount)
            st.rerun()
    else:
        if st.button(f"{reward['Reward']} (-{reward['Points']})"):
            redeem_reward(reward["Reward"], reward["Points"])
            st.rerun()
