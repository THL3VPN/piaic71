class human():
    def __init__(self,name,age):
        self.name = name
        self.age = age

    def eat(self):
        print("Eating with right hand")    

class student(human):
    def __init__(self,name,age,rollNo):
        super().__init__(name,age)
        self.rollNo = rollNo

class teacher(human):
    def __init__(self,name,age,salary):
        super().__init__(name,age)
        self.salary = salary

    def eat(self):
        print("Eating with left hand")    

std1 = student("john","21","001")
teach1 = teacher("Sir Mohsin","32","30000")

print(std1.name)
std1.eat()

print(teach1.name)
teach1.eat()