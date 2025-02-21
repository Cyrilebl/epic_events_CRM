def user_choice(number_of_choices):
    while True:
        try:
            user_choice = int(input("Enter your choice: "))
            if 0 < user_choice <= number_of_choices:
                return user_choice
            else:
                print("Invalid choice... ")
        except ValueError:
            print("Invalid input. Please enter a number.")
