import streamlit as st
from utils import load_data, save_data, get_today_date

data = load_data()
today = get_today_date()
st.title("Redeem Rewards")
st.markdown(f"### 🏆 Current Points: {data['total_points']}")

if today not in data["history"]:
    data["history"][today] = {"completed_tasks": [], "redeemed_rewards": []}

for reward in data["rewards"]:
    if reward["name"] == "买玩具":
        amount = st.number_input("Buy Toy - Enter amount to deduct", min_value=1, step=1, key="toy_amount")
        if st.button("Redeem Toy"):
            if data["total_points"] >= amount:
                data["total_points"] -= amount
                data["history"][today]["redeemed_rewards"].append({"name": "买玩具", "points": amount})
                save_data(data)
                st.success("Toy redeemed!")
    else:
        if st.button(f"Redeem {reward['name']} (-{reward['points']} pts)", key=reward["name"]):
            if data["total_points"] >= reward["points"]:
                data["total_points"] -= reward["points"]
                data["history"][today]["redeemed_rewards"].append({"name": reward["name"], "points": reward["points"]})
                save_data(data)
                st.success(f"{reward['name']} redeemed!")
            else:
                st.warning("Not enough points!")

st.subheader("Undo Redemption")
for d, record in data["history"].items():
    for idx, r in enumerate(record.get("redeemed_rewards", [])):
        label = f"{r['name']} on {d} (-{r['points']} pts)"
        if st.button(f"Undo: {label}", key=f"{d}_{idx}"):
            data["total_points"] += r["points"]
            record["redeemed_rewards"].remove(r)
            save_data(data)
            st.success(f"Undid: {label}")
            st.stop()