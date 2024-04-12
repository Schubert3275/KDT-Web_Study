import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
from PIL import Image
import cgi, os, sys, codecs, datetime

sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())


class AnimalModule(nn.Module):
    def __init__(self, in_, out_):
        super().__init__()
        self.conv1 = nn.Conv2d(in_channels=in_, out_channels=10, kernel_size=5)
        self.conv2 = nn.Conv2d(in_channels=10, out_channels=20, kernel_size=3)
        self.pool1 = nn.MaxPool2d(kernel_size=2)
        self.pool2 = nn.MaxPool2d(kernel_size=3)
        self.f1 = nn.Linear(7 * 7 * 20, 100)
        self.out_layer = nn.Linear(100, out_)

    def forward(self, x):
        x = F.relu(self.conv1(x))
        x = self.pool1(x)
        x = F.relu(self.conv2(x))
        x = self.pool2(x)

        x = x.view(-1, 7 * 7 * 20)
        x = F.relu(self.f1(x))
        x = self.out_layer(x)
        return x


def predict_animal(model, img):
    animal_dict = {0: "고양이", 1: "강아지", 2: "코끼리", 3: "말", 4: "사자"}
    image = Image.open(img).convert("RGB")
    resized_image = image.resize((50, 50))
    test_img = torch.FloatTensor(np.array(resized_image)).permute(2, 0, 1).unsqueeze(0)

    result = model(test_img).argmax().item()
    return animal_dict[result]


def display_browser(img_path="", img_name="", result=""):
    # HTML 파일 읽기 -> body 문자열
    filename = "./html/animal_class.html"
    with open(filename, "r", encoding="utf-8") as f:
        # HTML Header
        print("Content-Type: text/html; charset=utf-8")
        print()
        # HTML Body
        print(f.read().format(img_path, img_name, result))


form = cgi.FieldStorage()

if "img_file" in form:
    fileitem = form["img_file"]

    # 서버에 이미지 파일 저장
    filename = fileitem.filename.rsplit(".")[:-1][0]
    extension = "." + fileitem.filename.rsplit(".")[-1]

    img_file = datetime.datetime.now().strftime("%y%m%d_%H%M%S") + extension

    save_path = f"./image/{img_file}"
    with open(save_path, "wb") as f:
        f.write(fileitem.file.read())

    img_path = f"../image/{img_file}"
else:
    img_path = "None"
    filename = "None"


model = torch.load("./model/animal_model.pth")
result = predict_animal(model, save_path)

display_browser(img_path, filename, result)
