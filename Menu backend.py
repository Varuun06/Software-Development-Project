class Menu:
    def __init__(self):
        self.prices = {
            'Pizza': 200,
            'Pasta': 230,
            'Lasagna': 220,
            'Caprese Salad': 220,
            'Garlic Bread': 120,
            'Chicken Pasta': 160,
            'Tacos': 110,
            'Burritos': 130,
            'Enchiladas': 150,
            'Guacamole': 220,
            'Nachos': 220,
            'Queso Fundido': 220,
            'Kung Pao Chicken': 140,
            'Fried Rice': 120,
            'Chow Mein': 130,
            'Egg Rolls': 50,
            'Spring Rolls': 70,
            'Wontons': 120,
            'Butter Chicken': 250,
            'Biryani': 220,
            'Paneer Tikka': 200,
            'Samosa': 100,
            'Naan': 50,
            'Rogan Josh': 240
        }
        self.selected = []

    def italian(self):
        print("Italian menu items:")
        print("1. Pizza - Rs200")
        print("2. Pasta - Rs230")
        print("3. Lasagna - Rs220")
        print("4. Caprese Salad - Rs220")
        print("5. Garlic Bread - Rs120")
        print("6. Chicken Pasta - Rs160")

    def mexican(self):
        print("Mexican menu items:")
        print("1. Tacos - Rs110")
        print("2. Burritos - Rs130")
        print("3. Enchiladas - Rs150")
        print("4. Guacamole - Rs220")
        print("5. Nachos - Rs220")
        print("6. Queso Fundido - Rs220")

    def chinese(self):
        print("Chinese menu items:")
        print("1. Kung Pao Chicken - Rs140")
        print("2. Fried Rice - Rs120")
        print("3. Chow Mein - Rs130")
        print("4. Egg Rolls - Rs50")
        print("5. Spring Rolls - Rs70")
        print("6. Wontons - Rs120")

    def indian(self):
        print("Indian menu items:")
        print("1. Butter Chicken - Rs250")
        print("2. Biryani - Rs220")
        print("3. Paneer Tikka - Rs200")
        print("4. Samosa - Rs100")
        print("5. Naan - Rs50")
        print("6. Rogan Josh - Rs240")

    def add_item(self, item):
        self.selected.append(item)

    def total_price(self):
        total = 0
        for item in self.selected:
            total += self.prices.get(item, 0)
        return total

m = Menu()

while True:
    print("WELCOME TO ORDER THE DISHES")
    print("1. Italian\n2. Chinese\n3. Mexican\n4. Indian\n")
    x = input("Which of the following cuisines do you want to explore? Enter the number: ")
    if x == '1':
        m.italian()
    elif x == '2':
        m.chinese()
    elif x == '3':
        m.mexican()
    elif x == '4':
        m.indian()
    else:
        print("Sorry, that was a mistake. Please re-enter your entry.")
        continue
    while True:
        choice = input("Enter the item you want to order,type'Cancel' to ccancel this current order, type 'done' to finish ordering, or 'menu' to see the menu again: ").strip().title()
        if choice == 'Done':
            break
        elif choice=='Cancel':
            m.selected=[]
            print("YEAH YOUR ORDER IS CANCELLED!!")
            break
        elif choice == 'Menu':
            break
        elif choice in m.prices:
            m.add_item(choice)
        else:
            print("Sorry, that item is not available. Please choose again.")
    if choice == 'Done':
        total = m.total_price()
        print("Your total price is: Rs" + str(total))
        print("Your order is placed.thankyou:)")
        another_order = input("Do you want to place another order? (yes/no): ").strip().lower()
        if another_order == 'no':
            
            break
        else:
            m.selected = []
    elif choice == 'Menu':
        continue
