# -*- coding: utf-8 -*-
import pytesseract
import requests as req
from PIL import Image
from io import BytesIO


# URL到图片
def url_to_img(url):
    response = req.get(url)
    image = Image.open(BytesIO(response.content)).resize((600, 180), Image.ANTIALIAS)
    return image


# 图片识别
def img_to_string(url):
    if len(url):
        pytesseract.pytesseract.tesseract_cmd = 'F://Program Files (x86)/Tesseract-OCR/tesseract.exe'
        text = pytesseract.image_to_string(url_to_img(url))
        print("图片识别：%s" % text)
        return text

