### 모듈 로딩
import cgi, sys, codecs

sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())

# 웹페이지의 form 태그 내의 input 태그 입력값 가져와서
# 저장하고 있는 인스턴스
form = cgi.FieldStorage()

if "img_file" in form and "message" in form:
    filename = form["img_file"].value
    msg = form["message"].value

print("Content-type: text/html; charset=utf-8\n")

print("<TITLE>CGI script output</TITLE>")
print("<H1>This is my first CGI script</H1>")
print(f"Hello, world! : {form}<br>")
print("<br")
print(f"<img src={filename} alt={msg}>")
print(f"<h3> {msg} </h3>")
