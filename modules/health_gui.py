"""모듈 3: Tkinter 기반 GUI 및 이벤트 바인딩 (모듈 2의 HealthManager와 연결)."""
# 모듈 연결
import tkinter as tk # tk 모듈
from tkinter import ttk, messagebox # 더 이쁜 tk 모듈이랑 팝업창

from modules.health_db import FORMATS
from modules.health_logic import HealthManager


# [AI 사용 기록]
# - AI 종류   : Claude
# - 사용 목적 : GUI와 모듈 연결 및 최적화 추가 기능
# - 프롬프트  : GUI틀을 만들어 놨거든? 이 GUI랑 모듈 1,2 연결해줘 그리고 혹시 추가할 기능같은거나 최적화 할 사항 있으면 일단 말해줘
# - 사용한 사람: 황현준
# - 사용 날짜 : 2026-11-24


# 상수
# Treeview 열 정보 (열 이름, 화면에 보이는 제목, 너비)
COLUMNS = [
    ("id", "식별번호", 100),
    ("name", "이름", 80),
    ("birth_year", "생년", 60),
    ("gender", "성별", 50),
    ("height", "키(cm)", 70),
    ("weight", "몸무게(kg)", 80),
    ("bmi", "BMI", 60),
    ("status", "비만도", 90),
]

EMPTY_DETAIL_TEXT = "목록에서 행을 선택하세요."

