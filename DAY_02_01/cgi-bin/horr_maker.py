###-==> 모듈 로딩
import numpy as np
import pandas as pd
import torch, pickle
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
from torch.utils.data import Dataset, DataLoader
from torchmetrics.functional import accuracy, f1_score
import cgi, sys, codecs, os, cgitb

## -----------------------------------------------------------------
## WEB 인코딩 설정
## -----------------------------------------------------------------
sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())


## -----------------------------------------------------------------
## 전역 변수 설정
## -----------------------------------------------------------------
device = "cuda" if torch.cuda.is_available() else "cpu"

file_dir = os.path.dirname(__file__)

with open(file_dir + "/char_set_small.pkl", "rb") as f:
    char_set = pickle.load(f)

char_to_id = {char: idx for idx, char in enumerate(char_set)}
id_to_char = {idx: char for idx, char in enumerate(char_set)}
dict_size = len(char_to_id)


## -----------------------------------------------------------------
## 사용자 정의 클래스
## -----------------------------------------------------------------
class CharGRU(nn.Module):
    def __init__(self, dict_size, hidden_size, n_layers) -> None:
        super().__init__()
        self.gru = nn.GRU(
            input_size=dict_size,
            hidden_size=hidden_size,
            num_layers=n_layers,
            batch_first=True,
            bidirectional=True,
        )
        self.linear = nn.Linear(hidden_size * 2, dict_size)
        self.init_weights()

    def init_weights(self):
        initrange = 0.5
        self.linear.weight.data.uniform_(-initrange, initrange)
        self.linear.bias.data.zero_()

    def forward(self, text):
        output, _ = self.gru(text)
        return self.linear(output)


## -----------------------------------------------------------------
## 사용자 정의 함수
## -----------------------------------------------------------------
def predict(model, word):
    pred_text = []
    for char in word:
        if char in char_to_id.keys():
            pred_text.append(
                F.one_hot(torch.tensor(char_to_id[char]), dict_size).float()
            )
        else:
            pred_text.append(
                F.one_hot(torch.tensor(char_to_id[" "]), dict_size).float()
            )
    pred_text = torch.stack(pred_text).to(device)
    model.eval()
    with torch.no_grad():
        pred_num = model(pred_text).argmax(1).tolist()
        result = "".join([id_to_char[i] for i in pred_num])
    return result


def make_sentence(model, start, num=100, stopword="."):
    sentence = start
    for _ in range(num):
        next_char = predict(model, sentence[-10:])
        sentence += next_char[-1]
        if next_char[-1] in stopword:
            break
    return sentence


### ==> Web 브라우저 화면 출력 코드
def display_browser(result=""):
    # HTML 파일 읽기 -> body 문자열
    filename = "./html/horror.html"
    with open(filename, "r", encoding="utf-8") as f:
        # HTML Header
        print("Content-Type: text/html; charset=utf-8")
        print()
        # HTML Body
        print(f.read().format(result))


## -----------------------------------------------------------------
## 요청 처리 및 브라우징
## -----------------------------------------------------------------
model = torch.load(file_dir + "/classifier_512_2.pt", map_location=device)

### ==> Client 요청 데이터 즉, Form 데이터 저장 인스턴스
form = cgi.FieldStorage()

### ==> 데이터 추출
if "data" in form:
    result = form.getvalue("data")
else:
    result = "No Data"

if result == "No Data":
    msg = "No Data"
else:
    msg = make_sentence(model, result, num=200, stopword=".")

display_browser(msg)
