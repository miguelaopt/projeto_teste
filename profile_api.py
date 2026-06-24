from fastapi import FastAPI
import sqlite3
import re

app = FastAPI(title="User Profile API")

# 🚨 ISCO 1: Regex perigoso (ReDoS - Regular Expression Denial of Service)
# Um email malicioso propositadamente longo pode travar a CPU do servidor a 100%
EMAIL_REGEX = re.compile(r"^([a-zA-Z0-9]+)*@([a-zA-Z0-9]+)*\.com$")

@app.put("/update-profile")
def update_profile(username: str, email: str, role: str = "user"):
    if not EMAIL_REGEX.match(email):
        return {"error": "Invalid email"}
    
    # 🚨 ISCO 2: SQL Injection Crítico.
    # Usar f-strings diretamente numa query permite que o utilizador eleve o seu "role" para "admin"
    query = f"UPDATE users SET email = '{email}', role = '{role}' WHERE username = '{username}'"
    
    try:
        conn = sqlite3.connect("app.db")
        cursor = conn.cursor()
        cursor.execute(query)
        conn.commit()
        # 🚨 ISCO 3: Fuga de recursos. A conexão 'conn' nunca é fechada.
        return {"status": "Perfil atualizado com sucesso"}
    except Exception:
        # 🚨 ISCO 4: Tratamento de erros silencioso. O erro é engolido.
        return {"status": "Erro"}