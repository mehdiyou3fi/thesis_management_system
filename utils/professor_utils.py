import os
from .data_manager import DataManager
def decrease_reviewer_capacity(professor_name):
    professors_file = os.path.join ("data", "professor.json")
    professors = DataManager.read_json(professors_file)

    for p in professors :
        if p["name"] == professor_name:
            if p["review_capacity"] > 0 :
                p["review_capacity"]-=1
                DataManager.write_json(professors_file, professors)
                return True
            else:
                print (f"professor dos not have capacity ")
                return False
    return False

