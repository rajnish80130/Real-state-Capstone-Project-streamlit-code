import streamlit as st

def home():
    st.set_page_config(page_title="Gurgaon Real Estate App", layout="wide")
    st.title("🏙️ Gurgaon Real Estate App")

    st.markdown("""
    Welcome to the **Gurgaon Real Estate App** – your one-stop platform for everything real estate in Gurgaon!  
    Whether you're a home buyer, investor, or just exploring – we've got you covered with smart tools and real data insights.

    ### 🔍 What You Can Do:
    - **📈 Explore Market Trends**:  
      Dive into **interactive analytics** of Gurgaon sectors using geospatial data, price trends, and room distributions.

    - **💰 Predict Flat Prices**:  
      Use our **smart price prediction tool** to estimate the expected price of a property based on detailed input features.

    - **🏡 Get Personalized Flat Recommendations**:  
      Choose a **location and radius** to explore nearby properties and get **AI-based recommendations** for similar flats.

    ---

    👉 Use the **sidebar** to switch between features and begin your real estate journey with confidence!

    """)

if __name__ == "__main__":
    home()
