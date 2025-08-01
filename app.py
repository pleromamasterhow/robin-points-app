
import streamlit as st
import json
import os
from datetime import date

# --------------------------
# 配置：初始密码
# --------------------------
PASSWORD = "robin"

# --------------------------
# 密码验证功能
# --------------------------
def check_password():
    def password_entered():
        if st.session_state["password"] == PASSWORD:
            st.session_state["password_correct"] = True
            del st.session_state["password"]
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        st.text_input("请输入密码进入 Robin 的打卡系统：", type="password", on_change=password_entered, key="password")
        st.stop()
    elif not st.session_state["password_correct"]:
        st.error("密码错误，请重试")
        st.text_input("请输入密码进入 Robin 的打卡系统：", type="password", on_change=password_entered, key="password")
        st.stop()

# --------------------------
# 数据加载和保存函数
# --------------------------
DATA_FILE = "data.json"

def load_data():
    if not os.path.exists(DATA_FILE):
        return {"total_points": 0, "tasks": [], "history": []}
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# --------------------------
# 主程序入口
# --------------------------
check_password()
st.title("🎯 Robin 的每日打卡积分系统")

data = load_data()
today = date.today().isoformat()

# --------------------------
# 显示当前总积分
# --------------------------
st.markdown(f"### 🧮 当前积分：{data['total_points']} 分")

# --------------------------
# 显示并打卡任务
# --------------------------
st.markdown("## ✅ 今天的任务打卡")
completed = []
for task in data["tasks"]:
    if st.checkbox(f"{task['name']}（{task['points']} 分）", key=task['name'] + today):
        completed.append(task)

if st.button("🎉 提交今日打卡"):
    already_checked = any(h["date"] == today for h in data["history"])
    if already_checked:
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
        st.success(f"今日打卡成功！获得 {earned} 分")

# --------------------------
# 编辑任务和分数
# --------------------------
st.markdown("---")
st.markdown("## 🛠️ 编辑任务与分数")

edited_tasks = []
for i, task in enumerate(data["tasks"]):
    col1, col2 = st.columns([3, 1])
    name = col1.text_input(f"任务名称 {i+1}", value=task["name"], key=f"name_{i}")
    points = col2.number_input("积分", value=task["points"], min_value=1, step=1, key=f"points_{i}")
    edited_tasks.append({"name": name, "points": points})

if st.button("💾 保存任务设置"):
    data["tasks"] = edited_tasks
    save_data(data)
    st.success("任务已更新！")

# --------------------------
# 显示历史记录
# --------------------------
st.markdown("---")
st.markdown("## 📅 打卡历史")
for record in reversed(data["history"][-7:]):
    st.markdown(f"- {record['date']}：{', '.join(record['completed'])}，+{record['points']}分")
