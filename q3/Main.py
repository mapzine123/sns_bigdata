from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import os
import requests
# 1. 크롤링할 이미지 키워드
# 2. 크롤링할 건수
# 3. 파일이 저장될 경로

print('==========================================================')
print('pixbay 사이트에서 이미지를 검색하여 수집하는 크롤러 입니다')
print('==========================================================')

keyword = input('1. 크롤링할 이미지의 키워드는 무엇입니까? : ')
img_num = int(input('2. 크롤링 할 건수는 몇건입니까? : '))
save_path = input('3. 파일이 저장될 경로만 쓰세요(예 : c:/temp/) : ')

driver = webdriver.Chrome()

if not os.path.exists(save_path):
    os.makedirs(save_path)

img_elements = []


i = 1
while len(img_elements) < img_num :
    driver.get(f'https://pixabay.com/ko/images/search/{keyword}/?pagi={i}')
    driver.implicitly_wait(10)
    driver.find_element(By.CSS_SELECTOR, "body").send_keys(Keys.END)
    img_elements += driver.find_elements(By.CSS_SELECTOR, 'div.container--MwyXl')
    i += 1
    time.sleep(2)

img_count = 1
for img_element in img_elements[:img_num] :
    driver.implicitly_wait(10)
    img_tag = img_element.find_element(By.CSS_SELECTOR, 'a > img')
    img_url = img_tag.get_attribute('src')

    if img_url :
        response = requests.get(img_url)
        with open(save_path + f"image_{img_count}.jpg", 'wb') as f :
            f.write(response.content)
    time.sleep(1)
    print(f"{img_count}번째 완료")
    img_count += 1

driver.quit()