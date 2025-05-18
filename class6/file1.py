#datatypes addition in the code is a good practice
#return's data type is string
#you can use union to have multiple datatypes

first_name:str = "Tahir"
age:int = 31
is_married:bool = True
friends:list[str] = ["Ali","Arham","Osama"]

def greet(name:str) -> str :
    return f"hello, {name}"