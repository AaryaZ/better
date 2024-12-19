
# Library Management System - Flask API

This project implements a simple Library Management System using Flask. It allows CRUD operations for books and members, with token-based authentication and additional features like book search and pagination. The system is implemented in-memory, without using a database.

## Table of Contents
- [Prerequisites](#prerequisites)
- [How to Run](#how-to-run)
- [API Endpoints](#api-endpoints)
- [Design Choices](#design-choices)
- [Assumptions and Limitations](#assumptions-and-limitations)
- [License](#license)

## Prerequisites

Before running the project, ensure you have the following installed:
- Python 3.x
- `Flask`
- `PyJWT` (for JWT authentication)

To install the required dependencies, use the following command:

```bash
pip install Flask PyJWT
```

## How to Run

1. Clone the repository:

```bash
git clone https://github.com/your-username/library-management-system.git
```

2. Navigate to the project folder:

```bash
cd library-management-system
```

3. Run the Flask application:

```bash
python app.py
```

The API will be available at `http://127.0.0.1:5000/`.

## API Endpoints

### 1. POST /login

- **Description**: Logs in a user and generates a JWT token for authentication.
- **Request Body**:
  ```json
  {
    "username": "admin",
    "password": "admin123"
  }
  ```
- **Response**:
  - **Success**: 
    ```json
    {
      "token": "<JWT_TOKEN>"
    }
    ```
  - **Error**: 
    ```json
    {
      "error": "Invalid credentials"
    }
    ```

### 2. POST /register-librarian

- **Description**: Registers a new librarian (Admin only).
- **Request Body**:
  ```json
  {
    "username": "new_librarian",
    "password": "librarian123"
  }
  ```
- **Response**:
  - **Success**:
    ```json
    {
      "message": "Librarian registered successfully"
    }
    ```
  - **Error**:
    ```json
    {
      "error": "User already exists"
    }
    ```

### 3. POST /books

- **Description**: Adds a new book to the library collection (Librarians and Admins only).
- **Request Body**:
  ```json
  {
    "title": "Book Title",
    "author": "Author Name",
    "year": 2022
  }
  ```
- **Response**:
  - **Success**:
    ```json
    {
      "message": "Book added successfully"
    }
    ```

### 4. GET /books

- **Description**: Retrieves all books in the library.
- **Response**:
  - **Success**:
    ```json
    {
      "1": {
        "title": "Learn C++",
        "author": "Aarya Z",
        "year": 2024
      },
      "2": {
        "title": "Red Staircase",
        "author": "K J Ram",
        "year": 2023
      }
    }
    ```

### 5. GET /books/<book_id>

- **Description**: Retrieves a specific book by its ID.
- **Response**:
  - **Success**:
    ```json
    {
      "title": "Learn C++",
      "author": "Aarya Z",
      "year": 2024
    }
    ```
  - **Error**:
    ```json
    {
      "error": "Book not found"
    }
    ```

### 6. PUT /books/<book_id>

- **Description**: Updates a specific book by its ID.
- **Request Body**:
  ```json
  {
    "title": "Updated Book Title",
    "author": "Updated Author Name",
    "year": 2024
  }
  ```
- **Response**:
  - **Success**:
    ```json
    {
      "message": "Book updated successfully"
    }
    ```
  - **Error**:
    ```json
    {
      "error": "Book not found"
    }
    ```

### 7. DELETE /books/<book_id>

- **Description**: Deletes a specific book by its ID.
- **Response**:
  - **Success**:
    ```json
    {
      "message": "Book deleted successfully"
    }
    ```
  - **Error**:
    ```json
    {
      "error": "Book not found"
    }
    ```

### 8. GET /books/search

- **Description**: Searches for books by title or author.
- **Query Parameters**:
  - `title`: The title of the book (optional)
  - `author`: The author of the book (optional)
- **Response**:
  - **Success**:
    ```json
    {
      "1": {
        "title": "Learn C++",
        "author": "Aarya Z",
        "year": 2024
      }
    }
    ```
  - **Error**:
    ```json
    {
      "error": "At least one query parameter (title or author) is required"
    }
    ```

## Design Choices

- **In-memory storage**: The system does not use a database. All the books and users are stored in memory, allowing for a fast, simple implementation without the need for an external database.
- **JWT authentication**: Token-based authentication (JWT) is used to secure API endpoints. Users must log in to obtain a token, which is then included in the Authorization header of subsequent requests.
- **Role-based access**: Users are assigned roles (Admin, Librarian). Different endpoints are accessible depending on the user's role.

## Assumptions and Limitations

- **In-memory storage**: Data is lost when the server is restarted. This project does not use a persistent database.
- **Role-based restrictions**: Only Admin can register Librarians, and only Librarians/Admins can perform CRUD operations on books.
- **Search**: The search functionality allows filtering books by title or author but cannot combine multiple filters.

## License

This project is open-source and licensed under the MIT License.

