class UserView:
    def login(self):
        email = input("Email: ")
        password = input("Password: ")

        return email, password

    def create_user(self):
        first_name = input("First name: ")
        last_name = input("Last name: ")
        email = input("Email: ")
        password = input("Password: ")
        role_name = input("User role ('manager', 'commercial', 'support'): ")

        return first_name, last_name, email, password, role_name
