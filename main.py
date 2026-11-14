from modules.health_db import healthmanage, healthdata, FORMATS
def main():
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

    for fmt in FORMATS:    # 4가지 형식으로 저장 (save_json, save_csv, ... 호출)
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