# GUI 전용 클래스 생성
class HealthManagerGUI:
    """건강정보 관리 GUI. 생성될 때 HealthManager 객체를 만들어 연관시킨다."""


    # 1. 초기화

    def __init__(self, root):
        self.root = root        # 메인 창 객체 저장
        self.root.title("건강정보 관리 시스템 (BMI)")
        self.root.geometry("900x620")

        # 모듈 2의 HealthManager 객체와 연관 (버튼 콜백에서 이 객체의 메소드를 호출)
        self.manager = HealthManager()  # 모듈2 객체 생성
        self.manager.load("json")       # 시작할 때 json 파일 불러오기

        self.selected_id = None         # 목록에서 선택된 식별번호

        self.build_widgets()    # 위젯 만들기
        self.reload_all()       # 불러온 데이터 표시

        # 이벤트 바인딩 창 닫기 버튼누르면 on_close 실행시켜서 한번더 물어보기
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)


    # 2. 화면 만들기 (위젯 배치)
    #    Tkinter Designer 사이트에서 미리 만들어보기
    def build_widgets(self):
        """화면 전체를 영역별로 나누어 만든다."""
        self.build_file_area()      # 1. 파일 (불러오기/내보내기)
        self.build_form_area()      # 2. 입력 (추가/수정/삭제)
        self.build_list_area()      # 3. 목록 / 검색
        self.build_bottom_area()    # 4. 상세 조회 / 통계

    def build_file_area(self):
        """1. 파일 영역: 형식 선택 + 불러오기/내보내기 버튼."""
        file_frame = ttk.LabelFrame(self.root, text="파일 (모듈1)")
        file_frame.pack(fill="x", padx=10, pady=(10, 5))

        ttk.Label(file_frame, text="형식:").pack(side="left", padx=(10, 2), pady=8)
        self.fmt_var = tk.StringVar(value="json")
        ttk.Combobox(file_frame, textvariable=self.fmt_var, values=FORMATS,
                     state="readonly", width=6).pack(side="left", padx=5)
        ttk.Button(file_frame, text="불러오기",
                   command=self.on_load).pack(side="left", padx=5)
        ttk.Button(file_frame, text="내보내기",
                   command=self.on_save).pack(side="left", padx=5)

    def build_form_area(self):
        """2. 입력 영역: 입력칸 + 추가/수정/삭제/초기화 버튼."""
        form_frame = ttk.LabelFrame(self.root, text="건강정보 입력")
        form_frame.pack(fill="x", padx=10, pady=5)

        # 입력값과 연결되는 변수
        self.name_var = tk.StringVar()
        self.birth_var = tk.StringVar()
        self.gender_var = tk.StringVar(value="남")
        self.height_var = tk.StringVar()
        self.weight_var = tk.StringVar()

        # 첫째 줄: 이름 / 생년 / 성별
        ttk.Label(form_frame, text="이름").grid(row=0, column=0, padx=5, pady=5)
        self.name_entry = ttk.Entry(form_frame, textvariable=self.name_var, width=12)
        self.name_entry.grid(row=0, column=1, padx=5)

        ttk.Label(form_frame, text="생년").grid(row=0, column=2, padx=5)
        self.birth_entry = ttk.Entry(form_frame, textvariable=self.birth_var, width=8)
        self.birth_entry.grid(row=0, column=3, padx=5)

        ttk.Label(form_frame, text="성별").grid(row=0, column=4, padx=5)
        self.gender_box = ttk.Combobox(form_frame, textvariable=self.gender_var,
                                       values=["남", "여"], state="readonly", width=4)
        self.gender_box.grid(row=0, column=5, padx=5)

        # 둘째 줄: 키 / 몸무게
        ttk.Label(form_frame, text="키(cm)").grid(row=1, column=0, padx=5, pady=5)
        ttk.Entry(form_frame, textvariable=self.height_var, width=12).grid(row=1, column=1, padx=5)

        ttk.Label(form_frame, text="몸무게(kg)").grid(row=1, column=2, padx=5)
        ttk.Entry(form_frame, textvariable=self.weight_var, width=8).grid(row=1, column=3, padx=5)

        # 버튼: command에 콜백 메소드를 바인딩
        btn_frame = ttk.Frame(form_frame)
        btn_frame.grid(row=0, column=6, rowspan=2, padx=15)
        ttk.Button(btn_frame, text="추가", command=self.on_add).grid(row=0, column=0, padx=3, pady=2)
        ttk.Button(btn_frame, text="수정", command=self.on_update).grid(row=0, column=1, padx=3, pady=2)
        ttk.Button(btn_frame, text="삭제", command=self.on_delete).grid(row=1, column=0, padx=3, pady=2)
        ttk.Button(btn_frame, text="입력 초기화", command=self.clear_form).grid(row=1, column=1, padx=3, pady=2)

        # 안내 문구 만들기 = 추가
        ttk.Label(form_frame, text="※ 수정은 키/몸무게만 가능합니다. (목록에서 행을 선택하세요)",
                  foreground="gray").grid(row=2, column=0, columnspan=7, sticky="w", padx=5, pady=(0, 5))

    def build_list_area(self):
        """3. 목록/검색 영역: 검색창 + Treeview 목록."""
        list_frame = ttk.LabelFrame(self.root, text="목록 조회 / 검색")
        list_frame.pack(fill="both", expand=True, padx=10, pady=5)

        # 검색창
        search_frame = ttk.Frame(list_frame)
        search_frame.pack(fill="x", padx=5, pady=5)
        ttk.Label(search_frame, text="식별번호 또는 이름:").pack(side="left")
        self.search_var = tk.StringVar()
        search_entry = ttk.Entry(search_frame, textvariable=self.search_var, width=18)
        search_entry.pack(side="left", padx=5)
        ttk.Button(search_frame, text="검색", command=self.on_search).pack(side="left", padx=3)
        ttk.Button(search_frame, text="전체 목록", command=self.on_show_all).pack(side="left", padx=3)

        # 이벤트 바인딩 검색창에서 Enter 키 상호작용되도록 만들기 = 추가
        search_entry.bind("<Return>", lambda event: self.on_search())

        # 목록 표(Treeview) + 스크롤바
        tree_frame = ttk.Frame(list_frame)
        tree_frame.pack(fill="both", expand=True, padx=5, pady=(0, 5))
        self.tree = ttk.Treeview(tree_frame, columns=[c[0] for c in COLUMNS],
                                 show="headings", height=8, selectmode="browse")
        for key, title, width in COLUMNS:
            self.tree.heading(key, text=title)
            self.tree.column(key, width=width, anchor="center")
        scroll = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scroll.set)
        self.tree.pack(side="left", fill="both", expand=True)
        scroll.pack(side="right", fill="y")

        # 이벤트 바인딩 행 선택 시 상세 조회(on_select 연결) = 추가
        self.tree.bind("<<TreeviewSelect>>", self.on_select)

    def build_bottom_area(self):
        """4. 하단 영역: 상세 조회(왼쪽) + 통계(오른쪽)."""
        bottom_frame = ttk.Frame(self.root)
        bottom_frame.pack(fill="x", padx=10, pady=(5, 10))

        # 상세 조회
        detail_frame = ttk.LabelFrame(bottom_frame, text="상세 조회")
        detail_frame.pack(side="left", fill="both", expand=True, padx=(0, 5))
        self.detail_label = ttk.Label(detail_frame, text=EMPTY_DETAIL_TEXT,
                                      justify="left", anchor="nw")
        self.detail_label.pack(fill="both", expand=True, padx=8, pady=5)

        # 통계
        stats_frame = ttk.LabelFrame(bottom_frame, text="통계")
        stats_frame.pack(side="left", fill="both", expand=True, padx=(5, 0))
        self.stats_label = ttk.Label(stats_frame, text="", justify="left", anchor="nw")
        self.stats_label.pack(fill="both", expand=True, padx=8, pady=5)
        ttk.Button(stats_frame, text="통계 조회",
                   command=self.show_statistics).pack(pady=(0, 5))


    # 3. 화면 갱신 도우미 (데이터 → 화면)
    
    def refresh_list(self, records=None):
        """Treeview를 비우고 records(없으면 전체 목록)으로 다시 채운다."""
        if records is None:
            records = self.manager.get_all()        # 모듈 2: 전체 조회
        self.tree.delete(*self.tree.get_children())
        for r in records:
            self.tree.insert("", "end", values=(r.id, r.name, r.birth_year, r.gender,
                                                r.height, r.weight, r.bmi, r.status))

    def show_statistics(self):
        """모듈 2의 get_statistics() 결과를 통계 라벨에 표시한다."""
        stats = self.manager.get_statistics()       # 모듈 2: 통계
        lines = [f"전체 인원수: {stats['count']}명"]
        for field, label in (("height", "키"), ("weight", "몸무게"), ("bmi", "BMI")):
            if field in stats:
                mean, std = stats[field]
                lines.append(f"{label}  평균 {mean:.2f} | 표준편차 {std:.2f}")
        self.stats_label.config(text="\n".join(lines))

    def reload_all(self):
        """목록, 통계를 현재 데이터로 새로 그린다."""
        self.refresh_list()
        self.show_statistics()

    def clear_form(self):
        """입력칸과 선택 상태를 모두 초기화한다."""
        self.name_var.set("")
        self.birth_var.set("")
        self.gender_var.set("남")
        self.height_var.set("")
        self.weight_var.set("")
        self.selected_id = None
        self.tree.selection_remove(self.tree.selection())
        self.detail_label.config(text=EMPTY_DETAIL_TEXT)



    # 4. 콜백: 추가 / 수정 / 삭제 (버튼 → 모듈 2 메소드 호출 → 화면 갱신)

    def on_add(self):
        """추가 버튼 입력값을 변환해 add_health를 호출한다."""
        try:
            record = self.manager.add_health(
                self.name_var.get(),
                int(self.birth_var.get()),
                self.gender_var.get(),
                float(self.height_var.get()),
                float(self.weight_var.get()),
            )
        except ValueError as e:     # 숫자 변환 실패, 모듈 2의 검증 오류 모두 처리
            messagebox.showerror("입력 오류", f"{e}\n(생년은 정수, 키/몸무게는 숫자로 입력하세요.)")
            return
        self.reload_all()
        self.clear_form()
        messagebox.showinfo("등록 완료", f"{record.name}님이 등록되었습니다.\n"
                                         f"식별번호 {record.id} | BMI {record.bmi} ({record.status})")

    def on_update(self):
        """수정 버튼 선택된 레코드의 키/몸무게를 update_health로 수정한다."""
        if self.selected_id is None:
            messagebox.showwarning("선택 필요", "수정할 행을 목록에서 먼저 선택하세요.")
            return
        try:
            record = self.manager.update_health(
                self.selected_id,
                float(self.height_var.get()),
                float(self.weight_var.get()),
            )
        except ValueError as e:
            messagebox.showerror("수정 오류", str(e))
            return
        self.reload_all()
        messagebox.showinfo("수정 완료", f"{record.name}님의 BMI가 {record.bmi} ({record.status})로 수정되었습니다.")
        self.clear_form()

    def on_delete(self):
        """삭제 버튼 확인 후 선택된 레코드를 delete_health로 삭제한다."""
        if self.selected_id is None:
            messagebox.showwarning("선택 필요", "삭제할 행을 목록에서 먼저 선택하세요.")
            return
        if not messagebox.askyesno("삭제 확인", f"{self.selected_id} 데이터를 삭제할까요?"):
            return
        if self.manager.delete_health(self.selected_id):    # 모듈 2: 삭제
            self.reload_all()
            self.clear_form()
        else:
            messagebox.showerror("삭제 오류", "해당 식별번호가 없습니다.")


    # 5. 콜백: 조회 / 검색 = ai 추가 기능

    def on_select(self, event=None):
        """행 선택 이벤트 find_by_id로 상세 정보를 보여주고 입력칸에 채운다."""
        selection = self.tree.selection()
        if not selection:
            return
        record_id = self.tree.item(selection[0], "values")[0]
        record = self.manager.find_by_id(str(record_id))    # 모듈 2: 상세 조회
        if record is None:
            return
        self.selected_id = record.id
        self.name_var.set(record.name)
        self.birth_var.set(str(record.birth_year))
        self.gender_var.set(record.gender)
        self.height_var.set(str(record.height))
        self.weight_var.set(str(record.weight))
        self.detail_label.config(text=(
            f"식별번호: {record.id}\n"
            f"이름: {record.name}  ({record.birth_year}년생, {record.gender})\n"
            f"키: {record.height}cm  몸무게: {record.weight}kg\n"
            f"BMI: {record.bmi}  비만도: {record.status}"
        ))

    def on_search(self):  # ai 추가 기능 enter키 상호작용
        """검색 버튼 / Enter 식별번호 우선, 없으면 이름으로 검색한다."""
        key = self.search_var.get().strip()
        if not key:
            self.on_show_all()
            return
        record = self.manager.find_by_id(key)
        results = [record] if record else self.manager.search_by_name(key)
        self.refresh_list(results)
        if not results:
            messagebox.showinfo("검색 결과", "일치하는 데이터가 없습니다.")

    def on_show_all(self):
        """전체 목록 버튼 검색창을 비우고 전체 목록을 다시 보여준다."""
        self.search_var.set("")
        self.refresh_list()



    # 6. 콜백: 파일 입출력 / 종료

    def on_load(self):
        """불러오기 버튼 선택한 형식의 파일을 load로 읽는다."""
        fmt = self.fmt_var.get()
        self.manager.load(fmt)
        self.reload_all()
        self.clear_form()
        messagebox.showinfo("불러오기", f"{fmt} 파일에서 {len(self.manager.records)}건을 불러왔습니다.")

    def on_save(self):
        """내보내기 버튼 선택한 형식으로 save를 호출한다."""
        fmt = self.fmt_var.get()
        if self.manager.save(fmt):
            messagebox.showinfo("내보내기", f"health_data.{fmt} 파일로 저장했습니다.")
        else:
            messagebox.showerror("내보내기 실패", "파일 저장에 실패했습니다.")

    def on_close(self):     # ai 추가 기능 마지막으로 묻기
        """창 닫기 이벤트 종료 전에 json으로 저장할지 묻는다."""
        answer = messagebox.askyesnocancel("종료", "종료하기 전에 json 파일로 저장할까요?")
        if answer is None:      # 취소 하면 종료하지 않음
            return
        if answer:
            self.manager.save("json")
        self.root.destroy()



# 실행 함수 main.py에서 호출시키기
def run_gui():
    """GUI 창을 만들고 메인 루프를 실행한다."""
    root = tk.Tk()
    HealthManagerGUI(root)
    root.mainloop()