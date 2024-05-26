import torch
import os
import cv2
from yolo.utils.utils import *
from predictors.YOLOv3 import YOLOv3Predictor
import glob
from tqdm import tqdm
import sys
from PIL import Image
import math
from colortheory import color_theory
from colortheory import closest_color
from colortheory import suggest_colors
from webcam_take_pic import take_pic
import time as t
import requests
from ThemesDetection import determine_theme
from weather import weather_clothing_advice

#mirrorIP = '192.168.3.30' #home
mirrorIP = '192.168.130.195' #hotspot
port = '8080'


""" Send a message to the mirror given a title for the notification 
and a msg that will be displayed as the content of the notification on the mirror"""
def send_msg_to_mirror(title: str, msg: str):
    #url = 'http://'+mirrorIP+':'+port+'/remote?action=SHOW_ALERT&title='+title+'&message='+msg
    #requests.get(url)
    print("results: \n" + msg)
    print("uncomment send_msg_to_mirror function with correct mirror IP to work with the mirror")
# Function that goes over a list and returnns the most common element in it
def most_common(l):
    list_of_tuples = []
    for i in l:
        list_of_tuples.append((i[0], i[1], i[2], i[3]))
    # Creating a list of all the elements in the original list without duplicating them
    s = set(list_of_tuples)
    values = list(s)
    # Dictionary to store the elements and their numbers 
    d = dict()
    # Looping over the elements in the list
    for i in values:
        number = 0
        for j in list_of_tuples:
            # If the element is found in the original list, number is incremented
            if i == j:
                number += 1
        # The dictionary updating with the element and its number
        d.update({number:i})
    # Creating a new list from the previous dictionary
    list_with_values = list(d.items())
    # Sorting the list
    list_with_values.sort()
    # The list got sorted in ascending order, so it is reversed
    list_with_values.reverse()
    # The first element of the reversed list is returned which is the most frequently occurring element in the original list
    return list_with_values[0][1]
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
torch.cuda.empty_cache()

#YOLO PARAMS
yolo_modanet_params = {   "model_def" : "yolo/modanetcfg/yolov3-modanet.cfg",
"weights_path" : "yolo/weights/yolov3-modanet_last.weights",
"class_path":"yolo/modanetcfg/modanet.names",
"conf_thres" : 0.5,
"nms_thres" :0.4,
"img_size" : 416,
"device" : device}


yolo_params = yolo_modanet_params


#Classes
classes = load_classes(yolo_params["class_path"])

#Colors
cmap = plt.get_cmap("rainbow")
colors = np.array([cmap(i) for i in np.linspace(0, 1, 13)])
#np.random.shuffle(colors)



detectron = YOLOv3Predictor(params=yolo_params)


#Faster RCNN / RetinaNet / Mask RCNN

