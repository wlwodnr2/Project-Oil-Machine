import os, sys, cv2, pymysql, requests, re, serial,time
import numpy as np
from bs4 import BeautifulSoup
from datetime import datetime

def oilcap():
    net = cv2.dnn.readNet("/home/ubuntu/Desktop/oilcap/yolov3_custom_final.weights", "/home/ubuntu/Desktop/oilcap/yolov3_custom.cfg")
    classes = []

    with open("/home/ubuntu/Desktop/oilcap/obj.names", "r") as f:
        classes = [line.strip() for line in f.readlines()]
    layer_names = net.getLayerNames()
    output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()] 
    colors = np.random.uniform(0, 255, size=(80, 3))
    
    cap = cv2.VideoCapture(0,cv2.CAP_V4L)
    while True:
        ret,img_1 = cap.read()
        img = cv2.resize(img_1, dsize=(720, 720), interpolation=cv2.INTER_AREA)
        height, width = img.shape[:2] 

        blob = cv2.dnn.blobFromImage(img, 0.00392, (480, 480), (0, 0, 0), True, crop=False)
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
                    boxes.append([x, y, w, h]) 
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
                cv2.putText(img, label, (x, y + 50), font, 3, color, 3)
        cv2.imshow('carcap',img)
        cv2.waitKey(0)
        if class_ids:
            break
    cv2.destroyAllWindows()
    return center_y

################################################################################################################################################

def oilplate(all_y):
    net = cv2.dnn.readNet("/home/ubuntu/Desktop/oiltest/yolov3_custom_last.weights", "/home/ubuntu/Desktop/oiltest/yolov3_custom.cfg")
    classes = []

    with open("/home/ubuntu/Desktop/oiltest/obj.names", "r") as f:
        classes = [line.strip() for line in f.readlines()]
    layer_names = net.getLayerNames()
    output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]
    colors = np.random.uniform(0, 255, size=(80, 3))
    
    cap = cv2.VideoCapture(0,cv2.CAP_V4L)
    while True:
        ret,img_1 = cap.read()
        img = cv2.resize(img_1, dsize=(720, 720), interpolation=cv2.INTER_AREA)
        height, width = img.shape[:2] 

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
                    boxes.append([x, y, w, h]) 
                    confidences.append(float(max_conf))
                    class_ids.append(class_id)
        
        if class_ids: #객체 탐지 시 x,y중심 좌표 대입 
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
        cv2.imshow("cutplate",img)
        cv2.waitKey(0)
        if len(all_y) ==2:
            break
    
    avg_y =0
    for i in range(2):
        avg_y += all_y[i]
    cv2.destroyAllWindows()
    return int(avg_y/2)

################################################################################################################################################

def finduser(): #결제 권한이 1인 사용자 찾기. 1번 주유 로봇 기준.
    conn = pymysql.connect(host='175.112.158.229', user='root',port = 3308 , password = '00yoonmandu00', db='aos', charset = 'utf8')
    cursor = conn.cursor() 
    
    userAmount = "SELECT * FROM users where userRole = %s"
    cursor.execute(userAmount,(1))
    res = cursor.fetchall()
    
    try:
        for data in res:     
            print(data[6])
        if data[6]:
            conn.commit()
            conn.close()
            return data[4],data[6]
        else:
            conn.commit()
            conn.close()
            return 0, 0
    except:
        return 0,0

def start():
    conn = pymysql.connect(host='175.112.158.229', user='root',port = 3308 , password = '00yoonmandu00', db='aos', charset = 'utf8')
    cursor = conn.cursor() 
    
    try:
        userAmount = "SELECT * FROM users where userRole = %s"
        cursor.execute(userAmount,(1))
        res = cursor.fetchall()
        for data in res:     
            print("")
        if data[1]:
            return 1
        else:
            return 0
    except:
        return 0

