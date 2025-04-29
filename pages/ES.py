import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Set the page to wide layout
st.set_page_config(layout="wide")

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv("Sequence_ES_2019_21_22_23_24_25csv.csv")
    df.columns = [
        "Date", "Day", "High / Low", "High / Low 2", "Start Point", "End Point",
        "ADR Model", "ADR Integrity", "ODR Model", "ODR Integrity",
        "RDR Model", "ODR Broke ADR", "TRN Broke ADR",
        "Start Point Session", "End Point Session"
    ]
    df = df.dropna(subset=["Start Point", "High / Low", "End Point Session"])  # clean incomplete rows
    return df

df = load_data()

# Apply global font size via custom HTML/CSS
st.markdown("""
    <style>
    div.block-container {font-size: 18px;}
    .comparison-text {font-size: 20px !important; text-align: center; margin-top: 2em;}
    </style>
""", unsafe_allow_html=True)

st.title("ES Sequence Outcome Analyzer")

# Create two columns for Scenario 1 and Scenario 2
col1, col2 = st.columns(2)

# --- SCENARIO 1 ---
with col1:
    st.header("Scenario 1")
    start_point1 = st.selectbox("Start Point (Scenario 1)", sorted(df["Start Point"].dropna().unique()), key="sp1")
    position_type1 = st.selectbox("High/Low Type (Scenario 1)", sorted(df["High / Low"].dropna().astype(str).unique()), key="pt1")
    day_filter1 = st.selectbox("Day (Scenario 1)", ["All"] + sorted(df["Day"].dropna().unique()), key="df1")

    filtered1 = df[(df["Start Point"] == start_point1) & (df["High / Low"] == position_type1)]
    if day_filter1 != "All":
        filtered1 = filtered1[filtered1["Day"] == day_filter1]

    if not filtered1.empty:
        outcome_counts1 = filtered1.groupby(["End Point Session"]).size().reset_index(name='Count')
        total1 = outcome_counts1['Count'].sum()
        outcome_counts1['Percentage'] = (outcome_counts1['Count'] / total1 * 100).round(2)

        st.subheader("Outcomes")
        for _, row in outcome_counts1.sort_values("Count", ascending=False).iterrows():
            st.write(f"{row['End Point Session']} | Count: {int(row['Count'])} ({row['Percentage']}%)")

        st.write(f"**Number of datasets:** {total1}")

        fig1, ax1 = plt.subplots(figsize=(6, 3))
        ax1.barh(outcome_counts1['End Point Session'], outcome_counts1['Percentage'])
        ax1.set_xlabel("Percentage")
        ax1.set_title("Scenario 1: End Point Distribution")
        st.pyplot(fig1)
    else:
        st.warning("No matching data found for Scenario 1.")

# --- SCENARIO 2 ---
with col2:
    st.header("Scenario 2")
    start_point2 = st.selectbox("Start Point (Scenario 2)", sorted(df["Start Point"].dropna().unique()), key="sp2")
    position_type2 = st.selectbox("High/Low Type (Scenario 2)", sorted(df["High / Low"].dropna().astype(str).unique()), key="pt2")
    day_filter2 = st.selectbox("Day (Scenario 2)", ["All"] + sorted(df["Day"].dropna().unique()), key="df2")

    filtered2 = df[(df["Start Point"] == start_point2) & (df["High / Low"] == position_type2)]
    if day_filter2 != "All":
        filtered2 = filtered2[filtered2["Day"] == day_filter2]

    if not filtered2.empty:
        outcome_counts2 = filtered2.groupby(["End Point Session"]).size().reset_index(name='Count')
        total2 = outcome_counts2['Count'].sum()
        outcome_counts2['Percentage'] = (outcome_counts2['Count'] / total2 * 100).round(2)

        st.subheader("Outcomes")
        for _, row in outcome_counts2.sort_values("Count", ascending=False).iterrows():
            st.write(f"{row['End Point Session']} | Count: {int(row['Count'])} ({row['Percentage']}%)")

        st.write(f"**Number of datasets:** {total2}")

        fig2, ax2 = plt.subplots(figsize=(6, 3))
        ax2.barh(outcome_counts2['End Point Session'], outcome_counts2['Percentage'])
        ax2.set_xlabel("Percentage")
        ax2.set_title("Scenario 2: End Point Distribution")
        st.pyplot(fig2)
    else:
        st.warning("No matching data found for Scenario 2.")

# --- COMPARISON SECTION ---
st.markdown("---")
st.markdown("<div class='comparison-text'><h3>🔍 Comparison</h3>", unsafe_allow_html=True)

if 'total1' in locals() and 'total2' in locals() and total1 > 0 and total2 > 0:
    percentage1 = round((total1 / (total1 + total2)) * 100, 2)
    percentage2 = round((total2 / (total1 + total2)) * 100, 2)

    st.markdown(f"<div class='comparison-text'>Scenario 1: {percentage1}% of total ({total1} datasets)</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='comparison-text'>Scenario 2: {percentage2}% of total ({total2} datasets)</div></div>", unsafe_allow_html=True)
else:
    st.markdown("<div class='comparison-text'>Run both scenarios with results to enable comparison.</div>", unsafe_allow_html=True)
