import ast
import streamlit as st
from PIL import Image
import io
from helpers import Mqtt as mqtt
from helpers import Param


# if 'receiver' not in st.session_state:
#     st.session_state['receiver'] = 0
# else:
#     st.session_state['receiver'] += 1
# st.write(st.session_state['receiver'])

# instance the classes or smth
globs = Param()
page_mqtt = mqtt('receiver')


msgbox = st.empty()
msgbox2 = st.empty()
msgbox3 = st.empty()


def on_connect(client, userdata, flags, rc):
    print(client, userdata, flags, rc)

def on_message(client, userdata, message):
    msgbox.empty()
    msg = message.payload.decode()
    try:
        rsp = ast.literal_eval(msg)
        msgbox.write(rsp['line'])
        if type(rsp['foto']) != int:
            msgbox2.image(Image.open(io.BytesIO(rsp['foto'])))
        msgbox3.write(rsp)

    except:
        msgbox.write('error')


with st.form('dd', clear_on_submit=True):
    vall = st.text_area('ddd')
    submitted = st.form_submit_button("Submit")
    if submitted:
        print(f'yess {vall}')

page_mqtt.make_connection()
page_mqtt.client.on_connect = on_connect
page_mqtt.client.on_message = on_message
for each in globs.extr_lines_be:
    page_mqtt.client.subscribe(f'SCRAP/{each}', qos=1)

# page_mqtt.client.loop_forever()
# manually call the loop, otherwise the client is confused if the webpage gets revisited?
while True:
    page_mqtt.client.loop(.1)
