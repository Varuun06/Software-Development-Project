class TableBooking:
    def __init__(self, time_slot, people, name, table_no, date, month):
        self.time_slot = int(time_slot)
        self.people = int(people)
        self.name = name
        self.table_no = int(table_no)
        self.date = int(date)
        self.month = int(month)

class Table:
    def __init__(self):
        self.table_bookings = {}
        self.load_data()

    def booking(self):
        name = input("Enter the name of the customer: ").strip()
        people = int(input("Enter the number of people (excluding children below 6 years): ").strip())
        table_no = int(input("Enter the table number: ").strip())
        time_slot = int(input("Enter the time you want to book the table (hhmm): ").strip())
        date = int(input("Enter the date (dd): ").strip())
        month = int(input("Enter the month (mm): ").strip())

        # Check if the table is already booked at the given date and time
        if any(booking.table_no == table_no and booking.date == date and booking.month == month and booking.time_slot == time_slot for booking in self.table_bookings.values()):
            print("The table is already booked for this date and time.")
        else:
            key = (table_no, date, month, time_slot)
            self.table_bookings[key] = TableBooking(time_slot, people, name, table_no, date, month)
            print("The table is booked.")
            self.save_data()

    def load_data(self):
        try:
            with open('custmordetails.txt', 'r') as file:
                for line in file:
                    time_slot, people, name, table_no, date, month = line.strip().split(',')
                    key = (int(table_no), int(date), int(month), int(time_slot))
                    self.table_bookings[key] = TableBooking(time_slot, int(people), name, int(table_no), int(date), int(month))
        except FileNotFoundError:
            pass

    def save_data(self):
        with open('custmordetails.txt', 'w') as file:
            for booking in self.table_bookings.values():
                file.write(f"{booking.time_slot},{booking.people},{booking.name},{booking.table_no},{booking.date},{booking.month}\n")

    def delete_data(self):
        delname = input("Enter the name of the customer to delete: ").strip()
        deltableno = int(input("Enter the table number you want to delete: ").strip())
        deldate = int(input("Enter the date of the booking to delete (dd): ").strip())
        delmonth = int(input("Enter the month of the booking to delete (mm): ").strip())

        found = False
        for key, booking in list(self.table_bookings.items()):
            if booking.name == delname and booking.table_no == deltableno and booking.date == deldate and booking.month == delmonth:
                del self.table_bookings[key]
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
