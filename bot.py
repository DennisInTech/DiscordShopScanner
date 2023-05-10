import discord
import responses
import pytesseract
import requests
import io
import cv2
import numpy as np
from PIL import Image
import re

#Tesseract directory
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

#Bot token
TOKEN = 'INSERT TOKEN HERE'


#All of the Bot Intents
intents = discord.Intents.default()
intents.message_content = True
intents.guild_messages = True
client = discord.Client(intents=intents)

# Tesseract OCR function
def better_img_to_string(pil_image):
    # convert PIL image to opencv format
    np_img = np.asarray(pil_image)

    # cropping the image in half hotdog style since we only need the bottom half
    height, width, channels = np_img.shape
    np_img = np_img[int(height / 2):height, 0:width]

    # resizing image
    resize = cv2.resize(np_img, None, fx=1.2, fy=1.2, interpolation=cv2.INTER_CUBIC)

    #preprocessing grayscale
    gray = cv2.cvtColor(resize, cv2.COLOR_BGR2GRAY)

    #preprocessing blur
    blur = cv2.GaussianBlur(gray, (7, 7), 0)

    #preprocessing threshold
    thresh = cv2.threshold(blur, 0, 225, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

    #preprocessing kernels, dilation & erode
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3,13))
    dilate = cv2.dilate(thresh, kernel, iterations=1)
    erode = cv2.erode(dilate, kernel, iterations=1)

    #bounding boxes that needs to be fixed
    contours = cv2.findContours(erode, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours = contours[0] if len(contours) == 2 else contours[1]
    contours = sorted(contours, key=lambda x: cv2.boundingRect(x)[0])
    for contour in contours:
        x,y,w,h = cv2.boundingRect(contour)
        # boxes.append((x,y,x+w,y+h))
        cv2.rectangle(np_img,(x,y), (x+w,y+h), (36,255,12), 2)

    cv2.imshow('Result', np_img)
    cv2.waitKey(0)

    #config option to only return letters & numbers
    # config = '-c tessedit_char_whitelist=abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 --psm 6'
    result = pytesseract.image_to_string(thresh)

    return result


# function for cleaner text after image goes through ocr
def clean_text(text):
    clean_text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
    clean_text = ' '.join(clean_text.split())
    clean_text = clean_text.lower()
    return clean_text



@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):

    username = str(message.author)
    user_message = str(message.content)
    channel = str(message.channel)

    # prevent the bot from looping
    if message.author == client.user:
        return

    # bot responsed to img messages in chat
    if message.attachments:

        myurl = message.attachments[0]
        theResponse = requests.get(myurl)
        img = Image.open(io.BytesIO(theResponse.content))
        text = better_img_to_string(img)

        text = clean_text(text)

        print(text)
        await message.channel.send(text)

    #test
    print(f"{username} said: '{user_message}' ({channel})")

client.run(TOKEN)













#