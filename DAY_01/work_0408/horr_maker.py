import numpy as np
import pandas as pd
import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
from torch.utils.data import Dataset, DataLoader
from torchmetrics.functional import accuracy, f1_score

horrorDF = pd.read_excel(
    "2조 괴담 파일.xlsx", skiprows=0, header=1, sheet_name="SY", usecols=[3]
)

horrorSR = horrorDF["TEXT"].str.replace(r"[^ㄱ-ㅎㅏ-ㅣ가-힣a-zA-Z\d ]", "", regex=True)

print(horrorSR.info())
