
names = ["Alice", "Bob", "Charlie"]
ages = [25, 30, 22]


for name, age in zip(names, ages):
    print(f"{name} is {age} years old")

print("---")

for index, name in enumerate(names, start=1):
    print(f"{index}. {name}")