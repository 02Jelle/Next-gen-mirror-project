import torch
import os
import cv2
from yolo.utils.utils import *
from predictors.YOLOv3 import YOLOv3Predictor
#from predictors.DetectronModels import Predictor
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

#mirrorIP = '192.168.3.30' #'192.168.130.195' #home
mirrorIP = '192.168.130.195' #hotspot
port = '8080'

def send_msg_to_mirror(title: str, msg: str):
    url = 'http://'+mirrorIP+':'+port+'/remote?action=SHOW_ALERT&title='+title+'&message='+msg
    requests.get(url)

def most_common(l):
    list_of_tuples = []
    for i in l:
        list_of_tuples.append((i[0], i[1], i[2], i[3]))
    s = set(list_of_tuples)
    values = list(s)
    d = dict()
    for i in values:
        number = 0
        for j in list_of_tuples:
            if i == j:
                number += 1
        d.update({number:i})
    list_with_values = list(d.items())
    list_with_values.sort()
    list_with_values.reverse()
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


while(True):
    detections = []
    while(len(detections) == 0):
        t.sleep(10)
        take_pic()
        path = 'capture.png'
        if not os.path.exists(path):
            print('Img does not exists..')
            continue
        img = cv2.imread(path)
        detections = detectron.get_detections(img)
        print(detections)
    with Image.open(path) as im:
        px = im.load()
    names_colors = []
    rgb_colors = []
    clothing_types = list(map (lambda detection: detection[-1], detections))
    print(clothing_types)
    for i in range(len(detections)):
        item_colors = []
        for m in range(int(math.ceil(detections[i][0])) + 5, int(math.floor(detections[i][2])) - 5):
            for n in range(int(math.ceil(detections[i][1])) + 5, int(math.floor(detections[i][3])) - 5):
                try:
                    color_detected = closest_color(px[m,n])
                    list.append(item_colors, color_detected)
                except IndexError:
                    print("There was an error processing your outfit colors, please stand infront of the mirror again")
        rgb_colors.append([most_common(item_colors)[0], most_common(item_colors)[1], most_common(item_colors)[2]])
        names_colors.append(most_common(item_colors)[3])
    print(names_colors)
    print(rgb_colors)
    print()

    theme = determine_theme(item_colors)
    print(f"theme is: {theme}")
    weather_advice = weather_clothing_advice(clothing_types)
    print(weather_advice)

    if color_theory(rgb_colors):
        if theme: send_msg_to_mirror("Outfit Evaluation", f"Your outfit looks good \n Your outfit is in a nice {theme} style! \n {weather_advice}")
        else:     send_msg_to_mirror("Outfit Evaluation", "Your outfit looks good \n {weather_advice}")
    else:
        suggested_colors = suggest_colors(rgb_colors)
        print(suggested_colors)
        

        if theme: send_msg_to_mirror("Outfit Evaluation", f"{suggested_colors} \n Your outfit is in a nice {theme} style! \n {weather_advice}")
        else:     send_msg_to_mirror("Outfit Evaluation", f"{suggested_colors} \n {weather_advice}")




    #unique_labels = np.array(list(set([det[-1] for det in detections])))
    #n_cls_preds = len(unique_labels)
    #bbox_colors = colors[:n_cls_preds]

    # if len(detections) != 0 :
    #     detections.sort(reverse=False ,key = lambda x:x[4])
    #     for x1, y1, x2, y2, cls_conf, cls_pred in detections:
                
    #             #feat_vec =detectron.compute_features_from_bbox(img,[(x1, y1, x2, y2)])
    #             #feat_vec = detectron.extract_encoding_features(img)
    #             #print(feat_vec)
    #             #print(a.get_field('features')[0].shape)
    #             print("\t+ Label: %s, Conf: %.5f" % (classes[int(cls_pred)], cls_conf))           
    #             print(detections)
                
    #             color = bbox_colors[np.where(unique_labels == cls_pred)[0]][0]
    #             color = colors[int(cls_pred)]
                
    #             color = tuple(c*255 for c in color)
    #             color = (.7*color[2],.7*color[1],.7*color[0])       
                    
    #             font = cv2.FONT_HERSHEY_SIMPLEX   
            
            
    #             x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
    #             text =  "%s conf: %.3f" % (classes[int(cls_pred)] ,cls_conf)
                
    #             cv2.rectangle(img,(x1,y1) , (x2,y2) , color,3)
    #             y1 = 0 if y1<0 else y1
    #             y1_rect = y1-25
    #             y1_text = y1-5

    #             if y1_rect<0:
    #                 y1_rect = y1+27
    #                 y1_text = y1+20
    #             cv2.rectangle(img,(x1-2,y1_rect) , (x1 + int(8.5*len(text)),y1) , color,-1)
    #             cv2.putText(img,text,(x1,y1_text), font, 0.5,(255,255,255),1,cv2.LINE_AA)
                
                

                
    #             cv2.imshow('Detections',img)
    #             img_id = path.split('/')[-1].split('.')[0]
    #             print(cv2.imwrite('output/ouput-test_{}_{}_{}.jpg'.format(img_id,model,dataset),img))
    #             cv2.waitKey(0)