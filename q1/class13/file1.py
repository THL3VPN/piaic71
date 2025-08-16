#class variables
#ye self k sath use nai hoskte , inko ap class.X variable k through call and change kr skte hain
# eg: teacher = "hamza" , ye hum neeche class.object k sath call horha hai

class person:

    teacher = "hamza"
    quarter = "q1"
   
    def __init__(self,name,age):
        self.name = name
        self.age = age
    
    def say_hi(self):
        print("Hello")

    @classmethod
    def change_quarter(cls,quarter):
        cls.qarter = quarter
        print(f"{quarter} quarter started")

p1 = person("john","30")
p2 = person("alice","40")

print(p1.name)
print(p1.quarter)

p2.quarter = "q2"
print(p2.quarter)

p1.say_hi()
p1.change_quarter(2)

