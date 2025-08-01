
import streamlit as st
import json

DATA_FILE = "data.json"

def load_data():
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

st.set_page_config(page_title="🎁 奖励兑换", page_icon="🎁")
st.title("🎁 使用积分兑换奖励")

data = load_data()
st.markdown(f"当前积分：**{data['total_points']} 分**")

reward_options = [r["name"] for r in data["rewards"]]
selected = st.selectbox("选择要兑换的奖励", options=reward_options)

points_needed = 0
if selected == "买玩具":
    amount = st.number_input("输入购买金额（$）：", min_value=0, value=0, step=1)
    points_needed = amount
else:
    reward = next((r for r in data["rewards"] if r["name"] == selected), None)
    if reward:
        points_needed = reward["points"]

if st.button("💥 兑换"):
    if data["total_points"] < points_needed:
        st.error("积分不足，无法兑换")
    else:
        data["total_points"] -= points_needed
        data["redeemed"].append({
            "date": date.today().isoformat(),
            "reward": selected,
            "points": points_needed
        })
        save_data(data)
        st.success(f"已成功兑换「{selected}」，扣除 {points_needed} 分")
