import streamlit as st
import pickle
import pandas as pd
import numpy as np

st.set_page_config(page_title="Price Predictor", layout="wide")

@st.cache_resource
def load_assets():
    with open('df.pkl', 'rb') as file:
        df = pickle.load(file)
    with open('pipeline.pkl', 'rb') as file:
        pipeline = pickle.load(file)
    return df, pipeline

df, pipeline = load_assets()

# 🔰 Title and Description
st.title("💰 Gurgaon Property Price Predictor")
st.markdown("#### 📌 Estimate property prices with Machine Learning precision")
st.markdown("""
This tool helps you **predict the price of flats and houses in Gurgaon** based on various features like location, size, furnishing, and property category.

Just fill in the details of the property, and our model will show you the **estimated price range** based on current real estate trends.

""")

st.markdown("---")
st.subheader('📝 Enter Your Property Details Below:')

# 🏡 User Inputs
property_type = st.selectbox('Property Type', ['flat', 'house'])

sector = st.selectbox('Sector', sorted(df['sector'].unique().tolist()))

bedrooms = float(st.selectbox('Number of Bedrooms', sorted(df['bedRoom'].unique().tolist())))

bathroom = float(st.selectbox('Number of Bathrooms', sorted(df['bathroom'].unique().tolist())))

balcony = st.selectbox('Balconies', sorted(df['balcony'].unique().tolist()))

property_age = st.selectbox('Property Age', sorted(df['agePossession'].unique().tolist()))

built_up_area = float(st.number_input('Built Up Area (in sq. ft.)'))

# Extra rooms
servant_room_input = st.selectbox('Servant Room', ['No', 'Yes'])
servant_room = 1.0 if servant_room_input == 'Yes' else 0.0

store_room_input = st.selectbox('Store Room', ['No', 'Yes'])
store_room = 1.0 if store_room_input == 'Yes' else 0.0

furnishing_type = st.selectbox('Furnishing Type', sorted(df['furnishing_type'].unique().tolist()))

luxury_category = st.selectbox('Luxury Category', sorted(df['luxury_category'].unique().tolist()))

floor_category = st.selectbox('Floor Category', sorted(df['floor_category'].unique().tolist()))

# 🔮 Predict Button
if st.button('🔍 Predict Price'):
    data = [[property_type, sector, bedrooms, bathroom, balcony, property_age, built_up_area,
             servant_room, store_room, furnishing_type, luxury_category, floor_category]]

    columns = ['property_type', 'sector', 'bedRoom', 'bathroom', 'balcony',
               'agePossession', 'built_up_area', 'servant room', 'store room',
               'furnishing_type', 'luxury_category', 'floor_category']

    one_df = pd.DataFrame(data, columns=columns)
    base_price = np.expm1(pipeline.predict(one_df))[0]
    low = base_price - 0.22
    high = base_price + 0.22

    st.success(f"🏷️ The estimated price range of the property is between **₹{round(low, 2)} Cr** and **₹{round(high, 2)} Cr**.")

with st.expander("ℹ️ How is the price calculated?"):
    st.write("The predicted price is based on trained machine learning models using real-world listings from Gurgaon.")
