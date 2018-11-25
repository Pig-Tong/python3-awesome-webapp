# -*- coding: utf-8 -*-
import numpy as np
import urllib.request
import pytesseract
from PIL import Image
import requests as req
from PIL import Image
from io import BytesIO


def img_to_string():
    pytesseract.pytesseract.tesseract_cmd = 'F://Program Files (x86)/Tesseract-OCR/tesseract.exe'
    # text = pytesseract.image_to_string(Image.open(r'C:\Users\pig\Desktop\XZJ2qRsJ_X5PBYpG2YZJnVRI8J8XpbCY0KF.jpg'))
    text = pytesseract.image_to_string(url_to_image("http://www.huawa.com/phone/CWiLX3A11pUGjn1CF9iC2b5AFBjT2T7CABx"))
    print(text)


# URL到图片
def url_to_image(url):
    response = req.get(url)
    image = Image.open(BytesIO(response.content)).resize((600, 180), Image.ANTIALIAS)
    return image


img_to_string()
