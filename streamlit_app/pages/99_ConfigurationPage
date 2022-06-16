import streamlit as st
import database_files.crud

inlog = st.text_input('Login')
if inlog == 'Admin':
    with st.expander('Database Rebuild'):
        b = st.button('REBUILD DB')
        if b:
            database_files.crud.recreate_database()