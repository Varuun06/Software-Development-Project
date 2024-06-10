from flask import Flask, jsonify, render_template, request, redirect, url_for, flash, session
import json
import smtplib
import random
import string
from email.message import EmailMessage 
import os
from random import randint
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key'

admin_credentials = {
    'username': 'admin',
    'password': '123456'
}

otp_storage = {}

def generate_otp():
    return ''.join(random.choices(string.digits, k=6))

def send_otp_via_email(to, otp):
    user = "vaibhavsp16@gmail.com"
    key = "awxuuatnydkvqfeb"

    msg = EmailMessage()

    msg["Subject"] = "Your OTP code"

    msg["From"] = user

    msg["To"] = to

    msg.set_content(f"Your OTP code is {otp}")

    server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
    server.login(user, key)
    server.send_message(msg)
    server.quit()

def load_user_data():
    try:
        with open('data.txt', 'r') as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def save_user_data(user_data):
    with open('data.txt', 'w') as file:
        json.dump(user_data, file, indent=4)

def load_reservations():
    reservations = []
    try:
        with open('bookingdetails.txt', 'r') as file:
            for line in file:
                if line.strip():
                    try:
                        reservation = json.loads(line.strip())
                        # Trim whitespace from time field
                        reservation['time'] = reservation['time'].strip()
                        reservations.append(reservation)
                    except json.JSONDecodeError:
                        flash('Error loading reservation data.')
                        continue
    except FileNotFoundError:
        flash('No reservation data found.')
    return reservations

def l_orders():
    orders=[]
    try:
        with open('menuorder.txt','r') as file:
            for line in file:
                if line.strip():
                    try:
                        order = json.loads(line.strip())
                        orders.append(order)
                    except json.JSONDecodeError:
                        flash('Error loading reservation data.')
                        continue
    except FileNotFoundError:
        flash('No reservation data found.')
    return orders
                    

def load_orders():
    try:
        with open('menuorder.txt', 'r') as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}
    
def write_orders(orders):
        with open('menuorder.txt', 'w') as file:
            for order in orders:
                file.write(json.dumps(order) + '\n')


def save_reservations(reservations):
    with open('bookingdetails.txt', 'w') as file:
        for reservation in reservations:
            file.write(json.dumps(reservation) + '\n')

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
        
        if isinstance(node.data, list) and len(node.data) == 2:
            if node.data[0] == item_name:
                return node.data[1]
        
        for child in node.children:
            cost = self.find_cost(child, item_name)
            if cost is not None:
                return cost
        
        return None

tree = BinaryTree()
tree.add_root("Menu")

indian_node, international_node = tree.add_children(tree.root, "Indian", "International")

indian_main = tree.add_child(indian_node, "Main Dish")
indian_appetizers = tree.add_child(indian_node, "Appetizers")

tree.add_child(indian_main, ["Biryani", 200])
tree.add_child(indian_main, ["Roti", 200])
tree.add_child(indian_main, ["Chapati", 200])
tree.add_child(indian_main, ["Butter Chicken", 200])

tree.add_child(indian_appetizers, ["Samosa", 200])
tree.add_child(indian_appetizers, ["Vada", 200])
tree.add_child(indian_appetizers, ["Bhel Puri", 200])

intl_main = tree.add_child(international_node, "Main Dish")
intl_appetizers = tree.add_child(international_node, "Appetizers")

tree.add_child(intl_main, ["Pasta", 200])
tree.add_child(intl_main, ["Pizza", 200])
tree.add_child(intl_main, ["Burger", 200])
tree.add_child(intl_main, ["Sushi", 200])

tree.add_child(intl_appetizers, ["Bruschetta", 200])
tree.add_child(intl_appetizers, ["Baguette", 200])
tree.add_child(intl_appetizers, ["Croissant", 200])

@app.route('/')
def home():
    return render_template("webpage.html")

@app.route('/menu', methods=['GET'])
def get_menu():
    return jsonify(tree.serialize(tree.root))

@app.route('/customer_login', methods=['GET', 'POST'])
def customer_login():
    if request.method == "POST":
        phone_number = request.form.get('phone_number')
        password = request.form.get('password')
        
        user_data = load_user_data()
        user = user_data.get(phone_number)
        session['email'] = user["email"]
        if user and user['password'] == password:
            return redirect(url_for('table_booking', phone_number=phone_number))
        else:
            flash('Invalid credentials, Sign up or enter the correct details.')
    return render_template("customer login page.html")

