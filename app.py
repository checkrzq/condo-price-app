import streamlit as st
import pandas as pd
import joblib
import os
import urllib.request

# ==========================================
# 1. CONFIGURATION & DOWNLOAD MODEL
# ==========================================
SAVE_PATH = "."  # ใช้โฟลเดอร์ปัจจุบันของเซิร์ฟเวอร์
MODEL_FILE = os.path.join(SAVE_PATH, "best_condo_model.pkl")
COLUMNS_FILE = os.path.join(SAVE_PATH, "model_columns.pkl")

# ลิงก์ Dropbox (เปลี่ยน dl=0 เป็น dl=1 แล้วเพื่อให้โหลดอัตโนมัติ)
DROPBOX_URL = "https://www.dropbox.com/scl/fi/kkkbi8pfbrm3cc1cs1wjs/best_condo_model.pkl?rlkey=wvz9rlw3w3b75ojxl1wq60i0g&st=d7jt6e0k&dl=1"

# ฟังก์ชันโหลด Assets
@st.cache_resource
def load_assets():
    model = joblib.load(MODEL_FILE)
    columns = joblib.load(COLUMNS_FILE)
    return model, columns

# ตรวจสอบว่ามีไฟล์โมเดลในเครื่อง(เซิร์ฟเวอร์)หรือยัง ถ้ายังให้ดาวน์โหลด
if not os.path.exists(MODEL_FILE):
    with st.spinner("⏳ กำลังดาวน์โหลดไฟล์โมเดล AI... (อาจใช้เวลา 1-2 นาทีสำหรับการเปิดครั้งแรก)"):
        urllib.request.urlretrieve(DROPBOX_URL, MODEL_FILE)

# โหลดโมเดลเข้าสู่ระบบ
try:
    model, expected_columns = load_assets()
    SUCCESS = True
except Exception as e:
    st.error(f"⚠️ ไม่สามารถโหลดโมเดลได้ โปรดตรวจสอบ: {e}")
    SUCCESS = False

# ==========================================
# 2. DICTIONARY สำหรับสิ่งอำนวยความสะดวก
# ==========================================
FACILITIES_MAP = {
    "สระว่ายน้ำ (Pool)": "Facility_Pool",
    "ฟิตเนส (Fitness)": "Facility_Fitness",
    "ระบบรักษาความปลอดภัย (Security)": "Facility_Security",
    "กล้องวงจรปิด (CCTV)": "Facility_CCTV",
    "ที่จอดรถ (Parking)": "Facility_Parking",
    "ลิฟต์ (Lift)": "Facility_Lift",
    "คีย์การ์ด/สแกนนิ้ว (Access Control)": "Facility_AccessControl",
    "สวนหย่อม/พื้นที่ BBQ (Park/BBQ)": "Facility_ParkBBQ",
    "อนุญาตให้เลี้ยงสัตว์ (Pet Friendly)": "Facility_PetFriendly",
    "ห้องสมุด/Co-working (Library)": "Facility_Library",
    "สนามเด็กเล่น (Kids Playground)": "Facility_KidsPlayground",
    "รถรับส่ง (Shuttle)": "Facility_Shuttle",
    "ร้านสะดวกซื้อ (Convenience Store)": "Facility_ConvenienceStore",
    "จุดชาร์จรถยนต์ไฟฟ้า (EV Charger)": "Facility_EVCharger",
    "ห้องประชุม (Meeting Room)": "Facility_MeetingRoom",
    "ซาวน่า (Sauna)": "Facility_Sauna",
    "สตรีมรูม (Steam Room)": "Facility_SteamRoom",
    "อ่างจากุซซี่ (Jacuzzi)": "Facility_Jacuzzi",
    "บริการซักรีด (Laundry)": "Facility_Laundry",
    "อินเทอร์เน็ตส่วนกลาง (WIFI)": "Facility_WIFI",
    "ร้านอาหาร (Restaurant)": "Facility_Restaurant",
    "ที่จอดรถมอเตอร์ไซค์ (Motorcycle Parking)": "Facility_MotorcycleParking"
}

# ==========================================
# 3. STREAMLIT UI
# ==========================================
st.set_page_config(page_title="Condo Price Predictor", page_icon="🏢", layout="centered")

