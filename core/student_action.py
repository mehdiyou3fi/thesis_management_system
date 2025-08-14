import os
from utils.data_manager import DataManager
from datetime import datetime , timedelta
from .models.student import Student

def submit_thesis_request(student) :
    professor_file = os.path.join("data", "professor.json")
    courses_file = os.path.join("data", "courses.json")
    request_file = os.path.join("data", "thesis_requests.json")
    professor = DataManager.read_json(professor_file)
    courses = DataManager.read_json(courses_file)
    request = DataManager.read_json(request_file)
    if not courses:
        print ("No courses found! ")
        return 
    
    print ("\n Available Thesis Course: ")
    for i,course in enumerate(courses, start=1):
        print(f"{i}. {course['title']} | Professor Name: {course['professor']} | Professor Id {course['professor_id']} | Course Capacity : {course['capacity']}")
        for j in professor:
            if j["id"] == course["professor_id"] :
                print (f"professor capacity : {j["guidance_capacity"]}")
    choice = input("select course number: ")
    try :
        choice = int (choice) -1 
        selected_course = courses[choice]
    except(ValueError, IndexError):
        print ("invalid selection! ")
        return
    
            # چک برای اینکه دوبار درخواست یک درس را نده 
    for req in request:
        if req["student_id"] == student.id and req["course_id"]== selected_course["id"]:
            print("You have already submitted a request for this course!")
            return 
        
    # چک ظرفیت درس  
    if selected_course["capacity"]<=0:
        print ("This course has no availble capacity! ")
        return 
    for k in professor:
        if selected_course["professor_id"] == k["id"]:
            if k["guidance_capacity"]<=0:
                print ("This professor has no availble capacity!")
                return 
            
    # ساخت درخواست 
    new_request = {
        "request_date":datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "student_id":student.id,
        "student_name":student.name,
        "course_id":selected_course["id"],
        "course_title":selected_course["title"],
        "professor_name":selected_course["professor"],
        "professor_id":selected_course["professor_id"],
        "status":"pending"
    }

    # دخیره در فایل درخواست ها
    DataManager.append_json(request_file, new_request)

    print ("Thesis request submitted successfully ")

def submit_defense_request(student):
    thesis_requests_file = os.path.join("data", "thesis_requests.json")
    defense_requests_file = os.path.join("data", "thesis_defense_requests.json")

    thesis_requests = DataManager.read_json(thesis_requests_file)

    # پیدا کردن دانشجو و در خواست های تایید شده ان 
    approved_theses = [t for t in thesis_requests if t["student_id"]==student.id and t["status"]=="approved"]

    if not approved_theses :
        print ("you have no approved thesis to defiend")
        return 
    

    # چک گذشتن سه ماه از درخواست پایان نامه 
    now_date = datetime.now()
    eligible_theses = []
    for thesis in approved_theses:
        approval_date = datetime.strptime(thesis["approval_date"], "%Y-%m-%d %H:%M:%S")
        if now_date - approval_date>= timedelta(days=90):
            eligible_theses.append(thesis)

    if not eligible_theses:
        print ("You most wait at least 3 month after approval before defending ")
        return 
    
    # نمایش پایان نامه های قابل دفاع
    for i, thesis in enumerate(eligible_theses,start=1):
        print (f"{i}. {thesis['course_title']}  Approved on : {thesis['approval_date']}")

        choice = input("Select thesis to request defense: ")

        try:
            choice = int (choice) -1 
            selected_thesis = eligible_theses[choice]
        except (ValueError, IndexError):
            print ("Invalid selection")
            return
        

        # ایجاد درخواست فاع 
        new_defense_request = {
        
        "student_id": student.id,
        "student_name": student.name,
        "course_id": selected_thesis["course_id"],
        "course_title": selected_thesis["course_title"],
        "professor_name":selected_thesis["professor_name"],
        "professor_id": selected_thesis["professor_id"],
        "status": "pending",
        "request_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    

    # ثبت 
    DataManager.append_json(defense_requests_file, new_defense_request)
    print ("Defense request submitted successfully!")

def view_request_status(student):
    thesis_requests_file = os.path.join("data", "thesis_requests.json")
    thesis_requests = DataManager.read_json(thesis_requests_file)
    list_requests =[t for t in thesis_requests if t["student_id"]==student.id]
    if not list_requests :
        print("No request has been registered for you.")
        return
    for i,status in enumerate(list_requests, start=1):
        print (f"{i}. course: {status['course_title']} - status: {status["status"]}")
        



        



    


        