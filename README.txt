본 코드 목적 : 아주대 미래모빌리티 공지사항에 새 글이 올라올 시 메일로 해당 글 URL 전송

파일명
- requests : 파이썬 가상환경 폴더
- latest_URL.txt : 공지글, 일반글의 마지막 URL 저장 텍스트파일
- url.py : 아주대 미래모빌리티 공지사항 웹크롤링, 새 글인지 확인, 메일 전송


주의 사항
- crontab으로 3시간마다 url.py실행. vscode는 종료해도 되나 로컬 컴퓨터가 꺼진경우 실행 불가
- crontab 명령어 설명:
crontab -e => 크롬탭 편집기 실행
crontab -l => 크롬탭 리스트 확인
* */3 * * * => 모든 분 3시간마다 모든 날 모든 월 모든 년 에 실행. 
~~bin/python3 => 가상환경내 파이썬 경로. (which python3 로 확인)
~~url.py => 파이썬 스크립트 절대경로

- 스크립트 실행 시간에 네트워크 접속 없으면 실행 실패
- password는 gmail앱 비밀번호로, 계정 비밀번호와 다름
- 테스트시 latest_URL.txt 내부 내용 삭제하고 url.py 실행.
- 실행시 반드시 가상환경 진입 후 실행. (requests) imhojin@imhojin-ui-MacBookAir WebCrawling % source requests/bin/activate