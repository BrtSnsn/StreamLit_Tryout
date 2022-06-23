import cv2
import streamlit as st
import numpy as np

imgcam = st.camera_input('Take a picture of the QR code')

if imgcam:
    imgvalue = imgcam.getvalue()
    imgdec = cv2.imdecode(np.frombuffer(imgvalue, np.uint8), cv2.IMREAD_COLOR)

    detector = cv2.QRCodeDetector()
    data, bbox, _ = detector.detectAndDecode(imgdec)
    # check if there is a QRCode in the image
    if data:
        st.write('THIS IS YOUR QR CODE (⌐■_■)')
        st.write(data)

