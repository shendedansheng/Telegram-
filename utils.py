import html
from rapidfuzz import process, fuzz

def find_matching_rows(worksheet, question: str, min_match_ratio: float):
    """
    遍历“问题关键词”列，返回所有能匹配到的行号及具体匹配到的关键词：
    返回值：[(row_num1, keyword1), (row_num2, keyword2), ...]
    """
    try:
        # 缓存关键词列表：[(row_num, [kw1, kw2, ...]), …]
        if not hasattr(worksheet, '_cached_keywords'):
            records = worksheet.get_all_records()
            worksheet._cached_keywords = [
                (idx + 2, [
                    k.strip().lower()
                    for k in str(row.get("问题关键词", "")).split("/")
                    if k.strip()
                ])
                for idx, row in enumerate(records)
            ]

        clean_question = question.strip().lower()
        matches = []

        # 1. 精确匹配
        for row_num, keywords in worksheet._cached_keywords:
            for kw in keywords:
                if clean_question == kw:
                    matches.append((row_num, kw))

        # 2. 如果没有精确匹配，再做模糊匹配
        if not matches:
            cutoff = int(min_match_ratio * 100)
            for row_num, keywords in worksheet._cached_keywords:
                result = process.extractOne(
                    clean_question,
                    keywords,
                    scorer=fuzz.WRatio,
                    score_cutoff=cutoff
                )
                if result:
                    matches.append((row_num, result[0]))  # result[0] 是匹配到的关键词

        return matches

    except Exception as e:
        print(f"查找匹配行时出错: {e}")
        return []

def format_answer(answer: str) -> str:
    """
    将多行答案每行用 <code>…</code> 包裹，并对内容做 HTML 转义；
    空行输出一个空格，避免被忽略。
    """
    if not answer:
        return "<code>答案待补充</code>"

    lines = answer.split("\n")
    wrapped = []
    for line in lines:
        text = line if line.strip() else " "
        wrapped.append(f"<code>{html.escape(text)}</code>")
    return "\n".join(wrapped)
