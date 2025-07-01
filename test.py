from flask import Flask, request

app = Flask(__name__)

contacts = []  # In-memory list to store contact dictionaries

@app.route("/", methods=["GET", "POST"])
def contact_book():
    message = ""

    if request.method == "POST":
        name = request.form.get("name")
        phone = request.form.get("phone")
        
        if name and phone:
            contacts.append({"name": name, "phone": phone})
            message = "Contact added!"
        else:
            message = "Please fill in both fields."

    # Build HTML
    html = f"""
    <h2>Contact Book</h2>
    <form method="POST">
        Name: <input type="text" name="name" required><br>
        Phone: <input type="text" name="phone" required><br>
        <button type="submit">Add Contact</button>
    </form>
    <p style='color:green;'>{message}</p>

    <h3>Saved Contacts:</h3>
    <ul>
    """
    for i, contact in enumerate(contacts):
        html += f"<li>{contact['name']} - {contact['phone']} <a href='/delete/{i}'>Delete</a></li>"

    html += "</ul>"

    return html

@app.route("/delete/<int:index>")
def delete_contact(index):
    if 0 <= index < len(contacts):
        removed = contacts.pop(index)
        return f"<p>Deleted {removed['name']}'s contact.</p><a href='/'>Back</a>"
    return "<p>Invalid index.</p><a href='/'>Back</a>"

if __name__ == "__main__":
    app.run(debug=True)

