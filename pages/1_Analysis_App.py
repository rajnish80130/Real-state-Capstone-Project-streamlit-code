import streamlit as st
import pandas as pd
import plotly.express as px
import pickle
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="Gurgaon Real Estate Analytics", layout="wide")

# Title and Introduction
st.markdown("""
    <h1 style='text-align: center; color: #3A86FF;'>🏙️ Gurgaon Real Estate Analytics Dashboard</h1>
    <p style='text-align: center;'>Gain deep insights into the property trends, features, pricing, and more across different sectors of Gurgaon.</p>
""", unsafe_allow_html=True)

# Load Data
new_df = pd.read_csv('datasets/data_viz1.csv')
feature_text = pickle.load(open('datasets/feature_text.pkl','rb'))

# Aggregated Data
group_df = new_df.groupby('sector').agg({
    'price': 'mean',
    'price_per_sqft': 'mean',
    'built_up_area': 'mean',
    'latitude': 'first',
    'longitude': 'first'
})

# 1. Geomap
st.subheader('1️⃣ Sector-wise Price per Sqft Geo Map')
fig = px.scatter_mapbox(
    group_df,
    lat="latitude",
    lon="longitude",
    color="price_per_sqft",
    size='built_up_area',
    color_continuous_scale=px.colors.cyclical.IceFire,
    zoom=10,
    mapbox_style="open-street-map",
    hover_name=group_df.index
)
st.plotly_chart(fig, use_container_width=True)

# 2. WordCloud
st.subheader("2️⃣ 🏘️ Sector-wise Features WordCloud")
sector_options = ['Overall'] + sorted(feature_text['sector'].unique().tolist())
selected_sector = st.selectbox("Choose Sector", sector_options)

if selected_sector == 'Overall':
    text = ' '.join(feature_text['feature'].tolist())
else:
    text = ' '.join(feature_text[feature_text['sector'] == selected_sector]['feature'].tolist())

wordcloud = WordCloud(width=800, height=800, background_color='black').generate(text)
fig, ax = plt.subplots(figsize=(8, 8))
ax.imshow(wordcloud, interpolation='bilinear')
ax.axis("off")
st.pyplot(fig)

# 3. Area vs Price
st.subheader('3️⃣ 📐 Area vs Price')
property_type = st.selectbox('Select Property Type', ['Overall', 'flat', 'house'])
filtered_df = new_df if property_type == 'Overall' else new_df[new_df['property_type'] == property_type]
fig1 = px.scatter(filtered_df, x="built_up_area", y="price", color="bedRoom", title=f"Area vs Price for {property_type.title() if property_type != 'Overall' else 'All'}")
st.plotly_chart(fig1, use_container_width=True)

# 4. BHK Pie Chart
st.subheader('4️⃣ 🛏️ BHK Distribution by Sector')
sector_options = ['overall'] + sorted(new_df['sector'].unique())
selected_sector = st.selectbox('Select Sector for Pie Chart', sector_options)
fig2 = px.pie(new_df if selected_sector == 'overall' else new_df[new_df['sector'] == selected_sector], names='bedRoom')
st.plotly_chart(fig2, use_container_width=True)

# 5. BHK Price Comparison
st.subheader('5️⃣ 💵 BHK-wise Price Distribution')
fig3 = px.box(new_df[new_df['bedRoom'] <= 4], x='bedRoom', y='price', title='Price Range for BHK Types')
st.plotly_chart(fig3, use_container_width=True)

# 6. Property Type Distribution
st.subheader('6️⃣ 🏠 Property Type Price Distribution')
fig4 = plt.figure(figsize=(10, 4))
sns.histplot(new_df[new_df['property_type'] == 'house']['price'], label='House', kde=True, color='green')
sns.histplot(new_df[new_df['property_type'] == 'flat']['price'], label='Flat', kde=True, color='blue')
plt.legend()
st.pyplot(fig4)

# 7. Top 10 Luxury Sectors
st.subheader('7️⃣ 🏆 Top 10 Sectors by Luxury Score')
top_sectors = new_df.groupby('sector')['luxury_score'].mean().nlargest(10).reset_index()
fig5 = px.bar(top_sectors, x='sector', y='luxury_score', title='Top 10 Luxury Sectors', color='luxury_score', color_continuous_scale='Viridis')
st.plotly_chart(fig5, use_container_width=True)

# 8. Sector Price Variation
st.subheader('8️⃣ 🏷️ Sector Price Variation')
fig6 = px.box(new_df, x='sector', y='price', points='all', title='Price Variation by Sector')
st.plotly_chart(fig6, use_container_width=True)

# 9. Room Type Availability
st.subheader('9️⃣ 🧾 Room Availability by Property Type')
room_property_type = st.selectbox("Select Property Type", ['Overall', 'flat', 'house'], key="room_property_type")
room_data = new_df if room_property_type == 'Overall' else new_df[new_df['property_type'] == room_property_type]
room_df = room_data[['servant room', 'study room', 'pooja room', 'store room', 'others']].sum().reset_index()
room_df.columns = ['Room Type', 'Count']
fig7 = px.bar(room_df, x='Room Type', y='Count', title=f'Room Availability - {room_property_type}')
st.plotly_chart(fig7, use_container_width=True)

# 10. Built-Up Area vs Price per Sqft
st.subheader('🔟 📊 Built-Up Area vs Price Per Sqft')
scatter_prop_type = st.selectbox("Select Property Type", ['Overall', 'flat', 'house'], key="scatter_prop_type")
df_filtered = new_df if scatter_prop_type == 'Overall' else new_df[new_df['property_type'] == scatter_prop_type]
fig8 = px.scatter(df_filtered, x='built_up_area', y='price_per_sqft', size='bedRoom', color='sector',
                  hover_data=['price', 'bedRoom', 'bathroom', 'sector', 'furnishing_type', 'luxury_score'],
                  color_continuous_scale='Turbo', title=f"Built-Up Area vs Price Per Sqft ({scatter_prop_type})",
                  opacity=0.7, height=600)
fig8.update_layout(
    xaxis_title="Built-Up Area (sqft)",
    yaxis_title="Price per Sqft (₹)",
    font=dict(size=12),
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)'
)
st.plotly_chart(fig8, use_container_width=True)

# Footer
st.markdown("""
---
<p style='text-align: center;'>Made with ❤️ for Gurgaon Home Seekers</p>
""", unsafe_allow_html=True)
