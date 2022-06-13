import re
import streamlit as st
from helpers import Mqtt as mqtt
from helpers import Param
import pandas as pd
import matplotlib.pyplot as plt
import ast
from datetime import datetime
import base64

# https://discuss.streamlit.io/t/streamlit-script-run-context-gone-with-1-8/23526/4
# from streamlit.scriptrunner.script_run_context import add_script_run_ctx, get_script_run_ctx
# stcontext = get_script_run_ctx()

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
# client should be timenotation otherwise duplicate clients will throw errror in mqtt
globs = Param()
client_id = datetime.now().strftime('%d/%b/%Y %H:%M:%S')
page_mqtt = mqtt(datetime.now().strftime('%d/%b/%Y %H:%M:%S'))
st.write(f'mqtt client_id: {client_id}')



# dicts
title_dict = {}
graph_dict = {}
mstatus_icon_dict = {}
line_dict_1 = {}
line_dict_2 = {}

# status dicts
mstatus_dict = {}
pstatus_dict = {}

# global data
status_dict_text = dict(globs.status_text)
status_dict_color = dict(globs.status_color)
print(status_dict_color)

# make columns
cols = st.columns(len(globs.extr_lines_be) + 1)


# background for sidebar, this might not work for python on linux containers (TODO: test this out!)
def sidebar_bg():
    """
    removed the background url call to make the full transparent
    """

    st.markdown(
    f"""
    <style>
    [data-testid="stSidebar"] > div:first-child {{
        background-color: transparent;
    }}
    </style>
    """,
    unsafe_allow_html=True,
    )


def set_bg_hack_url(full_bg):
    """
    To make the image repeat over the full page: delete 'background-size: cover'
    """
    side_bg_ext = 'png'

    st.markdown(
    f"""
    <style>
    .stApp {{
        background: url(data:image/{side_bg_ext};base64,{base64.b64encode(open(full_bg, "rb").read()).decode()});
        background-size: cover
    }}
    </style>
    """,
    unsafe_allow_html=True
    )

def image_gen(path, height):
    img = f"""
    <div class="container" align="center">
        <img class="logo-img" src="data:image/png;base64,{base64.b64encode(open(path, "rb").read()).decode()}" height="{height}"
        aligh=>
    </div>
    """
    return img

# call the background image functions etc
image_link_1 = R'Icons\Burning.png'
image_link_2 = R'Icons\getsitelogo.png'
image_link_3 = R'Icons\background.png'


sidebar_bg()
set_bg_hack_url(image_link_3)


# fill columns based on the dict
# make empty container
for slot, each in enumerate(globs.extr_lines_be):
    title_dict[each] = cols[slot + 1].empty()
    line_dict_1[each] = cols[slot + 1].empty()
    mstatus_icon_dict[each] = cols[slot + 1].empty()
    line_dict_2[each] = cols[slot + 1].empty()
    graph_dict[each] = cols[slot + 1].empty()

st.sidebar.write(st.session_state)  # debug

# fill first column of the dashboard
col0_lines = f'''<p 
    style="
    font-family:sans-serif; 
    color:Black; 
    font-size: 30px;
    padding: 13px 0px 10px 0px;
    text-align: left
    ">Lines</p>'''
cols[0].markdown(col0_lines, unsafe_allow_html=True)
cols[0].markdown('***')
col0_mstatus = f'''<p 
    style="
    font-family:sans-serif; 
    color:Black; 
    font-size: 20px;
    padding: 0px 0px 3px 0px;
    text-align: left
    ">Status:</p>'''
cols[0].markdown(col0_mstatus, unsafe_allow_html=True)
cols[0].markdown('***')
cols[0].write('graph')


# initiate the empty fields
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
    line_dict_1[each].markdown("***")
    line_dict_2[each].markdown("***")

    """ Initiate the graphs and fill them with blanks """
    sparkline = pd.DataFrame([], columns=[each])
    fig, ax = plt.subplots(figsize=(1,1), dpi=80)
    
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(False)  # misschien toch tijdnotatie toevoegen
    ax.get_xaxis().set_visible(False)
    ax.plot(sparkline)

    # mstatus_dict[each].write('_')
    image_path = R'Icons/Quickness.png'
    mstatus_icon_dict[each].markdown(image_gen(image_path, 50), unsafe_allow_html=True)
    graph_dict[each].pyplot(fig, transparent=True)
    plt.close(fig)

    pstatus_dict[each] = 0
    pstatus_dict[each] = 0

def on_connect(client, userdata, flags, rc):
    print(client, userdata, flags, rc)

def call_sparkline(client, userdata, message):
    payload = str(message.payload.decode("utf-8"))
    topic = str(message.topic)
    linemessage = re.search(R"EL(\d{2})", topic).group()
    print(f'{linemessage} --> {payload}')
    x = ast.literal_eval(payload)
    result = [n for n in x]

    sparkline = pd.DataFrame(result, columns=['_'])
    fig, ax = plt.subplots(figsize=(4,4), dpi=80)
    
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.get_xaxis().set_visible(False)
    ax.plot(sparkline, 'o-', linewidth=2, markersize=5)
    
    graph_dict[linemessage].pyplot(fig, transparent=True)  # dit gebruiken liefst
    plt.close(fig)  # anders warning over memory


