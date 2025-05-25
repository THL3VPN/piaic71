for count in range(1,10):
    print(f"Count is {count}")


square_list = [num**2 for num in range(1,11)]
print(square_list)

square_list = [num**2 for num in range(1,11) if num % 2 == 0]
print(square_list)