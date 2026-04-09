#Automated AjouUniv Notice Alert

아주대학교 미래모빌리티공학과 공지사항, 아주대학교 미래자동차 혁신융합단 공지사항에서 새 글을 읽어 메일로 자동 전송

##사용한 기술
-Python
-WebCrawling

##실행방법
1. 깃클론
git clone https://github.com/imozin0323/Automatic-AjouUniv-Notice-Alerts-using-Webcrawling.git
2. 가상환경 설정. 
source requests/bin/activate
3. 크론탭 편집기 진입
crontab -e
4. 크론탭 설정1 (미래모빌리티공학과 공지글)
0 * * * * {가상환경 내 파이썬 경로} {프로젝트 폴더 경로}/WebCrawling/url_Mobility.py
5. 크론탭 설정2 (미래자동차 공지글)
2 * * * * {가상환경 내 파이썬 경로} {프로젝트 폴더 경로}/WebCrawling/url_FutureCar.py
6. 저장소 초기화. latest_URL_FutureCar.txt, latest_URL_Mobility.txt 내부 내용 삭제
7. cd 프로젝트명
8. python url_FutureCar.py
9. python url_Mobility.py

##주의사항
인텔 맥에서의 환경임.
크론탭 자동 실행시간에 네트워크 연결 필요
python url_FutureCar.py, python url_Mobility.py의 from_email, to_email, password에 본인 정보 입력 필요
테스트시 저장소 초기화 필요
반드시 가상환경 진입 후 실행

##개발목적
아주대학교 공지사항들을 같은 과 학생들에게 자동으로 전송해 학교생활의 편의성 개선
