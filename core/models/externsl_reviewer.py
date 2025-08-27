from core.models.user import User
from core.models.thesis import Thesis
class ExternalReviewer(User):
    def __init__(self, id, name, username, password, judge_capacity=10, professor_code=None):
        super().__init__(id, name, username, password)
        self.judge_capacity = judge_capacity
        self.professor_code = username or professor_code

    def grade_thesis_as_external(self):
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

        # ثبت نمره داور خارجی 
        thesis.submit_grade("external", grade)

        print ("External grade submitted. ")
