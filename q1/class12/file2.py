class student:
    def __init__(self,name,roll_no):
        self.name : str = name
        self.roll_no : int = roll_no
        self.institue = "PIAIC"
    
    def get_admission (self):
        print (f"name is {self.name} , rollNo is {self.roll_no} , institute is {self.institue}")

student1 = student("John","001")
student2 = student("Alice","002")

student1.get_admission()
student2.get_admission()

class course:
    def __init__(self, course_name):
        self.course_name = course_name
        self.student = []
    
    def add_student(self, student):
        self.student.append(student)
    

ai_course = course("AI")    #new class called

ai_course.add_student(student1) #purani class ka student

print(ai_course.student[0].name)    #purani class k sturent ki name property