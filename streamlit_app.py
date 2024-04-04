import streamlit as st
st.write("Hello World")
st.write("Welcome to Liyu's world")

x = st.text_input("What's your name?")
is_clicked = st.button("Send")
st.write(f"Oh, Hi {x}!")
