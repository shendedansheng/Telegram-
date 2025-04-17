import gspread
from google.oauth2.service_account import Credentials
from config import config

_client = None

def initialize_connection():
    global _client
    try:
        creds = Credentials.from_service_account_file(
            config["SERVICE_ACCOUNT_FILE"],
            scopes=[
                "https://www.googleapis.com/auth/spreadsheets",
                "https://www.googleapis.com/auth/drive"
            ]
        )
        _client = gspread.authorize(creds)
        return True
    except Exception as e:
        print(f"表格连接失败: {str(e)}")
        return False

def append_to_sheet(title: str, content: str) -> bool:
    try:
        if not _client and not initialize_connection():
            return False
        sheet = _client.open(config["SPREADSHEET_NAME"]).worksheet(config["WORKSHEET_NAME"])
        sheet.append_row([title, content], value_input_option='USER_ENTERED')
        return True
    except Exception as e:
        print(f"写入失败: {str(e)}")
        return False

def get_worksheet():
    try:
        if not _client and not initialize_connection():
            return None
        return _client.open(config["SPREADSHEET_NAME"]).worksheet(config["WORKSHEET_NAME"])
    except Exception as e:
        print(f"获取工作表失败: {str(e)}")
        return None
