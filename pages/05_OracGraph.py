import pandas as pd
import numpy as np
import plotly.express as px
import streamlit as st

st.set_page_config(
    page_title="Graph",
    page_icon="✅",
    layout="wide",
)

graph_slot = st.empty()

np.random.seed(1)
df = pd.DataFrame(np.random.randn(50, 3))

# job_filter = st.selectbox("Select data", pd.unique(df.columns))
# df = df.loc[:, job_filter]

st.write(df)

with graph_slot.container():
    fig_col1, fig_col2 = st.columns(2)
    with fig_col1:
        st.markdown("### First Chart")
        fig = px.line(
                data_frame=df
            )
        st.write(fig)