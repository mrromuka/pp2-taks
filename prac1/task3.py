a = input()

c = 0
for i in a:
    if not i.isdigit():
        c += 1

if c == 0:
    print("int")
else:
    print("str")
