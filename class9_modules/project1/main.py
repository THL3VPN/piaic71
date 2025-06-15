from auth import login
from modules.payments import pay_fees
from colorama import Fore,Back

login("admin")
pay_fees(100)

print(Fore.RED + "Hello World")
print(Fore.WHITE)


