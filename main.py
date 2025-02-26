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

# Streamlit UI
st.title("🎉 Loved Ones' Special Dates Tracker")
st.sidebar.header("💖 Add a Loved One")

# Input fields
name = st.sidebar.text_input("📌 Name")
currentdate = st.sidebar.text_input("📆 Current Date (YYYY-MM-DD)")
special_date = st.sidebar.text_input("🎊 Special Date (YYYY-MM-DD)")
image = st.sidebar.file_uploader("📷 Upload Image", type=["jpg", "png", "webp"])

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
        time.sleep(2)  # Keep toast visible for 2 seconds

        # Refresh the app
        st.rerun()
    else:
        st.sidebar.warning("⚠️ Please fill in all fields before saving.")

# Show stored data
st.subheader("📌 All Loved Ones")
for index, row in df.iterrows():
    col1, col2 = st.columns([4, 1])  # Create two columns: Name+Details | Delete Button

    with col1:
        st.write(f"**{row['Name']}** - ⭐ {row['currentdate']} -  {row['Special Date']}")
        if isinstance(row['Image'], str) and row['Image'] and os.path.exists(row['Image']):
            image = Image.open(row['Image'])
            image = image.resize((800, 400))  # Resize image
            st.image(image, caption=row['Name'], use_container_width=True)

    with col2:
        if st.button(f"🗑️ Delete {row['Name']}", key=f"delete_{index}"):
            df = df.drop(index)  # Remove the entry
            save_data(df)  # Save updated data

            st.toast(f"✅ {row['Name']} deleted successfully!", icon="🗑️")
            time.sleep(2)  # Pause to show success message
            st.rerun()  # Refresh the app

# Search Feature
search_query = st.text_input("🔍 Search for a Loved One")
if search_query:
    result = df[df["Name"].str.contains(search_query, case=False, na=False)]
    if not result.empty:
        st.dataframe(result)
    else:
        st.warning("⚠️ No results found.")
