from time import sleep

from PIL import Image

from utils.image import encode as image_encode
from utils.image import decode as image_decode
from utils.text import encode as text_encode
from utils.text import decode as text_decode

if __name__ == '__main__':
    original_text = input("Input some text here: ")
    original_text_encode = text_encode(original_text)

    with Image.open('container.png') as img:
        image_encode(img, original_text_encode)

    sleep(1)

    with Image.open('new.png') as image:
        text_encode = image_decode(image)

    text = text_decode(text_encode)

    print(f"Result, {text}")
