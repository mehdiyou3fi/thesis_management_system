# from .user import User
# class Professor(User):
#     def __init__(self, id, name, username, password):
#         super().__init__(id, name, username, password)
import os
from datetime import datetime
from core.models.thesis import Thesis
from .user import User
from utils.data_manager import DataManager
from utils.check_3month_passed import check_three_month_passed
from utils.file_manager import open_file
from utils.paths import COURSES_JSON

class Professor(User):
    def __init__(self, id, name, username, password, professor_code = None, email= None ):
        super().__init__(id, name, username, password)
        self.professor_code = professor_code or username
        self.email = email
    def review_thesis_requests(self):
        # request_file = os.path.join("data", "thesis_requests.json")
        course_file = os.path.join("data", "courses.json")
        professor_file = os.path.join("data", "professor.json")
        professor_data = DataManager.read_json(professor_file)
        requests = Thesis._load_all()
        courses = DataManager.read_json(course_file)
        
        # فیلتر درخواست‌های منتظر برای این استاد
        pending_requests = [r for r in requests if r["professor_code"]==self.professor_code and r["status"]=="pending"]
        
        if not pending_requests:
            print("No pending request found!")
            return
        
        print("\nPending thesis requests:")
        for i, req in enumerate(pending_requests, start=1):
            print(f"Date: {req['request_date']}")
            print(f"{i}. Student: {req['student_code']} | Course: {req['title']}")
            print("_"*30)
            print()

        choice = input("Select request number to review (or 0 to exit): ")
        try:
            choice = int(choice) - 1
            if choice == -1:
                return
            select_request = pending_requests[choice]
        except (ValueError, IndexError):
            print("Invalid selection")
            return

        # پیدا کردن درس و استاد مربوطه
        # وقتی اولین رو ملاقات میکنه برمیگردونه و اگر نبود نان رو برمیگردونه اینطوری بهینه
        relate_course = next((c for c in courses if c['id'] == select_request["course_ID"]), None)
        relate_professor = next((p for p in professor_data if p["username"] == self.professor_code), None)

        # چک ظرفیت درس
        if relate_course and relate_course["capacity"] <= 0:
            print("No capacity left for this course! Cannot approve.")
            Thesis.mark_rejected()
        # چک ظرفیت استاد
        elif relate_professor and relate_professor["guidance_capacity"] <= 0:
            print(f"No guidance capacity left for Professor {relate_professor['name']}! Cannot approve.")
            Thesis.mark_rejected()
        else:
            decision = input("Approve (a) or Reject (r)? ").lower()
            if decision in ['a', 'approve']:
                select_request["status"] = "approved"
                select_request["rejected_date"] =None
                select_request["approval_date"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                if relate_course:
                    relate_course["capacity"] -= 1
                if relate_professor:
                    relate_professor["guidance_capacity"] -= 1
                print("Request approved.")

            elif decision in ['r', 'reject']:
                select_request["status"] = "rejected"
                select_request["rejected_date"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                select_request["approval_date"] = None
                print("Request rejected.")
            else:
                print("Invalid choice!")
                return

        # ذخیره تغییرات
        # DataManager.write_json(request_file, requests)
        Thesis._save_all(requests)
        DataManager.write_json(course_file, courses)
        DataManager.write_json(professor_file, professor_data)


    def decrease_reviewer_capacity(self, reviewer_type, reviewer_name):
        if reviewer_type == "internal":
            professors_file = os.path.join("data", "professor.json")
            professors = DataManager.read_json(professors_file)

            for p in professors:
                if p["name"].strip().lower() == reviewer_name.strip().lower():
                    if p["review_capacity"] > 0:
                        p["review_capacity"] -= 1
                        DataManager.write_json(professors_file, professors)
                        return True
                    else:
                        print("Professor does not have capacity")
                        return False
            print ("professor not found!")
            return False

        elif reviewer_type == "external":
            external_file = os.path.join("data", "external_reviewers.json")
            external_reviewers = DataManager.read_json(external_file)

            for p in external_reviewers:
                if p["name"].strip().lower() == reviewer_name.strip().lower():
                    if p["reviewer_capacity"] > 0:
                        p["reviewer_capacity"] -= 1
                        DataManager.write_json(external_file, external_reviewers)
                        return True
                    else:
                        print("Reviewer does not have capacity")
                        return False
            print ("professor not found!")
            return False

    def view_defense_requests(self):
        # defense_request_file = os.path.join("data", "thesis_defense_requests.json")
        # defense_requests = DataManager.read_json(defense_request_file)
        thesis_requests = Thesis._load_all()
        # چک کردن اینکه درخواستی برای دفاع امده یا ن
        defense_requests = [
    req for req in thesis_requests
    if req["professor_code"] == self.professor_code and req["status"] == "defense_requested"
]

        
        if not defense_requests:
            print("No defense request found!")
            return
        
        print("\n---Defense Requests List---")
        # pending_requests = [r for r in defense_requests if r["professor_id"] == self.id and r["status"] == "pending"]
        for i, r in enumerate(defense_requests, start=1):
            print(f"{i}. student: {r['student_code']} | course: {r['title']} | approved_date: {r['approval_date']}")
            print("Files submitted:")
            for key, path in r["files"].items():
                print(f"- {key}: {path}")

        choice = input("Select request number to review (or 0 to exit): ")
        try:
            choice = int(choice) - 1
            if choice == -1:
                return
            select_request = defense_requests[choice]
        except (ValueError, IndexError):
            print("Invalid selection")
            return

        # باز کردن فایل‌ها
        while True:
            view_choice = input("Do you want to open one of the files? yes(y) or no(n): ")
            if view_choice.lower() in ['y', 'yes']:
                file_key = input("File name: (pdf/img_first/img_last/: ").lower()
                if file_key in select_request["files"]:
                    file_key_path = select_request["files"][file_key]
                    print(file_key_path)
                    open_file(file_key_path)
                else:
                    print("Invalid file")
            else:
                break

        # پیدا کردن تاریخ تایید درخواست پایان‌نامه
        data_request = None
        for tr in thesis_requests:
            if tr["student_code"] == select_request["student_code"] and tr["professor_code"] == select_request["professor_code"] and tr["course_ID"] == select_request["course_ID"] and tr["status"] == "defense_requested":
                data_request = tr["approval_date"]
                break

        if not data_request:
            print("Approval date not found")
            return

        # بررسی گذشت سه ماه
        if not check_three_month_passed(data_request):
            print("It hasn't been three months yet.")
            return
        # گرفتن تاریخ دفاع از پرفسور
        defense_date = input("Enter defense date (yyyy-MM-DD): ")
        print(f"\nSuggested reviewer: {select_request.get('suggested_reviewer', 'N/A')}")

        # گرفتن داور داخلی 
        internal_reviewer = input("Enter (name) of internal reviewer: ")
        select_request["defense_date"] = defense_date
        select_request["judges"]["internal_reviewer"] = internal_reviewer
        if not self.decrease_reviewer_capacity("internal",internal_reviewer):
            return
        # گرفتن داور خارجی
        external_reviewer = input("Enter (name) of external reviewer: ")
        select_request["judges"]["external_reviewer"] = external_reviewer
        if not self.decrease_reviewer_capacity("external", external_reviewer):
            return
        
        # تغییر وضعیت 
        select_request["status"] = "scheduled"

        # DataManager.write_json(defense_request_file, defense_requests)
        Thesis._save_all(thesis_requests)
        print("The thesis defense was successfully scheduled.")


    def grade_thesis_as_internal(self):
        """ثبت نمره  پایان نامه توسط داور داخلی
        --------------------------------------------
        کاربر باید :
        -student_code
        -course_ID
        -grade(flaot)
        را وارد کند 
        """

        # دریاغت اطلاعات کاربر 
        student_code = input("Enter student_code: ")
        course_ID = input("Enter course_ID: ")
        grade = float(input("Enter grade: "))

        # بررسی وجود پایان نامه 
        thesis_data = Thesis.get(student_code, course_ID)
        if not thesis_data:
            print ("Thesis not found :")
            return 
        
        # ساخت ابچکتاز داده های پیدا شده 
        thesis =Thesis(
            student_code = thesis_data["student_code"],
            course_ID = thesis_data["course_ID"],
            title = thesis_data["title"],
            professor_code= self.professor_code
        )

        # ثبت نمره داور داخلی 
        thesis.submit_grade("internal", grade)

        print ("Internal grade submitted. ")
    
    def add_course(self):
        '''اضافه کردن یک درس جدید توسط استاد '''
        courses = DataManager.read_json(COURSES_JSON)
        print ("\n Add New Course")
        course_id = input ("Enter course_id").strip()
        # جلوگیری از تکرار 
        if any(c["id"] == course_id for c in courses):
            print ("This course ID already exist")
            return 
        course_title = input("Enter Course title : ").strip()
        year = input("Enter Year (e.g., 2025): ").strip()
        semester = input("Enter Semester (first/second): ").strip()
        capacity = int(input("Enter Capacity: ").strip())
        resources = input("Enter Resources (comma separated): ").strip().split(",")
        sessions = int(input("Enter Number of Sessions: ").strip())
        unit = int(input("Enter Unit count: ").strip())

        # ساخت دیکشنری جدید برای درس جدید 
        new_course = {
            "id":course_id,
            "title":course_title,
            "professor":self.name,
            "professor_code":self.username,
            "year":year,
            "semester":semester,
            "capacity":capacity,
            "resources":resources,
            "sessions":sessions,
            "unit":unit
        }

        DataManager.append_json(COURSES_JSON, new_course)
        print("✅ New course added successfully!")
        
