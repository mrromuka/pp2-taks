import os


os.makedirs("folder1/subfolder1", exist_ok=True)
os.makedirs("folder2", exist_ok=True)


dirs = [d for d in os.listdir(".") if os.path.isdir(d)]
print(dirs)