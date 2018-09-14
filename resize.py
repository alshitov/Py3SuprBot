import PIL
from PIL import Image
import os


def resize_images():
    basewidth = 200
    images_path = os.path.dirname(os.path.realpath(__file__)) + '/TempPNGS'
    images_list = sorted(['TempPNGS/' + img for img in os.listdir(images_path)])

    for idx, img in enumerate(images_list):
        img = Image.open(images_list[idx])
        wpercent = (basewidth / float(img.size[0]))
        hsize = int((float(img.size[1]) * float(wpercent)))
        image = img.resize((basewidth, hsize), PIL.Image.ANTIALIAS)
        image.save('TempPNGS/' + 'new' + str(0) + str(idx + 1) + '.png')

    for pic in images_list:
        os.remove(pic)