import streamlit as st
from dotenv import load_dotenv
import os
import google.generativeai as genai
from PIL import Image

# Load environment variables (likely your Google API key)
load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Function to load Google Gemini Pro Vision API and get response
def get_gemini_response(image_data, input_prompt):
    model = genai.GenerativeModel('gemini-pro-vision')
    response = model.generate_content([image_data[0], input_prompt])
    return response.text

# Function to set up image for processing
def input_image_setup(uploaded_file):
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()
        mime_type = uploaded_file.type
        image_parts = [
            {
                "mime_type": mime_type,
                "data": bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded")

# Streamlit app configuration
st.set_page_config(page_title="Gemini Health App")
st.header("Gemini Health App")

# Image upload section
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image.", use_column_width=True)

# Prompt (predefined) for calorie calculation
calorie_prompt = """
You are an expert nutritionist analyzing the food items in the image. 
Please calculate the total calories and provide details of each item, 
with calorie intake, in the following format:

1. Item 1 - Calories
2. Item 2 - Calories
...

"""

# Text area for user questions
food_question = st.text_area("Ask a question about the food in the image:", key="food_question")

# Combined processing section
if st.button("Analyze Image"):
    if uploaded_file is not None:
        try:
            image_data = input_image_setup(uploaded_file)

            # Get calorie response
            calorie_response = get_gemini_response(image_data, calorie_prompt)

            # Get user question response (if provided)
            question_response = None
            if food_question:
                question_response = get_gemini_response(image_data, food_question)

            # Display both responses (consider using st.columns for better layout)
            st.subheader("Analysis Results:")
            st.write("Total Calories:")
            st.write(calorie_response)
            if question_response:
                st.write("Answer to your question:")
                st.write(question_response)

        except FileNotFoundError as e:
            st.error(str(e))
    else:
        st.error("Please upload an image.")
