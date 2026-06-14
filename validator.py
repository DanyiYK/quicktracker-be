import re

# TODO: Separate validators

STANDARD_BOX_SIZES = {
    "small": {
        "measurements": [4, 2, 4],
        "price_increment": 1.05
    },
    "medium": {
        "measurements": [6, 3, 6],
        "price_increment": 1.15
    },
    "large": {
        "measurements": [8, 4, 6],
        "price_increment": 1.20
    },
}

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
    return len(string.strip())>=3

def check_string(string:str):
    return len(string.split())>0

def check_size(size:str):
    return size in STANDARD_BOX_SIZES

def check_weight(weight:float):
    return weight >= 0 or weight <= 500

