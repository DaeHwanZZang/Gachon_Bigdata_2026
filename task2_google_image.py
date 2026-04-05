import urllib.request
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time
import os

# 크롤링할 키워드와 저장할 폴더 설정
keyword = "spiderman"
folder_name = f"{keyword}_images"

if not os.path.exists(folder_name):
    os.makedirs(folder_name)
    print(f"[{folder_name}] 폴더를 생성했습니다.")

# 셀레니움 설정 및 브라우저 실행
options = Options()
options.add_argument("--window-size=1920,1080")
options.add_experimental_option("excludeSwitches", ["enable-logging"])
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

# 구글 이미지 검색 페이지 접속
print(f"[{keyword}] 구글 이미지 검색을 시작합니다...")
url = f"https://www.google.com/search?q={keyword}&tbm=isch"
driver.get(url)
time.sleep(3)

try:
    # 화면 끝까지 스크롤 내리기
    print("이미지를 불러오기 위해 스크롤을 내립니다...")
    for i in range(3):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        print(f" - {i + 1}번째 스크롤 완료")

    # 화면에 있는 이미지 태그(<img>) 모두 찾기
    print("이미지 주소를 추출합니다...")
    images = driver.find_elements(By.CSS_SELECTOR, "img")

    count = 1
    max_images = 5  # 다운로드할 최대 이미지 개수

    for img in images:
        if count > max_images:
            break

        img_url = img.get_attribute("src") or img.get_attribute("data-src")

        if img_url:
            exclude_keywords = [
                "/tia/tia.png",  # 가상 키보드 아이콘
                "profile/picture",  # 구글 계정 프로필 사진
                "/branding/",  # 구글 로고
                "favicon"  # 탭 아이콘
            ]

            if any(keyword in img_url for keyword in exclude_keywords):
                continue
            # 주소에 gstatic.com이 있는데, 'encrypted-tbn'이 없다면 구글의 잡다한 UI 아이콘으로 유추 후 skip
            if "gstatic.com" in img_url and "encrypted-tbn" not in img_url:
                continue

            # 정상적인 이미지 다운로드
            if img_url.startswith("http"):
                file_path = os.path.join(folder_name, f"{count}.jpg")

                # 구글 서버에 사람인 척 이미지 다운로드 요청
                opener = urllib.request.build_opener()
                opener.addheaders = [
                    ('User-Agent',
                     'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36')
                ]
                urllib.request.install_opener(opener)

                try:
                    urllib.request.urlretrieve(img_url, file_path)
                    print(f"[{count}/{max_images}] 이미지 저장 완료: {file_path}")
                    count += 1
                    time.sleep(0.5)
                except Exception as down_error:
                    print(f"[{count}] 다운로드 실패: {down_error}")

    print("\n모든 이미지 다운로드가 완료되었습니다!")

except Exception as e:
    print(f"오류가 발생했습니다: {e}")

finally:
    time.sleep(2)
    driver.quit()