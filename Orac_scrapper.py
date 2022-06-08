from asyncio.windows_events import NULL
from typing import OrderedDict
import streamlit as st
import paho.mqtt.client as mqtt
from PIL import Image
import json
from collections import OrderedDict
import io

# het lukt me niet op de imports goed te krijgen bij het opstarten van een streamlit site

# MQTT blok
def read_jsonconfig(extension):
    with open(f'mqtt_config{extension}.json') as jsonfile:
        return json.load(jsonfile, object_pairs_hook=OrderedDict)

def config_version():
    with open('config.ini') as f:
        line = f.readline()
        return line

# cnf = read_jsonconfig('_oracdev')
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



LINES = ['_'] + [f'EL{x:02d}' for x in range(1, 11)]
SCRAP_REASONS = ['_', 'line', 'H20', 'scratch', 'other']

st.set_page_config(
    page_title="Orac_dashboard",
    page_icon="logo.ico",
    layout="wide",
)

logo = Image.open(R"getsitelogo.png")

# message_box = st.empty()
# message_box = st.container()

def line_selecter():
    st.header('SCRAP')
    col1, col2 = st.columns(2)
    col1.radio('Select your line', LINES, key='line')
    col2.image(logo)
    st.number_input('Amount', 0, 999,step=1, key='amount')
    col1, col2 = st.columns(2)
    col1.radio('Reason', SCRAP_REASONS, key='reason')
    col2.text_area('Extra opmerking', key='extra')
    st.markdown('***')
    foto_check = st.checkbox('Optional: Photo', key='foto')
    foto_bytes = NULL
    if foto_check:
        foto = st.camera_input('Take of a picture of the problem')
        if foto is not None:
            foto_bytes = foto.getvalue()

    data = {
        'line' : st.session_state.line,
        'amount': st.session_state.amount,
        'reason': st.session_state.reason,
        'opmerking': st.session_state.extra,
        'foto': 0
        }

    t = json.loads(json.dumps(data))

    if data['foto'] == 0:
        t['foto'] = foto_bytes

    return t

def reset():
    # initialise de keys!!!
    # key_list = [y for y in st.session_state.keys()]
    # if all(x in key_list for x in ['line', 'amount']) and st.session_state.send == True:
    # if st.session_state.send == True:
    if 'reset' in st.session_state.keys():
        if st.session_state.reset == True:
            # hier reset ik de selection boxes
            st.session_state['line'] = '_'
            st.session_state['amount'] = 0
            st.session_state['reason'] = '_'
            st.session_state['extra'] = ''
            st.session_state['foto'] = False


reset()
data_to_send = line_selecter()

# session state gebruiken om kg om te rekenen naar stuks
# https://docs.streamlit.io/library/api-reference/session-state rond 8:26

def send_mqtt(topic, payload):
    # print(topic)
    client.publish(topic=topic, payload=str(payload), qos=0, retain=True)

# st.write(data_to_send['foto'])
# print(type(data_to_send))
# f = json.loads(data_to_send)

# foto visualiseren in de sidebar
# print(data_to_send['foto'])
if type(data_to_send['foto']) != int:
    st.sidebar.image(Image.open(io.BytesIO(data_to_send['foto'])))

st.sidebar.write("# Send Message")
st.sidebar.write(st.session_state)

send_confirm = st.sidebar.button('SEND MQTT', key='send')
key_values = [y for y in st.session_state.values()]


# this causes flickering!!
# message_box.write('ok')
if send_confirm:
#     if any(x == '_' for x in key_values):
#         # message_box.write('# Error on  :grey_exclamation:')
#         with message_box:
#             new_title = '''<p style="font-family:sans-serif; color:Red; font-size: 42px;">Error: incomplete data </p>'''
#             message_box.markdown(new_title, unsafe_allow_html=True)
#             message_box.write('Please select line, amount & reason before sending :grey_exclamation:')
#     else:
#         message_box.write('''
#         # Message Send :+1:
#         _Please press reset_
#         ''')
    line = data_to_send['line']
    topic = Rf'SCRAP/{line}'
    send_mqtt(topic, data_to_send)

for i in range(8):
    st.sidebar.write('\n')

st.sidebar.write('***')
st.sidebar.button('reset', key='reset')

# # dit is hoe columns werken
# columns = st.columns(4)
# n_radio_button = 2
# columns[2].header("Sample Radio Button")
# for i in range(n_radio_button):
#     key = "radio_button_" + str(i + 1)
#     label = "Radio Selection " + str(i + 1)
#     values = ["Radio " + str(n) for n in range(n_radio_button)]
#     columns[2].radio(label, values, key=key)
