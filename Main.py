import secrets
import string
import math
import re

common_words = {"password", "123456", "123456789", "12345678", "12345", "qwerty", "abc123", "football", "monkey", 
                "letmein", "dragon", "baseball", "welcome", "admin", "login", "princess", "sunshine", "master", 
                "hello", "freedom", "whatever", "qazwsx", "trustno1", "starwars", "passw0rd", "shadow", "superman", 
                "michael", "jessica", "charlie", "ashley", "donald", "password1", "iloveyou", "lovely", "computer", 
                "internet", "access", "secret", "flower", "hottie", "mustang", "pokemon", "batman", "cheese", "killer", 
                "soccer", "hockey", "basketball", "summer", "winter", "spring", "autumn", "orange", "purple", "yellow", 
                "banana", "chocolate", "coffee", "pepper", "cookie", "tigger", "ginger", "buster", "harley", "thomas", 
                "jordan", "andrew", "robert", "daniel", "matthew", "joshua", "hunter", "michelle", "jennifer", "amanda", 
                "nicole", "samantha", "family", "friends", "school", "student", "teacher", "india", "america", "london", 
                "paris", "liverpool", "arsenal", "chelsea", "pokemon123", "admin123", "welcome123", "qwerty123", 
                "abc123456", "love123", "user", "root", "guest", "test", "default"}
KEYBOARD_PATTERNS = {"qwerty", "asdf", "zxcv", "12345", "123456", "987654", "qaz", "wsx", "edc"}

#LENGTH INPUT
def length_input():
    while True:
        try:
            length = int(input("Enter length: "))

            if length > 0:
                return length

            print("Length must be greater than zero.")

        except ValueError:
            print("Please enter a valid integer.")


# INPUT TAKING OF YES AND NO
def yes_no_input(message):
    while True:
        choice = input(message).lower()

        if choice in ("y","yes"):
            return True

        elif choice in ("n","no"):
            return False

        print("Please enter Y or N.")
        
def generator(length, upper, lower, digits, symbols):
    
    selected_sets = []
    password = []

    if upper:
        selected_sets.append(string.ascii_uppercase)
        password.append(secrets.choice(string.ascii_uppercase))

    if lower:
        selected_sets.append(string.ascii_lowercase)
        password.append(secrets.choice(string.ascii_lowercase))

    if digits:
        selected_sets.append(string.digits)
        password.append(secrets.choice(string.digits))

    if symbols:
        selected_sets.append(string.punctuation)
        password.append(secrets.choice(string.punctuation))

    if not selected_sets:
        return None 

    if length < len(password):
        return False

    all_characters = "".join(selected_sets)

    while len(password) < length:
        password.append(secrets.choice(all_characters))
    
    secrets.SystemRandom().shuffle(password)
    return "".join(password)

def passcode():

    print("=" * 55)
    print("       Automatic Password Generator")
    print("=" * 55)
    length = length_input()
    print("=" * 55)
    print("Chose categories for your password, ")
    use_upper = yes_no_input("Do you want Uppercase letters[Answer in Y/n] :")
    use_lower = yes_no_input("Do you want Lowercase letters[Answer in Y/n] :")
    use_digit = yes_no_input("Do you want Digits[Answer in Y/n] :")
    use_symbol = yes_no_input("Do you want Symbols[Answer in Y/n] :")

    pwd = generator(length, use_upper, use_lower, use_digit, use_symbol)

    if pwd is None:
        print("Please select atleast one character")
        return None

    if pwd is False :
        required = (use_upper + use_lower + use_digit + use_symbol)
        print("=" * 55)
        print(f"Invalid Length. \n Please enter atleast {required} number as length")
        print("~" * 55)
        return 'short'
    
    print("=" * 55)
    print(f"Your generated password is : {pwd}")
    print("=" * 55)
    
    
    return pwd
        

""" Strength Check start """

# Length check
def length_checker(password):
    if(len(password) >= 16):
        return 30
    elif(len(password) >= 12):
        return 25
    elif(len(password) >= 8):
        return 15
    elif(len(password) < 8):
        return 5

#Character Diversity
def character_diversity(password):
    score = 0

    any_upper = any(char.isupper() for char in password)
    any_lower = any(char.islower() for char in password)
    any_digit = any(char.isdigit() for char in password)
    any_symbol = any(not char.isalnum() for char in password)

    if any_upper:
        score += 7

    if any_lower :
        score += 7

    if any_digit :
        score += 8
        

    if any_symbol :
        score += 8
        
    return score

# Dictionary Word
def dictionary_word(password):
    
    small  = password.lower()

    for word in common_words:
        if word in small:
            return True, word

    return False, ""

# KEYBOARD PATTERN RECOGNITION
def keyboard_pattern(password):


    small  = password.lower()

    for word in KEYBOARD_PATTERNS:
        if word in small:
            return True

    return False
#Repeated Patterns
def repeated_pattern(password):

    pattern_rec = re.search(r"(.)\1{3,}", password)

    return bool(pattern_rec)

# Entropy
def estimate_entropy(password):
    pool = 0

    if any(i.isupper() for i in password):
        pool += 26
    if any(i.islower() for i in password):
        pool += 26
    if any(i.isdigit() for i in password):
        pool += 10
    if any(not i.isalnum() for i in password):
        pool += 32

    if pool == 0:
        entropy = 0
    else:
        entropy = len(password) * math.log2(pool)

    return entropy

# Evaluation of password
def evaluation(password):

    score = 0

    # Length Check
    score += length_checker(password)
    
    # Character diversity
    char_score = character_diversity(password)
    score += char_score

    # Dictionary Word
    found, word = dictionary_word(password)

    if found :
        score -= 20
    # Keyboard pattern
    if keyboard_pattern(password):
        score -= 15

    # Repeated Pattern
    if repeated_pattern(password):
        score -= 10

    # Entropy
    entropy = estimate_entropy(password)

    if entropy >= 90:
        score += 40
    
    elif entropy >= 70:
        score += 35

    elif entropy >= 50:
        score += 25

    elif entropy >= 30:
        score += 15

    elif entropy < 30:
        score += 5
    
    score = max(0, min(score,100))

    # Standard Decision
    if score >= 90:
        rating = "Excellent"

    elif score >= 75:
        rating = "Strong"

    elif score >= 50:
        rating = "Moderate"

    elif score >= 25:
        rating = "Weak"

    else:
        rating = "Very Weak"

    return {
        "score": score,
        "standard": rating,
        "entropy" : round(entropy, 2)
    }
    

# Showing the output
def main():
    while True: 

        password = passcode()
        if password is 'short':
            continue

        result = evaluation(password)

        print(f"Score : {result['score']}/100")
        print(f"Standard : {result['standard']}")
        print(f"Entropy : {result['entropy']} bits")
        print("=" * 55)
    
        again = yes_no_input("Generate another password[Answer in Y/n] :")

        if not again:
            print("Thank You for using password generator.")
            print("~" * 55)
            break
        
        print("~" * 55)

main()
