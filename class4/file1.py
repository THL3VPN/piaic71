first_name = "Tahir"
# print ( id(first_name) ) #it is used to give the memory idenifier

# print( type(first_name)) #it will give the data type

# print(type(first_name) == str)

#validation operator

age = input("Enter your age ")

if age.isdigit():                   #isdigit is a function which returns TRUE if the variable has only digit
    print(f"Your age is {age}")
else:
    print("Invalid input")