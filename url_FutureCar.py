import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import smtplib
from email.message import EmailMessage
import os

# 1. 메일 전송 함수
def send_email(subject, body, to_email):
    from_email = "{your email adress}"
    password = "{your email app password}" 
    
    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = from_email
    msg["To"] = to_email
    msg.set_content(body)

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(from_email, password)
        smtp.send_message(msg)

# 2. 웹 크롤링 함수 (리스트를 사용하여 순서 유지)
def fetch_all_posts():
    headers = {'User-Agent': 'Mozilla/5.0'}
    
    base_url = "https://future-car.ajou.ac.kr/bbs/board.php?bo_table=04_01"
    
    res = requests.get(base_url, headers=headers)
    soup = BeautifulSoup(res.text, "html.parser")
    
    current_urls = []

    # 게시글 링크 찾기 (wr_id 포함)
    for a in soup.select("a[href*='wr_id=']"):
        href = a.get("href")

        if not href:
            continue

        full_url = urljoin("https://future-car.ajou.ac.kr/", href)

        # 중복 방지
        if full_url not in current_urls:
            current_urls.append(full_url)

    return current_urls

# 3. 메인 로직
file_name = "/Users/imhojin/Documents/code/WebCrawling/latest_URL_FutureCar.txt"

# 기존에 저장된 URL 불러오기 (순서 상관없이 비교용으로 set 변환)
if os.path.exists(file_name):
    with open(file_name, "r", encoding="utf-8") as f:
        saved_urls = set(line.strip() for line in f if line.strip())
else:
    saved_urls = set()

# 현재 페이지의 모든 URL 가져오기 (홈페이지 순서 그대로)
current_urls = fetch_all_posts()

# 새롭게 올라온 글만 추출 (순서 유지)
new_posts = [url for url in current_urls if url not in saved_urls]

if new_posts:
    print(f"{len(new_posts)}개의 새 글 발견!")
    
    # 4. 파일 업데이트 (홈페이지에서 긁어온 순서대로 저장)
    with open(file_name, "w", encoding="utf-8") as f:
        for url in current_urls:
            f.write(url + "\n")
            
    # 5. 이메일 내용 작성 (새 글들도 순서대로 나열)
    email_body = "새로 등록된 공지사항 링크입니다:\n\n" + "\n".join(new_posts)
    
    try:
        send_email(
            subject=f"Ajou Future Car 새 공지 알림 ({len(new_posts)}건)",
            body=email_body,
            to_email="{your email adress}"
        )
        print("이메일 전송 완료!")
    except Exception as e:
        print(f"이메일 전송 중 오류 발생: {e}")
else:
    print("새로운 공지사항이 없습니다.")
    
