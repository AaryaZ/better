from flask import Flask, request, jsonify
import jwt
import datetime

app = Flask(__name__)

SECRET_KEY = "your_secret_key"

users = {
    "admin": {"username": "admin", "password": "admin123", "role": "admin"},
    "librarian": {"username": "librarian", "password": "librarian123", "role": "librarian"},
}

books = {
    1: {"title": "Learn C++", "author": "Aarya Z", "year": 2024},
    2: {"title": "Red Staircase", "author": "K J Ram", "year": 2023},
    3: {"title": "Blah Blah bu bu", "author": "Xi Zhnag", "year": 2022}
}
bid_counter = 4  

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

@app.route('/register-librarian', methods=['POST']) 
def register_librarian():
    if request.user["role"] != "admin":     #admins only
        return jsonify({"error": "Forbidden"}), 403  
    data = request.json
    username = data.get("username")
    password = data.get("password")
    if username in users:
        return jsonify({"error": "User already exists"}), 400
    users[username] = {"username": username, "password": password, "role": "librarian"}
    return jsonify({"message": "Librarian registered successfully"}), 201

#Create book
@app.route('/books', methods=['POST'])
def add_book():
    if request.user["role"] not in ["admin", "librarian"]:
        return jsonify({"error": "Forbidden"}), 403
    global bid_counter
    data = request.json
    books[bid_counter] = data
    bid_counter += 1
    return jsonify({"message": "Book added successfully"}), 201

#Retrive all
@app.route('/books', methods=['GET'])
def get_books():
    if request.user["role"] not in ["admin", "librarian"]:
        return jsonify({"error": "Forbidden"}), 403
    return jsonify(books)

#Retrieve one book using id
@app.route('/books/<int:book_id>', methods=['GET'])
def get_book(book_id):
    if request.user["role"] not in ["admin", "librarian"]:
        return jsonify({"error": "Forbidden"}), 403
    book = books.get(book_id)
    if book:
        return jsonify(book)
    return jsonify({"error": "Book not found"}), 404

#Update book
@app.route('/books/<int:book_id>', methods=['PUT'])
def update_book(book_id):
    if request.user["role"] not in ["admin", "librarian"]:
        return jsonify({"error": "Forbidden"}), 403
    data = request.json
    if book_id in books:
        books[book_id] = data
        return jsonify({"message": "Book updated successfully"})
    return jsonify({"error": "Book not found"}), 404

#Delte book
@app.route('/books/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    if request.user["role"] not in ["admin", "librarian"]:
        return jsonify({"error": "Forbidden"}), 403
    if book_id in books:
        del books[book_id]
        return jsonify({"message": "Book deleted successfully"})
    return jsonify({"error": "Book not found"}), 404

#Search book
@app.route('/books/search', methods=['GET'])
def search_books():
    title_query = request.args.get("title")
    author_query = request.args.get("author")

    if not title_query and not author_query:
        return jsonify({"error": "At least one query parameter (title or author) is required"}), 400

    found_books = {}
    for book_id, book in books.items():
        if title_query and title_query.lower() in book["title"].lower():
            found_books[book_id] = book
        elif author_query and author_query.lower() in book["author"].lower():
            found_books[book_id] = book

    if found_books:
        return jsonify(found_books)
    return jsonify({"error": "No books of given title or author"}), 404


if __name__ == "__main__":
    app.run(debug=True)
