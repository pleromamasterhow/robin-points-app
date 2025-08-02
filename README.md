# Robin Points Tracker (Google Sheets + Streamlit)

## 📋 功能说明
- ✅ 打卡任务（每日打卡 + 补登）
- 🎁 积分兑换奖励
- 🔄 撤销错误记录
- ⚙️ 编辑任务和奖励项目

## ☁️ 部署方法

1. 将项目上传至 GitHub
2. 在 [Streamlit Cloud](https://streamlit.io/cloud) 创建新 App，连接该仓库
3. 打开 `Manage App` → 添加 `Secrets`：

```
[gcp_service_account]
type = "service_account"
project_id = "..."
private_key_id = "..."
private_key = "-----BEGIN PRIVATE KEY-----\n...\n-----END PRIVATE KEY-----\n"
client_email = "..."
client_id = "..."
...
```

4. Rerun 即可访问页面
