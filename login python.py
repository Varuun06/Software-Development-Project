class User:
    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password

class UserManager:
    def __init__(self):
        self.users = {}
        self.load_data()

    def load_data(self):
        try:
            with open('data.txt', 'r') as file:
                for line in file:
                    username, email, password = line.strip().split(',')
                    self.users[username] = User(username, email, password)
        except FileNotFoundError:
            pass
        except Exception as e:
            print("An error occurred while loading data:", e)

    def save_data(self):
        try:
            with open('data.txt', 'w') as file:
                for user in self.users.values():
                    file.write(f"{user.username},{user.email},{user.password}\n")
        except Exception as e:
            print("An error occurred while saving data:", e)

    def login(self):
        username = input("Enter username: ").strip()
        password = input("Enter password: ").strip()
        if username in self.users and self.users[username].password == password:
            print("Login successful!")
        else:
            print("Username or password incorrect.")
            choice = input("Do you want to sign up? (yes/no): ").strip().lower()
            if choice == 'yes':
                self.signup()
            else:
                print("Goodbye!")
    def signup(self):
        while True:
            username = input("Enter username: ").strip()
            email = input("Enter email: ").strip()
            password = input("Enter password: ").strip()

            if not (username and email and password):
                print("Please enter valid values for username, email, and password.")
                continue

            if username in self.users:
                print("Username already exists. Please choose another.")
            else:
                self.users[username] = User(username, email, password)
                self.save_data()
                print("Sign up successful!")
                break

if __name__ == "__main__":
    userManager = UserManager()
    userManager.login()
