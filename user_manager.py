import ast
import random
import smtplib

class User:
    def __init__(self, phone_number, email, password):
        self.phone_number = phone_number
        self.email = email
        self.password = password

    def __repr__(self):
        return f"User(phone_number={self.phone_number}, email={self.email}, password={self.password})"

class UserManager:
    def __init__(self):
        self.users = {}
        self.load_data()

    def load_data(self):
        try:
            with open('data.bin', 'r') as file:
                data = file.read()
                if data:
                    self.users = ast.literal_eval(data)
                    for phone_number, user_data in self.users.items():
                        self.users[phone_number] = User(**user_data)
        except FileNotFoundError:
            pass
        except Exception as e:
            print("An error occurred while loading data:", e)

    def save_data(self):
        try:
            with open('data.bin', 'w') as file:
                data = {phone_number: user.__dict__ for phone_number, user in self.users.items()}
                file.write(str(data))
        except Exception as e:
            print("An error occurred while saving data:", e)

    def login(self, phone_number, password):
        if phone_number in self.users and self.users[phone_number].password == password:
            return True
        return False

    def forgot_password(self, phone_number, email):
        if phone_number in self.users and self.users[phone_number].email == email:
            return self.generate_otp(phone_number)
        return None

    def generate_otp(self, phone_number):
        OTP = random.randint(100000, 999999)
        receiver_email = self.users[phone_number].email

        # SMTP Configuration
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login("your_email@example.com", "your_email_password")

        body = f"Respected Customer,\n\nYour OTP is {OTP}."
        subject = "OTP Verification"
        message = f'Subject: {subject}\n\n{body}'

        server.sendmail("your_email@example.com", receiver_email, message)
        server.quit()

        return OTP

    def reset_password(self, phone_number, new_password):
        if phone_number in self.users:
            self.users[phone_number].password = new_password
            self.save_data()
            return True
        return False

    def signup(self, phone_number, email, password):
        if phone_number not in self.users:
            self.users[phone_number] = User(phone_number, email, password)
            self.save_data()
            return True
        return False
