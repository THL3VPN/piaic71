# print ("Hello World!")
# print ("Hello World!")
# print ("Hello World!")

user_percentage = int(input("Enter your percentage = "))

if user_percentage > 90 and user_percentage < 100:
    print("You have got A+ grade")
elif user_percentage > 80 and user_percentage < 90:
    print("You have got A grade")
elif user_percentage > 100:
    print("input a valid percentage")
else:
    print("you have failed")