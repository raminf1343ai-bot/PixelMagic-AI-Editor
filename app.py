# -*- coding: utf-8 -*-

import streamlit as st
from google import genai
# ... بقیه کد ...
import streamlit as st
from google import genai
from PIL import Image # نیاز به این کتابخانه برای پردازش تصویر

# --- ۱. تعریف نقش (System Prompt) ---
SYSTEM_INSTRUCTION = "SYSTEM_INSTRUCTION = "You are PixelMagic AI editor, giving artistic suggestions." 
st.set_page_config(page_title="✨ PixelMagic AI Editor", layout="centered")
st.title("✨ PixelMagic AI Editor")

# فراخوانی کلید امنیتی
try:
    API_KEY = st.secrets["GEMINI_API_KEY"]
except KeyError:
    st.error("خطا: کلید API در Streamlit Secrets تنظیم نشده است.")
    st.stop()

client = genai.Client(api_key=API_KEY)

# --- ۳. کامپوننت آپلود عکس ---
uploaded_file = st.file_uploader(
    "یک عکس برای اعمال جادو آپلود کنید 🪄", 
    type=["png", "jpg", "jpeg"]
)

# --- ۴. دریافت دستور ویرایش ---
user_prompt = st.text_area(
    "دستور ویرایش خود را وارد کنید (مثلاً: آن را به سبک نقاشی ون گوگ در بیاورید).", 
    placeholder="چه چیزی در عکس تغییر کند؟"
)

# --- ۵. منطق پردازش (Multimodal) ---
if st.button("اعمال جادو", type="primary"):
    if uploaded_file is None:
        st.warning("لطفاً ابتدا یک فایل عکس آپلود کنید.")
    elif not user_prompt:
        st.warning("لطفاً دستور ویرایش خود را وارد کنید.")
    else:
        # ساخت محتوای چندوجهی (عکس + متن)
        try:
            # الف) باز کردن تصویر
            image = Image.open(uploaded_file)
            st.image(image, caption='عکس آپلود شده', use_column_width=True)
            
            # ب) ساخت لیست محتوا برای Gemini (ترکیب تصویر و متن)
            contents = [
                f"دستور سیستمی: {SYSTEM_INSTRUCTION}",
                image, # تصویر
                f"دستور کاربر: {user_prompt}" # متن
            ]

            with st.spinner('PixelMagic در حال پردازش...'):
                # فراخوانی مدل (Multimodal Call)
                response = client.models.generate_content(
                    model="gemini-1.5-flash", 
                    contents=contents 
                )
                
                st.success(f"✅ پیشنهاد نهایی: {response.text}")

        except Exception as e:
            st.error(f"متاسفانه خطایی رخ داد: {e}")


