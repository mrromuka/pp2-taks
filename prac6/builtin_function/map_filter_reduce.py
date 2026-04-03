from functools import reduce

# Sample list
numbers = [1, 2, 3, 4, 5, 6]


squared = list(map(lambda x: x**2, numbers))
print("Squared:", squared)


evens = list(filter(lambda x: x % 2 == 0, numbers))
print("Evens:", evens)


total = reduce(lambda x, y: x + y, numbers)
print("Sum:", total)