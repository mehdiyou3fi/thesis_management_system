import os 
import platform
import subprocess
from  utils.paths import ensure_dirs
import shutil

def copy_file_safe(src_path:str , dest_dir:str, dest_filename:str) -> str:
    # حتما باید دایرکتوری موحود باشه
    ensure_dirs()

    # حتما دایرکت.ری مقصد موجود باشه
    os.makedirs(dest_dir, exist_ok=True)

    # اسم فایل و پسوند ان را ازهم جدا میکنیم 
    base, ext =os.path.splitext(dest_filename)
    dst = os.path.join(dest_dir, dest_filename)

    # جلوگیری از بازنویسی فایل موجود 
    i = 1 
    while os.path.exists(dst):
        dst = os.path.join(dest_dir, f"{base}_{i}{ext}")
        i+=1

    # کپی فایل 
    shutil.copy2(src_path, dst)

    # مسیر نرمال شده را پس میفرستیم
    return dst.replace("\\", "/")
    


def open_file(file_path):
    if os.path.exists(file_path):
        # wimdos
        if platform.system() == "Windows":
            os.startfile(file_path)
            # macos
        elif platform.system() == "Darwin":
            subprocess.run(["open", file_path])
        # linux
        else:
            subprocess.run(["xdg-open", file_path])
    else:
        print ("⚠️ File not found:", file_path)



