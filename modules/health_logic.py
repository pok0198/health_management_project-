# 판다스 모듈 및 json 모듈 불러오기 & 실험 단계
import pandas as pd
import json

with open('data/health_data.json', 'r', encoding = 'utf-8') as f:
    md = json.load(f)

# 실험
qwer = pd.DataFrame(md)

if qwer.duplicated(keep=False) == True: