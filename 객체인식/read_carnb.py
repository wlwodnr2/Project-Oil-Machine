import io, os ,sys, time
from google.cloud import vision
import numpy as np


credential_path = "/home/ubuntu/Downloads/photochange-5dce6d3f15ed.json"
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credential_path

client = vision.ImageAnnotatorClient()

file_name = '/home/ubuntu/Desktop/cutplate/real_car.jpg'

with io.open(file_name, 'rb') as image_file:
    content = image_file.read()

image = vision.Image(content = content)

response = client.text_detection(image=image, image_context={"language_hints": ["ko"]})
labels = response.text_annotations

empty_all = []

for label in labels:
    
    if len(label.description) > 7:
        continue
    else:
        empty = list(label.description)
        for i in range(len(empty)):
            empty_all.append(empty[i])

plate_number = []
plate_weight = [0 for h in range(len(empty_all))]
for j in range(len(empty_all)):
    try:    
        if empty_all[j].isdigit() and empty_all[j+1].isdigit():
            plate_weight[j] = plate_weight[j] + 1
            plate_weight[j+1] = plate_weight[j+1] + 1
        if empty_all[j].isdigit() and empty_all[j+1].isdigit() and empty_all[j+2].isdigit() and empty_all[j+3].isdigit():
            
            plate_weight[j] = plate_weight[j] + 1
            plate_weight[j+1] = plate_weight[j+1] + 1
            plate_weight[j+2] = plate_weight[j+2] + 1
            plate_weight[j+3] = plate_weight[j+3] + 1
    except:
        continue
    
string_plate = []
for z in range(len(plate_weight)):
    try:
        if plate_weight[z] > 0:
            string_plate.append(empty_all[z])
        if (plate_weight[z] > 0) and (plate_weight[z+1] == 0) and (plate_weight[z+2] > 0):
            string_plate.append(empty_all[z+1])
            
             
    except:
        continue
carnb = "".join(string_plate)
print(carnb)
