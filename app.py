import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv("Sequence(2019,2021,2022)py1.csv", skiprows=1)
    df.columns = [
        "Date", "Day", "High / Low", "High / Low 2", "Start Point", "End Point",
        "ADR Model", "ADR Integrity", "ODR Model", "ODR Integrity",
        "RDR Model", "Start Point Session", "End Point Session"
    ]
    return df

df = load_data()

st.title("Sequence Outcome Analyzer")

# --- FILTERS ---
start_point = st.selectbox("Select Start Point (includes color):", sorted(df["Start Point"].dropna().unique()))
position_type = st.selectbox(
    "Select Position & Session (from High/Low column):",
    sorted(df["High / Low"].dropna().astype(str).unique())
)
day_filter = st.selectbox("(Optional) Select Day of Week:", ["All"] + sorted(df["Day"].dropna().unique()))

# --- FILTERING LOGIC ---
filtered = df[
    (df["Start Point"] == start_point) &
    (df["High / Low"] == position_type)
]

if day_filter != "All":
    filtered = filtered[filtered["Day"] == day_filter]

# --- OUTCOME COUNTS ---
if not filtered.empty:
    outcome_counts = filtered.groupby(["End Point Session"]).size().reset_index(name='Count')
    total = outcome_counts['Count'].sum()
    outcome_counts['Percentage'] = (outcome_counts['Count'] / total * 100).round(2)

    st.subheader("Most Likely Outcome Sessions")
    for _, row in outcome_counts.sort_values("Count", ascending=False).iterrows():
        st.write(f"{row['End Point Session']} | Count: {int(row['Count'])} ({row['Percentage']}%)")

    # Optional Graph
    if st.button("Show Chart"):
        fig, ax = plt.subplots()
        ax.barh(
            outcome_counts['End Point Session'],
            outcome_counts['Percentage']
        )
        ax.set_xlabel("Percentage")
        ax.set_title("End Point Session Distribution")
        st.pyplot(fig)
else:
    st.warning("No matching data found for the selected filters.")
