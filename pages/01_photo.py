from PIL import Image
import io
from pic_bert import bpic
# from pic_bert2 import bpic
import streamlit as st
import paho.mqtt.client as mqtt

# mqtt.Client.subscribe('')

# print(bpic)
img = Image.open(io.BytesIO(bpic))
# img.show()
st.image(img)