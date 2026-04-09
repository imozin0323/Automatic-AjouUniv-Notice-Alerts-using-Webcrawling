import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import smtplib
from email.message import EmailMessage
import os

# 1. 메일 전송 함수
def send_email(subject, body, to_email):
    from_email = "hoim03@ajou.ac.kr"
    password = "qclb qtmw tfah hoxk" 
    
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
            to_email="hoim03@ajou.ac.kr"
        )
        print("이메일 전송 완료!")
    except Exception as e:
        print(f"이메일 전송 중 오류 발생: {e}")
else:
    print("새로운 공지사항이 없습니다.")
    
'''import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import smtplib
from email.message import EmailMessage

#메일 전송
def send_email(subject, body, to_email):
    # 보내는 사람 정보
    from_email = "hoim0323@gmail.com"
    password = "wolv eois kjgp jyiz"  # Gmail 앱 비밀번호

    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = from_email
    msg["To"] = to_email
    msg.set_content(body)

    # Gmail SMTP 서버 연결
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(from_email, password)
        smtp.send_message(msg)


#웹 크롤링
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
base_url = "https://mobility.ajou.ac.kr/mobility/board/notice.do"
file_name = "latest_URL.txt"


def fetch_latest_posts():
    res = requests.get(base_url, headers=headers)
    soup = BeautifulSoup(res.text, "html.parser")

    notice_posts = []
    normal_posts = []

    for a in soup.select("a[href*='articleNo=']"):
        href = a.get("href")
        if "mode=view" not in href:
            continue
        full_url = urljoin(base_url, href)
        is_notice = a.select_one("span.b-notice") is not None

        if is_notice:
            notice_posts.append(full_url)
        else:
            normal_posts.append(full_url)

    latest_notice = notice_posts[0] if notice_posts else None
    latest_normal = normal_posts[0] if normal_posts else None

    return {"공지글": latest_notice, "일반글": latest_normal}

# 기존 기록 불러오기
latest_dict = {"공지글": None, "일반글": None}
try:
    with open(file_name, "r", encoding="utf-8") as f:
        for line in f:
            if ":" in line:
                key, value = line.strip().split(":", 1)
                latest_dict[key] = value
except FileNotFoundError:
    pass

# 최신 글 가져오기
fetched_dict = fetch_latest_posts()
new_posts_found = []  # 새로 발견된 글을 저장할 리스트

# 비교 및 감지 로직
for key in ["공지글", "일반글"]:
    fetched_url = fetched_dict.get(key)
    saved_url = latest_dict.get(key)
    
    # 새 글이 발견된 경우
    if fetched_url and fetched_url != saved_url:
        print(f"새 {key} 발견: {fetched_url}")
        new_posts_found.append(f"새 {key}: {fetched_url}")
        latest_dict[key] = fetched_url  # 메모리 상의 데이터 갱신

# 새 글이 하나라도 있다면 실행
if new_posts_found:
    # 1. 파일 업데이트 (latest_URL.txt 갱신)
    with open(file_name, "w", encoding="utf-8") as f:
        for key in ["공지글", "일반글"]:
            if latest_dict[key]:
                f.write(f"{key}:{latest_dict[key]}\n")

    # 2. 이메일 내용 작성
    email_body = "\n".join(new_posts_found)

    # 3. 이메일 전송
    try:
        send_email(
            subject="Ajou Mobility 새 공지 알림",
            body=email_body,
            to_email="hoim03@ajou.ac.kr"
        )
        print("이메일 전송 완료!")
    except Exception as e:
        print(f"이메일 전송 중 오류 발생: {e}")
else:
    print("새로운 공지사항이 없습니다.")


'''


'''import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import time

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
base_url = "https://mobility.ajou.ac.kr/mobility/board/notice.do"
file_name = "latest_URL.txt"
check_interval = 3600

res = requests.get(base_url, headers=headers)
soup = BeautifulSoup(res.text, "html.parser")

notice_posts = []
normal_posts = []

for a in soup.select("a[href*='articleNo=']"):
    href = a.get("href")
    
    #첨부파일 제외
    if "mode=view" not in href:
        continue
    
    full_url = urljoin(base_url, href)

    # 공지글, 일반글 판단
    is_notice = a.select_one("span.b-notice") is not None
    if is_notice:
        notice_posts.append(full_url)
    else:
        normal_posts.append(full_url)

latest_notice = notice_posts[0]
latest_normal = normal_posts[0]

with open(file_name, "w", encoding="utf-8") as f:
    if latest_notice:
        f.write(latest_notice + "\n")
    if latest_normal:
        f.write(latest_normal + "\n")
        '''