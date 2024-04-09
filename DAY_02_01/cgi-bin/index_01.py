###-==> 모듈 로딩
import cgi, sys, codecs, os, cgitb

## -----------------------------------------------------------------
## WEB 인코딩 설정
## -----------------------------------------------------------------
sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())


## -----------------------------------------------------------------
## 사용자 정의 함수
## -----------------------------------------------------------------
### ==> Web 브라우저 화면 출력 코드
def display_browser(result=""):
    # HTML 파일 읽기 -> body 문자열
    filename = "./html/test.html"
    with open(filename, "r", encoding="utf-8") as f:
        # HTML Header
        print("Content-Type: text/html; charset=utf-8")
        print()
        # HTML Body
        print(f.read().format(result))


## -----------------------------------------------------------------
## 요청 처리 및 브라우징
## -----------------------------------------------------------------
### ==> Client 요청 데이터 즉, Form 데이터 저장 인스턴스
form = cgi.FieldStorage()

### ==> 데이터 추출
if "data" in form and "no" in form:
    result = form.getvalue("data") + " - " + form.getvalue("no")
else:
    result = "No Data"


display_browser(result)
