# 量子隧穿效应可视化平台

## Streamlit Community Cloud 部署

1. 在 GitHub 新建一个仓库。
2. 上传本目录内全部文件，保持以下结构：

```text
app.py
requirements.txt
.streamlit/config.toml
```

3. 登录 Streamlit Community Cloud，并连接 GitHub。
4. 点击 **Create app**。
5. 选择刚创建的仓库、分支 `main`、入口文件 `app.py`。
6. 点击 **Deploy**。

部署完成后会生成一个可公开访问的网址，格式通常类似：

```text
https://你的应用名称.streamlit.app
```

## 可选 AI API

不开启“AI 助教使用真实 API”时，应用可直接运行。

如需启用真实 API，请在 Streamlit Community Cloud 的应用设置中添加 Secrets，
再通过环境变量或相应配置方式提供：

- `OPENAI_API_BASE`
- `OPENAI_API_KEY`
- `OPENAI_MODEL`
