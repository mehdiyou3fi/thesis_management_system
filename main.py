from core.authentication import Authentication
from core.menu import student_menu
from core.menu import professor_menu
from core.menu import external_reviewer_menu
from core.models.thesis import Thesis
if __name__ =="__main__":
    Thesis.auto_update_status_all()
    print ("Welcome to the Thesis Management System\n")
    role = input("what is your role (student(s) or professor(p) or external(e) :")
    username = input("username: ")
    password = input("password: ")
    # check login student 
    if role.lower() in ["s","student"]:
        user = Authentication.student_login(username, password)
        if not user :
            print ("Username or password is incorrect.")
        else:
            student_menu(user)
            
    # check login professor
    elif role.lower() in ["p","professor"]:
        user = Authentication.professor_login(username, password)
        if not user :
            print ("Username or password is incorrect.")
        else:
            professor_menu(user) 
    
    # check login external reviewer 
    elif role.lower() in ["e","external"]:
        user = Authentication.external_reviewer(username, password)
        if not user :
            print ("Username or password is incorrect.")
        else:
            external_reviewer_menu(user)
            