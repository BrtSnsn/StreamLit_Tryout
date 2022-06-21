import streamlit as st
from datetime import datetime
from helpers import Param
from helpers import Mqtt as mqtt

st.set_page_config(
    page_title="Update Machine Status",
    page_icon="🏭",
    layout="wide",
    initial_sidebar_state='auto'
)

globs = Param()
client_id = datetime.now().strftime('%d/%b/%Y %H:%M:%S') + '_statuspush'
page_mqtt = mqtt(f'{client_id}')
page_mqtt.make_connection()

line = st.selectbox('LINE', globs.extr_lines_be)
status = st.selectbox('Status', globs.inv_status_text.keys())

sendbutton = st.button('send')

def send_mqtt(topic, payload):
    page_mqtt.client.publish(topic=topic, payload=str(payload), qos=1, retain=True)


if sendbutton:
    if line and status:
        payload = globs.inv_status_text[status]
        topic = Rf'orac/BEL/OST/PROD/EXTR/{line}/DASHB/PSTATUS'
        send_mqtt(topic, payload=payload)

