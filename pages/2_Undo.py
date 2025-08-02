import streamlit as st
from sheet_utils import undo_last_action, get_total_points

st.set_page_config(page_title="Undo", layout="centered")
st.title("Undo Last Action")

if st.button("Undo Last"):
    undo_last_action()
    st.rerun()

st.markdown(f"### Total Points: {get_total_points()}")
