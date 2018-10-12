import PIL
from PIL import Image
import os
import re


def resize_images():
    sizes = [200, 500]
    images_path = os.path.dirname(os.path.realpath(__file__)) + '/img/main/'

    images_list = sorted([file[:-4] for file in os.listdir(images_path)
                          if re.search('(.*?).jpg', file)], key=int)


    for basewidth in sizes:
        for idx, img in enumerate(images_list):
            img = Image.open(images_path + img + '.jpg')
            wpercent = (basewidth / float(img.size[0]))
            hsize = int((float(img.size[1]) * float(wpercent)))
            image = img.resize((basewidth, hsize), PIL.Image.ANTIALIAS)

            if basewidth == 200:
                image.save(images_path + '../200px/' + str(idx) + '.jpg')
            elif basewidth == 500:
                image.save(images_path + '../500px/' + str(idx) + '.jpg')