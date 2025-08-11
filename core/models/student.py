from .user import User
class Student(User):
    def __init__(self, id, name, username, password):
        super().__init__(id, name, username, password)