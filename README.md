# Telegram 智能问答机器人

本项目是一个基于 Telegram 的智能问答机器人，支持问题搜索、记录和管理功能，并通过 Google Sheets 作为知识库进行存储和查询。

## 功能特性

- **搜索功能**：用户可以输入问题，机器人通过 Google Sheets 查询知识库并返回匹配答案。
- **记录功能**：支持用户将问题和答案记录到知识库。
- **删除功能**：用户可以通过指定序号删除特定的记录。
- **底部菜单支持**：通过 Telegram 的自定义键盘，用户可快速选择功能。
- **可扩展性**：代码结构清晰，便于二次开发和功能扩展。

## 系统要求

- Python 3.8 或更高版本
- Telegram Bot Token （需要在 Telegram 上创建机器人以获取）
- Google Service Account 配置文件 (`.json`)
- 必要的 Python 库：
  - `python-telegram-bot`
  - `gspread`
  - `google-auth`
  - `rapidfuzz`
  - `pystray`
  - `Pillow`
  - `python-dotenv`

## 环境变量配置

项目使用 `.env` 文件管理配置。以下是需要配置的环境变量：

```
TG_BOT_TOKEN=<您的Telegram机器人Token>
SERVICE_ACCOUNT_FILE=./path/to/google-service-account.json
SPREADSHEET_NAME=知识库表格名称
WORKSHEET_NAME=工作表名称
MIN_MATCH_RATIO=0.8
```

## 安装与运行

### 1. 克隆项目

```bash
git clone https://github.com/shendedansheng/Telegram-.git
cd Telegram-
```

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

### 3. 配置环境文件

在项目根目录创建 `.env` 文件，并按照上述格式填写内容。

### 4. 运行机器人

```bash
python main.py
```

## 文件结构

```
Telegram-
├── bot_handlers.py       # 机器人核心逻辑
├── config.py             # 配置信息加载
├── google_sheets.py      # Google Sheets 操作封装
├── tray.py               # 系统托盘管理脚本
├── utils.py              # 工具函数
├── main.py               # 主入口
└── requirements.txt      # 项目依赖
```

## 使用说明

- 启动机器人后，用户可在 Telegram 中与机器人进行交互。
- 使用 `/start` 命令查看欢迎信息。
- 通过自定义键盘选择功能：
  - 🔍 搜索：输入问题，查询知识库。
  - 📝 记录：输入标题和内容，添加到知识库。
  - ➕ 添加：功能未启用。

## 贡献指南

欢迎对本项目提出意见和建议，贡献方式如下：

1. 提交 Issue 描述问题或建议。
2. Fork 本仓库，提交您的修改并发起 Pull Request。

## 许可证

本项目基于 MIT 许可证开源。

---

感谢您使用 Telegram 智能问答机器人！若有任何问题，请与我联系。
