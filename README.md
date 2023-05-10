# Discord Bot Valorant Shop OCR

This is a discord bot that scans a screenshot of the daily valorant shop and 
converts the image to text. The text is sent to excel spreadsheet to be kept 
as data for other uses

This idea of the project came from my friends sending screenshot of there
daily valorant shop to general chat in discord. I decided to start making a bot that
can convert the screenshot into data and be kept on record just for funzies.

Some libraries that are used for this project is discord.py, tesseract ocr, 
and opencv-python

The process starts by getting the PIL of the image and converting to opencv. After
taking the image, it is then cropped in half because I only wanted to the names of weapons
for now. Then using preprocessing techniques such as; resizing, grayscale, blur, threshold, 
kernels, dilation, eroding and bounding boxes, to help tesseract's output be more accurate.
After that, the text is cleaned up to remove an unnecessary spaces or symbols. Then it is sent
to an excel spreadsheet to be kept for usage. 

Some features are not implemented yet. 

