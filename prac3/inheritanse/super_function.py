class Person:
    def __init__(self, fname, lname):
        self.fname = fname
        self.lname = lname

class Student(Person):
    def __init__(self, fname, lname):
        super().__init__(fname, lname)

s = Student("Alice", "Smith")
print(s.fname)  # Alice
print(s.lname)  # Smith
