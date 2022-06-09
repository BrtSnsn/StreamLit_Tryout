import paho.mqtt.client as mqtt
import streamlit as st
import json
from PIL import Image
import io
import ast

MQTT_BROKER = 'localhost'

msgbox = st.empty()
# msgbox = st.container()

def on_connect(client, userdata, flags, rc):
    # st.write(client, userdata, flags, rc)
    print(client, userdata, flags, rc)

def on_message(client, userdata, message):
    msgbox.empty()
    # msg = message
    msg = message.payload.decode()
    try:
        # print(type(msg))
        # print(msg)
        # print(ast.literal_eval(msg))
        # sj = json.loads(msg.replace("\'", "\""))  # hacky because the bits in the photo are being altered
        # sj = json.loads(msg)
        rsp = ast.literal_eval(msg)
        msgbox.write(rsp)
        if type(rsp['foto']) != int:
            msgbox.image(Image.open(io.BytesIO(rsp['foto'])))

    except:
        msgbox.write('error')
    # print(json.loads(msg))
    # msgbox.write(type(msg))
    # msg = json.loads(msg)
    # print(json.loads(msg))
    # print(msg)
    # msgbox.write(msg)
    # if type(msg['foto']) != int:
    # st.sidebar.image(Image.open(io.BytesIO(data_to_send['foto'])))

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

with st.form('dd', clear_on_submit=True):
    vall = st.text_area('ddd')
    submitted = st.form_submit_button("Submit")
    if submitted:
        print(f'yess {vall}')

client.connect(MQTT_BROKER)

# sg = client.subscribe('TEST', qos=1)
client.subscribe('SCRAP/EL05', qos=1)
# client.publish('TEST', 'blabla', qos=1, retain=True)

# print(sg)
# st.write(sg)

# client.loop_start()
client.loop_forever()
# while True:
    # client.loop(timeout=10.0, max_packets=1)