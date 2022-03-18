import random
import ntpath

import string
import re

from html.parser import HTMLParser

##
# Strip HTML Tags
# --------------------------
# strip_tags(html)

class MLStripper(HTMLParser):
    def __init__(self):
        self.reset()
        self.strict = False
        self.convert_charrefs= True
        self.fed = []
    def handle_data(self, d):
        self.fed.append(d)
    def get_data(self):
        return ''.join(self.fed)

def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()

def clean_result(result , text_to_remove = [],single_line = True):
    if (result==None):
        return "-"
    
    result = strip_tags(result)

    for s in text_to_remove:
        result = result.replace(s,'')

    result = result.strip()

    if(single_line):
        result = result.replace('\n', ' ').replace('\r', '')

    result = re.sub(' +', ' ', result)

    return result

def safe_split(txt , separetor , index_needed):
    t = txt.split(separetor)

    if (index_needed == 0):
        return t[0]
    elif index_needed > len(t) + 1:
        return '-'
    else:
        return t[index_needed]
 
##
# Random Generator
# --------------------------
# id_generator()
# >>> 'G5G74W'
#
# id_generator(3, "6793YUIO")
# >>>'Y3U'
##


def id_generator(size=10, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


# #
# Extract Images From Text
# Changes Name in main


def extract_link_from_text(text_with_image, web_safe_topic, new_name):
    image_string = ""
    images = re.findall(r"\/images\/.*?JPG", text_with_image, re.MULTILINE)
    images += re.findall(r"\/images\/.*?jpg", text_with_image, re.MULTILINE)
    images += re.findall(r"\/images\/.*?PNG", text_with_image, re.MULTILINE)
    images += re.findall(r"\/images\/.*?png", text_with_image, re.MULTILINE)

    img_count = 0

    web_safe_topic = web_safe_topic + "/"

    for j in images:
        img_count += 1

        new_dir_name = ntpath.dirname(j) + "/"
        new_dir_name = new_dir_name.replace("solution-image/", "")
        new_dir_name = new_dir_name.replace(web_safe_topic, "")
        new_dir_name = new_dir_name.replace(config.IMAGE_LINK_OLD, config.IMAGE_LINK_NEW)
    
        new_file_name = "{0}-{1}.png".format(web_safe_topic + new_name, img_count)
        new_file_path = new_dir_name + new_file_name
    
        text_with_image = text_with_image.replace(j, new_file_path)
        image_string = image_string + j + ":" + new_file_path + "|"

    return (text_with_image, image_string)


def count_lines(file_path):
    with open(file_path) as f:
        for i, l in enumerate(f):
            pass
    return i + 1
