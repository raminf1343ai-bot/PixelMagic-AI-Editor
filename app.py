# -*- coding: utf-8 -*-
# Adding the encoding hint just in case

import streamlit as st
from google import genai
from PIL import Image

# --- 1. System Prompt (English) ---
SYSTEM_INSTRUCTION = "You are PixelMagic AI editor, giving creative and artistic image editing suggestions based on the user's uploaded photo and request."

# --- 2. Frontend & Key Setup ---
st.set_page_config(page_title="✨ PixelMagic AI Editor", layout="centered")
st.title("✨ PixelMagic AI Editor")

# API Key Check (The key is safe in Secrets)
try:
    API_KEY = st.secrets["GEMINI_API_KEY"]
except KeyError:
    st.error("Error: API Key not configured in Streamlit Secrets.")
    st.stop()

client = genai.Client(api_key=API_KEY)

# --- 3. File Uploader Component ---
uploaded_file = st.file_uploader(
    "Upload a photo for editing 🪄", 
    type=["png", "jpg", "jpeg"]
)

# --- 4. Get Edit Command ---
user_prompt = st.text_area(
    "Enter your editing command (e.g., 'Make it look like a Van Gogh painting').", 
    placeholder="What should change in the image?"
)

# --- 5. Processing Logic ---
if st.button("Apply Magic", type="primary"):
    if uploaded_file is None:
        st.warning("Please upload a photo first.")
    elif not user_prompt:
        st.warning("Please enter your editing command.")
    else:
        try:
            image = Image.open(uploaded_file)
            st.image(image, caption='Uploaded Photo', use_column_width=True)
            
            contents = [
                f"System Instruction: {SYSTEM_INSTRUCTION}",
                image,
                f"User Command: {user_prompt}"
            ]

            with st.spinner('PixelMagic Processing...'):
                response = client.models.generate_content(
                    model="gemini-1.5-flash", 
                    contents=contents 
                )
                
                st.success(f"✅ Final Suggestion: {response.text}")

        except Exception as e:
            st.error(f"An error occurred: {e}")
