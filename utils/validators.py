import os 

def is_pdf(path: str) -> bool:
    return os.path.splitext(path)[1].lower() == ".pdf"

def is_jpg(path: str) -> bool :
    return os.path.splitext(path)[1].lower() in (".jpg",".jpeg")

def validate_defense_files(pdf_path, first_img_path, last_img_path):
    if not is_pdf(pdf_path):
        return False, "Only PDF files are allowed ."
    if not (is_jpg(first_img_path) and is_jpg(last_img_path)):
        return False, "First and last page image must be jpg/jpeg."
    return True, ""