import pytesseract
from PIL import Image
"""need verify code is normal"""
image =  Image.open("D:/xx-1.png")
text = pytesseract.image_to_string(image)

