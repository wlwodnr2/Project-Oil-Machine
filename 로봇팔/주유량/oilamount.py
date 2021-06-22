import os, sys, requests, re,time
import numpy as np
from bs4 import BeautifulSoup
from datetime import datetime

def parsing():
    url = "https://www.knoc.co.kr"  
    result = requests.get(url)     
    bs_obj = BeautifulSoup(result.content, "html.parser")
    return bs_obj
    
parse_obj = parsing() 
cost_all = parse_obj.find("table", {"class":"tbl_domestic"})
data1 = [] 

for tr in cost_all.find_all('tr'):  
    tds = list(tr.find_all('td'))
    data1.append(tds[0].text)    
    
costOfGasoline = float(data1[0])  

Litter = round(float(amount/costOfGasoline),2)
print("충전해야 할 기름의 양은 " + str(Litter) +"L 입니다.\n")
