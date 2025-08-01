import streamlit as st
from utils import load_data, save_data

st.title("Redeem Rewards")
data = load_data()
st.subheader("Available Rewards")
for reward in data["rewards"]:
    if st.button(f'{reward["name"]} (-{reward["points"]} pts)'):
        if data["total_points"] >= reward["points"]:
            data["total_points"] -= reward["points"]
            data["history"].setdefault(reward["date"], {"completed_tasks": [], "redeemed_rewards": []})
            data["history"][reward["date"]]["redeemed_rewards"].append(reward["name"])
            save_data(data)
            st.success(f"Redeemed {reward['name']}")
        else:
            st.warning("Not enough points!")

# 撤销操作
st.subheader("Undo Redemption")
for date, record in data["history"].items():
    for reward in record.get("redeemed_rewards", []):
        if st.button(f"Undo {reward} on {date}"):
            for r in data["rewards"]:
                if r["name"] == reward:
                    data["total_points"] += r["points"]
                    data["history"][date]["redeemed_rewards"].remove(reward)
                    save_data(data)
                    st.success(f"Undid redemption: {reward} on {date}")
                    st.experimental_rerun()