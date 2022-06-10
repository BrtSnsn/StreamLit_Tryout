from cgitb import reset
import re
import streamlit as st
from helpers import Mqtt as mqtt
from helpers import Param
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import ast

# https://discuss.streamlit.io/t/streamlit-script-run-context-gone-with-1-8/23526/4
from streamlit.scriptrunner.script_run_context import add_script_run_ctx, get_script_run_ctx

stcontext = get_script_run_ctx()

'''
How to use:
Docker -> run mosquitto locally (anonymous true etc)
Run the batch file
Go to main page (Orac Scrapper) insert a number e.g. 5 and press send
the number is nog in your mqtt broker

Go back to dashboard page and press Start loop

the number is nog being read and I try to add it to the sessionstate lists to make it persistent
Then it blocks...


https://discuss.streamlit.io/t/live-plot-from-a-thread/247/2
https://github.com/streamlit/streamlit/issues/1326
https://discuss.streamlit.io/t/how-to-run-a-subprocess-programs-using-thread-inside-streamlit/2440
'''

st.set_page_config(
    page_title="Bert's Cool Dashboard Concept",
    page_icon="🎉",
    layout="wide",

)


# instance the classes or smth
globs = Param()
page_mqtt = mqtt('dashboard')



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

st.sidebar.write(st.session_state)  # debug

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

for slot, each in enumerate(globs.extr_lines_be):
    sparkline = pd.DataFrame([], columns=[each])
    fig, ax = plt.subplots()
    
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.get_xaxis().set_visible(False)
    ax.plot(sparkline)

    graph_dict[each].pyplot(fig)  # dit gebruiken liefst

# testbutton to trigger mqtt message (retained)
# butstart = st.button('start loop')
# if butstart:
#     page_mqtt.client.loop_start()
# else:
#     page_mqtt.client.loop_stop()

def on_connect(client, userdata, flags, rc):
    print(client, userdata, flags, rc)

def call_sparkline(client, userdata, message):
    payload = str(message.payload.decode("utf-8"))
    topic = str(message.topic)
    print(f'>> Message: {topic} --> {payload}')

    linemessage = re.search(R"EL(\d{2})", topic).group()
    print(linemessage)
    x = ast.literal_eval(payload)
    # print(x)
    result = [n for n in x]
    # print(result)
    # print(type(result))

    sparkline = pd.DataFrame(result, columns=['_'])
    fig, ax = plt.subplots()
    
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.get_xaxis().set_visible(False)
    ax.plot(sparkline)
    
    graph_dict[linemessage].pyplot(fig)  # dit gebruiken liefst
    plt.close(fig)  # anders warning over memory
    

page_mqtt.make_connection()
page_mqtt.client.on_connect = on_connect
# page_mqtt.client.on_disconnect = on_disconnect  # TODO: client dupe eruithalen
page_mqtt.client.on_message = call_sparkline

# subscribe
for eachline in globs.extr_lines_be:  # sparkline subscribe
    topic_temp = fR'orac/BEL/OST/PROD/EXTR/{eachline}/DASHB/SPARK'
    print('subscribed', topic_temp)
    page_mqtt.client.subscribe(topic_temp, qos=1)



page_mqtt.client.loop_forever()
