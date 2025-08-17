from .student_action import *
from .professor_action import review_thesis_requests
from .professor_action import view_defense_requests
def student_menu(student):
    while(True):
        print ("\n---Student Menu")
        print ("1. Thesis Submission Request: ")
        print ("2. View Request Status: ")
        print ("3. Resubmit Thesis Course Request ")
        print ("4. Submit Thesis Defense Request ")
        print ("5. Search in Thesis Database ")
        print ("0. Exit")
        choice = int(input("Please select "))
        if choice == 0:
            break
        if choice == 1:
            submit_thesis_request(student)
        if choice == 2:
            view_request_status(student)
        if choice == 4:
            submit_defense_request(student)
            



def professor_menu(professor):
    while(True):
        print ("1. Thesis Advisor Section")
        print ("2. Enter Reviewer Section ")
        print ("0. Exit")
        choice = int(input("Please select "))
        if choice == 0:
            break
        if choice == 1:
            advisor_menu(professor)
        if choice == 2:
            Reviewer_menu(professor)
        

def advisor_menu(professor):
    while(True):
        print ("1. View, Review, and Approve Thesis Course Requests ")
        print ("2. Approval and Management of Submitted Defense Requests ")
        print ("0. Exit ")
        choice = int(input("Please select "))
        if choice == 0:
            break
        if choice == 1:
            review_thesis_requests(professor)
        if choice == 2:
            view_defense_requests(professor)


def Reviewer_menu(professor):
    while(True):
        print ("1. Submission of Grades ")
        print ("2. Search in Thesis Database ")
        choice = int(input("Please select "))
        if choice == 0:
            break
        
