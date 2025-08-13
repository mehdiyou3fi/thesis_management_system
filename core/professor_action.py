import os
from utils.data_manager import DataManager
def review_thesis_requests(professor):
    request_file = os.path.join("data", "thesis_requests.json")
    course_file = os.path.join("data", "courses.json")
    professor_file = os.path.join("data", "professor.json")
    professor_data = DataManager.read_json(professor_file)
    requests = DataManager.read_json(request_file)
    courses = DataManager.read_json(course_file)
    
    # فیلتر کردن بر اساس درخواست هایی ک هنوز در حالت انتظار هستند و برای ان پرفسور است 
    pending_requests = [r for r in requests if r["professor_id"]==professor.id and r["status"]=="pending"]
    
    if not pending_requests:
        print ("No pending request found! ")
        return 
    
    print ("\n pending thesis requests!")
    for i, req in enumerate(pending_requests, start=1):
        print (f"Date: {req['request_date']}")
        print (f"{i}. Student: {req['student_name']} | Course: {req['course_title']}")
        print ("_"*30)
        print ()

    choice = input("Select request number to reviw (or 0 to exit): ")
    try:
        choice =int (choice) -1
        if choice == -1:
            return 
        select_request =pending_requests[choice]
    except (ValueError, IndexError):
        print ("Invalid selection ")
        return 
        
    # پیدا کردن درس برای چک ظرفیت 
    relate_course = None 
    for c in courses:
        if c['id'] == select_request["course_id"]:
            relate_course = c
            break

    # پیدا کردن استاد برای جک ظرفیت
    relate_professor = None
    for p in professor_data:
        if p["id"] == professor.id:
            relate_professor = p
            break

    # چک ظرفیت درس 
    if relate_course and relate_course["capacity"]<=0:
        print("No capacity left for this course! Cannot approve.")
        select_request["status"] = "rejected"

    # چک کردن ظرفیت خود استاد 
    elif relate_professor and relate_professor["guidance_capacity"]<=0:
        print(f"No guidance capacity left for Professor {relate_professor['name']}! Cannot approve.")
        select_request["status"] = "rejected"

    else:
        decision = input("Approve (a) or Reject (r)? ").lower()
        if decision in ['a', 'approve']:
            select_request["status"] = "approved"
            if relate_course:
                relate_course["capacity"] -= 1
            if relate_professor:
                relate_professor["guidance_capacity"] -=1
            print ("Request approved.")
        elif decision in ['r','reject']:
            select_request["status"] = "rejected"
            print ("request rejected ")
        else:
            print ("Invalid choice! ")
            return
    # ثبت تغییرات در فایل ها 
    DataManager.write_json(request_file, requests)
    DataManager.write_json(course_file, courses)
    DataManager.write_json(professor_file, professor_data)




