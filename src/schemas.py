import re

from flask import abort
from marshmallow import Schema, fields, validates, ValidationError


class AuthSchema(Schema):
    username = fields.Str(required=True)
    user_id = fields.Str(dump_only=True)
    password = fields.Str(required=True, load_only=True)
    
    

    @validates('username')
    def validate_username(self, user):
        if user is None:
            raise ValidationError("Username required")

    @validates('password')
    def validate_password(self, password):
        if password is None:
            raise ValidationError("Password required!")


class UserSchema(Schema):
    username = fields.Str(required=True)
    password = fields.Str(required=True)
    role = fields.Str(required=True)
    name = fields.Str(required=True)
    phone = fields.Str(required=True)
    address = fields.Str(required=True)
    city = fields.Str(required=True)
    state = fields.Str(required=True)
    pincode = fields.Str(required=True)

    @validates('username')
    def validate_username(self, username):
        pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        if not re.match(pattern, username):
            raise ValidationError("Not a valid email address.")

    @validates('password')
    def validate_password(self, password):
        password_pattern = r"^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[@#$%^&+=!]).{6,}$"
        if not re.match(password_pattern, password):
            raise ValidationError("Not a valid email address.")

    @validates('role')
    def validate_role(self, role):
        roles = ['Customer', 'Seller']
        if role not in roles:
            raise ValidationError("Not a valid role.")

    @validates('phone')
    def validate_phone(self, phone):
        phone_pattern = r"^(?!0{10})\d{10}$"
        if not re.match(phone_pattern, phone):
            raise ValidationError("Not a valid phone number.")

    @validates('address')
    def validate_address(self, address):
        allowed_chars_regex = re.compile(r'^[a-zA-Z0-9, -]+$')
        if not allowed_chars_regex.match(address):
            raise ValidationError("Not a valid address.")

    @validates('city')
    def validate_city(self, city):
        pattern = re.compile(r'^[a-zA-Z ]+$')
        if not pattern.match(city):
            raise ValidationError("Not a valid city.")

    @validates('state')
    def validate_state(self, city):
        pattern = re.compile(r'^[a-zA-Z ]+$')
        if not pattern.match(city):
            raise ValidationError("Not a valid state.")

    @validates('pincode')
    def validate_pincode(self, pincode):
        pincode_pattern = r"^(?!0{6})\d{6}$"
        if not re.match(pincode_pattern, pincode):
            raise ValidationError("Not a valid pincode.")


class UserResponseSchema(Schema):
    username = fields.Str(required=True)
    # password = fields.Str(required=True)
    role = fields.Str(required=True)
    name = fields.Str(required=True)
    phone = fields.Int(required=True)
    address = fields.Str(required=True)
    city = fields.Str(required=True)
    state = fields.Str(required=True)
    pincode = fields.Int(required=True)


class UserRequestSchema(Schema):
    username = fields.Str()
    status = fields.Str()


class ProductSchema(Schema):
    product_id = fields.Int()
    description = fields.Str()
    price = fields.Float()
    category = fields.Str()
    gender = fields.Str()
    size = fields.Str()


class SellerSchema(Schema):
    product_id = fields.Str(required=True)
    description = fields.Str(required=True)
    price = fields.Float(required=True)
    keyword = fields.Str(required=True)
    category = fields.Str(required=True)
    gender = fields.Str(required=True)
    size = fields.Str(required=True)
    quantity = fields.Str(required=True)

    @validates('product_id')
    def is_valid_product_id(self, product_id):
        return product_id.isdigit() and len(product_id) == 6

    @validates('category')
    def is_valid_category(self, category):
        categories = ['Ethnic', 'Casual', 'Party', 'Formal', 'Nightwear']
        if category in categories:
            return True
        return False

    @validates('gender')
    def is_valid_gender(self, gender):
        genders = ['Men', 'Women', 'Kids']
        if gender in genders:
            return True
        return False

    @validates('price')
    def is_valid_price(self, price):
        float_price = float(price)
        if '.' in str(float_price):
            return True
        else:
            return False

    @validates('size')
    def is_valid_size(self, size):
        sizes = ['S', 'M', 'L', 'XL', 'XXL', 'XXXL']
        if size in sizes:
            return True
        else:
            return False

    @validates('quantity')
    def is_valid_integer(self, input_value):
        try:
            int(input_value)
            return True
        except ValueError:
            return False


class OrderSchema(Schema):
    pass


class UserDetailsSchema(Schema):
    Name = fields.Str(required=True)
    Phone = fields.Int(required=True)
    Address = fields.Str(required=True)
    City = fields.Str(required=True)
    State = fields.Str(required=True)
    Pincode = fields.Int(required=True)


class UserUpdateSchema(Schema):
    username = fields.Str()
    password = fields.Str()
    phone = fields.Str()
    address = fields.Str()
    city = fields.Str()
    state = fields.Str()
    pincode = fields.Int()

    @validates('username')
    def validate_username(self, username):
        pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        if not re.match(pattern, username):
            # abort()
            raise ValidationError("Not a valid email address.")

    @validates('password')
    def validate_password(self, password):
        password_pattern = r"^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[@#$%^&+=!]).{6,}$"
        if not re.match(password_pattern, password):
            raise ValidationError("Not a valid email address.")

    @validates('phone')
    def validate_phone(self, phone):
        phone_pattern = r"^(?!0{10})\d{10}$"
        if not re.match(phone_pattern, phone):
            raise ValidationError("Not a valid phone number.")

    @validates('address')
    def validate_address(self, address):
        allowed_chars_regex = re.compile(r'^[a-zA-Z0-9, -]+$')
        if not allowed_chars_regex.match(address):
            raise ValidationError("Not a valid address.")

    @validates('city')
    def validate_city(self, city):
        pattern = re.compile(r'^[a-zA-Z ]+$')
        if not pattern.match(city):
            raise ValidationError("Not a valid city.")

    @validates('state')
    def validate_state(self, city):
        pattern = re.compile(r'^[a-zA-Z ]+$')
        if not pattern.match(city):
            raise ValidationError("Not a valid state.")

    @validates('pincode')
    def validate_pincode(self, pincode):
        pincode_pattern = r"^(?!0{6})\d{6}$"
        if not re.match(pincode_pattern, pincode):
            raise ValidationError("Not a valid pincode.")