def userinit(pt): #결제 권한 및 userAmount 초기화 
    conn = pymysql.connect(host='175.112.158.229', user='root',port = 3308 , password = '00yoonmandu00', db='aos', charset = 'utf8')
    cursor = conn.cursor() 
    
    init = "UPDATE users SET userRole = %s, userAmount = %s WHERE userPlate = %s"
    cursor.execute(init,(0,0,pt))
    
    print("결제 권한 변경 및 결제 초기화 하였습니다.")
    
    conn.commit()
    conn.close()

################################################################################################################################################

def parsing():
    url = "https://www.knoc.co.kr"  
    result = requests.get(url)     
    bs_obj = BeautifulSoup(result.content, "html.parser")
    return bs_obj

################################################################### Main ######################################################################

while(1):
    if (start()==1):
        print("시작 \n")
        break
    else:
        print ("시스템 대기중입니다.")
    time.sleep(5)

ser = serial.Serial('/dev/ttyACM0',9600,timeout = 1) #아두이노 시리얼 통신

parse_obj = parsing() 
cost_all = parse_obj.find("table", {"class":"tbl_domestic"})
data1 = [] 

for tr in cost_all.find_all('tr'):  
    tds = list(tr.find_all('td'))
    data1.append(tds[0].text)       

plate_y = []

costOfGasoline = float(data1[0])    

check = 0
chain = 0
rb_ct = 0

while(1): #결제하기 전 주유 커버 찾기 + 로봇팔 중심으로 움직이기 
    message = ser.readline()
    message = message.decode()
    print(message)

    if chain == 0 and message == "ok": #find oilplate
        print("주유커버 객체 탐지 시작\n") 
        move_y = oilplate(plate_y)

        print("주유커버의 y축 중심좌표는 " + str(move_y) + "입니다.\n")
        plate_y = []
        dis = round((360-move_y)*9/50)*10 

        if (350 <= move_y <= 370): 
            chain = 1    
            continue 
        ser.write(str(dis).encode('utf-8'))

    elif chain == 1: #move up
        print("로봇팔 중심 이동\n")
        ser.write('360'.encode('utf-8'))
        chain = 2

    elif (check==0 and chain ==2): #pay check
        pt, amount = finduser() 
        if (amount):
            check = 1
            Litter = round(float(amount/costOfGasoline),2)
            print("충전해야 할 기름의 양은 " + str(Litter) +"L 입니다.\n")
        else:
            print("아직 결제를 진행하지 않았습니다.")
        time.sleep(3)

    elif chain == 2 and amount: #oilplate open
        ser.write('1000'.encode('utf-8'))
        chain = 3

    elif chain == 3 and message == "ok": #move down
        ser.write('-360'.encode('utf-8'))
        chain = 4
    
    elif chain == 4 and message == "ok": #find oilcap    
        print("주유캡 객체 탐지 시작\n") 
        cap_y = oilcap() 

        print("주유캡의 y축 중심좌표는 " + str(cap_y) + "입니다.\n")
        dis1 = round((360-cap_y)*9/50)*10

        if (350 <= cap_y <= 370): 
            chain = 5    
            continue 
        ser.write(str(dis1).encode('utf-8')) 

    elif chain == 5: #move up
        print("로봇팔 중심 이동\n")
        rb_ct = round((356-cap_y)*9/50)*10 + 390
        ser.write(str(rb_ct).encode('utf-8'))
        chain = 6

    elif chain == 6 and message == "ok": #oilcap open
        ser.write('2000'.encode('utf-8'))
        chain = 7

    elif chain == 7 and message == "ok": #fill up
        ser.write('3000'.encode('utf-8'))
        chain = 8
        #delay = round(amount/5)
        #time.sleep(delay)

    elif chain == 8 and message == "ok": #oilcap close
        ser.write('4000'.encode('utf-8'))
        chain = 9
    
    elif chain == 9 and message == "ok": #oilplate close
        ser.write('5000'.encode('utf-8'))
        chain = 10

    elif chain == 10 and message == "ok": #fin
        ser.write('7000'.encode('utf-8'))
        chain = 11
    
    elif chain == 11:
        break

print("주유를 종료합니다.")
userinit(pt) #init
