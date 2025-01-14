# FastAPI Book Management System

A robust Book Management System built with FastAPI, SQLAlchemy, and JWT authentication. The API provides features for user authentication, and CRUD operations for managing books.

## Table of Contents
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Endpoints](#endpoints)
- [Authentication](#authentication)
- [License](#license)
- [Database Configuration](#Database Configuration)
- [Database Models]
- [Postgresql and API Testing]

---

## Features
- **JWT Authentication**: Secure user login and token generation.
- **Book Management**: Add, view, update, and delete books.
- **Request Middleware**: Logs unique request IDs.
- **Input Validation**: Ensures data integrity using Pydantic models.

---

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/your-username/fastapi-book-management.git
    ```

2. Navigate to the project directory:
    ```bash
    cd fastapi-book-management
    ```

3. Create a virtual environment:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

4. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

5. Set up the database:
    - Create a `.env` file for database credentials.
    - Update `database.py` with your database URL.

6. Start the server:
    ```bash
    uvicorn main:app --reload
    ```

---

## Usage

### Run the application:
1. Navigate to `http://127.0.0.1:8000/docs` for the Swagger UI.
2. Use Postman or Curl for manual testing.

---

## Endpoints

### **Authentication**
- **POST** `/auth/token`: Generate an access token with username and password.

### **Books**
- **GET** `/books`: Retrieve all books (authentication required).
- **GET** `/books/{id}`: Retrieve a book by ID.
- **POST** `/books`: Add a new book.
- **PUT** `/books/{id}`: Update a book by ID.
- **DELETE** `/books/{id}`: Delete a book by ID.

---

## Authentication
This project uses **OAuth2 with Password Flow** and JWT tokens for authentication.

1. First, generate a token using `/auth/token` with your credentials.
2. Use the token in the `Authorization` header for subsequent requests:
   ```bash
   Authorization: Bearer <token>
   ```

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

---

## Database Configuration

This project uses **PostgreSQL** as the database engine, managed with SQLAlchemy.

### Prerequisites
- Ensure you have PostgreSQL installed and running.
- Create a database named `Book` or modify the connection string in `database.py` to match your database name.

### Database Connection String
The connection string is defined in `database.py` as:
```python
DATABASE_URL = 'postgresql://<username>:<password>@<host>:<port>/<database_name>'
```

Example:
```python
DATABASE_URL = 'postgresql://postgres:ghazaldb1@localhost:5432/Book'
```

### Steps to Set Up the Database
1. Update the `DATABASE_URL` in `database.py` with your database credentials.
2. Create the database schema using SQLAlchemy:
    ```bash
    python
    from database import Base, engine
    Base.metadata.create_all(engine)
    ```
3. Run the application:
    ```bash
    uvicorn main:app --reload
    ```

---

## Database Models

This project uses SQLAlchemy ORM to define the database schema. Below are the primary models:

### **Book Model**
Represents the `book` table in the database.

| Column   | Type     | Constraints         | Description                  |
|----------|----------|---------------------|------------------------------|
| `id`     | Integer  | Primary Key, Indexed | Unique identifier for each book. |
| `task`   | String   | Not Null            | Name or title of the book.   |

Example SQL Table:
```sql
CREATE TABLE book (
    id SERIAL PRIMARY KEY,
    task VARCHAR(255) NOT NULL
);
```

### **Users Model**
Represents the `users` table in the database.

| Column          | Type     | Constraints         | Description                          |
|------------------|----------|---------------------|--------------------------------------|
| `id`            | Integer  | Primary Key, Indexed | Unique identifier for each user.     |
| `username`      | String   | Unique              | Username of the user.                |
| `hashed_password` | String |                     | Password stored as a hashed value.   |

Example SQL Table:
```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR UNIQUE,
    hashed_password VARCHAR
);
```

---

### Relationships and Usage
- The **`Book`** table is used for managing book-related operations like adding, retrieving, updating, and deleting records.
- The **`Users`** table supports user authentication and stores credentials securely using hashed passwords.

---

## Database and API Testing

### Database: PostgreSQL
The project uses **PostgreSQL** as its database backend.  

- **Database URL**: 
  The connection string is configured in `database.py`:
  ```python
  DATABASE_URL = 'postgresql://<username>:<password>@<host>:<port>/<database_name>'
  ```
  Example:
  ```python
  DATABASE_URL = 'postgresql://postgres:ghazaldb1@localhost:5432/Book'
  ```

- **Setup**:
  1. Ensure PostgreSQL is installed and running on your system.
  2. Create a database named `Book`:
      ```sql
      CREATE DATABASE Book;
      ```
  3. Run the migration script to create the required tables:
      ```bash
      python -c "from database import Base, engine; Base.metadata.create_all(engine)"
      ```

---

### API Testing: Postman
Postman is recommended for testing the API endpoints.

#### Steps to Use Postman:
1. Import the API collection:
   - Export your API collection from Postman and include it in your repository as `postman_collection.json`.
   - Users can import the collection into Postman for ready-to-use API requests.
   
2. Set up an **Authorization Token**:
   - Use the `/auth/token` endpoint to generate a JWT token.
   - Add the token in the **Authorization** tab of Postman:
     ```
     Type: Bearer Token
     Token: <your_generated_token>
     ```

3. Test the Endpoints:
   - Example request for getting all books:
     ```http
     GET /books
     Authorization: Bearer <your_token>
     ```

---

### Example Postman Requests

- **Get All Books**  
  **Method**: `GET`  
  **URL**: `http://127.0.0.1:8000/books`  
  **Headers**:  
  - `Authorization: Bearer <your_token>`

- **Add a New Book**  
  **Method**: `POST`  
  **URL**: `http://127.0.0.1:8000/books`  
  **Headers**:  
  - `Authorization: Bearer <your_token>`  
  **Body (JSON)**:  
  ```json
  {
    "task": "History"
  }
  ```
