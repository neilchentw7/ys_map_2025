import streamlit as st
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials

st.set_page_config(page_title="📗 Google Sheets 工地地圖", layout="centered")
st.title("📍 工地資訊地圖")
st.write("使用 Google Sheets 建立聯絡人與導航平台")

# ========================
# Google Sheets 認證設定
# ========================
scope = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]
creds_dict = st.secrets["gcp_service_account"]
creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
client = gspread.authorize(creds)

# ========================
# Google Sheet 讀取與顯示
# ========================
SHEET_NAME = "ys-map"
WORKSHEET_INDEX = 0

try:
    sheet = client.open(SHEET_NAME).get_worksheet(WORKSHEET_INDEX)
    data = sheet.get_all_records()
    df = pd.DataFrame(data)

    st.success("✅ 成功讀取 Google Sheets 資料")
    
    # 顯示每筆工地資料為卡片
    for _, row in df.iterrows():
        st.markdown("---")
        st.markdown(f"### 📍 {row.get('工地名稱', '').strip()}")
        
        if row.get("地址"):
            st.markdown(f"📌 **地址：** {row['地址']}")
        
        if row.get("GoogleMap網址"):
            st.markdown(
                f"<a href='{row['GoogleMap網址']}' target='_blank'>🗺️ 點我導航</a>",
                unsafe_allow_html=True
            )
        
        if row.get("工地主任"):
            st.markdown(f"👷 **主任：** {row['工地主任']}")
        
        if row.get("聯絡電話"):
            tel = str(row['聯絡電話']).replace(" ", "")
            st.markdown(f"📞 **電話：** [{row['聯絡電話']}](tel:{tel})")

    # 顯示原始表格
    with st.expander("📄 檢視原始表格"):
        st.dataframe(df)

except Exception as e:
    st.error("❌ 讀取 Google Sheets 時發生錯誤：")
    st.exception(e)
