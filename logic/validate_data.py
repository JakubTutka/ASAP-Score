import re

class Validate:

    password_pattern = "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d]{8,}$"
    # ^ upper patern means: Minimum eight characters,
    # at least one uppercase letter, one lowercase letter and one number:

    email_pattern = "[a-zA-Z0-9]+@[a-zA-Z]+\.(com|pl|net|edu)"

    def checkPassword(self, password):

        if re.search(self.password_pattern, password):
            return True
        else:
            return False

    def checkEmail(self, email):

        if re.search(self.email_pattern, email):
            return True
        else:
            return False

