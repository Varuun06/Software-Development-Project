class admin:
    def __init__(self, username, password):
        self.username = username
        self.password = password

class adminManager:
    def __init__(self):
        self.admin = {}
        self.load_data()

    def load_data(self):
        try:
            with open('dataadmin.bin', 'r') as file:
                for line in file:
                    username, password = line.strip().split(',')
                    self.admin[username] = admin(username, password)
        except FileNotFoundError:
            pass

    def save_data(self):
        with open('dataadmin.bin', 'w') as file:
            for admin in self.admin.values():
                file.write(f"{admin.username},{admin.password}\n")

    def login(self):
        username = input("Enter username: ")
        password = input("Enter password: ")
        if username in self.admin and self.admin[username].password == password:
            print("admin Login successful!")
            return True
        else:
            print("Username or password incorrect.")
            return False

class DeletionTable:
    def __init__(self):
        pass

    def deletion_table(self):
        try:
            deltable = int(input("Enter the table number you want to delete for customer: "))
        except ValueError:
            print("Invalid input. Please enter an integer.")
            return

        try:
            with open("custmordetails.bin", "r") as file:
                lines = file.readlines()
        except FileNotFoundError:
            print("File 'custmordetails.bin' not found.")
            return

        with open("custmordetails.bin", "w") as file:
            found = False
            for line in lines:
                if str(deltable) not in line:
                    file.write(line)
                else:
                    found = True

            if found:
                print(f"Table {deltable} has been deleted.")
            else:
                print(f"Table {deltable} not found.")

if __name__ == "__main__":
    adminManager = adminManager()
    if adminManager.login():
        dt = DeletionTable()
        dt.deletion_table()
