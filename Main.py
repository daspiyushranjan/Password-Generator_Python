import random
import string

#LENGTH INPUT
def length_input():
    length = int(input("Enter your required length : "))

    if length <= 0 :
        print("Enter the number greater than 0")
    else:
        return length


# INPUT TAKING OF YES AND NO
def yes_no_input(message):
    choice = input(message).lower()
    
    if choice in ['y', 'yes']:
        return True
    if choice in ['n', 'no']:
        return False
    else:
        print("Enter a valid character from Y/n")

def generator(length, upper, lower, digits, symbols):
    
    selected_sets = []
    password = []

    if upper:
        selected_sets.append(string.ascii_uppercase)
        password.append(random.choice(string.ascii_uppercase))

    if lower:
        selected_sets.append(string.ascii_lowercase)
        password.append(random.choice(string.ascii_lowercase))

    if digits:
        selected_sets.append(string.digits)
        password.append(random.choice(string.digits))

    if symbols:
        selected_sets.append(string.punctuation)
        password.append(random.choice(string.punctuation))

    if not selected_sets:
        print("Please select atleast one category")

    if length < len(password):
        return 'short'

    all_characters = "".join(selected_sets)

    while len(password) < length:
        password.append(random.choice(all_characters))
    
    random.shuffle(password)
    return "".join(password)

def main():

    length = length_input()

    use_upper = yes_no_input("Do you want Uppercase letters[Answer in Y/n] :")
    use_lower = yes_no_input("Do you want Lowercase letters[Answer in Y/n] :")
    use_digit = yes_no_input("Do you want Digits[Answer in Y/n] :")
    use_symbol = yes_no_input("Do you want Symbols[Answer in Y/n] :")

    password = generator(length, use_upper, use_lower, use_digit, use_symbol)

    if password == 'short':
        required = (use_upper + use_lower + use_digit + use_symbol)
        print(f"Invalid Length. \n Please enter atleast {required} number as length")

    print(f"Your generated password is : {password}")

    again = yes_no_input("Generate another password[Answer in Y/n] :")

    if not again:
        print("Thank You for using password generator.")
        

main()