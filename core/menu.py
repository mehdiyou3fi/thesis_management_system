from .student_action import *
from core.models.student import Student
from core.models.professor import Professor
def student_menu(student):
    while(True):
        print (f"\n---Student Menu --{student.name}--")
        print ("1. Thesis Submission Request: ")
        print ("2. View Request Status: ")
        print ("3. Resubmit Thesis Course Request ")
        print ("4. Submit Thesis Defense Request ")
        print ("5. Search in Thesis Database ")
        print ("0. Exit")
        choice = int(input("Please select \n"))
        if choice == 0:
            break
        if choice == 1:
            # submit_thesis_request(student)
            Student.submit_thesis_request(student)
        if choice == 2:
            Student.view_request_status(student)
        if choice == 4:
            Student.submit_defense_request(student)
            



def professor_menu(prof):
    while(True):
        print ("1. Thesis Advisor Section")
        print ("2. Enter Reviewer Section ")
        print ("0. Exit")
        choice = int(input("Please select "))
        if choice == 0:
            break
        if choice == 1:
            advisor_menu(prof)
        if choice == 2:
            Reviewer_menu(prof)
        

def advisor_menu(prof):
    while(True):
        print ("1. View, Review, and Approve Thesis Course Requests ")
        print ("2. Approval and Management of Submitted Defense Requests ")
        print ("0. Exit ")
        choice = int(input("\nPlease select "))
        if choice == 0:
            break
        if choice == 1:
            Professor.review_thesis_requests(prof)
        if choice == 2:
            Professor.view_defense_requests(prof)


def Reviewer_menu(prof):
    while(True):
        print ("1. Submission of Grades ")
        print ("2. Search in Thesis Database ")
        choice = int(input("Please select "))
        if choice == 0:
            break
        
