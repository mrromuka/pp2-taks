#1
class Dog:
    species = "Canis familiaris"

    def __init__(self, name, age):
        self.name = name
        self.age = age

dog1 = Dog("Buddy", 3)
dog2 = Dog("Max", 5)

print(dog1.species)
print(dog2.species)

Dog.species = "Canis lupus"
print(dog1.species)
print(dog2.species)
