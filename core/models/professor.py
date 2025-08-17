# from .user import User
# class Professor(User):
#     def __init__(self, id, name, username, password):
#         super().__init__(id, name, username, password)
from .user import User
import os
from utils.data_manager import DataManager
from datetime import datetime
from utils.check_3month_passed import check_three_month_passed
from utils.professor_utils import decrease_reviewer_capacity
from utils.file_manager import open_file

class Professor(User):
    def __init__(self, id, name, username, password):
        super().__init__(id, name, username, password)

    def review_thesis_requests(self):
        request_file = os.path.join("data", "thesis_requests.json")
        course_file = os.path.join("data", "courses.json")
        professor_file = os.path.join("data", "professor.json")
        professor_data = DataManager.read_json(professor_file)
        requests = DataManager.read_json(request_file)
        courses = DataManager.read_json(course_file)
        
        # فیلتر درخواست‌های منتظر برای این استاد
        pending_requests = [r for r in requests if r["professor_id"]==self.id and r["status"]=="pending"]
        
        if not pending_requests:
            print("No pending request found!")
            return
        
        print("\nPending thesis requests:")
        for i, req in enumerate(pending_requests, start=1):
            print(f"Date: {req['request_date']}")
            print(f"{i}. Student: {req['student_name']} | Course: {req['course_title']}")
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
        relate_course = next((c for c in courses if c['id'] == select_request["course_id"]), None)
        relate_professor = next((p for p in professor_data if p["id"] == self.id), None)

        # چک ظرفیت درس
        if relate_course and relate_course["capacity"] <= 0:
            print("No capacity left for this course! Cannot approve.")
            select_request["status"] = "rejected"
            select_request["rejection_date"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        # چک ظرفیت استاد
        elif relate_professor and relate_professor["guidance_capacity"] <= 0:
            print(f"No guidance capacity left for Professor {relate_professor['name']}! Cannot approve.")
            select_request["status"] = "rejected"
            select_request["rejection_date"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        else:
            decision = input("Approve (a) or Reject (r)? ").lower()
            if decision in ['a', 'approve']:
                select_request["status"] = "approved"
                select_request["approval_date"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                if relate_course:
                    relate_course["capacity"] -= 1
                if relate_professor:
                    relate_professor["guidance_capacity"] -= 1
                print("Request approved.")
            elif decision in ['r', 'reject']:
                select_request["status"] = "rejected"
                select_request["rejection_date"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                print("Request rejected.")
            else:
                print("Invalid choice!")
                return

        # ذخیره تغییرات
        DataManager.write_json(request_file, requests)
        DataManager.write_json(course_file, courses)
        DataManager.write_json(professor_file, professor_data)


    def view_defense_requests(self):
        defense_request_file = os.path.join("data", "thesis_defense_requests.json")
        thesis_requests_file = os.path.join("data", "thesis_requests.json")
        defense_requests = DataManager.read_json(defense_request_file)
        thesis_requests = DataManager.read_json(thesis_requests_file)

        if not defense_requests:
            print("No defense request found!")
            return
        
        print("\n---Defense Requests List---")
        pending_requests = [r for r in defense_requests if r["professor_id"] == self.id and r["status"] == "pending"]
        for i, r in enumerate(pending_requests, start=1):
            print(f"{i}. student: {r['student_name']} | course: {r['course_title']} | date: {r['request_date']}")
            print("Files submitted:")
            for f in r["files"]:
                print(f"- {f}")

        choice = input("Select request number to review (or 0 to exit): ")
        try:
            choice = int(choice) - 1
            if choice == -1:
                return
            select_request = pending_requests[choice]
        except (ValueError, IndexError):
            print("Invalid selection")
            return

        # باز کردن فایل‌ها
        while True:
            view_choice = input("Do you want to open one of the files? yes(y) or no(n): ")
            if view_choice.lower() in ['y', 'yes']:
                file_key = input("File name: (thesis/first_page/last_page/abstract/forms): ")
                if file_key in select_request["files"]:
                    file_key_path = os.path.join("file", select_request["files"][file_key])
                    print(file_key_path)
                    open_file(file_key_path)
                else:
                    print("Invalid file")
            else:
                break

        # پیدا کردن تاریخ تایید درخواست پایان‌نامه
        data_request = None
        for tr in thesis_requests:
            if tr["student_id"] == select_request["student_id"] and tr["professor_id"] == select_request["professor_id"] and tr["course_id"] == select_request["course_id"] and tr["status"] == "approved":
                data_request = tr["approval_date"]
                break

        if not data_request:
            print("Approval date not found")
            return

        # بررسی گذشت سه ماه
        if not check_three_month_passed(data_request):
            print("It hasn't been three months yet.")
            return

        defense_date = input("Enter defense date (yyyy-MM-DD): ")
        print(f"\nSuggested reviewer: {select_request['suggested_reviewer']}")
        internal_reviewer = input("Enter internal reviewer: ")
        external_reviewer = input("Enter external reviewer: ")

        select_request["defense_date"] = defense_date
        select_request["internal_reviewer"] = internal_reviewer
        if not decrease_reviewer_capacity(internal_reviewer):
            return

        select_request["external_reviewer"] = external_reviewer
        select_request["status"] = "scheduled"

        DataManager.write_json(defense_request_file, defense_requests)
        print("The thesis defense was successfully scheduled.")
