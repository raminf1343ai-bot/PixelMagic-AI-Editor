import streamlit as st
from google import genai

# --- ۱. تعریف نقش (System Prompt) ---
# نقش ویرایشگر هوش مصنوعی شما:
SYSTEM_INSTRUCTION = "تو یک ویرایشگر تصویر خلاق به نام PixelMagic هستی و پیشنهادات فانتزی و هنری برای ویرایش عکس‌ها ارائه می‌دهی. لحن تو باید هیجان‌انگیز باشد."

# --- ۲. رابط کاربری (Frontend) ---
st.set_page_config(page_title="✨ PixelMagic AI Editor", layout="centered")
st.title("✨ PixelMagic AI Editor")
st.write("درخواست‌های ویرایش خود را وارد کنید تا جادوی PixelMagic را ببینید.")

# --- ۳. فراخوانی کلید امنیتی (Secrets) ---
try:
    # کد کلید API را از تنظیمات امن Streamlit می‌خواند
    API_KEY = st.secrets["GEMINI_API_KEY"]
except KeyError:
    st.error("خطا: کلید API در Streamlit Secrets تنظیم نشده است. لطفاً آن را تنظیم کنید.")
    st.stop()

client = genai.Client(api_key=API_KEY)
# --- ۴. منطق برنامه ---
user_prompt = st.text_area("چه چیزی در عکس تغییر کند؟")

if st.button("اعمال جادو", type="primary"):
    if user_prompt:
        with st.spinner('PixelMagic در حال پردازش...'):
            try:
                # فراخوانی مدل و ترکیب دستور سیستمی و ورودی کاربر
                response = client.models.generate_content(
                    model="gemini-1.5-flash", 
                    contents=[f"{SYSTEM_INSTRUCTION} - ورودی کاربر: {user_prompt}"]
                )
                st.success(f"✅ نتیجه پیشنهاد: {response.text}")
            except Exception as e:
                st.error("متاسفانه در اتصال به هوش مصنوعی مشکلی پیش آمد.")
    else:
        st.warning("لطفاً یک دستور ویرایش وارد کنید.")