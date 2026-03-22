# -*- coding: utf-8 -*-
"""

#~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+#
#                                 \\|||||//                                  #
#                                 (  o o  )                                  #
#                ------------Ooo-----(_)--------------------                 #
#                |                                         |                 #
#                |       Programmed by: kale.braden        |                 #
#                |       Date: Sun Mar 22 11:48:44 2026    |                 #
#                |                                         |                 #
#                ------------------------------ooO----------                 #
#                                |___| |___|                                 #
#                                 | |   | |                                  #
#                                 ooO   Ooo                                  #
#~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+#

"""

import streamlit as st
import pandas as pd

# Set page title and icon for the mobile browser tab
st.set_page_config(page_title="Billboard Stats", page_icon="🎵")

st.title("🎵 Hot 100 Search")
st.write("Find the peak stats for any song.")

# --- Data Loading ---
@st.cache_data
def load_data():
    # Ensure 'hot-100-current.csv' is in the same folder as this script
    return pd.read_csv('hot-100-current.csv')

try:
    df = load_data()
except FileNotFoundError:
    st.error("CSV file not found. Please ensure 'hot-100-current.csv' is in the app directory.")
    st.stop()

# --- User Inputs ---
song_title = st.text_input("Song Title", placeholder="e.g., Blinding Lights")
artist_name = st.text_input("Artist Name", placeholder="e.g., The Weeknd")

if st.button("Search Statistics"):
    if song_title and artist_name:
        # Standardize strings
        search_title = song_title.lower().strip()
        search_artist = artist_name.lower().strip()
        
        # Filter the dataframe
        song_data = df[
            (df['title'].str.lower() == search_title) & 
            (df['performer'].str.lower().str.contains(search_artist))
        ]
        
        if song_data.empty:
            st.warning("No data found for that song/artist combination.")
        else:
            # 1. Find the highest position
            highest_pos = song_data['current_week'].min()
            
            # 2. Filter for weeks at peak
            at_peak_data = song_data[song_data['current_week'] == highest_pos]
            
            # 3. Get the first time it achieved that position
            at_peak_data = at_peak_data.sort_values(by='chart_week')
            achieved_on = at_peak_data['chart_week'].iloc[0]
            
            # 4. Count the number of weeks at that position
            weeks_at_peak = len(at_peak_data)
            
            # --- Results Display ---
            st.divider()
            st.subheader(f"Results for '{song_title}'")
            
            # Using columns for a nice mobile-friendly layout
            col1, col2 = st.columns(2)
            col1.metric("Highest Position", f"#{highest_pos}")
            col2.metric("Weeks at Peak", f"{weeks_at_peak} wk(s)")
            
            st.info(f"**First Achieved On:** {achieved_on}")
    else:
        st.error("Please enter both a song title and an artist name.")