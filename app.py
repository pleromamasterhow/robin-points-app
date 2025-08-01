import streamlit as st
from pages import home, redeem, backfill, settings

st.set_page_config(page_title="Robin's Points Tracker", layout="wide")

st.sidebar.title("Navigation")
pages = {
    "Home": home.render,
    "Redeem": redeem.render,
    "Backfill": backfill.render,
    "Settings": settings.render,
}

page = st.sidebar.radio("Go to", list(pages.keys()))
pages[page]()