
import streamlit as st
import json
import os
from datetime import date, datetime
import pandas as pd

DATA_FILE = "data.json"

def load_data():
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

st.set_page_config(page_title="📅 补录打卡", page_icon="📅")
st.title("📅 补录打卡记录")

data = load_data()

# 日期选择器
selected_date = st.date_input("选择一个日期补录任务/奖励", value=date.today(), max_value=date.today())
selected_date_str = selected_date.isoformat()

# 展示历史记录
st.markdown("### 📖 该日已有打卡记录")
existing = next((h for h in data["history"] if h["date"] == selected_date_str), None)
if existing:
    st.info(f"{selected_date_str} 已完成任务：{', '.join(existing['completed'])}，获得积分：{existing['points']} 分")
else:
    st.warning(f"{selected_date_str} 尚无任务记录")

st.markdown("---")
st.markdown("### ✅ 选择补录任务")
selected_tasks = []
for task in data["tasks"]:
    if st.checkbox(f"{task['name']}（{task['points']} 分）", key=task["name"] + selected_date_str):
        selected_tasks.append(task)

st.markdown("### 🎁 补录奖励领取")
reward_options = [r["name"] for r in data["rewards"]]
selected_reward = st.selectbox("选择奖励", options=["无"] + reward_options)
reward_points = 0

if selected_reward == "买玩具":
    amount = st.number_input("花费金额（$）", min_value=0, step=1, value=0)
    reward_points = amount
elif selected_reward != "无":
    reward_obj = next((r for r in data["rewards"] if r["name"] == selected_reward), None)
    if reward_obj:
        reward_points = reward_obj["points"]

if st.button("💾 保存补录信息"):
    # 积分计算
    task_points = sum(t["points"] for t in selected_tasks)
    total_earned = task_points
    total_spent = reward_points

    # 更新打卡记录
    existing_idx = next((i for i, h in enumerate(data["history"]) if h["date"] == selected_date_str), None)
    if existing_idx is not None:
        data["history"][existing_idx] = {
            "date": selected_date_str,
            "completed": [t["name"] for t in selected_tasks],
            "points": task_points
        }
    else:
        data["history"].append({
            "date": selected_date_str,
            "completed": [t["name"] for t in selected_tasks],
            "points": task_points
        })

    # 更新奖励记录
    if selected_reward != "无":
        data["redeemed"].append({
            "date": selected_date_str,
            "reward": selected_reward,
            "points": reward_points
        })

    # 更新积分
    if selected_date == date.today():
        data["total_points"] += task_points
        data["total_points"] -= reward_points

    save_data(data)
    st.success(f"保存成功！获得 {task_points} 分，兑换 {reward_points} 分，净增 {task_points - reward_points} 分")
