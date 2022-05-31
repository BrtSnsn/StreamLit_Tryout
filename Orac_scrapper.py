from asyncio.windows_events import NULL
import pandas as pd
import streamlit as st
import paho.mqtt.client as mqtt
from PIL import Image
import io
# from streamlit import caching

# MQTT blok
MQTT_BROKER = 'localhost'

st.write("""
SCRAP INPUT ORAC EXTRUSION BE
""")

client = mqtt.Client()
client.connect(MQTT_BROKER)

LINES = [f'EL{x:02d}' for x in range(1, 11)]
SCRAP_REASONS = ['line', 'H20', 'scratch', 'other']

def line_selecter():
    st.header('SCRAP')
    line = st.radio('Select your line', LINES)
    amount = st.number_input('Amount', 0, 999,step=1)
    reason = st.radio('Reason', SCRAP_REASONS)
    opmerking = st.text_area('Extra opmerking')
    foto_check = st.checkbox('foto?')
    foto_bytes = NULL
    if foto_check:
        foto = st.camera_input('hier komt foto')
        if foto is not None:
            foto_bytes = foto.getvalue()
            # st.image(Image.open(foto))
    data = {
        'line' : line,
        'amount': amount,
        'reason': reason,
        'opmerking': opmerking,
        'foto': foto_bytes
        }
    return data

data_to_send = line_selecter()

# st.write(pd.DataFrame(data_to_send, index=[' ']))
# st.sidebar.write(data_to_send)

# session state gebruiken om kg om te rekenen naar stuks
# https://docs.streamlit.io/library/api-reference/session-state rond 8:26

def send_mqtt(topic, payload):
    client.publish(topic=topic, payload=str(payload), qos=0, retain=False)

# st.write(data_to_send['foto'])
if type(data_to_send['foto']) != int:
    st.sidebar.image(Image.open(io.BytesIO(data_to_send['foto'])))


send_confirm = st.sidebar.button('SEND MQTT')
if send_confirm:
    line = data_to_send['line']
    topic = Rf'SCRAP/{line}'
    send_mqtt(topic, data_to_send)

# # dit is hoe columns werken
# columns = st.columns(4)
# n_radio_button = 2
# columns[2].header("Sample Radio Button")
# for i in range(n_radio_button):
#     key = "radio_button_" + str(i + 1)
#     label = "Radio Selection " + str(i + 1)
#     values = ["Radio " + str(n) for n in range(n_radio_button)]
#     columns[2].radio(label, values, key=key)