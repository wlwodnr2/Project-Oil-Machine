import io, os ,sys, cv2, time
import numpy as np


net = cv2.dnn.readNet("/home/ubuntu/Desktop/cutplate/obj_60000.weights", "/home/ubuntu/Desktop/cutplate/obj.cfg")
classes = []

with open("/home/ubuntu/Desktop/cutplate/obj.names", "r") as f:
    classes = [line.strip() for line in f.readlines()]
layer_names = net.getLayerNames()
output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()] #ok
colors = np.random.uniform(0, 255, size=(80, 3))
cap = cv2.VideoCapture(0)

while True:
    ret,img = cap.read()
    height, width = img.shape[:2]
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    
    blob = cv2.dnn.blobFromImage(img, 0.00392, (416,416), (0, 0, 0), True, crop=False) #ok
    net.setInput(blob) #ok
    outs = net.forward(output_layers)  #ok

    class_ids = []
    confidences = []
    boxes = []
    for out in outs:
        for detection in out:
            scores = detection[5:]
            class_id = np.argmax(scores)
            if class_id >= 5: #if문을 추가해서 5번이상 즉 번호판이 아니면 무시 
                max_conf = scores[class_id]
        
                if max_conf > 0.5:
       
                    center_x = int(detection[0] * width)
                    center_y = int(detection[1] * height)
                    w = int(detection[2] * width)
                    h = int(detection[3] * height)
        
                    x = int(center_x - w / 2)
                    y = int(center_y - h / 2)
                    boxes.append([x, y, w, h]) #여기서 객체 탐지한 모든 x,y,w,h값 저장 
                    confidences.append(float(max_conf))
                    class_ids.append(class_id)
    
    indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)
    font = cv2.FONT_HERSHEY_PLAIN

    for i in range(len(boxes)):
        if i in indexes:
            x, y, w, h = boxes[i]
            label = str(classes[class_ids[i]])
            color = colors[i]
            cv2.rectangle(img, (x, y), (x + w, y + h), color, 2)
    
    if class_ids:
        cropped_img = img[y:y+h,x:x+w]
        cv2.imwrite("/home/ubuntu/Desktop/cutplate/real_car.jpg",cropped_img)
        break
