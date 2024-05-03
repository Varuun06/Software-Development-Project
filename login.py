class User:
    def __init__(self, username, email, phone, password):
        self.username = username
        self.email = email
        self.phone = phone
        self.password = password

class UserManager:
    def __init__(self):
        self.users = {}
        self.load_data()

    def load_data(self):
        try:
            with open('data.txt', 'r') as file:
                for line in file:
                    username, email, phone, password = line.strip().split(',')
                    self.users[username] = User(username, email, phone, password)
        except FileNotFoundError:
            pass

    def save_data(self):
        with open('data.txt', 'w') as file:
            for user in self.users.values():
                file.write(f"{user.username},{user.email},{user.phone},{user.password}\n")

    def login(self):
        username = input("Enter username: ")
        password = input("Enter password: ")
        if username in self.users and self.users[username].password == password:
            print("Login successful!")
        else:
            print("Username or password incorrect.")
            choice = input("Do you want to sign up? (yes/no): ")
            if choice.lower() == 'yes':
                self.signup()
            else:
                print("Goodbye!")

    def signup(self):
        username = input("Enter username: ")
        email = input("Enter email: ")
        phone = input("Enter phone number: ")
        password = input("Enter password: ")

        if username in self.users:
            print("Username already exists. Please choose another.")
            self.signup()
        else:
            self.users[username] = User(username, email, phone, password)
            self.save_data()
            print("Sign up successful!")

if __name__ == "__main__":
    userManager = UserManager()
    userManager.login()
