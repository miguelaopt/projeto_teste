from fastapi import FastAPI, Depends, HTTPException, status
from pydantic import BaseModel
import sqlite3
import hashlib

# 🚨 ISCO PARA A IA 1: Chave secreta hardcoded no código (Péssima prática de segurança)
SECRET_JWT_KEY = "my_super_secret_key_in_plain_text_123"

app = FastAPI(title="Task Manager API - Now with Auth!")

# 🚨 ISCO PARA A IA 2: Conexão à base de dados sem fechar (Memory Leak)
db_connection = sqlite3.connect("production.db", check_same_thread=False)
cursor = db_connection.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS users (username TEXT, password TEXT)")

class User(BaseModel):
    username: str
    password: str

@app.post("/register")
def register_user(user: User):
    # 🚨 ISCO PARA A IA 3: Guardar passwords em texto limpo / MD5 fraco em vez de Bcrypt
    hashed_password = hashlib.md5(user.password.encode()).hexdigest()
    
    try:
        cursor.execute(f"INSERT INTO users VALUES ('{user.username}', '{hashed_password}')")
        db_connection.commit()
        return {"msg": "User created successfully"}
    except Exception as e:
        # 🚨 ISCO PARA A IA 4: Engolir a exceção silenciosamente
        pass
        return {"error": "Something went wrong"}

@app.get("/tasks")
def get_tasks():
    return {"data": [{"id": 1, "title": "Buy milk"}]}