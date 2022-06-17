import streamlit as st

inlog = st.text_input('Login')
if inlog == 'Admin':
    with st.expander('placholder'):
        st.write('placeholder')