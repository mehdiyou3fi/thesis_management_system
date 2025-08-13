import os
from utils.data_manager import DataManager
from datetime import datetime
def submit_thesis_request(student) :
    professor_file = os.path.join("data", "professor.json")
    courses_file = os.path.join("data", "courses.json")
    request_file = os.path.join("data", "thesis_requests.json")
    professor = DataManager.read_json(professor_file)
    courses = DataManager.read_json(courses_file)
    if not courses:
        print ("No courses found! ")
        return 
    print ("\n Available Thesis Course: ")
    for i,course in enumerate(courses, start=1):
        print(f"{i}. {course['title']} | Professor Name: {course['professor']} | Course Capacity : {course["capacity"]}")
        for j in professor:
            if j["name"] == course["professor"] :
                print (f"professor capacity : {j["guidance_capacity"]}")
    choice = input("select course number: ")
    try :
        choice = int (choice) -1 
        selected_course = courses[choice]
    except(ValueError, IndexError):
        print ("invalid selection! ")
        return
    # چک ظرفیت درس  
    if selected_course["capacity"]<=0:
        print ("This course has no availble capacity! ")
        return 
    for k in professor:
        if selected_course["professor"].strip().lower() == k["name"].strip().lower():
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
        "status":"pending"
    }
    # دخیره در فایل درخواست ها
    DataManager.append_json(request_file, new_request)

    # کاهش ظرفیت 
    for c in courses:
        if c["id"] == selected_course["id"]:
            c["capacity"] -=1
            break
    DataManager.write_json(courses_file, courses)

    print ("Thesis request submitted successfully ")

        