import pyrebase
from requests.exceptions import HTTPError
from config import FIREBASECONFIG
from utils.exceptions import FirebaseException
import json

firebase = pyrebase.initialize_app(FIREBASECONFIG)
auth = firebase.auth()

def login():
    email = input("Enter your email: ")
    password = input("Enter your password: ")
    try:
        user = auth.sign_in_with_email_and_password(email, password)
        print(f"User {user['email']} logged in")
        with open("test.json", "w") as f:
            json.dump(user, f)
        print(f"User Token: {user['idToken']}")
    except HTTPError as e:
        e = FirebaseException(e)
        print(e)

def signup():
    email = input("Enter your email: ")
    password = input("Enter your password: ")
    try:
        user = auth.create_user_with_email_and_password(email, password)
        print(f"User {user['email']} created")
    except HTTPError as e:
        e = FirebaseException(e)
        print(e)

def reset_password():
    email = input("Enter your email: ")
    auth.send_password_reset_email(email)
    print("Password reset email sent")

def verify_token(token):
    try:
        user = auth.sign_in_anonymous()
        print(f"Token is valid for user: {user['localId']}")
        user = auth.get_account_info(user['idToken'])
        with open("token.json", "w") as f:
            json.dump(user, f)
        print(f"Token is valid for user: {user['users'][0]['email']}")
    except HTTPError as e:
        e = FirebaseException(e)
        print(e)

def main():
    while True:
        print("1: Login")
        print("2: Signup")
        print("3: Reset password")
        print("4: Verify token")
        print("5: Exit")
        option = input("Enter your choice: ")
        if option == "1":
            login()
        elif option == "2":
            signup()
        elif option == "3":
            reset_password()
        elif option == "4":
            verify_token(input("Enter the token to verify: "))
        elif option == "5":
            break
        else:
            print("Invalid option")

if __name__ == "__main__":
    main()