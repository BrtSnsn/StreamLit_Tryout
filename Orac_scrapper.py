from asyncio.windows_events import NULL
import pandas as pd
import streamlit as st
import paho.mqtt.client as mqtt
# from streamlit import caching

# MQTT blok
MQTT_BROKER = 'localhost'

st.write("""
SCRAP INPUT ORAC EXTRUSION BE
""")

client = mqtt.Client()
client.connect(MQTT_BROKER)



def line_selecter():
    st.sidebar.header('SCRAP')
    line = st.sidebar.radio('Select your line', ('EL01', 'EL02'))
    amount = st.sidebar.number_input('Amount', 0, 999,step=1)
    reason = st.sidebar.radio('Reason', ('A', 'B', 'C'))
    opmerking = st.sidebar.text_area('Extra opmerking')
    foto_check = st.sidebar.checkbox('foto?')
    foto = NULL
    if foto_check:
        foto = st.sidebar.text_area('hier komt foto')
    data = {
        'line' : line,
        'amount': amount,
        'reason': reason,
        'opmerking': opmerking,
        'foto': foto
        }
    return data

data_to_send = line_selecter()

st.write(pd.DataFrame(data_to_send, index=[' ']))

# session state gebruiken om kg om te rekenen naar stuks
# https://docs.streamlit.io/library/api-reference/session-state rond 8:26

def send_mqtt(topic, payload):
    client.publish(topic=topic, payload=str(payload), qos=0, retain=False)


send_confirm = st.button('SEND MQTT')
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
