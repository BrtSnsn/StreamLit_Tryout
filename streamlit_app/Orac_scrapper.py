import streamlit as st
from datetime import datetime
from helpers import Param
from helpers import Mqtt as mqtt

st.set_page_config(
    page_title="Bert's Cool Dashboard Concept",
    page_icon="🎉",
    layout="wide",

)

st.write('hello ☜(ﾟヮﾟ☜)')

globs = Param()


select = st.selectbox('LINE', globs.extr_lines_be)

val = st.text_input('geef iets in')
but = st.button('send')
client_id = datetime.now().strftime('%d/%b/%Y %H:%M:%S')
page_mqtt = mqtt(f'{client_id}_main')
page_mqtt.make_connection()

def send_mqtt(topic, payload):
    page_mqtt.client.publish(topic=topic, payload=str(payload), qos=1, retain=True)

if but:
    if select:
        topic = Rf'orac/BEL/OST/PROD/EXTR/{select}/DASHB/PSTATUS'
        send_mqtt(topic, val)


if 'key' not in st.session_state:
    st.session_state['key'] = 0
else:
    st.session_state['key'] += 1

st.write(st.session_state)

st.radio('sdf', [x for x in range(1,100)], horizontal=True)

# exitbutton = st.button('press to stop code')
# if exitbutton:
#     st.stop()