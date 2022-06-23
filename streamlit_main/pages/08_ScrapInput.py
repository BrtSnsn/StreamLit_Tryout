import streamlit as st
from datetime import datetime, time, timedelta
from helpers import Mqtt as mqtt
from helpers import Param
from sqlalchemy import create_engine
from files_postgres.config import db_string
from files_postgres.models import Scrap
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from contextlib import contextmanager
import pandas as pd
import base64

st.set_page_config(
    page_title="Bert's Cool Dashboard Concept",
    page_icon="🎉",
    layout="centered",
    initial_sidebar_state='auto'
)

# instance the classes or smth
globs = Param()
client_id = datetime.now().strftime('%d/%b/%Y %H:%M:%S') + '_FormDB'
page_mqtt = mqtt(f'{client_id}')
st.write(f'mqtt client_id: {client_id}')
page_mqtt.make_connection()

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

# database connectie
engine = create_engine(db_string)
Session = sessionmaker(bind=engine)


def send_mqtt(topic, payload):
    page_mqtt.client.publish(topic=topic, payload=str(payload), qos=1, retain=True)


with st.form("my_form", clear_on_submit=True):
    st.header('SCRAP INPUT FORM')

    coltop1, coltop2 = st.columns([1, 3])
    # No nice formatting inside the widget yet
    dateselect = coltop1.date_input(
        "Select date of scrap",
        value=datetime.now(),
        key='dateselect'
        )

    timeselect = coltop2.slider(
        "Select time of scrap detection (±5min):",
        value=(time(datetime.now().hour, datetime.now().minute)),
        step=timedelta(minutes=5),
        format=('HH:mm'),
        key='timeselect'
        )

    # timestamp = datetime.combine(date, timeselect)
    # st.markdown(f"_Selected timestamp:_ **{timestamp.strftime('%d/%b/%Y %H:%M')}**")
    st.markdown('***')


    col1, col2 = st.columns(2)
    col1.radio('Select the line:', globs.LINES, key='line')
    col2.image(globs.logo, width=250)
    st.number_input('Amount', 0, 999, step=1, key='amount')
    col1, col2 = st.columns(2)
    col1.radio('Reason', globs.SCRAP_REASONS, key='reason')
    col2.text_area('Extra opmerking', key='extra')
    st.markdown('***')
    
    foto_bytes = 0
    
    data = {
        "date" : str(st.session_state.dateselect),
        "time" : str(st.session_state.timeselect),
        "line" : st.session_state.line,
        "amount": st.session_state.amount,
        "reason": st.session_state.reason,
        "opmerking": st.session_state.extra,
        "foto": str(0)
        }

    fotoval = st.camera_input('Take of a picture of the problem')
    # st.write(fotoval)

    st.markdown('***')
    # Every form must have a submit button.
    submitted = st.form_submit_button("Submit")
    if submitted:
        # st.write(data)
        # t = json.loads(json.dumps(data))
        if fotoval:
            foto_bytes = fotoval.getvalue()
            if data['foto'] == str(0):
                # data['foto'] = foto_bytes
                data['foto'] = base64.b64encode(foto_bytes)

        # st.write("slider", slider_val, "checkbox", checkbox_val)
        line = data['line']
        topic = Rf'SCRAP/{line}'
        if line in globs.extr_lines_be:
            now = datetime.now()
            now.strftime('%d/%m/%Y %H:%M:%S')
            send_mqtt(topic, data)  # een foto wil hij niet altijd doorsturen (misschien iets met de json die fout loopt?)

            timestamp = datetime.combine(
                st.session_state.dateselect, st.session_state.timeselect
            )
            
            scrap = Scrap(
                line=data['line'],
                amount=data['amount'],
                reason=data['reason'],
                opmerking=data['opmerking'],
                timestamp_scrap=timestamp,
                timestamp_input=datetime.now(),
                foto=data['foto'],
            )

            with session_scope() as s:
                s.add(scrap)
                s.commit()

lookback_window = datetime.now() - timedelta(hours=8)

with st.expander("Previous inputs - last 10min"):
    refresh = st.button('press to refresh')
    try:            
        if refresh:
            with session_scope() as s:
                qry = s.query(Scrap).filter(Scrap.timestamp_input > lookback_window)
                a = pd.read_sql(qry.statement, con=engine)
                st.dataframe(a)
                # st.write(pd.read_sql_query('select * from orac_scrap_be', con=engine))  # other method
                # filtersel = s.query(Scrap).filter(Scrap.timestamp > lookback_window).all()  # other method

    except Exception:
        pass

