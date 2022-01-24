"""
Code has been imported from the M3Inference Library.
"""

import urllib.request
from io import BytesIO
from PIL import Image

def get_extension(img_path):
    dotpos = img_path.rfind(".")
    extension = img_path[dotpos + 1:]
    if extension.lower() == "gif":
        return "png"
    return extension

def download_resize_img(url, img_out_path, img_out_path_fullsize=None):
    # url=url.replace("_200x200","_400x400")
    try:
        img_data = urllib.request.urlopen(url)
        img_data = img_data.read()

        if img_out_path_fullsize != None:
            with open(img_out_path_fullsize, "wb") as fh:
                fh.write(img_data)

    except:
        print("Something wrong happened in downloading the image")
        return False

    return resize_img(BytesIO(img_data), img_out_path, force=True)

def resize_img(img_path, img_out_path, filter=Image.BILINEAR, force=False):

    try:
        img = Image.open(img_path).convert("RGB")
        if img.size[0] + img.size[1] < 400 and not force:
            print(f'{img_path} is too small. Skip.')
            return
        img = img.resize((224, 224), filter)
        img.save(img_out_path)
        return True

    except Exception as e:
        print(f'Error when resizing {img_path}\nThe error message is {e} for {img_out_path}\n')
        return False
