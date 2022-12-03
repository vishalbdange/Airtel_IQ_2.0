from flask import *
import io 
import base64
from PIL import Image
from easyocr import Reader
import argparse 
import cv2
import numpy as np
import os
import soundfile
import speech_recognition as sr
from pydub import AudioSegment
from api.downloadMedia import getMedia
from utils.imageText import imageToText


app = Flask(__name__)

def textFromImage(imageFile):

    print("Hi in image to text")
    langs = ['en']
    image = cv2.imread(imageFile)
    print("[INFO] Performing OCR on input image...")
    reader = Reader(langs,gpu=False)
    results = reader.readtext(image)
    whole_text = ""
    for(bbox,text,prob) in  results:
        whole_text += text + ' '
    return whole_text

@app.route('/image', methods=['POST'])
def ImageToText():
    if request.method == 'POST':
        mediaId = "835796730969358"
        print(mediaId)
        response_bytes = (getMedia(mediaId)).json()
        bytes_data = response_bytes["bytes"]
        bytes_data = str(bytes_data)
        print(bytes_data)
        b = base64.b64decode(bytes_data.encode())
        print(b)
        img = Image.open(io.BytesIO(b))
        img_name = 'imageText.' + str(response_bytes["contentType"]["subtype"])
        img.save('static/messageMedia/' + img_name)
        textFromImage = imageToText('static/messageMedia/' + img_name)
        print(textFromImage)
        return textFromImage

@app.route('/audio', methods=['POST'])
def textFromAudio():
    
    mediaId = "1179931585961479"
    print("Media ID :" + mediaId)
    # response_bytes = json.loads(getMedia(mediaId))
    response_bytes = (getMedia(mediaId)).json()
    print("USING AIRTEL IQ CPaaS DOWNLOAD MEDIA API")
    print(response_bytes)
    bytes_data = response_bytes["bytes"]
    bytes_data = str(bytes_data)
    print("Bytes data from Download Media")
    print(bytes_data)
    
    b = base64.b64decode(bytes_data.encode())
    print(b)
    if os.path.exists("myfile.wav"):
        os.remove("myfile.wav")
    else:
        print("The file does not exist")
    with open('myfile.wav', mode='bx') as f:
        f.write(b)

    data, samplerate = soundfile.read('myfile.wav')
    soundfile.write('new.wav', data, samplerate, subtype='PCM_16')
    
    file_audio = sr.AudioFile(r"new.wav")
    r = sr.Recognizer()
    with file_audio as source:
        audio_text = r.record(source)
    print(type(audio_text))
    audio_text = r.recognize_google(audio_text)
    print(audio_text)
    return audio_text

if __name__ =='__main__':  
    app.run(debug = True)  