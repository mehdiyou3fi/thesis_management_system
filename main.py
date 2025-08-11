from core.models.authentication import Authentication
from core.models.menu import student_menu
from core.models.menu import professor_menu
if __name__ =="__main__":
    print ("Welcome to the Thesis Management System")
    role = input("what is your role (student or professor):")
    username = input("username: ")
    password = input("password: ")
    # check login student 
    user = Authentication.student_login(username, password)
    if not user :
        print ("Username or password is incorrect.")
    else:
        if role.lower() == "student":
            student_menu(user)
            
    # check login professor

    # show menu
