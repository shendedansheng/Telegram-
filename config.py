import os
from dotenv import load_dotenv

def load_config(env_file=".env"):
    # 获取当前脚本所在的目录
    base_dir = os.path.dirname(os.path.abspath(__file__))
    # 构建 .env 文件的完整路径
    env_path = os.path.join(base_dir, env_file)
    
    # 加载 .env 文件中的环境变量
    load_dotenv(env_path)
    
    # 从环境变量中获取配置信息
    TG_BOT_TOKEN = os.getenv("TG_BOT_TOKEN")
    if not TG_BOT_TOKEN:
        raise ValueError("TG_BOT_TOKEN 未在 .env 文件中找到")
    
    # 获取 SERVICE_ACCOUNT_FILE 的路径
    # 如果 .env 文件中未指定路径，则使用默认路径
    SERVICE_ACCOUNT_FILE = os.getenv("SERVICE_ACCOUNT_FILE", os.path.join(base_dir, "wendaxitong-a187b479fa71.json"))
    
    # 获取其他配置信息
    SPREADSHEET_NAME = os.getenv("SPREADSHEET_NAME", "第二个你系统")
    WORKSHEET_NAME = os.getenv("WORKSHEET_NAME", "KnowledgeBase")
    MIN_MATCH_RATIO = float(os.getenv("MIN_MATCH_RATIO", 0.8))
    
    # 返回配置字典
    return {
        "TG_BOT_TOKEN": TG_BOT_TOKEN,
        "SERVICE_ACCOUNT_FILE": SERVICE_ACCOUNT_FILE,
        "SPREADSHEET_NAME": SPREADSHEET_NAME,
        "WORKSHEET_NAME": WORKSHEET_NAME,
        "MIN_MATCH_RATIO": MIN_MATCH_RATIO
    }

# 加载配置
config = load_config()

# 调试输出（可选）
for key, value in config.items():
    print(f"{key}: {value}")
