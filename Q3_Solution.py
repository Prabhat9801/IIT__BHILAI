import random
import string

def generate_password(pwd_length):
    # min_size is minimum password length we allow
    min_size=4
    if pwd_length<min_size:
        error_msg="Length must be at least 4"
        print(error_msg)
        return None
    # uppercase_letters has all capital letters A to Z
    uppercase_letters=string.ascii_uppercase
    # lowercase_letters has all small letters a to z
    lowercase_letters=string.ascii_lowercase
    # number_chars has all digits 0 to 9
    number_chars=string.digits
    # special_symbols has all special characters like !@#
    special_symbols=string.punctuation
    
    # all_characters combines everything together
    all_characters=uppercase_letters+lowercase_letters+number_chars+special_symbols
    # pwd_list stores individual characters of password
    pwd_list=[]
    
    # char1 is one random uppercase letter
    char1=random.choice(uppercase_letters)
    pwd_list.append(char1)
    # char2 is one random lowercase letter
    char2=random.choice(lowercase_letters)
    pwd_list.append(char2)
    # char3 is one random number
    char3=random.choice(number_chars)
    pwd_list.append(char3)
    # char4 is one random special character
    char4=random.choice(special_symbols)
    pwd_list.append(char4)
    
    # remaining_length is how many more chars we need
    remaining_length=pwd_length-4
    # count tracks loop iterations
    count=0
    while count<remaining_length:
        # random_char is any random character from all types
        random_char=random.choice(all_characters)
        pwd_list.append(random_char)
        count=count+1
    
    # shuffle mixes up the order of characters
    random.shuffle(pwd_list)
    # final_password will be the complete password string
    final_password=""
    # idx is loop counter
    idx=0
    while idx<len(pwd_list):
        final_password=final_password+pwd_list[idx]
        idx=idx+1
    return final_password

def strengthen_password(user_password):
    if not user_password:
        error_text="Password cannot be empty"
        print(error_text)
        return None
    
    # password_chars is list of all characters in password
    password_chars=list(user_password)
    
    # has_uppercase is flag, 1 means we found uppercase
    has_uppercase=0
    # has_lowercase is flag, 1 means we found lowercase
    has_lowercase=0
    # has_number is flag, 1 means we found a digit
    has_number=0
    # has_symbol is flag, 1 means we found special char
    has_symbol=0
    
    # position tracks where we are in password
    position=0
    while position<len(user_password):
        # current_char is the character we are checking now
        current_char=user_password[position]
        if current_char.isupper():
            has_uppercase=1
        if current_char.islower():
            has_lowercase=1
        if current_char.isdigit():
            has_number=1
        if current_char in string.punctuation:
            has_symbol=1
        position=position+1
    
    # if missing any type, add a random one
    if has_uppercase==0:
        # new_char is the character we are adding
        new_char=random.choice(string.ascii_uppercase)
        password_chars.append(new_char)
    if has_lowercase==0:
        new_char=random.choice(string.ascii_lowercase)
        password_chars.append(new_char)
    if has_number==0:
        new_char=random.choice(string.digits)
        password_chars.append(new_char)
    if has_symbol==0:
        new_char=random.choice(string.punctuation)
        password_chars.append(new_char)
    
    # shuffle mixes characters randomly
    random.shuffle(password_chars)
    # strengthened_pwd is the final improved password
    strengthened_pwd=""
    # i is loop counter
    i=0
    while i<len(password_chars):
        strengthened_pwd=strengthened_pwd+password_chars[i]
        i=i+1
    return strengthened_pwd

def check_strength(password_to_check):
    # minimum_length is shortest strong password
    minimum_length=8
    if len(password_to_check)<minimum_length:
        return "Weak"
    
    # found_upper is flag for uppercase found
    found_upper=0
    # found_lower is flag for lowercase found
    found_lower=0
    # found_digit is flag for number found
    found_digit=0
    # found_special is flag for special char found
    found_special=0
    
    # index tracks position in password
    index=0
    while index<len(password_to_check):
        # character is current char being checked
        character=password_to_check[index]
        if character.isupper():
            found_upper=1
        if character.islower():
            found_lower=1
        if character.isdigit():
            found_digit=1
        if character in string.punctuation:
            found_special=1
        index=index+1
    
    # total_checks counts how many types we found
    total_checks=found_upper+found_lower+found_digit+found_special
    if total_checks==4:
        return "Strong"
    else:
        return "Weak"

def main():
    # title is the program header
    title="Password Generator System"
    print(title)
    # separator is line of equal signs
    separator="="*50
    print(separator)
    
    # program_running is flag to keep menu loop going
    program_running=1
    while program_running==1:
        menu_text="\nOptions:"
        print(menu_text)
        option1="1. Generate random strong password"
        print(option1)
        option2="2. Strengthen existing password"
        print(option2)
        option3="3. Check password strength"
        print(option3)
        option4="4. Exit"
        print(option4)
        
        user_choice=input("Enter choice (1-4): ")
        
        if user_choice=="1":
            input_valid=1
            try:
                length_input=input("Enter password length: ")
                password_length=int(length_input)
            except:
                input_valid=0
            
            if input_valid==0:
                error="Invalid input. Please enter a number."
                print(error)
            else:
                generated_pwd=generate_password(password_length)
                if generated_pwd!=None:
                    output="Generated password: "+generated_pwd
                    print(output)
        
        elif user_choice=="2":
            user_pwd=input("Enter your easy-to-remember password: ")
            improved_pwd=strengthen_password(user_pwd)
            if improved_pwd!=None:
                original="Original password: "+user_pwd
                print(original)
                improved="Strengthened password: "+improved_pwd
                print(improved)
        
        elif user_choice=="3":
            pwd_to_check=input("Enter password to check: ")
            strength_result=check_strength(pwd_to_check)
            result_msg="Password strength: "+strength_result
            print(result_msg)
        
        elif user_choice=="4":
            exit_message="Exiting..."
            print(exit_message)
            program_running=0
        
        else:
            invalid_msg="Invalid choice. Please try again."
            print(invalid_msg)

if __name__=="__main__":
    main()
