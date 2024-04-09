import numpy as np
import pandas as pd
import torch, pickle
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
from torch.utils.data import Dataset, DataLoader
from torchmetrics.functional import accuracy, f1_score


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


device = "cuda" if torch.cuda.is_available() else "cpu"

with open("./char_set_small.pkl", "rb") as f:
    char_set = pickle.load(f)

char_to_id = {char: idx for idx, char in enumerate(char_set)}
id_to_char = {idx: char for idx, char in enumerate(char_set)}
dict_size = len(char_to_id)

model = torch.load("./classifier_512_2.pt", map_location=device)

print(make_sentence(model, "빅데이터", num=200, stopword="."))
