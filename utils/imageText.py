from easyocr import Reader
import argparse 
import cv2
import numpy as np


def imageToText(imageFile):

    print("Hi")

    # parser = argparse.ArgumentParser()
    # parser.add_argument("-i","--image",default='../client_Image.jpg')
    # parser.add_argument("--langs",type=str,default="en",help="en")
    # parser.add_argument("-g","--gpu",type=int,default=-1,help=" hi be used")
    
    # args = vars(parser.parse_args())
    # print("Args added ")
    # langs = args["langs"].split(",")
    langs = ['en']

    # print("[INFO]Using the following languages : {}".format(langs))

    # load input image from the disk
    # image = cv2.imread(args["image"])

    # image = cv2.imread(imageFile)
    image = cv2.imread(imageFile)

    #OCR the input using EasyOCR
    print("[INFO] Performing OCR on input image...")
    # reader = Reader(langs,gpu=args["gpu"] > 0)
    reader = Reader(langs,gpu=False)

    results = reader.readtext(image)

    whole_text = ""
    for(bbox,text,prob) in  results:
        whole_text += text + ' '
    print("Printing text ...")
    print(whole_text)
    return whole_text

# imageToText("marathi0.jpg")