def call_pstatus(client, userdata, message):
    """
    Receive and store the machine status that is passed by the operator on any terminal in the productionhall
    """
    payload = str(message.payload.decode("utf-8"))
    topic = str(message.topic)
    linemessage = re.search(R"EL(\d{2})", topic).group()
    print(f'{linemessage} --> HUMAN {payload}')

    pstatus_dict[linemessage] = payload
    full_status(linemessage)


def call_mstatus(client, userdata, message):
    """ 
    display an image based on some status conditions
        The reason I want to go for css style markdown instead of build in  is that this allows centering
    """
    payload = str(message.payload.decode("utf-8"))
    topic = str(message.topic)
    linemessage = re.search(R"EL(\d{2})", topic).group()
    print(f'{linemessage} --> MACHINE {payload}')

    mstatus_dict[linemessage] = payload
    full_status(linemessage)

    # https://discuss.streamlit.io/t/how-do-i-use-a-background-image-on-streamlit/5067/7
    # https://discuss.streamlit.io/t/image-and-text-next-to-each-other/7627/18  # this fixed my problem

    
def full_status(line):
    """
    Create a complete machine status based on human & machine input
    """
    try:
        mstatus = mstatus_dict[line]
        pstatus = pstatus_dict[line]

        def send_mqtt_pstatus(payload, line):
            topic_temp = fR'orac/BEL/OST/PROD/EXTR/{line}/DASHB/PSTATUS'
            page_mqtt.client.publish(topic=topic_temp, payload=str(payload), qos=1, retain=True)
        
        def send_mqtt_status(payload, line):
            topic_temp = fR'orac/BEL/OST/PROD/EXTR/{line}/DASHB/STATUS'
            page_mqtt.client.publish(topic=topic_temp, payload=str(payload), qos=1, retain=True)


        if mstatus in ['0'] and not pstatus in ['50', '51', '10', '0']:
            send_mqtt_pstatus('0', line=line)  # reset pstatus naar 0
            status = mstatus
        elif mstatus in ['0'] and pstatus in ['50', '51', '10', '0']:  # koude machine die uit staat -> wissel & cold die
            status = pstatus
        elif mstatus in ['1', '2'] and pstatus not in ['3']:  # opwarmen & opstarten maar de code staat nog in productie
            status = mstatus
        elif mstatus in ['2'] and pstatus in ['3']:
            status = pstatus
        elif mstatus in ['5'] and pstatus in ['3']:  # machine detecteerd breuk
            send_mqtt_pstatus('2', line=line)  # reset pstatus naar 2
            status = mstatus
        elif mstatus in ['20'] and not pstatus in ['50', '51', '0']:
            send_mqtt_pstatus('0', line=line)  # reset pstatus naar 0
            status = mstatus
        elif mstatus in ['20'] and pstatus in ['50', '51']:
            status = pstatus
        else:
            status = pstatus = mstatus
        
        send_mqtt_status(status, line=line)
        mstatus_icon_dict[line].markdown(status_dict_text[status])
        # mstatus_icon_dict[linemessage].markdown(image_gen(logo_image_path, 50), unsafe_allow_html=True)

        def title_bar_status(status, line):
            colorcode = status_dict_color[status]
            kv = f'''<p 
                style="background-color:{colorcode}; 
                border: 2px solid black;
                border-radius: 5px;
                font-family:sans-serif; 
                color:Black; 
                font-size: 42px;
                text-align: center
                ">{line}</p>'''
            title_dict[line].markdown(kv, unsafe_allow_html=True)
        
        title_bar_status(status=status, line=line)

    except Exception as e:
        print(e)

page_mqtt.make_connection()
page_mqtt.client.on_connect = on_connect
# page_mqtt.client.on_disconnect = on_disconnect  # TODO: client dupe eruithalen? -> omzeild door client id op basis van tijd
# page_mqtt.client.on_message = call_sparkline

# subscribe & add callbacks for the Sparklines
for eachline in globs.extr_lines_be:
    topic_temp = fR'orac/BEL/OST/PROD/EXTR/{eachline}/DASHB/SPARK'
    print('subscribed', topic_temp)
    page_mqtt.client.message_callback_add(topic_temp, call_sparkline)
    page_mqtt.client.subscribe(topic_temp, qos=1)

for eachline in globs.extr_lines_be:
    topic_temp = fR'orac/BEL/OST/PROD/EXTR/{eachline}/DASHB/MSTATUS'
    print('subscribed', topic_temp)
    page_mqtt.client.message_callback_add(topic_temp, call_mstatus)
    page_mqtt.client.subscribe(topic_temp, qos=1)

for eachline in globs.extr_lines_be:
    topic_temp = fR'orac/BEL/OST/PROD/EXTR/{eachline}/DASHB/PSTATUS'
    print('subscribed', topic_temp)
    page_mqtt.client.message_callback_add(topic_temp, call_pstatus)
    page_mqtt.client.subscribe(topic_temp, qos=1)


page_mqtt.client.loop_forever()
