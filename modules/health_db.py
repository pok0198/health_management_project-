# 모듈 불러오기
import csv
import json
import pickle
import ast

# data 파일에 연결하기 
from pathlib import Path # 
data_dir = Path(__file__).parent / "data" # data 파일 주소 위치


class HealthData:
    def __init__(self, name, weight, height, bmi, status):
        self.name = name
        self.weight = float(weight)
        self.height = float(height)
        self.bmi = float(bmi)
        self.status = status

    def to_dict(self):  
        return {
            "name": self.name,
            "weight": self.weight,
            "height": self.height,
            "bmi": self.bmi,
            "status": self.status
        }