def auth_checker(calling_function):
    def wrapperNo1():
        print("checking user access")
        calling_function()

    return wrapperNo1

@auth_checker
def checking_access():
    print("This is checking_access function")

@auth_checker
def get_admission():
    print("This is get_admission function")


checking_access()
get_admission()
