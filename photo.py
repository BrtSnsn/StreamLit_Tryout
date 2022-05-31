import imp
from PIL import Image
import io
import base64
from pic_bert import bpic

print(bpic)
img = Image.open(io.BytesIO(bpic))
img.show()