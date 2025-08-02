import streamlit as st
from sheet_utils import get_tasks_and_rewards, batch_add_points, undo_last_redeem, get_total_points, safe_api_message, clear_caches
from datetime import date

st.title("Redeem Rewards")
st.markdown('<style> .stButton button {font-size:22px !important;} </style>', unsafe_allow_html=True)
def load_total_points():
    return get_total_points()

if "total_points" not in st.session_state:
    st.session_state["total_points"] = load_total_points()

try:
    st.metric("Total Points", st.session_state["total_points"])
    _, rewards = get_tasks_and_rewards()
    selected_reward = st.selectbox("Select reward to redeem:", [r["name"] for r in rewards])

    if selected_reward == "Buy Toy":
        amount = st.number_input("Enter points for Buy Toy:", min_value=1, value=10)
        points = -abs(amount)
    else:
        points = -abs(int([r["points"] for r in rewards if r["name"] == selected_reward][0]))

    if st.button("Confirm Redeem", use_container_width=True):
        to_add = [{"date": date.today().isoformat(), "type": "Reward", "name": selected_reward, "points": points}]
        batch_add_points(to_add)
        clear_caches()
        st.session_state["total_points"] = load_total_points()
        st.success(f"Redeemed: {selected_reward} ({-points} points). Total Points refreshed.")

    if st.button("Undo last redemption", use_container_width=True):
        undo_last_redeem()
        clear_caches()
        st.session_state["total_points"] = load_total_points()
        st.success("Last redeem record undone. Total Points refreshed.")
except Exception as ex:
    safe_api_message(ex)
