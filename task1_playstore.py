from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time
import csv
import re

# 셀레니움 크롬 브라우저 설정
options = Options()
options.add_argument("--window-size=1920,1080")
options.add_experimental_option("excludeSwitches", ["enable-logging"])
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)
scroll_cnt = 10 # 스크롤 횟수
target_count = 10 # 저장할 리뷰 갯수

# 플레이 스토어 접속
app_id = "com.spotify.music"
url = f"https://play.google.com/store/apps/details?id={app_id}&hl=ko&gl=KR"
driver.get(url)
time.sleep(3)

try:
    # '리뷰 모두 보기' 버튼 찾아서 클릭하기
    print("'리뷰 모두 보기' 버튼을 찾습니다...")
    # XPath를 이용해 화면에 있는 '리뷰 모두 보기'라는 텍스트를 가진 요소를 찾음
    see_all_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//*[contains(text(), '리뷰 모두 보기')]"))
    )
    driver.execute_script("arguments[0].click();", see_all_button)  # 자바스크립트로 클릭 강제 실행
    time.sleep(3)

    # 리뷰 팝업창 스크롤 내리기 (데이터 확보)
    print("리뷰 데이터를 불러오기 위해 스크롤을 내립니다...")
    # 현재 모달창의 스크롤 가능한 영역을 찾아 자바스크립트로 스크롤을 내림
    for i in range(scroll_cnt):
        print(f" - {i + 1}번째 스크롤 중...")
        driver.execute_script(
            "var modal = document.querySelector('.odk6He'); if(modal) modal.scrollTo(0, modal.scrollHeight);"
        )
        time.sleep(2)

    # 화면에 로딩된 HTML 데이터 가져오기
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    # BeautifulSoup으로 구글 클래스명 기준 리뷰 데이터 추출
    print("데이터 추출을 시작합니다...")
    review_boxes = soup.find_all('div', class_='RHo1pe')
    review_boxes = review_boxes[:target_count]

    print(f"최종적으로 {len(review_boxes)}개의 리뷰만 파일에 저장합니다.")

    file_name = 'playstore_reviews.csv'
    with open(file_name, mode='w', encoding='utf-8-sig', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['작성자', '별점', '리뷰 내용', '작성일자'])

        for box in review_boxes:
            # 작성자 이름 추출
            user_name_tag = box.find('div', class_='X5PpBb')
            user_name = user_name_tag.text if user_name_tag else "알 수 없음"

            # 별점 추출
            rating_tag = box.find('div', attrs={'role': 'img', 'aria-label': True})
            if rating_tag:
                rating_text = rating_tag['aria-label']
                # 정규표현식으로 숫자만 추출
                rating = re.findall(r'\d+', rating_text)[-1]
            else:
                rating = "0"

            # 리뷰 본문 추출
            content_tag = box.find('div', class_='h3YV2d')
            content = content_tag.text if content_tag else ""

            # 작성 일자 추출
            date_tag = box.find('span', class_='bp9Aid')
            date = date_tag.text if date_tag else ""

            if content:  # 내용이 있는 리뷰만 저장
                writer.writerow([user_name, rating, content, date])

    print(f"총 {len(review_boxes)}개의 리뷰 구조를 찾았습니다.")
    print(f"크롤링 완료! [{file_name}] 파일을 확인해 주세요.")

except Exception as e:
    print(f"오류가 발생했습니다: {e}")

finally:
    # 모든 작업이 끝나면 브라우저 닫기
    time.sleep(2)
    driver.quit()