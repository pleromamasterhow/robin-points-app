import streamlit as st
from utils import load_data, save_data, get_today_date

data = load_data()
today = get_today_date()
if "total_points" not in st.session_state:
    st.session_state["total_points"] = data["total_points"]
if "history" not in st.session_state:
    st.session_state["history"] = data["history"]

st.title("Redeem Rewards")
st.markdown(f"### 🏆 Total Points: {st.session_state.total_points}")

if today not in st.session_state["history"]:
    st.session_state["history"][today] = {"completed_tasks": [], "redeemed_rewards": []}

st.subheader("Available Rewards")
for reward in data["rewards"]:
    if reward["name"] == "Buy Toy":
        amount = st.number_input("Buy Toy - Enter points to deduct", min_value=1, step=1, key="toy_amount")
        if st.button("Redeem Toy"):
            if st.session_state["total_points"] >= amount:
                st.session_state["total_points"] -= amount
                st.session_state["history"][today]["redeemed_rewards"].append({"name": "Buy Toy", "points": amount})
                data["total_points"] = st.session_state["total_points"]
                data["history"] = st.session_state["history"]
                save_data(data)
                st.success("Toy redeemed!")
                st.rerun()
            else:
                st.warning("Not enough points.")
    else:
        if st.button(f"Redeem {reward['name']} (-{reward['points']} pts)", key=reward["name"]):
            if st.session_state["total_points"] >= reward["points"]:
                st.session_state["total_points"] -= reward["points"]
                st.session_state["history"][today]["redeemed_rewards"].append({"name": reward["name"], "points": reward["points"]})
                data["total_points"] = st.session_state["total_points"]
                data["history"] = st.session_state["history"]
                save_data(data)
                st.success(f"{reward['name']} redeemed!")
                st.rerun()
            else:
                st.warning("Not enough points.")

st.subheader("Undo Redemption")
for d, record in st.session_state["history"].items():
    for idx, r in enumerate(record.get("redeemed_rewards", [])):
        label = f"{r['name']} on {d} (-{r['points']} pts)"
        if st.button(f"Undo: {label}", key=f"undo_{d}_{idx}"):
            st.session_state["total_points"] += r["points"]
            record["redeemed_rewards"].remove(r)
            data["total_points"] = st.session_state["total_points"]
            data["history"] = st.session_state["history"]
            save_data(data)
            st.success(f"Undid: {label}")
            st.rerun()