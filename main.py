from modules import Health_db

db = Health_db()

db.add_record(
    "홍길동", "2000-01-01", "남성",
    175, 70, 22.86, "정상"
)

# 네 가지 형식 저장
for fmt in ["json", "csv", "txt", "pkl"]:
    db.save(fmt)

# JSON 불러오기
db.load("json")

for record in db.records:
    print(record.to_dict())