from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import os
import pandas as pd

# 1. 유튜브에서 검색할 주제 키워드
# 2. 몇개의 영상에서 댓글 추출?
# 3. 댓글은 몇개 추출?
# 4. 어디 저장?
keyword = input("1. 유튜브에서 검색할 주제 키워드를 입력하세요(예:롯데마트) : ")
youtube_num = int(input("2. 위 주제로 댓글을 크롤링할 유튜브 영상은 몇 건 입니까? : "))
comment_num = int(input("3. 각 동영상에서 추출한 댓글은 몇건 입니까? : "))
save_path = input("4. 크롤링 결과를 저장할 폴더명만 쓰세요(예: C:/temp/) : ")

driver = webdriver.Chrome()

if save_path == "" :
    save_path = "D:/sns_data/"

if not os.path.exists(save_path) :
    os.makedirs(save_path)

# 사용자 입력값으로 검색
driver.get(f"https://www.youtube.com/results?search_query={keyword}")
driver.implicitly_wait(10)

# 사용자가 원하는 수의 동영상이 나올 때 까지 스크롤
while len(driver.find_elements(By.CSS_SELECTOR, ".style-scope.ytd-video-renderer > .text-wrapper.style-scope.ytd-video-renderer")) < youtube_num :
    time.sleep(2)
    driver.find_element(By.CSS_SELECTOR, "body").send_keys(Keys.END)
    
# 사용자가 원한 수 만큼 동영상의 url 저장
videos = driver.find_elements(By.CSS_SELECTOR, ".style-scope.ytd-video-renderer > #video-title")
urls = [video.get_attribute("href") for video in videos[:youtube_num]]

all_url, authors, write_times, comments = [], [], [], []
count_url = 1
for url in urls :
    time.sleep(1)
    driver.get(url)
    driver.implicitly_wait(10)

    comment_box = driver.find_elements(By.CSS_SELECTOR, "#main.style-scope.ytd-comment-view-model")
    count = 0
    file_content = ""
    while len(comment_box) != 0 :
        file_content = f"-----------------------\n"
        file_content = f"1. 유튜브 url 주소 : {url}\n"

        if count == comment_num :
            break

        driver.implicitly_wait(10)
        try :
            all_url = url
            author = comment_box[count].find_element(By.CSS_SELECTOR, "a#author-text").text
            comment = comment_box[count].find_element(By.CSS_SELECTOR, "span.yt-core-attributed-string.yt-core-attributed-string--white-space-pre-wrap").text
            write_time = comment_box[count].find_element(By.CSS_SELECTOR, "span#published-time-text").text

            authors.append(author)
            write_times.append(write_time)
            comments.append(comment)
        except IndexError :
            if count == 1 :
                file_content += "댓글 없음\n"
            break
        # txt 파일로 저장
        file_content += f"2. 댓글 작성자명 : {author}\n"
        file_content += f"3. 댓글 작성일자 : {write_time}\n"
        file_content += f"4. 댓글 내용 : {comment} \n\n"
        count += 1

        with open(save_path + "result.txt", 'a', encoding='utf-8') as f :
            f.write(file_content)

    print(f"{count_url}번째 동영상 완료")
    count_url += 1
    
df = pd.DataFrame({
    'url 주소': all_url,
    '댓글작성자명': authors,
    '댓글작성일자': write_times,
    '댓글 내용': comments
})
# csv 파일로 저장
df.to_csv(save_path + 'result.csv', encoding='utf-8')
# excel 파일로 저장
df.to_excel(save_path + 'result.xlsx')