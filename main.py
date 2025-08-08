from fastapi import FastAPI, HTTPException, Depends #Imports FastAPI framework components: FastAPI to create the app,HTTPException for error responses,Depends to inject dependencies like the database connection.
from pydantic import BaseModel #to define request schemas (like username and password input)
from db import get_db_connection  #Imports the generator function that yields a SQLite connection.
from passlib.context import CryptContext  #to manage password hashing and verification.
import sqlite3 # to define the database connection type for type hinting.
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()  # Initialize FastAPI app

# Allow all origins (for development only)
app.add_middleware(    # the browser automatically sends an OPTIONS request first to check if the server allows it.This is called a CORS preflight request.
    CORSMiddleware,    #By default, browsers block frontend apps (like an HTML page running on http://localhost:5500) from making HTTP requests to a different domain, like http://127.0.0.1:8000 (your FastAPI backend).
    allow_origins=["*"],  # You can specify frontend domains here for production
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods (GET, POST, OPTIONS, etc.)
    allow_headers=["*"],  # Allow all headers (especially Content-Type, Authorization)
)

# Pydantic model for incoming request data (signup/login)
class User(BaseModel): #Used for request body validation.
    username: str
    password: str

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto") #Creates a password hashing context using the bcrypt algorithm.
# bcrypt is a strong, slow hashing algorithm designed specifically for passwords — widely recommended for secure password storage.a secure algorithm resistant to brute-force attacks.
#CryptContext is a class from passlib
# If you use multiple schemes (e.g., bcrypt + SHA256), passlib will warn you if a hash was created using a deprecated one.auto makes it automatically mark older/less secure schemes as deprecated, encouraging you to upgrade stored hashes over time.

@app.post("/signup") #Declares a POST route for user registration
async def signup(user: User, conn: sqlite3.Connection = Depends(get_db_connection)):   #user is automatically parsed from the request body.conn is a SQLite connection injected by FastAPI using Depends.
    try:
        existing = conn.execute("SELECT * FROM users WHERE username = ?", (user.username,))   # Check if the username already exists in the database
        if existing.fetchone():
            raise HTTPException(status_code=400, detail="Username already exists")

        hashed_password = pwd_context.hash(user.password) # Hash the user's password before storing it

        conn.execute("INSERT INTO users (username, password) VALUES (?, ?)", (user.username, hashed_password)) #Inserts the new user and hashed password into the users table.
        conn.commit() #Commits the transaction to save the new user.

        return {"message": "User registered successfully"}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) #Catches unexpected errors and returns a 500 Internal Server Error with the error message.

@app.post("/login") #Declares a POST route for user login.
async def login(user: User, conn: sqlite3.Connection = Depends(get_db_connection)):   #user is parsed from the request body; conn is injected.
    cursor = conn.execute("SELECT * FROM users WHERE username = ?", (user.username,)) #Retrieve user record by username
    db_user = cursor.fetchone()  #Fetches the result row.

    if not db_user:
        raise HTTPException(status_code=401, detail="Invalid username or password")   #If the user is not found, raises a 401 Unauthorized error.

    stored_password = db_user["password"]  #Extracts the stored hashed password from the database row

    if not pwd_context.verify(user.password, stored_password):  #Verify the entered password against the stored hashed password
        raise HTTPException(status_code=401, detail="Invalid username or password")

    return {"message": f"Welcome, {user.username}!"}  #If authentication succeeds, returns a welcome message.

# Functionality
#1. User Signup (/signup):
   # Accepts username and password in the request body.
   # Checks if the username already exists in the database.
   # If not:
   # Hashes the password using bcrypt (secure algorithm).
   # Stores the username and hashed password in the database.
   # Returns a success message.

#2. User Login (/login):
   # Accepts username and password.
   # Fetches the user record from the database using the given username.
   # If user is found:
      # Compares the hashed password from DB with the entered password using passlib.verify.
      # If valid, returns a welcome message.
      # If invalid, raises an "Invalid username or password" error.
   # If user is not found, raises an error.  