def cal(num1,num2,sign):
    if(sign=="+"):
        print(num1+num2)
        return "valid"
    elif(sign=="-"):
        print(num1-num2)
        return "valid"
    elif(sign=="*"):
        print(num1*num2)
    elif(sign=="/" and num2 != 0):
         print(num1/num2)
         return "valid"         
    else:
        print("Invalid input")
        return "invalid"

num1 = int(input("Enter first number = "))
num2 = int(input("Enter first second = "))
sign = input("Enter the sign = ")


while True:
    
    state = cal(num1,num2,sign)
    
    if (state=="valid"):
        break
    else:
        num1 = int(input("Enter first number = "))
        num2 = int(input("Enter first second = "))
        sign = input("Enter the sign = ")