from core.authentication import Authentication
from core.menu import student_menu
from core.menu import professor_menu
if __name__ =="__main__":
    print ("Welcome to the Thesis Management System\n")
    role = input("what is your role (student or professor):")
    username = input("username: ")
    password = input("password: ")
    # check login student 
    if role.lower() == "student":
        user = Authentication.student_login(username, password)
        if not user :
            print ("Username or password is incorrect.")
        else:
            student_menu(user)
            
    # check login professor
    elif role.lower() == "professor":
        user = Authentication.professor_login(username, password)
        if not user :
            print ("Username or password is incorrect.")
        else:
            professor_menu(user) 
    # show menu
