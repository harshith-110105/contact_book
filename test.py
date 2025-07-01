from flask import Flask, request

app = Flask(__name__)

# Global list to store order history
order_history = []

@app.route('/', methods=['GET', 'POST'])
def pizza_order():
    result = ''

    if request.method == 'POST':
        name = request.form.get('name')
        address = request.form.get('address')
        size = request.form.get('size')
        toppings = request.form.getlist('toppings')

        size_prices = {'small': 150, 'medium': 250, 'large': 350}
        topping_price = 40  # each topping costs 40

        base_price = size_prices.get(size, 0)
        total_price = base_price + (topping_price * len(toppings))
        size_display = size.capitalize() if size else "Not selected"

        # Create order dictionary
        order = {
            'name': name,
            'address': address,
            'size': size_display,
            'toppings': toppings,
            'total': total_price
        }

        # Add to history
        order_history.append(order)

        result = f'''
        <h3> Order Placed Successfully!</h3>
        <p><strong>Name:</strong> {name}</p>
        <p><strong>Address:</strong> {address}</p>
        <p><strong>Size:</strong> {size_display} - ₹{base_price}</p>
        <p><strong>Toppings:</strong> {', '.join(toppings)} - ₹{topping_price * len(toppings)}</p>
        <p><strong>Total Amount:</strong> ₹{total_price}</p>
        <a href="/history"> View Order History</a>
        '''

    return f'''
        <h2> PIZZA ORDER PROGRAM </h2>
        <form method="POST">
            Name: <input type="text" name="name" required><br><br>
            Address: <input type="text" name="address" required><br><br>

            Select Pizza Size:<br>
            <input type="radio" name="size" value="small" required> Small (₹150)<br>
            <input type="radio" name="size" value="medium"> Medium (₹250)<br>
            <input type="radio" name="size" value="large"> Large (₹350)<br><br>

            Choose Toppings (₹40 each):<br>
            <input type="checkbox" name="toppings" value="Cheese"> Cheese<br>
            <input type="checkbox" name="toppings" value="Tomato"> Tomato<br>
            <input type="checkbox" name="toppings" value="Onion"> Onion<br>
            <input type="checkbox" name="toppings" value="Olives"> Olives<br><br>

            <button type="submit">Place Order</button>
        </form>

        <hr>
        {result}
    '''

@app.route('/history')
def show_history():
    history_html = '<h2> Order History</h2>'
    if not order_history:
        history_html += '<p>No orders placed yet.</p>'
    else:
        for i, order in enumerate(order_history, 1):
            history_html += f'''
            <p><strong>Order {i}</strong><br>
            Name: {order['name']}<br>
            Address: {order['address']}<br>
            Size: {order['size']}<br>
            Toppings: {', '.join(order['toppings'])}<br>
            Total: ₹{order['total']}<br><hr></p>
            '''
    history_html += '<a href="/"> Back to Order </a>'
    return history_html

if __name__ == "__main__":
    app.run(debug=True)

