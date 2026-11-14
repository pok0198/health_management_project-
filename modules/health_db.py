# 모듈 불러오기
import csv
import json
import pickle

# data 파일에 연결하기 
from pathlib import Path # 
data_dir = Path(__file__).resolve().parent.parent / "data" # data 파일 주소 위치

FIELDS = ["id", "name", "birth_year", "gender", "height", "weight", "bmi", "status"]
FORMATS = ["json", "csv", "txt", "pkl"]    # 지원하는 파일 형식 목록

# 레코드 클래스 만들기(height, weight, bmi 실수로 저장하기)
class healthdata:
    """한 사람의 건강정보(식별번호, 이름, 생년, 성별, 키, 몸무게, BMI, 비만도)를 담는 레코드 클래스."""
    def __init__(self, id, name, birth_year, gender, height, weight, bmi, status):
        """값을 속성으로 저장한다. birth_year는 int, height/weight/bmi는 float으로 변환한다."""
        self.id = id
        self.name = name
        self.birth_year = int(birth_year)
        self.gender = gender
        self.height = float(height)
        self.weight = float(weight)
        self.bmi = float(bmi)
        self.status = status

    # 딕셔너리로 변환하기
    def to_dict(self): 
        """레코드를 딕셔너리로 바꿔 반환한다. (파일 저장용)"""
        return{
            "id": self.id,
            "name": self.name,
            "birth_year": self.birth_year,
            "gender": self.gender,
            "height": self.height,
            "weight": self.weight,
            "bmi": self.bmi,
            "status": self.status
            }

# 식별번호 자동 생성 만들기
id_auto = "P2026-"  # 식별번호 앞부분

