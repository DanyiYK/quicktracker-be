import re

# print(check_fiscal_code("test")) # False
# print(check_fiscal_code("RSSMRA80A01H501U")) # True
def check_fiscal_code(string:str):
    return re.compile(r"^[A-Z]{6}[0-9LMNPQRSTUVX]{2}[A-Z]{1}[0-9LMNPQRSTUVX]{2}[A-Z]{1}[0-9LMNPQRSTUVX]{3}[A-Z]{1}$").match(string) != None

# print(check_email("test")) # False
# print(check_email("text@example.com")) # True
def check_email(string:str):
    return re.compile(r"^\S+@\S+\.\S+$").match(string) != None

# print(check_phone_number("test")) # False
# print(check_phone_number("331 585 7421")) # True
def check_phone_number(string:str):
    return re.compile(r"^[+]*[(]{0,1}[0-9]{1,4}[)]{0,1}[-\s\./0-9]*$").match(string) != None

def check_name(string:str):
    return len(string)>=3