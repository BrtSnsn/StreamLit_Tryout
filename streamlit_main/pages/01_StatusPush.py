from sqlalchemy import false
import streamlit as st
from datetime import datetime
from helpers import Param
from helpers import Mqtt as mqtt
import numpy as np
import cv2

st.set_page_config(
    page_title="Update Machine Status",
    page_icon="🏀",
    layout="centered",
    initial_sidebar_state='auto'
)

globs = Param()
client_id = datetime.now().strftime('%d/%b/%Y %H:%M:%S') + '_statuspush'
page_mqtt = mqtt(f'{client_id}')
page_mqtt.make_connection()

st.sidebar.write(st.session_state)

wissel_chck = st.checkbox('Wissel?')

die = False
status = False
line = False

def imageprocess(val):
    data = False
    imgvalue = val.getvalue()
    imgdec = cv2.imdecode(np.frombuffer(imgvalue, np.uint8), cv2.IMREAD_COLOR)
    detector = cv2.QRCodeDetector()
    data, bbox, _ = detector.detectAndDecode(imgdec)
    return data

if wissel_chck:
    line_data = False
    die_data = False

    linecam = st.camera_input('line')
    if linecam:
        line_data = imageprocess(linecam)

    if line_data:
        diecam = st.camera_input('die')
        if diecam:
            die_data = imageprocess(diecam)

    with st.form("standard", clear_on_submit=True):
        st.header('WISSEL UPDATE @ EXTRUSIE BE')
        status = st.radio('selecteer', ['_', 'Wissel Opbouw', 'Wissel Afbouw'], horizontal=True)

        st.write(line_data)
        st.write(die_data)

        line = line_data
        die = die_data

        submitted = st.form_submit_button("Submit")
else:
    with st.form("standard", clear_on_submit=True):
        st.header('STATUS UPDATE @ EXTRUSIE BE')

        status = st.selectbox('Status', globs.inv_status_text.keys())
        line = st.selectbox('LINE', globs.extr_lines_be)

        submitted = st.form_submit_button("Submit")


def send_mqtt(topic, payload):
    page_mqtt.client.publish(topic=topic, payload=str(payload), qos=1, retain=True)


if submitted:
    if wissel_chck:
        if die and status:
            payload = globs.inv_status_text[status]
            topic = Rf'orac/BEL/OST/PROD/EXTR/{line}/DASHB/PSTATUS'
            send_mqtt(topic, payload=payload)
            payload = die
            topic = Rf'orac/BEL/OST/PROD/EXTR/{line}/DASHB/DIE'
            send_mqtt(topic, payload=payload)
    elif line and status:
        payload = globs.inv_status_text[status]
        topic = Rf'orac/BEL/OST/PROD/EXTR/{line}/DASHB/PSTATUS'
        send_mqtt(topic, payload=payload)

