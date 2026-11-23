"""모듈 2: 비즈니스 로직(CRUD + 통계) 및 콘솔(TUI) 테스트 앱."""
import statistics
from datetime import date

# bmi 코드 만들기 전에 팀과제로 만들어놨던 bmi코드 가져오기
def calculate_bmi(height, weight):
    """BMI = 체중 / (키/100)^2 을 소수 첫째 자리까지 계산한다."""
    return round(weight / (height / 100) ** 2, 1)


def judge_status(bmi):
    """BMI로 비만도를 판정한다."""
    if bmi < 18.5:
        return "저체중"
    if bmi < 23:
        return "정상"
    if bmi < 25:
        return "과체중"
    if bmi < 30:
        return "1단계 비만"
    if bmi < 35:
        return"2단계 비만"
    return "3단계 비만"
    

def check_body(height, weight):
    """키/몸무게가 현실적인 범위가 아니면 ValueError."""
    if not (50 <= height <= 250 and 10 <= weight <= 300):
        raise ValueError("키(50~250cm)나 몸무게(10~300kg) 범위가 올바르지 않습니다.")


class HealthManager(healthmanage):
    """healthmanage에 추가/조회/수정/삭제/통계 메소드를 더한 클래스 (메모리 데이터만 관리)."""

    def add_health(self, name, birth_year, gender, height, weight):
        """검증 후 BMI/비만도를 계산해 레코드를 추가하고 반환한다. 잘못된 값/중복이면 ValueError."""
        name = name.strip()
        if not name or gender not in ("남", "여") or not 1900 <= birth_year <= date.today().year:
            raise ValueError("이름, 성별(남/여), 생년을 확인하세요.")
        check_body(height, weight)
        
        if any((r.name, r.birth_year, r.gender) == (name, birth_year, gender) for r in self.records):
            raise ValueError("이미 등록된 사람입니다. (이름·생년·성별 동일)")
        bmi = calculate_bmi(height, weight)
        record = healthdata(self.generate_id(), name, birth_year, gender,
                            height, weight, bmi, judge_status(bmi))
        self.add(record)
        return record

    # [AI 사용 기록]
    # - AI 종류   : Claude
    # - 사용 목적 : choice에 들어갈 선택 함수 만들기
    # - 프롬프트  : choice는 대충 만들었는데 그안에 함수를 어떤식으로 만들지 감이 안잡히는데 틀만 좀 만들어줘
    # - 사용한 사람: 황현준
    # - 사용 날짜 : 2026-11-23

    def get_all(self):
        """전체 레코드 목록(복사본)을 반환한다."""
        return list(self.records)

    def find_by_id(self, record_id):
        """식별번호가 일치하는 레코드를 반환한다. 없으면 None."""
        return next((r for r in self.records if r.id == record_id), None)

    def search_by_name(self, keyword):
        """이름에 keyword가 포함된 레코드 목록을 반환한다."""
        return [r for r in self.records if keyword in r.name]

    def update_health(self, record_id, height, weight):
        """키/몸무게를 수정하고 BMI·비만도를 재계산한다. 대상이 없거나 값이 잘못되면 ValueError."""
        record = self.find_by_id(record_id)
        if record is None:
            raise ValueError("해당 식별번호의 데이터가 없습니다.")
        check_body(height, weight)
        record.height, record.weight = height, weight
        record.bmi = calculate_bmi(height, weight)
        record.status = judge_status(record.bmi)
        return record

    def delete_health(self, record_id):
        """식별번호의 레코드를 삭제한다. 지웠으면 True, 없으면 False."""
        record = self.find_by_id(record_id)
        if record:
            self.records.remove(record)
        return record is not None

    def get_statistics(self):
        """레코드 수와 키/몸무게/BMI의 (평균, 표준편차)를 딕셔너리로 반환한다."""
        stats = {"count": len(self.records)}
        if self.records:
            for field in ("height", "weight", "bmi"):
                values = [getattr(r, field) for r in self.records]
                stats[field] = (statistics.mean(values), statistics.pstdev(values))
        return stats



