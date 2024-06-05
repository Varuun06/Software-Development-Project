import random
import smtplib
import ast
import sys  # Import the sys module

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

    def login(self):
        phone_number = input("Enter phone_number: ").strip()
        password = input("Enter password: ").strip()
        if phone_number in self.users and self.users[phone_number].password == password:
            print("Login successful!")
        else:
            print("phone_number or password incorrect.")
            choice = input("Forgot password? (yes/no): ").strip().lower()
            if choice == 'yes':
                self.forgot_password(phone_number)
            else:
                choice = input("Do you want to sign up? (yes/no): ").strip().lower()
                if choice == 'yes':
                    self.signup()
                else:
                    print("Goodbye")
                    sys.exit()  # Terminate the program after printing "Goodbye"

    def forgot_password(self, phone_number):
        if phone_number in self.users:
            user = self.users[phone_number]
            self.generate_otp(phone_number)
        else:
            print("phone_number not found.")
            self.login()

    def generate_otp(self, phone_number):
        OTP = random.randint(100000, 999999)  # generating a random 6-digit OTP
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()

        receiver_email = self.users[phone_number].email

        def email_verification(receiver_email):
            email_check1 = ["gmail", "hotmail", "yahoo", "outlook"]
            email_check2 = [".com", ".in", ".org", ".edu", ".co.in"]
            count = 0

            for domain in email_check1:
                if domain in receiver_email:
                    count += 1
            for site in email_check2:
                if site in receiver_email:
                    count += 1

            if "@" not in receiver_email or count != 2:
                print("invalid email id")
                new_receiver_email = input("enter correct email id:")
                return email_verification(new_receiver_email)
            return receiver_email

        valid_receiver_email = email_verification(receiver_email)
        password1 = "stqqwjqoocucknsx"
        server.login("priyanshu25122002@gmail.com", password1)

        body = "Respected Customer," + "\n" + "\n" + "your OTP is " + str(OTP) + "."
        subject = "OTP verification using python"
        message = f'subject:{subject}\n\n{body}'

        server.sendmail("priyanshu25122002@gmail.com", valid_receiver_email, message)

        def sending_otp(receiver_email):
            new_otp = random.randint(100000, 999999)

            body = "Respected Customer," + "\n" + "\n" + "your OTP is " + str(new_otp) + "."
            subject = "OTP verification using python"
            message = f'subject:{subject}\n\n{body}'
            server.sendmail("priyanshu25122002@gmail.com", receiver_email, message)
            print("OTP has been sent to " + receiver_email)
            received_OTP = int(input("enter OTP:"))

            if received_OTP == new_otp:
                print("OTP verified")
                new_password = input("Enter new password: ").strip()
                self.users[phone_number].password = new_password
                self.save_data()
                print("Password reset successful!")
            else:
                print("invalid OTP")
                print("resending OTP.....")
                sending_otp(receiver_email)

        print("OTP has been sent to " + valid_receiver_email)
        received_OTP = int(input("enter OTP:"))

        if received_OTP == OTP:
            print("OTP verified")
            new_password = input("Enter new password: ").strip()
            self.users[phone_number].password = new_password
            self.save_data()
            print("Password reset successful!")
        else:
            print("invalid OTP")
            answer = input("enter yes to resend OTP on same email and no to enter a new email id:")
            YES = ['YES', 'yes', 'Yes']
            NO = ['NO', 'no', 'No']
            if answer in YES:
                sending_otp(valid_receiver_email)
            elif answer in NO:
                new_receiver_email = input("enter new email id:")
                email_verification(new_receiver_email)
                sending_otp(new_receiver_email)
            else:
                print("invalid input")

        server.quit()

    def signup(self):
        while True:
            phone_number = input("Enter phone_number: ").strip()
            email = input("Enter email: ").strip()
            password = input("Enter password: ").strip()

            if not (phone_number and email and password):
                print("Please enter valid values for phone_number, email, and password.")
                continue

            if phone_number in self.users:
                print("phone_number already exists. Please choose another.")
            else:
                self.users[phone_number] = User(phone_number, email, password)
                self.save_data()
                print("Sign up successful!")
                break

class TableBooking:
    def __init__(self, time_slot, people, name, table_no, date):
        self.time_slot = int(time_slot)
        self.people = int(people)
        self.name = name
        self.table_no = int(table_no)
        self.date = int(date)

class Table:
    def __init__(self):
        self.table_bookings = {}
        self.load_data()

    def booking(self):
        name = input("Enter the name of the customer: ").strip()
        people = int(input("Enter the number of people (excluding children below 6 years): ").strip())
        table_no = int(input("Enter the table number: ").strip())
        time_slot = int(input("Enter the time you want to book the table (hhmm): ").strip())
        date = int(input("Enter the date (ddmm): ").strip())

        # Check if the table is already booked at the given date and time
        if any(booking.table_no == table_no and booking.date == date and booking.time_slot == time_slot for booking in self.table_bookings.values()):
            print("The table is already booked for this date and time.")
        else:
            key = (table_no, date, time_slot)
            self.table_bookings[key] = TableBooking(time_slot, people, name, table_no, date)
            print("The table is booked.")
            self.save_data()

    def load_data(self):
        try:
            with open('custmordetails.bin', 'r') as file:
                for line in file:
                    time_slot, people, name, table_no, date = line.strip().split(',')
                    key = (int(table_no), int(date), int(time_slot))
                    self.table_bookings[key] = TableBooking(time_slot, int(people), name, int(table_no), int(date))
        except FileNotFoundError:
            pass

    def save_data(self):
        with open('custmordetails.bin', 'w') as file:
            for booking in self.table_bookings.values():
                file.write(f"{booking.time_slot},{booking.people},{booking.name},{booking.table_no},{booking.date}\n")

        availability = {}
        for booking in self.table_bookings.values():
            table_no = booking.table_no
            date = booking.date
            time_slot = booking.time_slot
            if table_no not in availability:
                availability[table_no] = []
            availability[table_no].append((date, time_slot))

        with open('availability.txt', 'w') as file:
            file.write(str(availability))

    def delete_data(self):
        delname = input("Enter the name of the customer to delete: ").strip()
        deltableno = int(input("Enter the table number you want to delete: ").strip())
        deldate = int(input("Enter the date of the booking to delete (ddmm): ").strip())

        found = False
        for key, booking in list(self.table_bookings.items()):
            if booking.name == delname and booking.table_no == deltableno and booking.date == deldate:
                del self.table_bookings[key]
                print("The booking has been deleted.")
                found = True
                self.save_data()
                break
        if not found:
            print("No matching booking found.")

if __name__ == "__main__":
    userManager = UserManager()
    userManager.login()
    
    table = Table()
    while True:
        action = input("Enter 'login' to log in, 'signup' to sign up, 'book' to book a table, 'delete' to delete a booking, or 'exit' to quit: ").strip().lower()
        if action == 'login':
            userManager.login()
        elif action == 'signup':
            userManager.signup()
        elif action == 'book':
            table.booking()
        elif action == 'delete':
            table.delete_data()
        elif action == 'exit':
            break
        else:
            print("Invalid action. Please enter 'login', 'signup', 'book', 'delete', or 'exit'.")
