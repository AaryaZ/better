
# API Documentation for Library Management System

## Overview
This API is designed to manage a library system with books and members. It supports CRUD operations for books, user authentication, and authorization based on roles (admin, librarian). The system also allows searching books by title or author and includes pagination for listing books.

## Authentication

Authentication is required for accessing most of the API endpoints. Token-based authentication is used, where a JWT (JSON Web Token) is issued on successful login. The token must be included in the `Authorization` header for subsequent requests.

### Login

#### Endpoint:
`POST /login`

#### Request:
- Body: 
  ```json
  {
      "username": "username",
      "password": "password"
  }
  ```

#### Response:
- Success (200): 
  ```json
  {
      "token": "JWT_TOKEN"
  }
  ```
- Error (401):
  ```json
  {
      "error": "Invalid credentials"
  }
  ```

## Book Endpoints

### Add a Book

#### Endpoint:
`POST /books`

#### Request:
- Headers:
  - `Authorization`: `Bearer JWT_TOKEN`
- Body: 
  ```json
  {
      "title": "Book Title",
      "author": "Book Author",
      "year": 2023
  }
  ```

#### Response:
- Success (201):
  ```json
  {
      "message": "Book added successfully"
  }
  ```
- Error (403): Unauthorized for non-librarians and non-admin users.
  ```json
  {
      "error": "Forbidden"
  }
  ```

### Retrieve All Books

#### Endpoint:
`GET /books`

#### Request:
- Headers:
  - `Authorization`: `Bearer JWT_TOKEN`

#### Response:
- Success (200):
  ```json
  {
      "1": {
          "title": "Book Title",
          "author": "Book Author",
          "year": 2023
      },
      "2": {
          "title": "Another Book",
          "author": "Another Author",
          "year": 2022
      }
  }
  ```

### Retrieve a Single Book by ID

#### Endpoint:
`GET /books/<book_id>`

#### Request:
- Headers:
  - `Authorization`: `Bearer JWT_TOKEN`

#### Response:
- Success (200):
  ```json
  {
      "title": "Book Title",
      "author": "Book Author",
      "year": 2023
  }
  ```
- Error (404):
  ```json
  {
      "error": "Book not found"
  }
  ```

### Update a Book

#### Endpoint:
`PUT /books/<book_id>`

#### Request:
- Headers:
  - `Authorization`: `Bearer JWT_TOKEN`
- Body: 
  ```json
  {
      "title": "Updated Title",
      "author": "Updated Author",
      "year": 2025
  }
  ```

#### Response:
- Success (200):
  ```json
  {
      "message": "Book updated successfully"
  }
  ```
- Error (404): Book not found
  ```json
  {
      "error": "Book not found"
  }
  ```

### Delete a Book

#### Endpoint:
`DELETE /books/<book_id>`

#### Request:
- Headers:
  - `Authorization`: `Bearer JWT_TOKEN`

#### Response:
- Success (200):
  ```json
  {
      "message": "Book deleted successfully"
  }
  ```
- Error (404): Book not found
  ```json
  {
      "error": "Book not found"
  }
  ```

### Search Books by Title or Author

#### Endpoint:
`GET /books/search`

#### Request:
- Query Parameters:
  - `title` (optional): Filter books by title.
  - `author` (optional): Filter books by author.

#### Response:
- Success (200):
  ```json
  {
      "1": {
          "title": "Book Title",
          "author": "Book Author",
          "year": 2023
      }
  }
  ```
- Error (400): Missing query parameter for title or author
  ```json
  {
      "error": "At least one query parameter (title or author) is required"
  }
  ```
- Error (404): No books found
  ```json
  {
      "error": "No books of given title or author"
  }
  ```

## Librarian Registration (Admin Only)

### Register a Librarian

#### Endpoint:
`POST /register-librarian`

#### Request:
- Headers:
  - `Authorization`: `Bearer JWT_TOKEN` (Admin role)
- Body:
  ```json
  {
      "username": "librarian_username",
      "password": "librarian_password"
  }
  ```

#### Response:
- Success (201):
  ```json
  {
      "message": "Librarian registered successfully"
  }
  ```
- Error (403): Forbidden for non-admin users
  ```json
  {
      "error": "Forbidden"
  }
  ```
- Error (400): User already exists
  ```json
  {
      "error": "User already exists"
  }
  ```

## Error Responses

- **Unauthorized (401)**: Missing or invalid token
  ```json
  {
      "error": "Unauthorized"
  }
  ```

- **Forbidden (403)**: User does not have the required role
  ```json
  {
      "error": "Forbidden"
  }
  ```

- **Not Found (404)**: Resource not found
  ```json
  {
      "error": "Resource not found"
  }
  ```


