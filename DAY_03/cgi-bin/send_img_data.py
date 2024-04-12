### 모듈 로딩
import cgi, sys, codecs, cgitb, datetime

cgitb.enable()

sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())

# 웹페이지의 form 태그 내의 input 태그 입력값 가져와서
# 저장하고 있는 인스턴스
form = cgi.FieldStorage()

# 클라이언트의 요청 데이터 추출
if "img_file" in form and "message" in form:
    fileitem = form["img_file"]

    # 서버에 이미지 파일 저장
    # img_file = fileitem.filename.rsplit(".")[-1]
    extension = "." + fileitem.filename.rsplit(".")[-1]

    # suffix = datetime.datetime.now().strftime("%y%m%d_%H%M%S") + '.' + img_file
    img_file = datetime.datetime.now().strftime("%y%m%d_%H%M%S") + extension

    save_path = f"./image/{img_file}"
    with open(save_path, "wb") as f:
        f.write(fileitem.file.read())

    img_path = f"../image/{img_file}"
    msg = form.getvalue("message")
else:
    img_path = "None"
    msg = "None"

print("Content-type: text/html; charset=utf-8\n")

print("<TITLE>CGI script output</TITLE>")
print("<H1>This is my first CGI script</H1>")
print(f"Hello, world!<br>")
print("<br>")
print(f"<img src={img_path} alt='고양이 사진'>")
print(f"<h3> {msg} </h3>")
