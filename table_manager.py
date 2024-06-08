class TableBooking:
    def __init__(self, time_slot, people, name, table_no, date):
        self.time_slot = int(time_slot)
        self.people = int(people)
        self.name = name
        self.table_no = int(table_no)
        self.date = int(date)

class TableManager:
    def __init__(self):
        self.table_bookings = {}
        self.load_data()

    def booking(self, name, people, table_no, time_slot, date):
        key = (table_no, date, time_slot)
        if key in self.table_bookings:
            return False
        self.table_bookings[key] = TableBooking(time_slot, people, name, table_no, date)
        self.save_data()
        return True

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

    def delete_booking(self, name, table_no, date):
        for key, booking in list(self.table_bookings.items()):
            if booking.name == name and booking.table_no == table_no and booking.date == date:
                del self.table_bookings[key]
                self.save_data()
                return True
        return False
