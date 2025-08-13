import os 
from utils.data_manager import DataManager
from .student import Student

class Authentication():
    @staticmethod
    def student_login(username, password):
        # مسیر برای پیدا کردن فایل جیسون در هر سیتسمی 
        student_file = os.path.join("data", "student.json")
        # جستو جو داشنجویان 
        for s in DataManager.read_json(student_file):
            if s["username"] == username and s["password"] == password:
                return Student(s["id"],s["name"], s["username"], s["password"])
        return None
    @staticmethod
    def professor_login(username, password):
        proffessor_file = os.path.join("data", "professor.json")
        for p  in DataManager.read_json(proffessor_file):
            if p["username"] == username and p["password"] == password:
                return Student(p["id"],p["name"], p["username"], p["password"])
            return None 
