#One function to check if a number is even or odd

def number_checker (num1):
    if num1 % 2 == 0:
        print("The number is even")
    else:
        print("The number is odd")

number1 = int(input("Enter the number = "))
number_checker (number1)