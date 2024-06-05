class MenuItem:
    def __init__(self, name, price):
        self.name = name
        self.price = price
        self.children = []

    def add_child(self, child):
        self.children.append(child)

    def get_price(self):
        return self.price


class MenuTree:
    def __init__(self):
        self.root = MenuItem("Menu", None)

    def add_item(self, cuisine, dish, price):
        cuisine_node = None
        for child in self.root.children:
            if child.name == cuisine:
                cuisine_node = child
                break
        if cuisine_node is None:
            cuisine_node = MenuItem(cuisine, None)
            self.root.add_child(cuisine_node)
        dish_node = MenuItem(dish, price)
        cuisine_node.add_child(dish_node)

    def print_menu(self, node=None, depth=0):
        if node is None:
            node = self.root
        prefix = "  " * depth
        if node.price is not None:
            print(f"{prefix}- {node.name}: Rs{node.price}")
        else:
            print(f"{prefix}{node.name}")
        for child in node.children:
            self.print_menu(child, depth + 1)

    def select_item(self, cuisine, dish=None):
        if dish is None:
            cuisine_node = None
            for child in self.root.children:
                if child.name == cuisine:
                    cuisine_node = child
                    break
            if cuisine_node is None:
                print("Invalid cuisine selection.")
                return None
            return cuisine_node
        else:
            cuisine_node = self.select_item(cuisine)
            if cuisine_node:
                for dish_node in cuisine_node.children:
                    if dish_node.name == dish:
                        return dish_node
                print("Invalid dish selection.")
                return None

    def total_price(self, selections):
        total = 0
        for cuisine, dish in selections:
            item = self.select_item(cuisine, dish)
            if item:
                total += item.get_price()
        return total


menu_tree = MenuTree()

menu_tree.add_item("Italian", "Pizza", 200)
menu_tree.add_item("Italian", "Pasta", 230)
menu_tree.add_item("Italian", "Lasagna", 220)
menu_tree.add_item("Italian", "Caprese Salad", 220)
menu_tree.add_item("Italian", "Garlic Bread", 120)
menu_tree.add_item("Italian", "Chicken Pasta", 160)

menu_tree.add_item("Mexican", "Tacos", 110)
menu_tree.add_item("Mexican", "Burritos", 130)
menu_tree.add_item("Mexican", "Enchiladas", 150)
menu_tree.add_item("Mexican", "Guacamole", 220)
menu_tree.add_item("Mexican", "Nachos", 220)
menu_tree.add_item("Mexican", "Queso Fundido", 220)

menu_tree.add_item("Chinese", "Kung Pao Chicken", 140)
menu_tree.add_item("Chinese", "Fried Rice", 120)
menu_tree.add_item("Chinese", "Chow Mein", 130)
menu_tree.add_item("Chinese", "Egg Rolls", 50)
menu_tree.add_item("Chinese", "Spring Rolls", 70)
menu_tree.add_item("Chinese", "Wontons", 120)

menu_tree.add_item("Indian", "Butter Chicken", 250)
menu_tree.add_item("Indian", "Biryani", 220)
menu_tree.add_item("Indian", "Paneer Tikka", 200)
menu_tree.add_item("Indian", "Samosa", 100)
menu_tree.add_item("Indian", "Naan", 50)
menu_tree.add_item("Indian", "Rogan Josh", 240)

menu_tree.print_menu()

selected_items = []
while True:
    x = input("\nEnter the cuisine number (or 'done' to finish): ")
    if x == 'done':
        break
    elif x not in ['1', '2', '3', '4']:
        print("Invalid choice.")
        continue

    cuisine_map = {'1': 'Italian', '2': 'Mexican', '3': 'Chinese', '4': 'Indian'}
    cuisine_choice = cuisine_map[x]

    menu_tree.print_menu(menu_tree.select_item(cuisine_choice))
    y = input("\nEnter the dish number (or 'back' to go back): ")
    if y == 'back':
        continue
    dish_map = {
        '1': 'Pizza', '2': 'Pasta', '3': 'Lasagna', '4': 'Caprese Salad', '5': 'Garlic Bread', '6': 'Chicken Pasta',
        '7': 'Tacos', '8': 'Burritos', '9': 'Enchiladas', '10': 'Guacamole', '11': 'Nachos', '12': 'Queso Fundido',
        '13': 'Kung Pao Chicken', '14': 'Fried Rice', '15': 'Chow Mein', '16': 'Egg Rolls', '17': 'Spring Rolls',
        '18': 'Wontons', '19': 'Butter Chicken', '20': 'Biryani', '21': 'Paneer Tikka', '22': 'Samosa', '23': 'Naan',
        '24': 'Rogan Josh'
    }
    if y not in dish_map.keys():
        print("Invalid choice.")
        continue

    dish_choice = dish_map[y]
    selected_items.append((cuisine_choice, dish_choice))

total_price = menu_tree.total_price(selected_items)
print(f"\nYour total price is: Rs {total_price}")
