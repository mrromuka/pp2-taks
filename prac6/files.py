import shutil, os

f = open("a.txt", "w", encoding="utf-8")
f.write("1\n2\n3\n")
f.close()

f = open("a.txt", "r", encoding="utf-8")
print(f.read())
f.close()

f = open("a.txt", "a", encoding="utf-8")
f.write("4\n5\n")
f.close()

f = open("a.txt", "r", encoding="utf-8")
print(f.read())
f.close()

shutil.copy("a.txt", "b.txt")

if os.path.exists("a.txt"):
    os.remove("a.txt")