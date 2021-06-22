import pymysql
import io, os ,sys, cv2, time
import numpy as np

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