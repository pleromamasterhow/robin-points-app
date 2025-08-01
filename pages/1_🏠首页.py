
import streamlit as st
import json
import os
from datetime import date

DATA_FILE = "data.json"

def load_data():
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

st.set_page_config(page_title="🏠 首页", page_icon="🏠")
st.title("🏠 今天的任务打卡")

data = load_data()
today = date.today().isoformat()

st.markdown(f"### 🧮 当前积分：{data['total_points']} 分")

# 今日任务打卡
st.markdown("## ✅ 勾选今天完成的任务")
completed = []
for task in data["tasks"]:
    if st.checkbox(f"{task['name']}（{task['points']} 分）", key=task['name'] + today):
        completed.append(task)

if st.button("🎉 提交今日打卡"):
    already = any(h["date"] == today for h in data["history"])
    if already:
        st.warning("今天已经打过卡了哦！")
    else:
        earned = sum(t["points"] for t in completed)
        data["total_points"] += earned
        data["history"].append({
            "date": today,
            "completed": [t["name"] for t in completed],
            "points": earned
        })
        save_data(data)
        st.success(f"成功打卡！获得 {earned} 分")

# 历史记录展示
st.markdown("---")
st.markdown("### 📅 最近打卡记录")
for r in reversed(data["history"][-7:]):
    st.markdown(f"- {r['date']}：完成 {', '.join(r['completed'])}，+{r['points']} 分")

st.markdown("### 🎁 最近奖励记录")
for r in reversed(data["redeemed"][-7:]):
    st.markdown(f"- {r['date']}：兑换 {r['reward']}，-{r['points']} 分")
