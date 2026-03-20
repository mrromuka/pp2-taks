import shutil
import os


shutil.copy("sample.txt", "sample_copy.txt")


os.remove("sample.txt")