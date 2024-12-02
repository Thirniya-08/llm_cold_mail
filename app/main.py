import streamlit as st
import validators  # Import the validators library for URL validation
from langchain_community.document_loaders import WebBaseLoader
from chains import Chain
from portfolio import Portfolio
from utils import clean_text

def add_background_image(image_path):
    """
    Add a background image to the Streamlit app.
    """
    # Read the image as base64 to embed in CSS
    import base64
    with open(image_path, "rb") as img_file:
        base64_image = base64.b64encode(img_file.read()).decode()
    
    st.markdown(
        f"""
        <style>
        .stApp {{
            background: linear-gradient(90deg, #e0f7e9, #ffffff, #dacbff);
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

def style_submit_button():
    """
    Add custom styling for the Submit button.
    """
    st.markdown(
        """
        <style>
        div.stButton > button {
            background-color: #333333;
            color: white;
            border-radius: 8px;
            border: none;
            font-size: 16px;
            font-weight: bold;
            padding: 10px 20px;
            cursor: pointer;
        }
        div.stButton > button:hover {
            background-color: #ff6666; /* Slightly lighter shade for hover effect */
        }
        </style>
        """,
        unsafe_allow_html=True
    )

def create_streamlit_app(llm, portfolio, clean_text):
    st.title("📩 Cold Mail Generator")
    
    # Input for URL
    url_input = st.text_input("Enter a URL:", value="https://jobs.nike.com/job/R-45734?from=job%20search%20funnel")
    submit_button = st.button("Submit")

    if submit_button:
        # Validate the URL
        if not validators.url(url_input):  # Check if the input is a valid URL
            st.error("Invalid link. Please enter a valid URL.")  # Display error if invalid
            return

        # Process the valid URL
        try:
            loader = WebBaseLoader([url_input])
            data = clean_text(loader.load().pop().page_content)
            portfolio.load_portfolio()
            jobs = llm.extract_jobs(data)
            for job in jobs:
                skills = job.get('skills', [])
                links = portfolio.query_links(skills)
                email = llm.write_mail(job, links)
                st.code(email, language='markdown')
        except Exception as e:
            st.error(f"An Error Occurred: {e}")

if __name__ == "__main__":
    chain = Chain()
    portfolio = Portfolio()

    # Set page configuration
    st.set_page_config(layout="wide", page_title="Cold Email Generator", page_icon="📩")

    # Add a background image (use the path to the downloaded image)
    background_image_path = "background.jpg"  # Replace with your image file path
    add_background_image(background_image_path)

    # Apply custom styling to the Submit button
    style_submit_button()

    # Run the Streamlit app
    create_streamlit_app(chain, portfolio, clean_text)
