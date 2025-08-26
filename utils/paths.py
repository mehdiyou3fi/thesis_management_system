import os 
'''همه ی مسیر ها اینجا تعریف شدند تا اشتباهی در کد پیش نیاد و اینکه اگر جایی تغییر کرد از اینجا فقط تغییر بدهیم'''

# ریشه ها 
DATA_DIR = "data"
FILES_DIR = "file"

# زیر پوشه های فایل های پایان نامه 
THESIS_PDF_DIR = os.path.join(FILES_DIR, "thesis")
IMAGES_DIR =os.path.join(FILES_DIR, "images")

# فایل های داده 
STUDENT_JSON = os.path.join(DATA_DIR,"student.json")
TEACHERS_JSON = os.path.join(DATA_DIR, "professor.json")   # قبلاً professor.json
COURSES_JSON = os.path.join(DATA_DIR, "courses.json")
THESIS_JSON = os.path.join(DATA_DIR, "thesis.json")       # ادغام thesis_requests/...
DEFENDED_JSON = os.path.join(DATA_DIR, "defended_thesis.json")
EXTERNAL_REVIEWERS_JSON = os.path.join(DATA_DIR, "external_reviewers.json")

def ensure_dirs():
    os.makedirs(DATA_DIR, exist_ok=True)
    os.makedirs(FILES_DIR, exist_ok=True)
    os.makedirs(THESIS_PDF_DIR, exist_ok=True)
    os.makedirs(IMAGES_DIR, exist_ok=True)