# The main loop of the mirror that keeps taking pictures and processing them
while(True):
    detections = []
    while(len(detections) == 0):
        t.sleep(10)
        # Uses the webcam_take_pic.py module to take a picture and save it as capture.png
        take_pic()
        path = 'capture.png'
        # Checks if the image taken exists
        if not os.path.exists(path):
            print('Img does not exists..')
            continue
        # Reads the saved image
        # kpyopvision, supra56, berak (2020) error: (-215:Assertion failed) !_src.empty() in function 'cvtColor', OpenCV, https://answers.opencv.org/question/224322/error-215assertion-failed-_srcempty-in-function-cvtcolor/, retrieved April 18, 2024
        # Lundh, F. and contributors, Clark A. J. and contributors (2024), ImageOps Module, Pillow (PIL Fork) 10.3.0 documentation, https://pillow.readthedocs.io/en/stable/reference/ImageOps.html, retrieved on April 18, 2024
        # Lundh, F. and contributors, Clark A. J. and contributors (2024), ImagePalette Module, Pillow (PIL Fork) 10.3.0 documentation, https://pillow.readthedocs.io/en/stable/reference/ImagePalette.html, retrieved on April 18, 2024
        # Lundh, F. and contributors, Clark A. J. and contributors, (2024) pillow, Python Imaging Library (Fork), version 10.3.0, https://pypi.org/project/pillow/, retrieved on April 18, 2024
        # Lundh, F. and contributors, Clark A. J. and contributors, (2024) pillow, Python Imaging Library (Fork), version 10.3.0, https://pillow.readthedocs.io/en/stable/, retrieved on April 18, 2024
        # Lundh, F. and contributors, Clark A. J. and contributors, (2024) PixelAccess Class, Pillow (PIL Fork) 10.3.0 documentation, https://pillow.readthedocs.io/en/stable/reference/PixelAccess.html, retrieved on April 18, 2024
        img = cv2.imread(path)
        # Gets the detected zones with their coordinates from the image taken
        detections = detectron.get_detections(img)
        print(detections)
    # Open the image
    with Image.open(path) as im:
        # Load it as pixels
        # Lundh, F. and contributors, Clark A. J. and contributors (2024), ImageOps Module, Pillow (PIL Fork) 10.3.0 documentation, https://pillow.readthedocs.io/en/stable/reference/ImageOps.html, retrieved on April 18, 2024
        # Lundh, F. and contributors, Clark A. J. and contributors (2024), ImagePalette Module, Pillow (PIL Fork) 10.3.0 documentation, https://pillow.readthedocs.io/en/stable/reference/ImagePalette.html, retrieved on April 18, 2024
        # Lundh, F. and contributors, Clark A. J. and contributors, (2024) pillow, Python Imaging Library (Fork), version 10.3.0, https://pypi.org/project/pillow/, retrieved on April 18, 2024
        # Lundh, F. and contributors, Clark A. J. and contributors, (2024) pillow, Python Imaging Library (Fork), version 10.3.0, https://pillow.readthedocs.io/en/stable/, retrieved on April 18, 2024
        # Lundh, F. and contributors, Clark A. J. and contributors, (2024) PixelAccess Class, Pillow (PIL Fork) 10.3.0 documentation, https://pillow.readthedocs.io/en/stable/reference/PixelAccess.html, retrieved on April 18, 2024
        px = im.load()
    names_colors = []
    rgb_colors = []
    clothing_types = list(map (lambda detection: detection[-1], detections))
    print(clothing_types)
    # Start looping over the detections
    # For each detected square
    for i in range(len(detections)):
        item_colors = []
        # Loop over the pixels of the square. Here, an inner square of the detected area is looped over to increase accuracy that the actual clothing
        # item is looped over rather than the area outside of it included
        for m in range(int(math.ceil(detections[i][0])) + 5, int(math.floor(detections[i][2])) - 5):
            for n in range(int(math.ceil(detections[i][1])) + 5, int(math.floor(detections[i][3])) - 5):
                try:
                    # Using the closest_color method of the colortheory module to detect what color the pixel at [m, n] is
                    # note that closest_color(px[m,n]) returns a list of the form [R, G, B, 'color name']
                    # Lundh, F. and contributors, Clark A. J. and contributors (2024), ImageOps Module, Pillow (PIL Fork) 10.3.0 documentation, https://pillow.readthedocs.io/en/stable/reference/ImageOps.html, retrieved on April 18, 2024
                    # Lundh, F. and contributors, Clark A. J. and contributors (2024), ImagePalette Module, Pillow (PIL Fork) 10.3.0 documentation, https://pillow.readthedocs.io/en/stable/reference/ImagePalette.html, retrieved on April 18, 2024
                    # Lundh, F. and contributors, Clark A. J. and contributors, (2024) pillow, Python Imaging Library (Fork), version 10.3.0, https://pypi.org/project/pillow/, retrieved on April 18, 2024
                    # Lundh, F. and contributors, Clark A. J. and contributors, (2024) pillow, Python Imaging Library (Fork), version 10.3.0, https://pillow.readthedocs.io/en/stable/, retrieved on April 18, 2024
                    # Lundh, F. and contributors, Clark A. J. and contributors, (2024) PixelAccess Class, Pillow (PIL Fork) 10.3.0 documentation, https://pillow.readthedocs.io/en/stable/reference/PixelAccess.html, retrieved on April 18, 2024
                    color_detected = closest_color(px[m,n])
                    # The color is then added to the list of colors of the current item of clothing
                    list.append(item_colors, color_detected)
                except IndexError:
                    print("There was an error processing your outfit colors, please stand infront of the mirror again")
        # List containing the item's colors in the form [R, G, B]
        rgb_colors.append([most_common(item_colors)[0], most_common(item_colors)[1], most_common(item_colors)[2]])
        # List containing the item's colors names
        names_colors.append(most_common(item_colors)[3])
    print(names_colors)
    print(rgb_colors)
    print()

    theme = determine_theme(item_colors)
    print(f"theme is: {theme}")
    weather_advice = weather_clothing_advice(clothing_types)
    print(weather_advice)
    # If the color_theory function of the color theory module returns true, it means the colors detected look well together and a message
    # is sent to the mirror
    if color_theory(rgb_colors):
        if theme: send_msg_to_mirror("Outfit Evaluation", f"Your outfit looks good \n Your outfit is in a nice {theme} style! \n {weather_advice}")
        else:     send_msg_to_mirror("Outfit Evaluation", "Your outfit looks good \n {weather_advice}")
    # Otherwise the suggest_colors method is called and a message is sent to the mirror with the suggested colors
    else:
        suggested_colors = suggest_colors(rgb_colors)
        print(suggested_colors)
        
        if theme: send_msg_to_mirror("Outfit Evaluation", f"{suggested_colors} \n Your outfit is in a nice {theme} style! \n {weather_advice}")
        else:     send_msg_to_mirror("Outfit Evaluation", f"{suggested_colors} \n {weather_advice}")


