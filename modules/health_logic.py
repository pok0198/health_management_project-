# 판다스 모듈 불러오기
import pandas as pd

FIELDS = ["id", "name", "birth_year", "gender", "height", "weight", "bmi", "status"]


# 파일 경로 연동 및 딕셔너리 변환
json = pd.read_json('data/health_data.json', encoding='utf-8')
dic = {f"{json}"}

# 데이터 프레임
df = pd.DataFrame(dic, index = ["실험"])
print(df)

