import streamlit as st
from datetime import date
from sheet_utils import get_tasks_and_rewards, get_history, add_history_entry, remove_history_entry

st.title("🎁 Redeem Rewards")
_, rewards = get_tasks_and_rewards()
history_df = get_history()
today = str(date.today())

for reward in rewards:
    if reward["name"] == "Buy Toy":
        points = st.number_input("How many points to deduct?", step=1, min_value=1)
        if st.button("Buy Toy"):
            add_history_entry(today, "reward", "Buy Toy", -int(points))
            st.experimental_rerun()
    else:
        if st.button(f"{reward['name']} (-{reward['points']})"):
            add_history_entry(today, "reward", reward["name"], -int(reward["points"]))
            st.experimental_rerun()

# Undo 功能
st.subheader("Undo Redemption")
rewards_today = history_df[(history_df["date"] == today) & (history_df["type"] == "reward")]
for _, row in rewards_today.iterrows():
    if st.button(f"Undo {row['name']}", key=f"undo_redeem_{row['name']}"):
        remove_history_entry(today, "reward", row["name"])
        st.experimental_rerun()