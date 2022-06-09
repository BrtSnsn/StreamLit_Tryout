import streamlit as st
from helpers import Mqtt as mqtt
from helpers import Param
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

'''
How to use:
Docker -> run mosquitto locally (anonymous true etc)
Run the batch file
Go to main page (Orac Scrapper) insert a number e.g. 5 and press send
the number is nog in your mqtt broker

Go back to dashboard page and press Start loop

the number is nog being read and I try to add it to the sessionstate lists to make it persistent
Then it blocks...
'''

st.set_page_config(
    page_title="Dashboard",
    page_icon="✅",
    layout="wide",
)


# instance the classes or smth
globs = Param()
page_mqtt = mqtt('dashboard')
page_mqtt.make_connection()


for each in globs.extr_lines_be:
    page_mqtt.client.subscribe(f'RPM/{each}', qos=1)

# dictionairies
title_dict = {}
graph_dict = {}
df_dict = {}
linedict = {}

# make columns
cols = st.columns(len(globs.extr_lines_be))


# fill columns based on the dict
# make empty container
for slot, each in enumerate(globs.extr_lines_be):
    title_dict[each] = cols[slot].empty()
    graph_dict[each] = cols[slot].empty()
    sparkid = f'spark_{each}'
    if sparkid not in st.session_state:
        st.session_state[f'spark_{each}'] = [0, 1, 2]
        print(sparkid)
        st.session_state[f'spark_{each}'].append(0)

st.sidebar.write(st.session_state)

for slot, each in enumerate(globs.extr_lines_be):
    kv = f'''<p 
    style="background-color:#c7c7c7; 
    border: 2px solid black;
    border-radius: 5px;
    font-family:sans-serif; 
    color:Black; 
    font-size: 42px;
    text-align: center
    ">{each}</p>'''
    title_dict[each].markdown(kv, unsafe_allow_html=True)


    np.random.seed(1)
    # sparkline = pd.DataFrame(np.random.randn(0, 1), columns=[each])
    df = pd.DataFrame(st.session_state[f'spark_{each}'], columns=[each])
    fig, ax = plt.subplots()
    
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.get_xaxis().set_visible(False)
    ax.plot(df)

    # graph_dict[each].pyplot(fig)  # dit gebruiken liefst
    cols[slot].pyplot(fig)  # dit gebruiken als ik merk dat de containers niet meer updaten wanneer streamlit draait

# testbutton to trigger mqtt message (retained)
butstart = st.button('start loop')
if butstart:
    page_mqtt.client.loop_start()
else:
    page_mqtt.client.loop_stop()



@st.experimental_memo
def on_message(client, userdata, message):
    payload = str(message.payload.decode("utf-8"))
    topic = str(message.topic)
    print(f'>> Message: {topic} --> {payload}')

    # add value to the df of the correct line
    linemessage = topic.split(sep='/')
    print(linemessage[1])
    st.write(st.session_state)
    print(st.session_state)
    # st.session_state[f'spark_{linemessage[1]}'].append(payload)
    st.write(st.session_state)

page_mqtt.client.on_message = on_message