import os 
import platform
import subprocess


def open_file(file_path):
    # wimdos
    if platform.system() == "Windows":
        os.startfile(file_path)
        # macos
    elif platform.system() == "Darwin":
        subprocess.run(["open", file_path])
    # linux
    else:
        subprocess.run(["xdg-open", file_path])

filepath = os.path.join("file", "fake_thesis.pdf")
print(filepath)
# open_file(filepath)