class healthmanage:
    """건강정보 레코드 목록을 관리하고 파일로 저장/불러오기를 하는 클래스."""
    def __init__(self):
        self.records = []   # 레코드 객체 저장 리스트

    def generate_id(self):
        """기존 식별번호 중 가장 큰 번호에 1을 더해 새 식별번호(예: P2026-0001)를 반환한다."""
        maxnum = 0  
        for r in self.records:
            num = int(r.id.split("-")[1])
            maxnum = max(maxnum, num)
        return f"{id_auto}{maxnum + 1:04d}"



    # 여기부터 파일 연결 코드
    # [AI 사용 기록]
    # - AI 종류   : Claude
    # - 사용 목적 : 직접 작성한 import/data_dir 코드를 바탕으로 JSON/CSV/TXT/Pickle 저장·불러오기 작성
    # - 프롬프트  : 해당 코드를 바탕으로 다중 파일 I/O(save/load) 만들어줘 그리고 이 코드 이해할 수 있게 설명란도 따로 작성해줘"
    # - 사용한 사람: 황현준
    # - 사용 날짜 : 2026-11-14

    def save(self,fmt = "json"):    # 세이브
        """records를 fmt 형식(json/csv/txt/pkl)의 파일로 저장한다. 성공하면 True, 실패하면 False를 반환한다."""
        path = data_dir / f"health_data.{fmt}"  # 저장할 파일의 경로 및 이름 지정
        rows = [r.to_dict() for r in self.records] # 레코드 -> 딕셔너리 리스트

        try:
            data_dir.mkdir(exist_ok=True)   # data 폴더 생성 

            if fmt == "json":   # json 형식
                with open(path, "w", encoding="utf-8") as f:
                    json.dump(rows, f, ensure_ascii=False, indent=2)

            elif fmt == "csv":  # csv 형식
                with open(path, "w", encoding="utf-8", newline="") as f:
                    writer = csv.DictWriter(f, fieldnames=FIELDS)
                    writer.writeheader()
                    writer.writerows(rows)

            elif fmt == "txt":  # txt 형식
                with open(path, "w", encoding="utf-8") as f:
                    for d in rows:
                        f.write(",".join(str(d[k]) for k in FIELDS) + "\n")

            elif fmt == "pkl":  # pkl 형식
                with open(path, "wb") as f:
                    pickle.dump(rows, f)

            else:   # 이상한 파일 형식
                print(f"지원하지 않는 형식: {fmt}")
                return False
            
            return True
        
        except OSError as e:    # 오류 발생을때 나오게 하기
            print(f"저장 실패: {e}")
            return False


    def load(self, fmt = "json"):   # 로드
        """fmt 형식의 파일을 읽어 records를 채우고 반환한다. 파일이 없거나 깨졌으면 빈 리스트를 반환한다."""
        path = data_dir / f"health_data.{fmt}"
        self.records = []
        try:
            if fmt == "json":   # json 형식
                with open(path, "r", encoding="utf-8") as f:
                    rows = json.load(f)

            elif fmt == "csv":  # csv 형식
                with open(path, "r", encoding="utf-8-sig", newline="") as f:
                    rows = list(csv.DictReader(f))

            elif fmt == "txt":  # txt 형식
                with open(path, "r", encoding="utf-8") as f:
                    rows = [dict(zip(FIELDS, line.strip().split(",")))
                            for line in f if line.strip()]
                    
            elif fmt == "pkl":  # pkl 형식
                with open(path, "rb") as f:
                    rows = pickle.load(f)

            else:   # 이상한 파일 
                print(f"지원하지 않는 형식: {fmt}")
                return self.records
            
        except FileNotFoundError:   # 파일 없을때
            print("파일이 없습니다. 빈 목록으로 시작합니다.")
            return self.records
            
        except (OSError, ValueError, csv.Error, pickle.UnpicklingError, EOFError) as e: # 오류 
            print(f"불러오기 실패: {e}")
            return self.records


        for row in rows:
            try:
                self.records.append(healthdata(**row)) # 딕셔너리 데이터를 healthdata로 변환시키기
            except (TypeError, ValueError) as e:    # 데이터 건너뛰기
                print(f"잘못된 데이터 건너뜀: {e}")

        return self.records # 리스트 반환



    # 건강정보 객체 추가
    def add(self, record):
        """건강정보 객체 하나를 목록에 추가한다."""
        self.records.append(record)

    # 목록 화면에 출력
    def print_all(self):
        """목록의 모든 건강정보를 한 줄씩 화면에 출력한다."""
        if not self.records:
            print("  (데이터 없음)")
            return
        for r in self.records:
            print(f"  {r.id} | {r.name} | {r.birth_year}년생 | {r.gender} | "
                  f"{r.height}cm | {r.weight}kg | BMI {r.bmi} | {r.status}")

    # 형식별 저장 메서드 (위의 save를 형식 이름만 정해서 호출)
    def save_json(self): return self.save("json")
    def save_csv(self): return self.save("csv")
    def save_txt(self): return self.save("txt")
    def save_pkl(self): return self.save("pkl")

    # 형식별 읽기 메서드 (위의 load를 형식 이름만 정해서 호출)
    def load_json(self): return self.load("json")
    def load_csv(self): return self.load("csv")
    def load_txt(self): return self.load("txt")
    def load_pkl(self): return self.load("pkl")


# 저장 전 값과 저장된 값이 일치하는지 검증
def main():
    """샘플 데이터를 4가지 형식으로 저장한 뒤 다시 읽어서 원래 정보와 일치하는지 검증한다."""
    mgr = healthmanage()
    samples = [
        ("홍길동", 1995, "남", 175.0, 72.5, 23.67, "과체중"),
        ("김영희", 1998, "여", 162.0, 52.0, 19.81, "정상"),
        ("박철수", 1990, "남", 170.0, 85.0, 29.41, "비만"),
    ]
    for name, year, gender, height, weight, bmi, status in samples:
        mgr.add(healthdata(mgr.generate_id(), name, year, gender, height, weight, bmi, status))

    print("[저장 전 목록]")
    mgr.print_all()
    original = [r.to_dict() for r in mgr.records]    # 비교용 원본

    for fmt in FORMATS:    # 4가지 형식으로 저장 (save_json, save_csv, 등등 호출)
        ok = getattr(mgr, f"save_{fmt}")()
        print(f"\n[{fmt.upper()} 저장] {'성공' if ok else '실패'}")

    for fmt in FORMATS:    # 4가지 파일을 각각 읽어서 원본과 비교
        loaded = healthmanage()
        getattr(loaded, f"load_{fmt}")()
        print(f"\n[{fmt.upper()} 읽기]")
        loaded.print_all()
        same = [r.to_dict() for r in loaded.records] == original
        print(f"  -> 원래 정보와 {'일치' if same else '불일치'}")


if __name__ == "__main__":
    main()