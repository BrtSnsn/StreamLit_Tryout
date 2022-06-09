import streamlit as st
from collections import OrderedDict
import json
import paho.mqtt.client as mqtt
from PIL import Image


def read_jsonconfig(extension):
    with open(f'mqtt_config{extension}.json') as jsonfile:
        return json.load(jsonfile, object_pairs_hook=OrderedDict)

def config_version():
    with open('config.ini') as f:
        line = f.readline()
        return line

cnf_version = config_version()
cnf = read_jsonconfig(cnf_version)

client = mqtt.Client(
    client_id=cnf['client_id'],
    clean_session=True,
    userdata=None,
    protocol=mqtt.MQTTv311,
    transport="tcp")

if cnf['broker_login'] != "":
    client.username_pw_set(username=cnf['broker_login'], password=cnf['broker_password'])
client.connect(
    host=cnf['broker_ip'], 
    port=cnf['broker_port'],
    )

extr_lines_be = [f'EL{x:02d}' for x in range(1, 11)]
LINES = ['_'] + extr_lines_be
SCRAP_REASONS = ['_', 'line', 'H20', 'scratch', 'other']
logo = Image.open(R"getsitelogo.png")


def send_mqtt(topic, payload):
    # print(topic)
    client.publish(topic=topic, payload=str(payload), qos=0, retain=True)


with st.form("my_form", clear_on_submit=True):
    # st.write("Inside the form")
    # slider_val = st.slider("Form slider")
    # checkbox_val = st.checkbox("Form checkbox")

    st.header('SCRAP')
    col1, col2 = st.columns(2)
    col1.radio('Select your line', LINES, key='line')
    col2.image(logo)
    st.number_input('Amount', 0, 999,step=1, key='amount')
    col1, col2 = st.columns(2)
    col1.radio('Reason', SCRAP_REASONS, key='reason')
    col2.text_area('Extra opmerking', key='extra')
    st.markdown('***')
    
    foto_bytes = 0
    
    data = {
        'line' : st.session_state.line,
        'amount': st.session_state.amount,
        'reason': st.session_state.reason,
        'opmerking': st.session_state.extra,
        'foto': 0
        }


    # foto_check = st.checkbox('Optional: Photo', key='foto')
    fotoval = st.camera_input('Take of a picture of the problem')
    st.write(fotoval)

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
        if line in extr_lines_be:
            send_mqtt(topic, t)

