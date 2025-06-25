import streamlit as st
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials

st.set_page_config(page_title="📗 Google Sheets Demo", layout="centered")

st.title("📗 Streamlit + Google Sheets")
st.write("本應用示範如何使用服務帳戶連接 Google Sheets 並讀取資料。")

# ========================
# Google Sheets 認證設定
# ========================
scope = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]
creds_dict = st.secrets["gcp_service_account"]

# 使用金鑰授權
creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
client = gspread.authorize(creds)

# ========================
# Google Sheet 讀取與顯示
# ========================

# 將此處換成你實際要讀取的試算表名稱
SHEET_NAME = "ys-map"
WORKSHEET_INDEX = 0  # 預設第一個工作表

try:
    sheet = client.open(SHEET_NAME).get_worksheet(WORKSHEET_INDEX)
    data = sheet.get_all_records()
    df = pd.DataFrame(data)

    st.success("✅ 成功連接並讀取 Google Sheets 資料")
    st.dataframe(df)

except Exception as e:
    st.error("❌ 讀取 Google Sheets 時發生錯誤：")
    st.exception(e)
