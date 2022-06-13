import streamlit as st

st.write('hello ☜(ﾟヮﾟ☜)')

# from datetime import datetime, timedelta
# with st.form('test'):
#     start_time = st.slider(
#         "When do you start?", 
#         value=datetime.now(),
#         format="DD/MM/YYYY HH:mm:s",
#         min_value=datetime.now() - timedelta(7),
#         max_value=datetime(2023, 1, 1, 15, 25),
#         # step=datetime('1day')
#         )

#     date = st.date_input(
#         "Datum van vandaag",
#         value=datetime.now()
#         # datetime(2019, 7, 6).strftime('%d/%m/%Y'),
#         )
#     st.write(f"Your date is: {date.strftime('%d/%b/%Y')}")

#     from datetime import time
#     timeselect = st.slider(
#         "Tijdstip:",
#         value=(time(datetime.now().hour, datetime.now().minute)),
#         step=timedelta(minutes=5),
#         format=('HH:mm')
#         )
#     st.write(f"Selected Time: {timeselect.strftime('%H:%M')}")
    
#     submitted = st.form_submit_button("Submit")
#     if submitted:
#         print(f'yess {start_time}')


# import streamlit as st

# m = st.markdown("""
# <style>
# div.stButton > button:first-child {
#     background-color: rgb(204, 49, 49);
#     position:relative;left:50%;
# }
# </style>""", unsafe_allow_html=True)

# b = st.button("test")

from helpers import Mqtt as mqtt

val = st.text_input('geef iets in')
but = st.button('send')
page_mqtt = mqtt('tester')
page_mqtt.make_connection()

def send_mqtt(topic, payload):
    page_mqtt.client.publish(topic=topic, payload=str(payload), qos=1, retain=True)

if but:
    topic = Rf'RPM/EL01'
    send_mqtt(topic, val)


if 'key' not in st.session_state:
    st.session_state['key'] = 0
else:
    st.session_state['key'] += 1

st.write(st.session_state)

# exitbutton = st.button('press to stop code')
# if exitbutton:
#     st.stop()