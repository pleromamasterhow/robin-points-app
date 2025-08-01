
import streamlit as st
import json

DATA_FILE = "data.json"

def load_data():
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

st.set_page_config(page_title="⚙️ 设置中心", page_icon="⚙️")
st.title("⚙️ 设置任务与奖励")

data = load_data()

st.markdown("### ✅ 任务设置")
edited_tasks = []
for i, task in enumerate(data["tasks"]):
    col1, col2 = st.columns([3, 1])
    name = col1.text_input(f"任务名称 {i+1}", value=task["name"], key=f"name_{i}")
    points = col2.number_input("分数", value=task["points"], min_value=1, key=f"points_{i}")
    edited_tasks.append({"name": name, "points": points})

if st.button("保存任务设置"):
    data["tasks"] = edited_tasks
    save_data(data)
    st.success("任务已更新！")

st.markdown("### 🎁 奖励设置")
edited_rewards = []
for i, reward in enumerate(data["rewards"]):
    if reward["name"] == "买玩具":
        st.info("买玩具为特殊奖励，按金额扣分")
        edited_rewards.append({"name": "买玩具", "points_per_dollar": 1})
        continue
    col1, col2 = st.columns([3, 1])
    name = col1.text_input(f"奖励名称 {i+1}", value=reward["name"], key=f"r_name_{i}")
    points = col2.number_input("分数", value=reward["points"], min_value=1, key=f"r_points_{i}")
    edited_rewards.append({"name": name, "points": points})

if st.button("保存奖励设置"):
    data["rewards"] = edited_rewards
    save_data(data)
    st.success("奖励已更新！")
