#One function to multiply two numbers

def multiply(num1,num2):
    num3 = num1 * num2
    return num3

number_1 = int(input("Enter the first number = "))
number_2 = int(input("Enter the second number = "))

number_3 = multiply(number_1,number_2)

print (f"""first number is {number_1}  
second number is {number_2} 
multiplicaiton result is {number_3}""")

