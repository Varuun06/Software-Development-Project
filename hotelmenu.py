
import tkinter as tk
from tkinter import ttk
class TreeNode:
    def __init__(self, data, price=0):
        self.data = data
        self.price = price
        self.children = []

    def add_child(self, child_node):
        self.children.append(child_node)


class CuisineTree:
    def __init__(self):
        self.root = TreeNode("Cuisines")

    def add_cuisine(self, cuisine_name, appetizers, appetizer_prices, main_dishes, main_dish_prices):
        cuisine_node = TreeNode(cuisine_name)
        appetizers_node = TreeNode("Appetizers")
        main_dishes_node = TreeNode("Main Dishes")

        for app, price in zip(appetizers, appetizer_prices):
            appetizers_node.add_child(TreeNode(app, price))

        for dish, price in zip(main_dishes, main_dish_prices):
            main_dishes_node.add_child(TreeNode(dish, price))

        cuisine_node.add_child(appetizers_node)
        cuisine_node.add_child(main_dishes_node)

        self.root.add_child(cuisine_node)

    def get_cuisines(self):
        cuisines = []
        for child in self.root.children:
            cuisines.append(child.data)
        return cuisines

    def get_categories(self, cuisine_name):
        for child in self.root.children:
            if child.data == cuisine_name:
                categories = []
                for category in child.children:
                    categories.append(category.data)
                return categories

    def get_items(self, cuisine_name, category_name):
        for child in self.root.children:
            if child.data == cuisine_name:
                for category in child.children:
                    if category.data == category_name:
                        items = []
                        for item in category.children:
                            items.append((item.data, item.price))
                        return items
root = tk.Tk()
root.title("Cuisine Explorer")
cuisine_tree = CuisineTree()
cuisine_tree.add_cuisine("Italian", 
                         appetizers=["Bruschetta", "Caprese Salad", "Garlic Bread","caponeta","goat cheese dip","antipasto platter","marinated olives","atbread mini pizza","burrattta with tomatoes","easy stuffed mushroom"],
                         appetizer_prices=[100,150,155,124,80,130,145,135,200,170],
                         main_dishes=["Pizza", "Pasta", "Lasagna", "Risotto", "Tiramisu","Truffle","spaghetti","Fiorentina Steak","homemade papardelle","baked italian sub","creamy tuscan chicken pasta"],
                         main_dish_prices=[200,230,220,245,270,245,260,230,345,300,315])
cuisine_tree.add_cuisine("Mexican", 
                         appetizers=["Guacamole", "Queso Fundido", "Nachos","Tamales","Empanadas","Ceviche","Mexican Shrimp Cocktail","Molletes","Aguachile","Cactus Salad","Esquites"],
                         appetizer_prices=[100,230,450,460,280,340,290,310,340,230],
                         main_dishes=["Tacos", "Burritos", "Enchiladas", "Quesadillas","Chicken fajitaa tacos","dorito casserole","chicken falutas"],
                         main_dish_prices=[11, 13, 15, 12])
cuisine_tree.add_cuisine("Chinese", 
                         appetizers=["Egg Rolls", "Spring Rolls", "Wontons"],
                         appetizer_prices=[5, 6, 7],
                         main_dishes=["Kung Pao Chicken", "Fried Rice", "Chow Mein", "Dumplings"],
                         main_dish_prices=[14, 12, 13, 10])
cuisine_tree.add_cuisine("Indian", 
                         appetizers=["Samosa", "Pakora", "Paneer Tikka"],
                         appetizer_prices=[4, 5, 6],
                         main_dishes=["Butter Chicken", "Biryani", "Naan"],
                         main_dish_prices=[15, 16, 3])
def show_items(event):
    selected_item = tree.focus()
    if selected_item:
        item_text = tree.item(selected_item, "text")
        cuisine_name, category_name = item_text.split(" - ")
        food_list.delete(*food_list.get_children())
        if category_name == "Appetizers":
            items = cuisine_tree.get_items(cuisine_name, "Appetizers")
            for item, price in items:
                food_list.insert("", "end", text=item, values=(price,))
        elif category_name == "Main Dishes":
            items = cuisine_tree.get_items(cuisine_name, "Main Dishes")
            for item, price in items:
                food_list.insert("", "end", text=item, values=(price,))

tree = ttk.Treeview(root, columns=("Category"))
tree.heading("#0", text="Cuisine")
tree.heading("Category", text="Category")
tree.pack(fill="both", expand=True)
for cuisine in cuisine_tree.get_cuisines():
    cuisine_node = tree.insert("", "end", text=cuisine)
    categories = cuisine_tree.get_categories(cuisine)
    for category in categories:
        tree.insert(cuisine_node, "end", text=f"{cuisine} - {category}", tags=("category",))
tree.bind("<ButtonRelease-1>", show_items)
food_list = ttk.Treeview(root, columns=("Price"))
food_list.heading("#0", text="Food Items")
food_list.heading("Price", text="Price")
food_list.pack(fill="both", expand=True)
def calculate_total_price():
    selected_items = food_list.selection()
    total_price = 0
    for item in selected_items:
        price = float(food_list.item(item, "values")[0])
        total_price += price
    total_price_label.config(text=f"Total Price: Rs{total_price:.2f}")
calculate_button = ttk.Button(root, text="Calculate Total Price", command=calculate_total_price)
calculate_button.pack()
total_price_label = tk.Label(root, text="")
total_price_label.pack()
root.mainloop()



