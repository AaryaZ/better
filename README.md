
# Better Flask API

This project implements a simple Library Management System using Flask. It allows CRUD operations for books and members, with token-based authentication and book search. The system is implemented in-memory, without using a database.

## Table of Contents
- [Prerequisites](#prerequisites)
- [How to Run](#how-to-run)
- [API Endpoints](#api-endpoints)
- [Design Choices](#design-choices)
- [Assumptions and Limitations](#assumptions-and-limitations)

## Prerequisites

Before running the project, ensure you have the following installed:
- `Flask`
- `PyJWT` (for JWT authentication)

To install the required dependencies, use the following command:

```bash
pip install flask pyjwt
```

## How to Run

1. Clone the repository:

```bash
https://github.com/AaryaZ/better.git
```

2. Navigate to the project folder:

```bash
cd better
```

3. Run the Flask application:

```bash
python app.py
```

The API will be available at `http://127.0.0.1:5000/`.

## API Endpoints
For detailed API documentation, refer to [Docs](https://github.com/AaryaZ/better/blob/master/Docs/api_documentation.md).

## Design Choices

- **In-memory storage**: The system does not use a database. All the books and users are stored in memory, allowing for a fast, simple implementation without the need for an external database.
- **JWT authentication**: Token-based authentication (JWT) is used to secure API endpoints. Users must log in to obtain a token, which is then included in the Authorization header of subsequent requests.
- **Role-based access**: Users are assigned roles (Admin, Librarian). Different endpoints are accessible depending on the user's role.

## Assumptions and Limitations

- **In-memory storage**: Data is lost when the server is restarted. This project does not use a persistent database.
- **Role-based restrictions**: Only Admin can register Librarians, and only Librarians/Admins can perform CRUD operations on books.
- **Search**: The search functionality allows filtering books by title or author but cannot combine multiple filters.


