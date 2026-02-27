import math
#1
degree = float(input("Input degree: "))
radian = degree * math.pi / 180
print(f"Output radian: {radian:.6f}")
#2
h = float(input("Height: "))
a = float(input("Base, first value: "))
b = float(input("Base, second value: "))

area = (a + b) * h / 2

print(f"Expected Output: {area}")
#3
n = int(input("Input number of sides: "))
side = float(input("Input the length of a side: "))

area = side ** 2 if n == 4 else "Only implemented for square"
print(f"The area of the polygon is: {area}")
#4
base = float(input("Length of base: "))
height = float(input("Height of parallelogram: "))
area = base * height
print(f"Expected Output: {area}")