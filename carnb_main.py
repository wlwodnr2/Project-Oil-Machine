import pymysql
import io, os ,sys, cv2, time
from google.cloud import vision
import numpy as np

def cutplate():
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

def carnumber(): #번호판 한글로 출력 
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
    return carnb

def findplate(pn): #번호판에 해당하는 사용자 찾기
    conn = pymysql.connect(host='0.0.0.0', user='root',port = 3306 , password = '*************', db='***', charset = 'utf8')
    cursor = conn.cursor() 
    
    platenb = "SELECT * FROM users where userPlate = %s"
    cursor.execute(platenb,(pn))
    res = cursor.fetchall()

    for data in res:
        print(data[2])
    if data[2]:
        conn.commit()
        conn.close()
        return 1
    else:
        conn.commit()
        conn.close()
        return 0

def rolechange(pn): #결제 할 수 있도록 권한 부여
    conn = pymysql.connect(host='0.0.0.0', user='root',port = 3306 , password = '*************', db='***', charset = 'utf8')
    cursor = conn.cursor() 

    pay_role = "UPDATE users SET userRole = %s WHERE userPlate = %s"

    cursor.execute(pay_role,(1,pn)) #권한 부여시 기계 번호에 따라 다르게 권한 부여 
    print("결제 권한 부여 했습니다.")

    conn.commit()
    conn.close()

def pay_check(pn): #userAmount
    conn = pymysql.connect(host='0.0.0.0', user='root',port = 3306 , password = '*************', db='***', charset = 'utf8')
    cursor = conn.cursor() 

    what_amount = "SELECT * FROM users where userPlate = %s"

    cursor.execute(what_amount,(pn))
    res = cursor.fetchall()
    
    for data in res:
        print(data[6])
    if data[6]: #userAmount에 0이 아닌 값이 들어있다면,
        conn.commit()
        conn.close() 
        return 1
    else: #userAmount가 0이라면 
        conn.commit()
        conn.close()
        return 0

#################################################################################################################################################


cutplate() #cut plate
plate_number = carnumber() #car number

print(plate_number + "에 해당하는 사용자를 찾겠습니다.\n")

if (findplate(plate_number)): #만약 번호판 유저를 찾았다면,
    rolechange(plate_number) #권한 부여

    while(1):
        if(pay_check(plate_number)==1): #userAmount에 값이 들어있다면 루프 탈출
            break
        print("아직 결제 안 했습니다")
        time.sleep(7)  
    print("만큼 결제했습니다.") 


    

