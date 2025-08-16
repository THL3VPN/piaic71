

calorieList = [("mango",10),("apple",20) ]

inputFruit = input("Enter the fruit = ").lower()

for count1 in calorieList:
    
    if inputFruit == count1[0]:

        print(f"The fruit is {inputFruit} and its calories are {count1[1]}")
    