import streamlit as st
from contextlib import contextmanager
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timedelta
import pandas as pd

import database_files.crud as dbcrud
import database_files.models as dbmodels


Session = sessionmaker(bind=dbcrud.engine)


@contextmanager
def session_scope():
    session = Session()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


lookback_window = datetime.now() - timedelta(hours=24)

inlog = st.text_input('Login')
if inlog == 'Admin':
    with st.expander('Database Debug'):
        cm = st.checkbox("Yes, I know what I'm doing")
        st.markdown('***')
        b1 = st.button('REBUILD DB: this will reset the complete database')
        b2 = st.button('Query DB')

        tx = st.number_input('ROW ID:', value=0, max_value=999, step=1)
        b3 = st.button('delete a row in the DB')

        msgbox = st.empty()


        if b1 and cm:
            dbcrud.recreate_database()
            msgbox.write('Delete the whole database and rebuild it')
            
        if b2:
            with session_scope() as s:
                qry = s.query(dbmodels.Scrap).filter(dbmodels.Scrap.timestamp_input > lookback_window)
                a = pd.read_sql(qry.statement, con=dbcrud.engine)
                msgbox.write('standard query')
                st.dataframe(a)

        if b3 and tx != 0 and cm:
            with session_scope() as s:
                s.query(dbmodels.Scrap).filter(dbmodels.Scrap.id == tx).delete()
            msgbox.write(f'deleted row with ID: {tx}')