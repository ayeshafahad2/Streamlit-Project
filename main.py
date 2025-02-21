import streamlit as st
import pandas as pd
import os
from PIL import Image  # For resizing images
import time

# File to store data
DATA_FILE = "loved_ones.csv"
IMAGE_FOLDER = "images"  # Folder to save uploaded images

# Ensure image folder exists
if not os.path.exists(IMAGE_FOLDER):
    os.makedirs(IMAGE_FOLDER)

# Function to load data
def load_data():
    if os.path.exists(DATA_FILE):
        try:
            df = pd.read_csv(DATA_FILE, dtype=str)  # Read all as strings
            return df
        except pd.errors.ParserError:
            st.error("❌ Error loading CSV file. The file might be corrupted. Try deleting and regenerating it.")
            return pd.DataFrame(columns=["Name", "Birthdate", "Special Date", "Image"])
    else:
        return pd.DataFrame(columns=["Name", "Birthdate", "Special Date", "Image"])

# Function to save data
def save_data(df):
    df.to_csv(DATA_FILE, index=False)

# Load existing data
df = load_data()

# Apply custom background
page_bg = """
    <style>
    body {
        background-image: url("/images/design.jpeg");
        background-size: cover;
        background-attachment: fixed;
    }
    .sidebar .sidebar-content {
        background: #FFDEE9; /* Light pink gradient */
        padding: 20px;
    }
    .stTextInput, .stButton, .stFileUploader {
        border-radius: 10px;
    }
    .stButton>button {
        background: #ff4b4b; /* Red button */
        color: white;
        font-size: 18px;
        border-radius: 10px;
        padding: 10px;
    }
    </style>
"""
st.markdown(page_bg, unsafe_allow_html=True)

# Streamlit UI
st.title("🎉 Loved Ones' Special Dates Tracker")
st.sidebar.header("💖 Add a Loved One")

# Input fields
name = st.sidebar.text_input("📌 Name")
currentdate = st.sidebar.text_input("📆 Current Date (YYYY-MM-DD)")
special_date = st.sidebar.text_input("🎊 Special Date (YYYY-MM-DD)")
image = st.sidebar.file_uploader("📷 Upload Image", type=["jpg", "png","webp"])

# Save the record
if st.sidebar.button("Save"):
    if name and currentdate and special_date:  # Ensure required fields are filled
        image_filename = ""
        if image:
            image_filename = os.path.join(IMAGE_FOLDER, image.name)
            with open(image_filename, "wb") as f:
                f.write(image.read())  # Save image file

        new_data = pd.DataFrame({
            "Name": [name],
            "currentdate": [currentdate],
            "Special Date": [special_date],
            "Image": [image_filename if image else ""]
        })
        df = pd.concat([df, new_data], ignore_index=True)
        save_data(df)

        # Success notification
        st.toast("✅ Saved successfully!", icon="🎉")
        time.sleep(5)  # Keep toast visible for 5 seconds

        # Refresh the app
        st.rerun()
    else:
        st.sidebar.warning("⚠️ Please fill in all fields before saving.")

# Show stored data
st.subheader("📌 All Loved Ones")
for _, row in df.iterrows():
    st.write(f"**{row['Name']}** - ⭐ {row['currentdate']} -  {row['Special Date']}")
    if isinstance(row['Image'], str) and row['Image'] and os.path.exists(row['Image']):
        image = Image.open(row['Image'])
        image = image.resize((800, 400))  # Resize image
        st.image(image, caption=row['Name'], use_container_width=True)

# Search Feature
search_query = st.text_input("🔍 Search for a Loved One")
if search_query:
    result = df[df["Name"].str.contains(search_query, case=False, na=False)]
    if not result.empty:
        st.dataframe(result)
    else:
        st.warning("⚠️ No results found.")
