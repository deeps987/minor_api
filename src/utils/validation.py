import re
import maskpass
from src.utils.config import queries, prompts, inputs


def is_valid_pincode(pincode):
    pincode_pattern = r"^(?!0{6})\d{6}$"
    return re.match(pincode_pattern, pincode) is not None


def is_valid_phone(phone):
    phone_pattern = r"^(?!0{10})\d{10}$"
    return re.match(phone_pattern, phone) is not None

    
def is_valid_username(obj, username):
    if not obj.check_user_exists(queries["USERNAME_EXISTS"], username):
        pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        return bool(re.match(pattern, username))
    return False


def is_valid_address(address):
    allowed_chars_regex = re.compile(r'^[a-zA-Z0-9, -]+$')
    if allowed_chars_regex.match(address):
        return True
    return False


def is_valid_string(inp):
    pattern = re.compile(r'^[a-zA-Z ]+$')
    if pattern.match(inp):
        return True
    return False
        
def is_valid_role(role):
    roles = ['Customer', 'Seller']
    if role in roles:
        return True
    return False


def is_valid_product_id(product_id):
    return product_id.isdigit() and len(product_id) == 6



def is_valid_category(category):
    categories = ['Ethnic', 'Casual', 'Party', 'Formal', 'Nightwear']
    if category in categories:
        return True
    return False


def is_valid_gender(gender):
    genders = ['Men', 'Women', 'Kids']
    if gender in genders:
        return True
    return False

def is_valid_price(price):
    float_price = float(price)
    if '.' in str(float_price):
        return True
    else:
        return False


def is_valid_size(size):
    sizes = ['S', 'M', 'L', 'XL', 'XXL', 'XXXL']
    if size in sizes:
        return True
    else:
        return False

    
def is_valid_integer(input_value):
    try:
        int(input_value)
        return True
    except ValueError:
        return False


def is_valid_password(password):
    password_pattern = r"^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[@#$%^&+=!]).{6,}$"
    return re.match(password_pattern, password) is not None

def password_validator(func):
    def wrapper():
        while True:
            password = maskpass.advpass()
            if not password:
                return None
            if is_valid_password(password):
                result = func(password)
                return result
            else:
                print(prompts["PASSWORD_VALIDITY"])
    return wrapper

@password_validator
def check_password_validity(password):
    return password     
    

    
def is_valid(product, product_id, quantity):
    Quantity = int(quantity)
    quan = product.check_quantity_exist(product_id)
    if quan is not None and Quantity <= int(quan[0]):
        return True
    else:
        print(prompts["INVALID_QUANTITY"])
        return False

        
def check_availability(product, product_id):
    while True:
        quantity = input(inputs["QUANTITY"])
        if quantity.isdigit():
            if is_valid(product, product_id, quantity):
                return quantity
            
        else:
            print(prompts["INVALID_INTEGER"])
    
    

    