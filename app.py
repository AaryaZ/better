from flask import Flask, request, jsonify
import jwt
import datetime

app = Flask(__name__)

# Secret key for JWT encoding/decoding
SECRET_KEY = "your_secret_key"

# In-memory user database
users = {
    "admin": {"username": "admin", "password": "admin123", "role": "admin"},
    "librarian": {"username": "librarian", "password": "librarian123", "role": "librarian"},
}

books = {}
book_id_counter = 1

def generate_token(username, role):
    payload = {
        "username": username,
        "role": role,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)  
    }
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    user = users.get(username)
    if user and user["password"] == password:
        token = generate_token(username, user["role"])
        return jsonify({"token": token})
    return jsonify({"error": "Invalid credentials"}), 401

@app.before_request
def authenticate_and_authorize():
    if request.endpoint == "login":
        return
    auth_header = request.headers.get("Authorization")
    if not auth_header:
        return jsonify({"error": "Unauthorized"}), 401
    try:
        token = auth_header.split(" ")[1]
        decoded_token = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        request.user = {"username": decoded_token["username"], "role": decoded_token["role"]}
    except (IndexError, jwt.ExpiredSignatureError, jwt.InvalidTokenError):
        return jsonify({"error": "Unauthorized"}), 401

# Admin-only endpoint to register new librarians
@app.route('/register-librarian', methods=['POST'])
def register_librarian():
    if request.user["role"] != "admin":
        return jsonify({"error": "Forbidden"}), 403
    data = request.json
    username = data.get("username")
    password = data.get("password")
    if username in users:
        return jsonify({"error": "User already exists"}), 400
    users[username] = {"username": username, "password": password, "role": "librarian"}
    return jsonify({"message": "Librarian registered successfully"}), 201

# CRUD operations for books (accessible by both admin and librarian)
@app.route('/books', methods=['POST'])
def add_book():
    if request.user["role"] not in ["admin", "librarian"]:
        return jsonify({"error": "Forbidden"}), 403
    global book_id_counter
    data = request.json
    books[book_id_counter] = data
    book_id_counter += 1
    return jsonify({"message": "Book added successfully"}), 201

@app.route('/books', methods=['GET'])
def get_books():
    if request.user["role"] not in ["admin", "librarian"]:
        return jsonify({"error": "Forbidden"}), 403
    return jsonify(books)

@app.route('/books/<int:book_id>', methods=['GET'])
def get_book(book_id):
    if request.user["role"] not in ["admin", "librarian"]:
        return jsonify({"error": "Forbidden"}), 403
    book = books.get(book_id)
    if book:
        return jsonify(book)
    return jsonify({"error": "Book not found"}), 404

@app.route('/books/<int:book_id>', methods=['PUT'])
def update_book(book_id):
    if request.user["role"] not in ["admin", "librarian"]:
        return jsonify({"error": "Forbidden"}), 403
    data = request.json
    if book_id in books:
        books[book_id] = data
        return jsonify({"message": "Book updated successfully"})
    return jsonify({"error": "Book not found"}), 404

@app.route('/books/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    if request.user["role"] not in ["admin", "librarian"]:
        return jsonify({"error": "Forbidden"}), 403
    if book_id in books:
        del books[book_id]
        return jsonify({"message": "Book deleted successfully"})
    return jsonify({"error": "Book not found"}), 404

if __name__ == "__main__":
    app.run(debug=True)
