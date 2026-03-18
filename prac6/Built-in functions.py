from functools import reduce

a = [1, 2, 3, 4, 5]

b = list(map(lambda x: x * 2, a))
print(b)

c = list(filter(lambda x: x % 2 == 0, a))
print(c)

d = reduce(lambda x, y: x + y, a)
print(d)

for i, v in enumerate(a):
    print(i, v)

x = ["a", "b", "c"]
y = [1, 2, 3]

for i, j in zip(x, y):
    print(i, j)

z = "123"
print(type(z))
z = int(z)
print(type(z))