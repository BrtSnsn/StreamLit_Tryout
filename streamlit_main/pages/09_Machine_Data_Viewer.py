from files_influxdb.influx_db import InfluxQuery
from helpers import Param
import streamlit as st
import plotly.express as px
from datetime import datetime, timedelta, time, date

st.set_page_config(
    page_title="Influx_ORAC",
    page_icon="🎈",
    layout="wide",
    initial_sidebar_state='collapsed'
)

config = {'displayModeBar': True}

# st.sidebar.write(st.session_state)
timereminder_slot = st.empty()
graph_slot = st.empty()
selector_slot = st.empty()
globs = Param()

# init the sessionstate
for each in ['timestamp_stop', 'timestamp_start']:
    if each not in st.session_state:
        st.session_state[each] = False


with st.form("timeselect", clear_on_submit=True):
    # https://github.com/streamlit/streamlit/issues/4873
    # start_time = st.slider(
    #     "timeselect",
    #     min_value= datetime.now() - timedelta(days=2),
    #     max_value= datetime.now() + timedelta(days=2),
    #     value=(datetime.now() - timedelta(days=1), datetime.now()),
    #     step= timedelta(hours=1),
    #     format="MM/DD/YY - hh:mm",
    #     key='selectedtime')
    # submitted = st.form_submit_button("Submit")

    # data = {
    # 'datetime' : str(st.session_state.selectedtime),
    # }

    # st.write(data)

    c1, c2, c3, c4, c5 = st.columns([1, 1, 1, 1, 1])
    selection = st.selectbox('LINE', globs.LINES)
    # No nice formatting inside the widget yet
    startdateselect = c1.date_input(
        "Select start date",
        value=datetime.now(),
        key='startdateselect'
        )

    previoustime = datetime.now() - timedelta(hours=1)
    timestartselect = c2.slider(
        "Select time (±5min):",
        value=(time(previoustime.hour, 0)),
        step=timedelta(minutes=30),
        format=('HH:mm'),
        key='timestartselect'
        )

    s = "<div style='text-align:center; font-size: 50px'> <span>&#8594;</span> </div>"
    c3.markdown(s, unsafe_allow_html=True)

    stopdateselect = c4.date_input(
        "Select date of scrap",
        value=datetime.now(),
        key='stopdateselect'
        )

    timestopselect = c5.slider(
        "Select time (±5min):",
        value=(time(datetime.now().hour, datetime.now().minute)),
        step=timedelta(minutes=30),
        format=('HH:mm'),
        key='timestopselect'
        )

    submitted = st.form_submit_button("Submit")

    timestamp_start = datetime.combine(
                st.session_state.startdateselect, st.session_state.timestartselect
            )

    timestamp_stop = datetime.combine(
                st.session_state.stopdateselect, st.session_state.timestopselect
            )

    st.session_state['timestamp_stop'] = timestamp_stop
    st.session_state['timestamp_start'] = timestamp_start


if selection in globs.extr_lines_be and submitted:
    try:
        stop = st.session_state['timestamp_stop'].isoformat('T') + 'Z'
        start = st.session_state['timestamp_start'].isoformat('T') + 'Z'

        influx_inst = InfluxQuery(line=selection, start=start, stop=stop)
        df_result = influx_inst.bruteforce()
        st.session_state['influxquery'] = df_result
        timereminder_slot.write(f"SUCCES: Query updated for timeframe: {st.session_state['timestamp_start']} --> {st.session_state['timestamp_stop']}")
    except:
        st.write('error on loading the query')

refresh_graph = st.button('refresh graph', key='refrsh_influxgraph')
if refresh_graph and not st.session_state['influxquery'].empty:
    timereminder_slot.write(f"{selection} __ {st.session_state['timestamp_start']} --> {st.session_state['timestamp_stop']}")
    
    with graph_slot:
        fig = px.line(
            data_frame=st.session_state['influxquery'],
            title=selection
            # template='plotly_white'
        )
        fig.update_layout(
            modebar_add=[
                'drawline',
                'drawopenpath',
                # 'drawclosedpath',
                # 'drawcircle',
                'drawrect',
                'eraseshape'
                ],
            # legend=dict(
            #     orientation="v",
            #     yanchor="top",
            #     y=-0.02,
            #     xanchor="right",
            #     x=1
            #     )
            # paper_bgcolor="LightSteelBlue"
                )
        st.plotly_chart(fig, use_container_width=True)
