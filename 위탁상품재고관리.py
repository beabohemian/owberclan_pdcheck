from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import pandas as pd

# 상품 불러오기
판매상품 = pd.read_csv('판매상품.csv', encoding='CP949')
상품코드 = 판매상품['상품코드']
print(판매상품)
#오너클랜 로그인/품절상품 확인창 
driver = webdriver.Chrome()
driver.get('https://ownerclan.com/')
driver.find_element_by_xpath('/html/body/div[11]/div[1]/div[2]/div[2]/ul/li[1]/a/p[2]').click()
time.sleep(1)
elem_login = driver.find_element_by_id("id")
elem_login.clear()
elem_login.send_keys("아이디") 
elem_login = driver.find_element_by_id("passwd")
elem_login.clear()
elem_login.send_keys("") 
driver.find_element_by_xpath('/html/body/div[8]/div/div[2]/form/div[2]/input').click()
#상품코드 검색
src = driver.find_element_by_xpath('/html/body/div[10]/div[4]/div[1]/form/div/div/div[12]/textarea')
for 상품 in 상품코드:
    src.send_keys(상품 + ',')
time.sleep(1)
driver.find_element_by_xpath('/html/body/div[10]/div[4]/div[1]/form/div/div/div[15]/a[1]').click()

time.sleep(2)

html = driver.page_source
soup = BeautifulSoup(html, "html.parser")
pdname = soup.select("#tblBody > tr > td.left > div:nth-child(2)")
pdchange = soup.select("#tblBody > tr > td:nth-child(3) > p > font")
pdchangecont = soup.select("#tblBody > tr > td:nth-child(5) > p:nth-child(1) > font")
change_info = [["상품명", "변경사항", "변경내용"]]
for name, change, changecont in zip(pdname, pdchange, pdchangecont):
    change_info.append([name.text, change.text, changecont.text])
print(change_info)

import csv  
with open('./상품재고관리.csv', 'a', encoding='utf-8', newline='') as f:
    makewrite=csv.writer(f)

    for info in change_info:
        makewrite.writerow(info)
