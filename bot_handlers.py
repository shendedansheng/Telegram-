import re
import html
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import ContextTypes
from config import config
from utils import find_matching_rows, format_answer
import google_sheets

# 底部菜单按钮
reply_keyboard = [
    [KeyboardButton("🔍 搜索"), KeyboardButton("📝 记录")],
    [KeyboardButton("➕ 添加")]
]
reply_markup = ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("欢迎使用智能问答系统", reply_markup=reply_markup)
    context.user_data["state"] = "search"

async def handle_search(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("请输入您的问题，我将为您搜索答案。")
    context.user_data["state"] = "search"

async def handle_record(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "请输入您要记录的文本，格式：\n"
        "第一行为标题\n第二行起为内容"
    )
    context.user_data["state"] = "record"

async def handle_add(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("新功能尚未启用，请稍后再试")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        user_input = update.message.text.strip()
        state = context.user_data.get("state", "search")

        # —— 删除命令 —— #
        # 格式：删除📖 回答：N
        del_match = re.match(r"^删除📖 回答：(\d+)$", user_input)
        if state == "search" and del_match:
            idx = int(del_match.group(1)) - 1
            last = context.user_data.get("last_matches", [])
            if not last:
                await update.message.reply_text("❌ 没有可删除的记录，请先查询后再删除。")
                return
            if idx < 0 or idx >= len(last):
                await update.message.reply_text("❌ 序号超出范围，请输入有效序号。")
                return

            row_num = last[idx]
            ws = google_sheets.get_worksheet()
            if not ws:
                await update.message.reply_text("⚠️ 表格服务异常，无法删除。")
                return

            try:
                # 使用 delete_rows 而非 delete_row
                ws.delete_rows(row_num)
                # 删除后清除关键词缓存
                if hasattr(ws, "_cached_keywords"):
                    del ws._cached_keywords

                # 更新 last_matches 列表
                last.pop(idx)
                context.user_data["last_matches"] = last

                await update.message.reply_text(f"✅ 已删除 第 {idx+1} 条（表格行 {row_num}）")
            except Exception as e:
                print(f"删除行时出错: {e}")
                await update.message.reply_text("⚠️ 删除失败，请稍后重试。")
            return

        # —— 搜索模式 —— #
        if state == "search":
            ws = google_sheets.get_worksheet()
            if not ws:
                await update.message.reply_text("⚠️ 表格服务异常")
                return

            matches = find_matching_rows(ws, user_input, config["MIN_MATCH_RATIO"])
            if not matches:
                await update.message.reply_text("❌ 无相关数据")
            else:
                parts = []
                for i, (row_num, kw) in enumerate(matches, start=1):
                    answer = ws.cell(row_num, 2).value or ""
                    esc_kw = html.escape(kw)
                    parts.append(
                        f"📖 回答：{i}（关键词：<code>{esc_kw}</code>）\n"
                        f"{format_answer(answer)}"
                    )
                # 保存行号列表，供删除命令使用
                context.user_data["last_matches"] = [row for row, _ in matches]

                await update.message.reply_text(
                    "\n\n".join(parts),
                    parse_mode="HTML"
                )

            context.user_data["state"] = "search"
            return

        # —— 记录模式 —— #
        if state == "record":
            lines = user_input.split("\n", 1)
            title = lines[0].strip()
            content = lines[1].strip() if len(lines) > 1 else ""
            success = google_sheets.append_to_sheet(title, content)
            await update.message.reply_text("📝 已记录到知识库" if success else "⚠️ 记录失败")
            context.user_data["state"] = "search"
            return

        # 未知状态
        await update.message.reply_text("未知命令，请使用 /start 或点击菜单按钮")

    except Exception as e:
        print(f"处理消息时出错: {e}")
        await update.message.reply_text("⚠️ 系统繁忙，请稍后再试")
