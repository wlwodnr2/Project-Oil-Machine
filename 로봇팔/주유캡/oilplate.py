import os, sys, cv2
import numpy as np

def yolo_v3(all_x,all_y):
    net = cv2.dnn.readNet("/home/ubuntu/Desktop/oiltest/yolov3_custom_last.weights", "/home/ubuntu/Desktop/oiltest/yolov3_custom.cfg")
    classes = []

    with open("/home/ubuntu/Desktop/oiltest/obj.names", "r") as f:
        classes = [line.strip() for line in f.readlines()]
    layer_names = net.getLayerNames()
    output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()] #ok
    colors = np.random.uniform(0, 255, size=(80, 3))
    
    cap = cv2.VideoCapture(0,cv2.CAP_V4L)
    while True:
        ret,img_1 = cap.read()
        img = cv2.resize(img_1, dsize=(720, 720), interpolation=cv2.INTER_AREA)
        height, width = img.shape[:2] #o

        blob = cv2.dnn.blobFromImage(img, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
        net.setInput(blob)
        outs = net.forward(output_layers)


        class_ids = []
        confidences = []
        boxes = []
        for out in outs:
            for detection in out:
                scores = detection[5:]
                class_id = np.argmax(scores)
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
        
        if class_ids: #class_ids is defined 
            all_x.append(center_x)
            all_y.append(center_y)
           
        indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)
       
        font = cv2.FONT_HERSHEY_PLAIN
        for i in range(len(boxes)):
            if i in indexes:
                x, y, w, h = boxes[i]
                label = str(classes[class_ids[i]])
                color = colors[i]
                cv2.rectangle(img, (x, y), (x + w, y + h), color, 2)
                cv2.putText(img, label, (x, y + 50), font, 3, color, 3)
        print(all_y)
        cv2.imshow("IMAGE",img)
      
        if cv2.waitKey(100)>0 or len(all_x) ==3:
            break
    avg_x =0
    avg_y =0
    for i in range(3):
        avg_x += all_x[i]
        avg_y += all_y[i]
    
    cv2.destroyAllWindows()
    return int(avg_x/3), int(avg_y/3)

all_x = []
all_y = []
average_x, average_y = yolo_v3(all_x,all_y)

print(average_x, average_y)
