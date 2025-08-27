from datetime import datetime
from decimal import Decimal
from utils.data_manager import DataManager
from utils.file_manager import copy_file_safe
from utils.validators import validate_defense_files
from utils.paths import THESIS_JSON, DEFENDED_JSON, THESIS_PDF_DIR, IMAGES_DIR

class Thesis:
    def __init__(self, student_code, course_ID, title, professor_code):
        self.student_code = str(student_code)
        self.course_ID = str(course_ID)
        self.professor_code = professor_code
        self.title = title
        self.status = "pending"
        self.request_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.approval_date = None
        self.rejected_date = None
        self.defense_date = None
        self.files = {}
        self.judges = {}
        self.grades = {}
        self.final_score = None


    def to_dict(self):
        return {
                "student_code": self.student_code,
                "course_ID": self.course_ID,
                "title": self.title,
                "professor_code":self.professor_code, 
                "status": self.status,
                "request_date": self.request_date,
                "approval_date": self.approval_date,
                "rejected_date":self.rejected_date,
                "defense_date": self.defense_date,
                "files": self.files,
                "judges": self.judges,
                "grades": self.grades,
                "final_score": self.final_score
            }


    # ساختن نوشتن خواندن حذف اپدیت کردن در فایل thesis
    # read
    @staticmethod
    def _load_all():
        return DataManager.read_json(THESIS_JSON)


    # write
    @staticmethod
    def _save_all(items):
        DataManager.write_json(THESIS_JSON, items)


    @staticmethod
    def get(student_code, course_ID):
        sc, cid = str(student_code), str(course_ID)
        for t in Thesis._load_all():
            if str(t["student_code"]) == sc and str(t["course_ID"])==cid:
                return t
        return None
        


    def save_request(self):
        items = Thesis._load_all()
        exists = any(str(t["student_code"]) == self.student_code and str(t["course_ID"]) == self.course_ID for t in items)
        if exists:
            raise ValueError("This request has already been filed.")
        items.append(self.to_dict())
        Thesis._save_all(items)

    def upload_files(self, pdf_path, first_page_path, last_page_path):
        # اگر اینها با پسوند درست ذخیره شده بودند 
        ok, msg = validate_defense_files(pdf_path, first_page_path, last_page_path)
        if not ok:
            raise ValueError(msg)
        # اسم های جدید براشون بزار
        pdf_name = f"{self.student_code}_{self.course_ID}.pdf"
        img_first_page = f"{self.student_code}_{self.course_ID}_title.jpg"
        img_last_page = f"{self.student_code}_{self.course_ID}_last.jpg"

        # کپی امنشون کن در مسیر درست
        pdf_dst = copy_file_safe(pdf_path, THESIS_PDF_DIR, pdf_name)
        f1_dst = copy_file_safe(first_page_path, IMAGES_DIR, img_first_page)
        f2_dst = copy_file_safe(last_page_path, IMAGES_DIR, img_last_page)
        # قرارشون بده در قسمت فایل های این یوزر 
        self.files = {"pdf": pdf_dst, "img_first":f1_dst, "img_last": f2_dst}


        # دخیره فایل در قالب جیسون
        items = Thesis._load_all()
        found = False
        for t in items :
            if t["student_code"] == self.student_code and t["course_ID"]== self.course_ID:
                t["files"] = self.files
                found = True
                break
        if not found:
            print ("Warning: Student record not found, files not saved in JSON.")
        Thesis._save_all(items)


    def mark_approved(self):
        self.status = "approved"
        self.approval_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        items = Thesis._load_all()
        for t in items :
            if t["student_code"] == self.student_code and t["course_ID"] == self.course_ID:
                t["status"] = self.status 
                t["approval_date"] = self.approval_date
                t["rejected_date"] = None
                break
        Thesis._save_all(items)

    def mark_rejected(self):
        self.status = "rejected"
        self.rejected_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        items = Thesis._load_all()
        for t in items :
            if t["student_code"] == self.student_code and t["course_ID"] == self.course_ID:
                t["status"] = self.status 
                t["approval_date"] = None
                t["rejected_date"] = self.rejected_date
                break
        Thesis._save_all(items)


    @staticmethod
    def auto_update_status_all():
        """
        بررسی تمام پایان‌نامه‌ها و آپدیت وضعیت:
        اگر تاریخ دفاع گذشته و وضعیت 'scheduled' است،
        آن را به 'defended' تغییر می‌دهد.
        """
        items = Thesis._load_all()
        now = datetime.now()
        updated = False

        for t in items:
            defense_date_str = t.get("defense_date")
            status = t.get("status")

            if defense_date_str and status == "scheduled":
                try:
                    defense_dt = datetime.strptime(defense_date_str, "%Y-%m-%d")
                    if defense_dt <= now:
                        t["status"] = "defended"
                        updated = True
                        print(f"✅ Thesis for {t['student_code']} - {t['course_ID']} updated to 'defended'.")
                except ValueError:
                    print(f"⚠️ Invalid date format for {t['student_code']} - {t['course_ID']}: {defense_date_str}")

        if updated:
            Thesis._save_all(items)

    @staticmethod
    def auto_result(grade:float)->str :
        if grade >= 17:
            return "A"
        elif grade >=13:
            return "B"
        elif grade >= 10:
            return "C"
        else:
            return "D"


    def submit_grade(self, judge_role, grade):
        """
        ثبت نمره توسط داور داخلی یا خارجی
        -----------------------------------
        judge_role: "internal" | "external"
        grade: نمره عددی (float)
        """
        
        # نعیین نتیجه بر اساس نمره 
        result =  Thesis.auto_result(float(grade))

        # بارگزاری پایان نامه
        items = Thesis._load_all()

        for t in items :
            if t["student_code"] == self.student_code and t["course_ID"] == self.course_ID and t["status"]== "defended":
                found = True
                # دخیره نمره و نتیجه برای داور مربوطه 
                grades = t.get("grades", {}) 
                grades[judge_role] = {
                    "grade": float(f"{grade:.2f}"),
                    "result" : result
                }
                t["grades"] = grades
                print ("ggrade added")
                # اگر هر دو داور نمره دادند نمره نهایی ثبت بشه 
                if "internal" in grades and "external" in grades :
                    g1 = Decimal(str(grades["internal"]["grade"]))
                    g2 = Decimal(str(grades["external"]["grade"]))

                    # محسابه نهایی
                    final = (g1 + g2) / Decimal("2")
                    final_score = float(f"{final:.2f}")
                    final_result = Thesis.auto_result(float(final_score))

                    # ثبت نمره ها 
                    t["final_score"] = final_score
                    t["final_result"] = final_result
                    t["status"]= "defended"

                    defended = DataManager.read_json(DEFENDED_JSON)
                    defended.append(t)
                    DataManager.write_json(DEFENDED_JSON, defended)


                    # حذف دفاع از تز ها چ.ن دفاع شد 
                    items = [x for x in items
                              if not (
                                  x["student_code"]== self.student_code and 
                                  x["course_ID"]== self.course_ID
                              )
                    ]
                break
        if not found :
            print(f"❌ Defended Thesis for student_code={self.student_code}, course_ID={self.course_ID} not found!")
        Thesis._save_all(items)



        
        


