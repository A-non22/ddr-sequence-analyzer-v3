import streamlit as st

st.set_page_config(layout="wide")

# Custom styles for center alignment and large font
st.markdown("""
    <style>
    .center {
        display: flex;
        justify-content: center;
        align-items: center;
        flex-direction: column;
        font-size: 22px;
    }
    .button-row {
        display: flex;
        justify-content: center;
        gap: 40px;
        margin-top: 40px;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="center">
    <h1>Welcome to DDR Sequence Analyzer version 3.0 😊</h1>
</div>
""", unsafe_allow_html=True)

# --- Buttons with navigation ---
col1, col2, col3 = st.columns([2, 1, 2])

with col2:
    st.markdown("""
    <div class="button-row">
        <a href="/CL" target="_self">
            <button style="font-size:18px;padding:10px 25px;">CL</button>
        </a>
        <a href="/ES" target="_self">
            <button style="font-size:18px;padding:10px 25px;">ES</button>
        </a>
    </div>
    """, unsafe_allow_html=True)

# Note:
# You need to save this file as `Home.py` or `main.py` in Streamlit's multi-page app setup
# Then save the CL analyzer as `pages/CL.py` and ES analyzer as `pages/ES.py`
# Streamlit will automatically handle the navigation internally