# References
# Lundh, F. and contributors, Clark A. J. and contributors (2024), ImageOps Module, Pillow (PIL Fork) 10.3.0 documentation, https://pillow.readthedocs.io/en/stable/reference/ImageOps.html, retrieved on April 18, 2024
# Lundh, F. and contributors, Clark A. J. and contributors (2024), ImagePalette Module, Pillow (PIL Fork) 10.3.0 documentation, https://pillow.readthedocs.io/en/stable/reference/ImagePalette.html, retrieved on April 18, 2024
# Lundh, F. and contributors, Clark A. J. and contributors, (2024) pillow, Python Imaging Library (Fork), version 10.3.0, https://pypi.org/project/pillow/, retrieved on April 18, 2024
# Lundh, F. and contributors, Clark A. J. and contributors, (2024) pillow, Python Imaging Library (Fork), version 10.3.0, https://pillow.readthedocs.io/en/stable/, retrieved on April 18, 2024
# Lundh, F. and contributors, Clark A. J. and contributors, (2024) PixelAccess Class, Pillow (PIL Fork) 10.3.0 documentation, https://pillow.readthedocs.io/en/stable/reference/PixelAccess.html, retrieved on April 18, 2024
# Python Software Foundation, (2024), Built-in Types, Python 3.12.3 documentation, https://docs.python.org/3/library/stdtypes.html#dict, retrieved on April 19, 2024
# Python Software Foundation (2024), Compound statements, Python 3.12.3 documentation, https://docs.python.org/3/reference/compound_stmts.html#try, retrieved April 20, 2024
# Python Software Foundation (2024), Data model, Python 3.12.3 documentation, https://docs.python.org/3/reference/datamodel.html#index-25, retrieved April 10, 2024
# Python Software Foundation, (2024), Data Structures, Python 3.12.3 documentation, https://docs.python.org/3/tutorial/datastructures.html, retrieved on April 12, 2024
# Python Software Foundation (2024), Errors and Exceptions, Python 3.12.3 documentation, https://docs.python.org/3/tutorial/errors.html, retrieved April 20, 2024
# Python Software Foundation, (2024), Python 3.12.3 documentation, Python 3.12.3 documentation, https://docs.python.org/3/, retrieved on April 10, 2024
# Python Software Foundation, (2024), The import system, Python 3.12.3 documentation, https://docs.python.org/3/reference/import.html, retrieved on April 20, 2024