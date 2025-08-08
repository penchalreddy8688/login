🔐 FastAPI User Authentication App
This is a simple user authentication API built using FastAPI, SQLite, and Passlib with bcrypt for password hashing.

🚀 Features
✅ User Signup (with unique username)
✅ Password hashing using bcrypt
✅ Secure user login
✅ SQLite as the database
✅ Clear error handling

# 🚀 FastAPI Auth App with CORS Support

This is a simple authentication backend built with **FastAPI** that includes:
- User signup and login functionality
- Password hashing using `passlib` and `bcrypt`
- SQLite database
- Proper CORS configuration for cross-origin frontend support

## 📦 Features

- ✅ User registration (`/signup`)
- ✅ User login (`/login`)
- ✅ Password hashing for secure storage
- ✅ CORS middleware to allow frontend JavaScript (e.g., from a different port) to interact with this API


📁 Project Structure

fastapi-auth-app/
├── main.py              # FastAPI application with signup/login
├── db.py                # SQLite DB connection + table creation
├── requirements.txt     # Required Python packages
└── README.md            # Project overview and setup guide(md-markdown documentation)

🔧 Requirements
      Python 3.7+
      pip (Python package manager)

📦 Installation
1.Clone the repo:

     git clone https://github.com/your-username/fastapi-auth-app.git
     cd fastapi-auth-app

2.Install dependencies:

     pip install -r requirements.txt

▶️ Running the App

    uvicorn main:app --reload

    #Open in browser: http://127.0.0.1:8000/docs
    #Use Swagger UI to test /signup and /login

🧪 API Endpoints
✅ POST /signup
Registers a new user.

#Request body:

{
  "username": "exampleuser",
  "password": "examplepass"
}

#Responses:

200 OK: User registered successfully

400: Username already exists

🔐 POST /login
Authenticates a user.

#Request body:

{
  "username": "exampleuser",
  "password": "examplepass"
}

#Responses:

200 OK: Welcome message

401: Invalid username or password

📚 Technologies Used

FastAPI
Passlib
SQLite (Python’s sqlite3 module)

✅ To-Do (Optional Features)
 
 JWT token authentication
 Password reset endpoint
 User logout
 Use PostgreSQL or MongoDB