@app.route('/admin_login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if username == admin_credentials['username'] and password == admin_credentials['password']:
            return redirect(url_for('display_tables'))
        else:
            flash('Invalid admin credentials, please try again.')
    return render_template("admin login page.html")

@app.route('/customer_signup', methods=['GET', 'POST'])
def customer_signup():
    if request.method == "POST":
        phone_number = request.form.get('phone_number')
        email = request.form.get('email')
        password = request.form.get('password')
        
        user_data = load_user_data()
        if phone_number in user_data:
            flash('Phone number already exists.')
        else:
            user_data[phone_number] = {
                'phone_number': phone_number,
                'email': email,
                'password': password
            }
            save_user_data(user_data)
            flash('Sign up successful! Please log in.')
        return redirect(url_for('customer_login'))
    return render_template("customer sign up page.html")

@app.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    phone_number = data['phone_number']
    email = data['email']
    password = data['password']
    
    user_data = load_user_data()
    if not phone_number.isdigit() or len(phone_number) != 10:
        return jsonify({"message": "Enter a valid phone number.", "success": False})
    if phone_number in user_data:
        return jsonify({"message": "Phone number already exists.", "success": False})
    
    user_data[phone_number] = {
        'phone_number': phone_number,
        'email': email,
        'password': password
    }
    save_user_data(user_data)
    return jsonify({"message": "Signup successful! Please log in.", "success": True})


@app.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == "POST":
        email = request.form.get('email')
        
        user_data = load_user_data()
        user = next((user for user in user_data.values() if user['email'] == email), None)
        
        if user:
            otp = generate_otp()
            otp_storage[email] = otp
            send_otp_via_email(email, otp)
            flash('OTP sent to your email.')
            session['show_otp_form'] = True
            session['email'] = email
        else:
            flash('Invalid email address.')
        
    return redirect(url_for('forgot_password_page'))

@app.route('/reset_password', methods=['POST'])
def reset_password():
    email = request.form.get('email')
    otp = request.form.get('otp')
    new_password = request.form.get('new_password')

    if otp_storage.get(email) == otp:
        user_data = load_user_data()
        user = next((user for user in user_data.values() if user['email'] == email), None)
        if user:
            user['password'] = new_password
            save_user_data(user_data)
            flash('Password reset successful! Please log in.')
            session.pop('show_otp_form', None)
            return redirect(url_for('customer_login'))
    else:
        flash('Invalid OTP. Please try again.')

    return redirect(url_for('forgot_password_page'))

@app.route('/forgot_password_page')
def forgot_password_page():
    return render_template("forgot password.html")

@app.route('/table_booking', methods=['GET', 'POST'])
def table_booking():
    if request.method == 'POST':
        name = request.form['name']
        tableno = request.form['tableno']
        date = request.form['date']
        time = request.form['time']
        booking_no = randint(100, 1000)
        session['bookid'] = booking_no
        reservations = load_reservations()

        if name.isdigit():
            flash('Enter a valid name.')
            return redirect(url_for('table_booking'))

        
        # Combine date and time for comparison
        booking_datetime_str = f"{date} {time.split(' - ')[0]}"
        booking_datetime = datetime.strptime(booking_datetime_str, '%Y-%m-%d %H:%M')
        now = datetime.now()
        
        # Server-side validation for past date and time
        if booking_datetime < now:
            flash('Cannot book for past date and time. Please choose a future date and time.')
            return redirect(url_for('table_booking'))
        
        for reservation in reservations:
            if reservation['tableno'] == tableno and reservation['date'] == date and reservation['time'] == time:
                flash('This table has already been booked for the selected date and time. Please choose a different table or time.')
                return redirect(url_for('table_booking'))
        
        reservation_data = {
            'name': name,
            'tableno': tableno,
            'date': date,
            'time': time,
            'booking_no': booking_no
        }
        with open('bookingdetails.txt', 'a') as file:
            file.write(json.dumps(reservation_data) + '\n')
        
        flash('Table booked successfully.')
        return redirect(url_for('menu_page'))
    
    return render_template("table_booking.html")

@app.route('/menu_page', methods=['GET', 'POST'])
def menu_page():
    return render_template("menu.html")

@app.route("/calculate_cost", methods=["POST"])
def calculate_cost():
    data = request.get_json()
    list_food = data.get("items")
    email = data.get("email")
    # Assuming you get the email from the request to identify the user
    cost = 0
    order_details = []

    for food in list_food:
        price = tree.find_cost(tree.root, food)
        if price:
            cost += price
            order_details.append({"item": food, "cost": price})

    # Prepare the order data to save
    order_data = {
        "email": session.get('email'),
        "order_details": order_details,
        "total_cost": cost,
        "booking_no": session.get('bookid')
    }

    # Write the order details to menuorder.txt
    with open('menuorder.txt', 'a') as file:
        file.write(json.dumps(order_data) + '\n')

    # Return the total cost as a JSON response
    return jsonify(cost)


@app.route('/delete_booking', methods=['POST'])
def delete_booking():
    name = request.form['name']
    table_no = int(request.form['table_no'])
    date = request.form['date']

    reservations = load_reservations()
    new_reservations = [r for r in reservations if not (r['name'] == name and r['tableno'] == table_no and r['date'] == date)]
    save_reservations(new_reservations)
    
    flash('Booking deleted successfully.')
    return redirect(url_for('home'))

@app.route("/app/reservation_successful")
def reservation_successful():
    return render_template("reservation_successful.html")

@app.route("/app/display_tables")
def display_tables():
    python_reservations = load_reservations()
    return render_template("display_tables.html", reservations=python_reservations)

@app.route("/delete_reservation/<int:tableno>/<date>/<time>/<bookid>", methods=['GET'])
def delete_reservation(tableno, date, time,bookid):
    reservations = load_reservations()
    new_reservations=[]
    for r in reservations:
        if r['booking_no']==int(bookid):
            pass
        else:
            new_reservations.append(r)
    orders = l_orders()
    print(orders)
    new_orders=[]
    for o in orders:
        if o['booking_no']==int(bookid):
            pass
        else:
            new_orders.append(o)
    print(new_orders)
    write_orders(new_orders)
    save_reservations(new_reservations)
    print(new_reservations)
    return redirect(url_for('delete_successful'))

@app.route("/view_reservation/<int:tableno>/<date>/<time>/<bookid>", methods=['GET'])
def view_reservation(tableno, date, time,bookid):
    reservations = load_reservations()
    reservation = next((r for r in reservations if str(r['tableno']) == str(tableno) and str(r['date']) == str(date) and str(r['time']) == str(time) and str(r['booking_no'])==str(bookid)), None)
    print(reservation)
    if not reservation:
        flash('Reservation not found')
        return redirect(url_for('display_tables'))

    phone_number = reservation.get('name', 'N/A')  # Assuming name is the phone number used for reservation

    user_data = load_user_data()
    #print(user_data)
    user = user_data.get(phone_number, {})
    
    customer_info = {
        'name': phone_number,
        'email': user.get('email', 'N/A'),
        'date': reservation.get('date', 'N/A'),
        'time': reservation.get('time', 'N/A'),
        'seater_status': reservation.get('tableno', 'N/A'),
        'order_id':reservation.get('booking_no',"N/A"),
        
        'menu': [],
        'total_cost': 0
    }
    
    # Load orders from text file
    orders = []
    try:
        with open('menuorder.txt', 'r') as file:
            for line in file:
                order = json.loads(line.strip())
                orders.append(order)
    except FileNotFoundError:
        # Handle the case where the file doesn't exist
        pass

    # Check if this customer has availed the menu
    print(orders)
    customer_orders=[]

    for order in orders:
        if order['booking_no']==int(reservation.get('booking_no')):
            email=order['email']
            total_cost=order["total_cost"]
            customer_orders=order['order_details']
    print(customer_orders)
    if customer_orders:
        customer_info['menu_availed'] = 'Yes'
        for order in customer_orders:
                print(order)
                customer_info['menu'].append(order["item"])
        print(customer_info['menu'])
    else:
        customer_info['menu_availed']='No'
    
    return render_template("user_info_display.html", **customer_info, orders=customer_orders, total=total_cost,useremail=email)

@app.route("/vie_reservation/<int:tableno>/<date>/<time>", methods=['GET'])
def vie_reservation(tableno, date, time):
    reservations = load_reservations()
    reservation = next((r for r in reservations if str(r['tableno']) == str(tableno) and str(r['date']) == str(date) and str(r['time']) == str(time)), None)
    if not reservation:
        flash('Reservation not found')
        return redirect(url_for('display_tables'))

    phone_number = reservation.get('name', 'N/A') 
    user_data = load_user_data()
    user = user_data.get(phone_number, {})
    
    customer_info = {
        'name': phone_number,
        'email': user.get('email', 'N/A'),
        'date': reservation.get('date', 'N/A'),
        'time': reservation.get('time', 'N/A'),
        'seater_status': reservation.get('tableno', 'N/A'),
        
    }
    if customer_info['menu_availed'] == 'Yes':
        orders = load_orders()
        selected_items = [item for sublist in orders.values() for item in sublist if item == phone_number]
        if selected_items:
            customer_info['menu'] = selected_items
            customer_info['total_cost'] = sum(item['cost'] for item in selected_items)
        else:
            customer_info['menu_availed'] = 'No'
            customer_info['menu'] = 'N/A'
            customer_info['total_cost'] = 0
    print(customer_info)
    return render_template("user_info_display.html", **customer_info)

@app.route("/delete_successful")
def delete_successful():
    return render_template("delete_successful.html")

if __name__ == "__main__":
    app.run(debug=True)