st.title("🏢 ระบบต้นแบบทำนายราคาคอนโดมิเนียม")
st.write("กรอกข้อมูลรายละเอียดคอนโดเพื่อประเมินราคาต่อตารางเมตร")

if SUCCESS:
    with st.form("prediction_form"):
        st.subheader("📋 ข้อมูลคุณลักษณะของห้อง")
        
        col1, col2 = st.columns(2)
        
        with col1:
            area = st.number_input("ขนาดพื้นที่ (ตร.ม.)", min_value=10.0, max_value=500.0, value=35.0, step=1.0)
            floor = st.number_input("ชั้นที่อยู่ (Floor)", min_value=1, max_value=100, value=5, step=1)
            bedrooms = st.number_input("จำนวนห้องนอน", min_value=0, max_value=10, value=1, step=1)
            bathrooms = st.number_input("จำนวนห้องน้ำ", min_value=1, max_value=10, value=1, step=1)
            
        with col2:
            district = st.text_input("ทำเล/เขต (เช่น Huai Khwang, Sukhumvit)", value="Huai Khwang")
            station_dist = st.number_input("ระยะห่างจากรถไฟฟ้า (กม.)", min_value=0.0, max_value=20.0, value=1.2, step=0.1)
            
        st.markdown("---")
        st.markdown("**🛋️ สิ่งอำนวยความสะดวกพื้นฐานส่วนกลาง (Facilities)**")
        
        selected_facilities = st.multiselect(
            "เลือกสิ่งอำนวยความสะดวกที่มีในโครงการ:",
            options=list(FACILITIES_MAP.keys()),
            default=["สระว่ายน้ำ (Pool)", "ฟิตเนส (Fitness)", "ระบบรักษาความปลอดภัย (Security)", "กล้องวงจรปิด (CCTV)", "ที่จอดรถ (Parking)", "ลิฟต์ (Lift)"]
        )

        submit_btn = st.form_submit_button("🔍 ทำนายราคา")

    # ==========================================
    # 4. PREDICTION
    # ==========================================
    if submit_btn:
        with st.spinner("กำลังประมวลผล..."):
            
            input_dict = {col: 0 for col in expected_columns}
            
            if "Area" in expected_columns: input_dict["Area"] = area
            if "Cleaned_Floor" in expected_columns: input_dict["Cleaned_Floor"] = floor
            if "Cleaned_Bedrooms" in expected_columns: input_dict["Cleaned_Bedrooms"] = bedrooms
            if "Cleaned_Bathrooms" in expected_columns: input_dict["Cleaned_Bathrooms"] = bathrooms
            if "Cleaned_District" in expected_columns: input_dict["Cleaned_District"] = district
            if "Avg_Distance_km_BTS/MRT" in expected_columns: input_dict["Avg_Distance_km_BTS/MRT"] = station_dist
            
            for fac_name in selected_facilities:
                col_name = FACILITIES_MAP[fac_name]
                if col_name in expected_columns:
                    input_dict[col_name] = 1

            input_data = pd.DataFrame([input_dict])

            input_data["Floor_Category"] = pd.cut([floor], bins=[0, 10, 20, 100], labels=["Low", "Mid", "High"])[0]
            input_data["Size_Category"] = pd.cut([area], bins=[0, 30, 60, 200], labels=["Small", "Medium", "Large"])[0]

            input_data = input_data[expected_columns]

            try:
                prediction_sqm = model.predict(input_data)[0]
                total_price = prediction_sqm * area
                
                st.success("🎉 **ประเมินราคาเสร็จสมบูรณ์!**")
                col_res1, col_res2 = st.columns(2)
                col_res1.metric(label="ราคาต่อตารางเมตร (ประเมิน)", value=f"{prediction_sqm:,.2f} ฿")
                col_res2.metric(label="ราคารวมโดยประมาณ (ประเมิน)", value=f"{total_price:,.2f} ฿")
            except Exception as e:
                st.error(f"❌ เกิดข้อผิดพลาดในการทำนาย: {e}")

st.markdown("---")
st.caption("พัฒนาขึ้นเพื่อการวิจัยการทำนายราคาคอนโดมิเนียมด้วยโมเดล Machine Learning")