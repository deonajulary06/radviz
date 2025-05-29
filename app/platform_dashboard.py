# platform_dashboard.py
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load your data
data = pd.read_csv('./data/pirus_clean.csv')

# Platform mapping
platform_map = {
    1: "Facebook", 2: "Twitter", 3: "YouTube", 4: "Vimeo", 5: "Instagram",
    6: "Flickr", 7: "Tumblr", 8: "Imgur", 9: "Snapchat", 10: "Google Plus",
    11: "Skype", 12: "LinkedIn", 13: "MySpace", 14: "4chan", 15: "Reddit",
    16: "Ask.fm", 17: "WhatsApp", 18: "Surespot", 19: "Telegram", 20: "Kik",
    21: "Paltalk", 22: "VK", 23: "Diaspora", 24: "JustPaste.it", 25: "SoundCloud",
    26: "Personal blogging websites", 27: "Other non-encrypted software",
    28: "Other encrypted software/unspecified encrypted software",
    29: "Discord", 30: "Gab", 31: "Iron March", 32: "Parler", 33: "Wire",
    -99: "Unknown", -88: "Not Applicable"
}

# Activity mapping
activity_map = {
    1: "Consuming content (passive)",
    2: "Disseminating content",
    3: "Participating in extremist dialogue",
    4: "Creating propaganda/content",
    5: "Direct communication for info (no plans)",
    6: "Direct communication to facilitate foreign travel",
    7: "Direct communication to facilitate domestic attack",
    -99: "Unknown",
    -88: "Not Applicable"
}

# Combine the platform columns
platform_cols = [
    'social_media_platform1', 'social_media_platform2',
    'social_media_platform3', 'social_media_platform4', 'social_media_platform5'
]

# Combine activity columns
activity_cols = [
    'social_media_activities1', 'social_media_activities2', 'social_media_activities3',
    'social_media_activities4', 'social_media_activities5', 'social_media_activities6',
    'social_media_activities7'
]

# Sidebar
st.sidebar.title("Platform Comparison Dashboard")

# Get unique platform codes (drop NaNs and convert to int)
platform_codes = data[platform_cols].stack().dropna().astype(int).unique()

# Map to platform names for display
platform_options = [platform_map.get(code, f"Unknown ({code})") for code in platform_codes]

# Sidebar selection
selected_platform_name = st.sidebar.selectbox("Select a platform:", platform_options)

# Reverse lookup to get code from name
selected_platform_code = None
for code, name in platform_map.items():
    if name == selected_platform_name:
        selected_platform_code = code
        break

# Filter data to include rows where the selected platform appears
filtered_data = data[data[platform_cols].isin([selected_platform_code]).any(axis=1)]

st.title(f"Analysis for {selected_platform_name}")

# 1️⃣ Frequency of radicalization (partial and primary separately)
st.header("Internet Radicalization Rate")

# Count partial (1) and primary (2)
partial_count = (filtered_data['internet_radicalization'] == 1).sum()
primary_count = (filtered_data['internet_radicalization'] == 2).sum()
total_count = len(filtered_data)

# Calculate percentages
partial_pct = (partial_count / total_count) * 100 if total_count > 0 else 0
primary_pct = (primary_count / total_count) * 100 if total_count > 0 else 0
combined_pct = partial_pct + primary_pct

# Display results
st.write(f"**{combined_pct:.2f}%** of users show signs of internet radicalization.")
st.write(f"- Partial role (1): **{partial_pct:.2f}%**")
st.write(f"- Primary role (2): **{primary_pct:.2f}%**")

# Optional: Pie chart visualization
if total_count > 0 and (partial_count > 0 or primary_count > 0):
    fig, ax = plt.subplots()
    labels = ['Partial Role (1)', 'Primary Role (2)']
    sizes = [partial_count, primary_count]
    ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90, colors=['#66b3ff', '#ff9999'])
    ax.axis('equal')  # Equal aspect ratio ensures pie is drawn as a circle.
    st.pyplot(fig)

# 2️⃣ Types of activities linked to the platform
st.header("Types of Activities Linked to This Platform")

# Initialize counts for all activity codes
activity_counts = pd.Series(0, index=activity_map.keys(), dtype=int)

# Count occurrences of each activity code
for col in activity_cols:
    activity_codes = filtered_data[col].dropna().astype(int)
    counts = activity_codes.value_counts()
    for code, count in counts.items():
        if code in activity_counts.index:
            activity_counts[code] += count

# Filter out zero counts
activity_counts = activity_counts[activity_counts > 0]

if not activity_counts.empty:
    # Map codes to descriptive names
    activity_labels = [activity_map.get(code, f"Unknown ({code})") for code in activity_counts.index]

    fig, ax = plt.subplots()
    sns.barplot(x=activity_labels, y=activity_counts.values, ax=ax, palette='cool')
    ax.set_xlabel("Activity Type")
    ax.set_ylabel("Count")
    ax.set_title("Activities Linked to Platform")
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha='right')
    st.pyplot(fig)
else:
    st.write("No activities linked to this platform.")
