import maskpass
from utils.config import queries, prompts, menu, inputs, constant
from utils import validation
from bcrypt import gensalt, hashpw



class Choice:

    def __init__(self):
        self.user = None


    def auth_login(self):
        """
        function to take username and password as input
        """
        username = input(inputs["CREDENTIALS_USERNAME"])
        password = maskpass.advpass()
        return [username,password]

    def get_valid_product(self, statement, prompt, func):
        """
        function to take product details as input
        """
        while True:
            inp = input(statement)
            if func(inp):
                return inp
            print(prompt)


    def get_product_description(self):
        """
        function to accept description of product
        """
        Description = input(inputs["DESCRIPTION"])
        return Description


    def get_product_keyword(self):
        """
        function to accept keyword of product
        """
        Keyword = input(inputs["KEYWORD"])
        return Keyword


    def accept_product_id(self):
        """
        function to accept product_id
        """
        product_id = input(inputs["PRODUCT_ID"])
        return product_id


    def get_valid_input(self, statement, prompt, func=None, obj=None):
        """
        function to take input details
        """
        while True:
            inp = input(statement)
            if not inp:
                return None
            if obj is not None:
                if func(obj, inp):
                    return inp
                print(prompt)
            else:
                if func(inp):
                    return inp
                print(prompt)

    @property
    def password(user):
        return user._password

    @password.setter
    def password(user, new_password):
        user._password = new_password

    def _change_password(self, user):
        password = validation.check_password_validity()
        if password is not None:
            salt = gensalt()
            hashed_password = hashpw(password.encode('utf-8'), salt)
            user.password = hashed_password
            user.change_password(hashed_password)
            return hashed_password
        else:
            return password

    def change_address(self, user):
        """
        function to take address details as input
        """
        address = self.get_valid_input(inputs["ADDRESS"], prompts["INVALID_ADDRESS"], validation.is_valid_address)
        user.address = address if address is not None else user.address
        city = self.get_valid_input(inputs["CITY"], prompts["ALPHABET_CHECK"], validation.is_valid_string)
        user.city = city if city is not None else user.city
        state = self.get_valid_input(inputs["STATE"], prompts["ALPHABET_CHECK"], validation.is_valid_string)
        user.state = state if state is not None else user.state
        pincode = self.get_valid_input(inputs["PINCODE"], prompts["PINCODE_VALIDITY"], validation.is_valid_pincode)
        user.pincode = pincode if pincode is not None else user.pincode
        details = [address, city, state, pincode, user.user_id]
        return details

    def change_phone(self, user):
        """
        function to take phone number as input
        """
        phone = self.get_valid_input(inputs["PHONE"], prompts["PHONE_VALIDITY"], validation.is_valid_phone)
        if phone is not None:
            user.phone = phone
        return phone

    def change_username(self, user):
        """
        function to take username as input
        """
        username = self.get_valid_input(inputs["NEW_USERNAME"], prompts["INVALID_USERNAME"],
                                        validation.is_valid_username, user)
        if username is not None:
            user.username = username
        return username

    def get_name(self):
        """
        function to take name
        """
        name = input(inputs["NAME"])
        return name

    def delete_seller_account(self, user):
        """
        function to acceot seller username
        """
        username = input(prompts["DELETE SELLER"])
        return username


    def address_choice(self):
        """
        function to accept address choice
        """
        address = input(prompts["ADDRESS_CHOICE"])
        return address
