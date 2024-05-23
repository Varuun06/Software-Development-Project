class DeletionTable:
    def __init__(self, deltable=None):
        self.deltable = deltable

    def deletion_table(self):
        try:
            deltable = int(input("Enter the table number you want to delete for customer: "))
        except ValueError:
            print("Invalid input. Please enter an integer.")
            return

        try:
            with open("custmordetails.txt", "r") as file:
                lines = file.readlines()
        except FileNotFoundError:
            print("File 'custmordetails.txt' not found.")
            return

        with open("custmordetails.txt", "w") as file:
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

dt = DeletionTable()
dt.deletion_table()


