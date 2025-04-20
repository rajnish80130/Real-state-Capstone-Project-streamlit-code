import streamlit as st
import pickle
import pandas as pd
import numpy as np

# Page configuration
st.set_page_config(page_title="🏠 Apartment Recommender", layout="centered")

# Load data
location_df = pickle.load(open('datasets/location_distance.pkl', 'rb'))
cosine_sim1 = pickle.load(open('datasets/cosine_sim1.pkl', 'rb'))
cosine_sim2 = pickle.load(open('datasets/cosine_sim2.pkl', 'rb'))
cosine_sim3 = pickle.load(open('datasets/cosine_sim3.pkl', 'rb'))

# Function to recommend similar properties
def recommend_properties_with_scores(property_name, top_n=5):
    cosine_sim_matrix = 0.5 * cosine_sim1 + 0.8 * cosine_sim2 + 1 * cosine_sim3
    sim_scores = list(enumerate(cosine_sim_matrix[location_df.index.get_loc(property_name)]))
    sorted_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    top_indices = [i[0] for i in sorted_scores[1:top_n + 1]]
    top_scores = [i[1] for i in sorted_scores[1:top_n + 1]]
    top_properties = location_df.index[top_indices].tolist()

    return pd.DataFrame({
        '🏘️ Property Name': top_properties,
        '⭐ Similarity Score': [round(score, 3) for score in top_scores]
    })

# --------------------------------------------
# ✨ Header
st.markdown("<h1 style='text-align: center; color: #4CAF50;'>📍 Apartment Finder & Recommender</h1>", unsafe_allow_html=True)

# --------------------------------------------
# STEP 1: Location + Radius Search
st.markdown("### 🔎 Search Nearby Apartments")

selected_location = st.selectbox('📌 Select a location:', sorted(location_df.columns.to_list()))
radius = st.number_input('📏 Enter radius (in km):', min_value=0.1, step=0.1)

if st.button('🔍 Search Nearby Properties'):
    nearby_series = location_df[location_df[selected_location] < radius * 1000][selected_location].sort_values()
    st.session_state['nearby_properties'] = nearby_series.to_dict()

# --------------------------------------------
# STEP 2: Show nearby and recommend from it
if 'nearby_properties' in st.session_state:
    nearby_dict = st.session_state['nearby_properties']

    if not nearby_dict:
        st.warning("⚠️ No properties found within this radius.")
    else:
        st.success(f"✅ Found {len(nearby_dict)} properties nearby.")
        st.markdown("### 🏘️ Choose a nearby property to get recommendations:")

        selected_nearby_property = st.selectbox(
            "🔽 Nearby properties:",
            list(nearby_dict.keys()),
            key='property_selector'
        )

        if st.button("✨ Show Recommendations"):
            st.subheader(f"🎯 Recommended Apartments similar to '{selected_nearby_property}':")
            rec_df = recommend_properties_with_scores(selected_nearby_property)
            st.dataframe(rec_df, use_container_width=True)

# --------------------------------------------
# STEP 3: Manual Direct Recommendation
with st.expander("💡 Or, recommend by selecting an apartment directly:"):
    st.markdown("### 🏢 Direct Apartment Recommendation")

    selected_appartment = st.selectbox(
        '🏠 Select an apartment:',
        sorted(location_df.index.to_list()),
        key='manual_recommend'
    )

    if st.button('🚀 Recommend Apartments'):
        recommendation_df = recommend_properties_with_scores(selected_appartment)
        st.subheader(f"🎯 Recommended Apartments similar to '{selected_appartment}':")
        st.dataframe(recommendation_df, use_container_width=True)
