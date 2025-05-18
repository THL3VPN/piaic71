# Squaring a number,
# Multiplying two numbers,
# Checking if a number is positive

numSquuare = lambda num1 : num1*num1
numMultiply = lambda num1,num2 : num1*num2
numPositive = lambda num1 : num1 % 2 == 0

firstNumber = int(input("Enter the first number = "))
secondNumber = int(input("Enter the second number = "))

print(f"The square of the number is = {numSquuare(firstNumber)}")
print(f"The multiplication of the number is = {numMultiply(firstNumber,secondNumber)}")

if numPositive(firstNumber) == True:
    print("The number is even")
else:
    print("The number is odd")

