import streamlit as st
from streamlit_gsheets import GSheetsConnection

st.set_page_config(page_title="📗 Google Sheets 連結示範", layout="centered")
st.title("📗 使用公開 Google Sheets 與 Streamlit 整合")

# 替換為你的 Google Sheet 公開網址
url = "https://docs.google.com/spreadsheets/d/1VV2AXV7-ZudWApvRiuKW8gcehXOM1CaPXGyHyFvDPQE/edit?usp=sharing"

st.header("1️⃣ 讀取公開 Google Sheet 為 DataFrame")

with st.echo():
    conn = st.connection("gsheets", type=GSheetsConnection)
    df = conn.read(spreadsheet=url, usecols=[0, 1])
    st.dataframe(df)

st.divider()
st.header("2️⃣ 使用 SQL 查詢 Google Sheet")
st.info("⚠️ 注意：SQL 查詢僅於記憶體內執行，不會影響實際 Google Sheet 資料", icon="ℹ️")

with st.echo():
    # Query 範例，請注意工作表名稱（例如 "Example 2"）
    df_sql = conn.query(
        'SELECT births FROM "sheet1" LIMIT 10',
        spreadsheet=url
    )
    st.dataframe(df_sql)
