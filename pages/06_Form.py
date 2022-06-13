import streamlit as st
import json
import paho.mqtt.client as mqtt
from datetime import datetime, time, timedelta
from helpers import Mqtt as mqtt
from helpers import Param

# instance the classes or smth
globs = Param()
page_mqtt = mqtt('form_supplier')
page_mqtt.make_connection()


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
        'date' : str(st.session_state.dateselect),
        'time' : str(st.session_state.timeselect),
        'line' : st.session_state.line,
        'amount': st.session_state.amount,
        'reason': st.session_state.reason,
        'opmerking': st.session_state.extra,
        'foto': 0
        }

    fotoval = st.camera_input('Take of a picture of the problem')
    # st.write(fotoval)

    st.markdown('***')
    # Every form must have a submit button.
    submitted = st.form_submit_button("Submit")
    if submitted:
        t = json.loads(json.dumps(data))
        if fotoval:
            foto_bytes = fotoval.getvalue()
            if data['foto'] == 0:
                t['foto'] = foto_bytes

        # st.write("slider", slider_val, "checkbox", checkbox_val)
        line = t['line']
        topic = Rf'SCRAP/{line}'
        if line in globs.extr_lines_be:
            now = datetime.now()
            now.strftime('%d/%m/%Y %H:%M:%S')
            send_mqtt(topic, t)

