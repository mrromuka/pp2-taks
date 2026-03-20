import shutil
import os


os.makedirs("destination", exist_ok=True)
shutil.move("sample_copy.txt", "destination/sample_copy.txt")