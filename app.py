from flask import Flask, jsonify, render_template, request

class Node:
    def __init__(self, data):
        self.data = data
        self.children = []

class BinaryTree:
    def __init__(self):
        self.root = None

    def add_root(self, data):
        self.root = Node(data)

    def add_children(self, parent, left_data, right_data):
        left_node = Node(left_data)
        right_node = Node(right_data)
        parent.children = [left_node, right_node]
        return left_node, right_node
    
    def add_child(self, parent, data):
        new_node = Node(data)
        parent.children.append(new_node)
        return new_node
    
    def serialize(self, node):
        if not node:
            return None
        return {
            'data': node.data,
            'children': [self.serialize(child) for child in node.children]
        }
    
    def find_cost(self, node, item_name):
        if not node:
            return None
        
        # Check if it's a leaf node with a food item and cost
        if isinstance(node.data, list) and len(node.data) == 2:
            if node.data[0] == item_name:
                return node.data[1]
        
        # Recursively search for the item in children
        for child in node.children:
            cost = self.find_cost(child, item_name)
            if cost is not None:
                return cost
        
        return None


app = Flask(__name__)

# Create the binary tree
tree = BinaryTree()
tree.add_root("Menu")

# Add children to root
indian_node, international_node = tree.add_children(tree.root, "Indian", "International")

# Add children to "Indian"
indian_main = tree.add_child(indian_node, "Main Dish")
indian_appetizers = tree.add_child(indian_node, "Appetizers")

# Add dishes to Indian Main Dish and Appetizers
tree.add_child(indian_main, ["Biryani",200])
tree.add_child(indian_main, ["Roti",200])
tree.add_child(indian_main, ["Chapati",200])
tree.add_child(indian_main, ["Butter Chicken",200])

tree.add_child(indian_appetizers, ["Samosa",200])
tree.add_child(indian_appetizers, ["Vada",200])
tree.add_child(indian_appetizers, ["Bhel Puri",200])

# Add children to "International"
intl_main = tree.add_child(international_node, "Main Dish")
intl_appetizers = tree.add_child(international_node, "Appetizers")

# Add dishes to International Main Dish and Appetizers
tree.add_child(intl_main, ["Pasta",200])
tree.add_child(intl_main, ["Pizza",200])
tree.add_child(intl_main, ["Burger",200])
tree.add_child(intl_main, ["Sushi",200])

tree.add_child(intl_appetizers, ["Bruschetta",200])
tree.add_child(intl_appetizers, ["Baguette",200])
tree.add_child(intl_appetizers, ["Croissant",200])

@app.route('/menu', methods=['GET'])
def get_menu():
    return jsonify(tree.serialize(tree.root))

@app.route('/', methods=['GET', 'POST'])
def menu():
    return render_template("menu.html")

@app.route("/menu", methods=["POST"])
def menu_get():
    data = request.get_json()
    List_food = data.get("items")

    cost = 0
    print(List_food)

    for food in List_food:
        cost += tree.find_cost(tree.root, food)

    return jsonify(str(cost))


if __name__ == '__main__':
    app.run(debug=True)

#OOMBA VARIYA NATHARI PUNDA
