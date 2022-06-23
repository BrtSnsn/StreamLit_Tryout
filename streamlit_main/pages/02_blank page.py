
import cv2
import streamlit as st

# st.camera_input('Take of a picture of the problem')

imagepath = R'C:\Users\bsa\PycharmProjects\Turtlez\Image_Magic\TESTBERT.jpg'

img = cv2.imread(imagepath)
print(f'new image: {img}')

detector = cv2.QRCodeDetector()
# detect and decode
data, bbox, _ = detector.detectAndDecode(img)
# check if there is a QRCode in the image
if data:
    a = data
    # keyboard.write(str(a))
    # keyboard.press('tab')
    # keyboard.wait('esc')
    st.write(a)

