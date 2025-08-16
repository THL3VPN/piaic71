def cal(num1,num2,sign):
    if(sign=="+"):
        print(num1+num2)
    elif(sign=="-"):
        print(num1-num2)
    elif(sign=="*"):
        print(num1*num2)
    elif(sign=="/" and num2 != 0):
         print(num1/num2)
    else:
        print("Invalid input")

num1 = int(input("Enter first number = "))
num2 = int(input("Enter first second = "))
sign = input("Enter the sign = ")

state = cal(num1,num2,sign)