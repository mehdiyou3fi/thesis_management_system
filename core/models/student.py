import os
from datetime import datetime, timedelta
from utils.data_manager import DataManager
from .user import User
from core.models.thesis import Thesis
from utils.paths import THESIS_JSON
from utils.check_3month_passed import check_three_month_passed


class Student(User):
    def __init__(self, id, name, username, password, student_code=None, email=None):
        super().__init__(id, name, username, password)
        self.student_code = student_code or username
        self.email = email
    

    def submit_thesis_request(self):
        '''در خواست برای اخذ پایان نامه '''
        professor_file = os.path.join("data", "professor.json")
        courses_file = os.path.join("data", "courses.json")
        

        professor = DataManager.read_json(professor_file)
        courses = DataManager.read_json(courses_file)
        

        if not courses:
            print("No courses found! ")
            return

        print("\n Available Thesis Course: ")
        for i, course in enumerate(courses, start=1):
            print(
                f"{i}. {course['title']} | Professor Name: {course['professor']} "
                f"| Professor code {course['professor_code']} | Course Capacity : {course['capacity']}"
            )
            for j in professor:
                if j["username"] == course["professor_code"]:
                    print(f"professor capacity : {j['guidance_capacity']}")

        choice = input("select course number: ")
        try:
            choice = int(choice) - 1
            selected_course = courses[choice]
        except (ValueError, IndexError):
            print("invalid selection! ")
            return



        # چک ظرفیت درس  
        if selected_course["capacity"] <= 0:
            print("This course has no available capacity! ")
            return
        for k in professor:
            if selected_course["professor_code"] == k["username"]:
                if k["guidance_capacity"] <= 0:
                    print("This professor has no available capacity!")
                    return
        # در این قسمت در خواست ما ثبت میشود
        try:
            thesis = Thesis(self.student_code, selected_course["id"], selected_course["title"], selected_course["professor_code"])
            thesis.save_request()
            print ("Thesis request submitted successfully.")
        except ValueError as e:
            print ("Error", e)




    def submit_defense_request(self):
        print("\n--- Submit Defense Request---")
        defense_requests_file = os.path.join("data", "thesis_defense_requests.json")

        thesis_requests = Thesis._load_all()

        # پیدا کردن دانشجو و درخواست‌های تایید شده‌اش
        approved_theses = [t for t in thesis_requests if t["student_code"] == self.student_code and t["status"] == "approved"]

        if not approved_theses:
            print("you have no approved thesis to defend")
            return

        # چک گذشتن سه ماه از درخواست پایان نامه 
        # now_date = datetime.now()
        eligible_theses = []
        for t in approved_theses:
            # approval_date = datetime.strptime(t["approval_date"], "%Y-%m-%d %H:%M:%S")
            approval_date = t["approval_date"]
            if check_three_month_passed(approval_date):
                eligible_theses.append(t)

        if not eligible_theses:
            print("You must wait at least 3 months after approval before defending ")
            return

        # نمایش پایان‌نامه‌های قابل دفاع
        for i, t in enumerate(eligible_theses, start=1):
            print(f"{i}. {t['title']}  Approved on : {t['approval_date']}")

        choice = input("Select thesis to request defense: ")

        try:
            choice = int(choice) - 1
            selected_thesis = eligible_theses[choice]
        except (ValueError, IndexError):
            print("Invalid selection")
            return

        # اطلاعات دفاع 
        # title = input("Enter thesis title: ")
        # keywords = input("Enter thesis keywords (comma separated): ")
        # abstract_text = input("Enter thesis abstract: ")

        thesis_file = os.path.normpath(input("Enter thesis PDF path:  ").strip('"'))
        first_page_file = os.path.normpath(input("Enter first page path:  ").strip('"'))
        last_page_file = os.path.normpath(input("Enter last page path:  ").strip('"'))

        thesis = Thesis(self.student_code, selected_thesis["course_ID"], selected_thesis["title"],selected_thesis["professor_code"])
        try:
            thesis.upload_files(thesis_file, first_page_file, last_page_file)
            print ("The files have been registered.")
        except ValueError as e:
            print ("ERROR", e)

        suggested_reviewer = input("Enter suggested reviewer name: ")
        items = Thesis._load_all()
        for t in items:
            if t["student_code"] == self.student_code and t["course_ID"] == selected_thesis["course_ID"]:
                t["suggested_reviewer"] = suggested_reviewer
                t["status"] = "defense_requested"
                break
        Thesis._save_all(items) 
        print("Suggested reviewer has been added successfully.")
        print("Defense request submitted successfully and all files have been registered.")


        

    def view_request_status(self):
        thesis = Thesis._load_all()
        

        list_requests = [t for t in thesis if t["student_code"] == self.student_code]

        if not list_requests:
            print("No request has been registered for you.")
            return

        for i, status in enumerate(list_requests, start=1):
            print(f"{i}. course: {status['title']} - status: {status['status']}")