# 출력 함수 (클래스 밖에서 출력 담당)
def format_record(r):
    return (f"{r.id} | {r.name} | {r.birth_year}년생 | {r.gender} | "
            f"{r.height}cm | {r.weight}kg | BMI {r.bmi} | {r.status}")


def print_records(records):
    for r in records:
        print("  " + format_record(r))
    print(f"  -> 총 {len(records)}건")


def print_statistics(stats):
    print(f"  전체 인원수: {stats['count']}명")
    for field, label in (("height", "키"), ("weight", "몸무게"), ("bmi", "BMI")):
        if field in stats:
            print(f"  {label} 평균 {stats[field][0]:.2f} | 표준편차 {stats[field][1]:.2f}")


MENU = """
---------------- 건강정보 관리 시스템 ----------------
 1. 추가
 2. 목록 조회
 3. 검색 및 상세조회
 4. 수정 및 삭제
 5. 통계조회
 6. 파일에서 가져오기 (모듈1)
 7. 파일로 저장 (모듈1)
 0. 종료"""



    # [AI 사용 기록]
    # - AI 종류   : Claude
    # - 사용 목적 : 위 코드들을 바탕으로 수정 기능과 정보 저장 기능 만들기
    # - 프롬프트  : choice 기능을 사용해서 프롬프트에 사용자가 대답한 결과에 따라 결과가 나오게 출력하고 싶어 대부분 만들어놨는데 수정 기능이랑 정보 저장기능을 못만들겠어 도와줘
    # - 사용한 사람: 황현준
    # - 사용 날짜 : 2026-11-23

def main():
    """콘솔 응용 프로그램: 모듈 1로 파일을 읽어 HealthManager에 넘기고 메뉴를 실행한다."""
    m = HealthManager()
    m.load("json")
    while True:
        print(MENU)
        choice = input("메뉴 선택: ").strip()
        try:
            if choice == "1":       # 이름, 생년, 성별, 키, 몸무게 등록 초이스 코드
                r = m.add_health(input("이름: "), int(input("생년: ")), input("성별(남/여): ").strip(),
                                 float(input("키(cm): ")), float(input("몸무게(kg): ")))
                print("[등록 완료] " + format_record(r))

            elif choice == "2":     # 등록된 정보 모두 출력시키기
                print_records(m.get_all())

            elif choice == "3":     # id 또는 이름으로 검색할수있는 기능
                key = input("식별번호 또는 이름: ").strip()
                r = m.find_by_id(key)
                print_records([r] if r else m.search_by_name(key))
                
            elif choice == "4":     # 기존에 있던 정보 수정 또는 삭제 
                rid = input("대상 식별번호: ").strip()
                sub = input("1. 수정  2. 삭제 : ").strip()
                if sub == "1":
                    r = m.update_health(rid, float(input("새 키(cm): ")), float(input("새 몸무게(kg): ")))
                    print("[수정 완료] " + format_record(r))
                elif sub == "2":
                    print("[삭제 완료]" if m.delete_health(rid) else "[오류] 해당 식별번호가 없습니다.")

            elif choice == "5":     # 건강정보를 바탕으로 통계 출력시키기
                print_statistics(m.get_statistics())

            elif choice == "6":     # json 등 지정된 형식의 데이터 불러오기
                m.load(input(f"형식 {FORMATS} (Enter=json): ").strip() or "json")
                print(f"현재 데이터 {len(m.records)}건")

            elif choice == "7":     # 새로 만든 정보 저장시키기
                if m.save(input(f"형식 {FORMATS} (Enter=json): ").strip() or "json"):
                    print("저장 완료")
            elif choice == "0":
                break
        except ValueError as e:
            print(f"[오류] {e}")