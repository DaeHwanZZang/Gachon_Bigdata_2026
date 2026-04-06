#!/bin/bash

echo "=================================================="
echo "  가천대학교 빅데이터 과제 자동 실행 스크립트"
echo "=================================================="

echo "[1/3] 가상환경 확인 중..."
if [ ! -d "venv" ]; then
    echo "가상환경이 없어서 새로 생성합니다. (잠시만 기다려주세요)"
    python3 -m venv venv
fi

echo "[2/3] 라이브러리 설치 및 업데이트 중..."
source venv/bin/activate
pip install --upgrade pip --quiet
pip install -r requirements.txt --quiet

echo "[3/3] 실행할 과제를 선택하세요."
echo "--------------------------------------------------"
echo "  1. 구글 플레이 스토어 리뷰 크롤링 (Task 1)"
echo "  2. 구글 이미지 검색 크롤링 (Task 2)"
echo "  3. 종료"
echo "--------------------------------------------------"

read -p "번호를 입력하고 엔터를 치세요 (1/2/3): " choice

if [ "$choice" == "1" ]; then
    echo "[Task 1] 실행 중..."
    python3 task1_playstore.py
elif [ "$choice" == "2" ]; then
    echo "[Task 2] 실행 중..."
    python3 task2_google_image.py
elif [ "$choice" == "3" ]; then
    echo "프로그램을 종료합니다."
    exit 0
else
    echo "잘못된 번호입니다. 다시 실행해 주세요."
fi

echo "--------------------------------------------------"
echo "모든 작업이 완료되었습니다."
