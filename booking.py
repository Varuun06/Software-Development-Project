class TableBooking:
    def __init__(self, time_slot, people, name, table_no):
        self.time_slot = int(time_slot)
        self.people = int(people)
        self.name = name
        self.table_no = int(table_no)

class Table:
    def __init__(self):
        self.table_bookings = {}
        self.load_data()

    def booking(self):
        name = input("Enter the name of the customer: ").strip()
        people = int(input("Enter the number of people (excluding children below 6 years): ").strip())
        table_no = int(input("Enter the table number: ").strip())
        time_slot = int(input("Enter the time you want to book the table (HHMM): ").strip())

        if any(booking.table_no == table_no for booking in self.table_bookings.values()):
            print("The table is already booked.")
        else:
            self.table_bookings[table_no] = TableBooking(time_slot, people, name, table_no)
            print("The table is booked.")
            self.save_data()

    def load_data(self):
        try:
            with open('custmordetails.txt', 'r') as file:
                for line in file:
                    time_slot, people, name, table_no = line.strip().split(',')
                    self.table_bookings[int(time_slot)] = TableBooking(time_slot, int(people), name, int(table_no))
        except FileNotFoundError:
            pass

    def save_data(self):
        with open('custmordetails.txt', 'w') as file:
            for booking in self.table_bookings.values():
                file.write(f"{booking.time_slot},{booking.people},{booking.name},{booking.table_no}\n")

    def delete_data(self):
        delname = input("Enter the name of the customer to delete: ").strip()
        deltableno = int(input("Enter the table number you want to delete: ").strip())

        found = False
        for time_slot, booking in list(self.table_bookings.items()):
            if booking.name == delname and booking.table_no == deltableno:
                del self.table_bookings[time_slot]
                print("The booking has been deleted.")
                found = True
                self.save_data()
                break
        if not found:
            print("No matching booking found.")

if __name__ == "__main__":
    table = Table()
    while True:
        action = input("Enter 'book' to book a table, 'delete' to delete a booking, or 'exit' to quit: ").strip().lower()
        if action == 'book':
            table.booking()
        elif action == 'delete':
            table.delete_data()
        elif action == 'exit':
            break
        else:
            print("Invalid action. Please enter 'book', 'delete', or 'exit'.")
