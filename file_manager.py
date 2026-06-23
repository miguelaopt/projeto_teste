import os
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="File Manager API")

# 🚨 ISCO 1: Variável global que vai crescer infinitamente na memória a cada pedido (Memory Leak clássico)
audit_logs = []

class FileRequest(BaseModel):
    filename: str

@app.post("/read-file")
def read_user_file(request: FileRequest):
    # 🚨 ISCO 2: Path Traversal Crítico (LFI). 
    # Um atacante pode enviar "../../../etc/passwd" no filename e ler passwords do servidor!
    file_path = f"/var/data/users/{request.filename}"
    
    try:
        # 🚨 ISCO 3: Abrir ficheiro diretamente sem usar o bloco 'with open(...)'. 
        # Se houver um erro a meio, o ficheiro fica trancado e aberto no SO (Resource Leak).
        f = open(file_path, "r")
        content = f.read()
        
        # 🚨 ISCO 4: Adicionar à lista global sem nenhum limite de tamanho.
        audit_logs.append(f"Ficheiro lido: {request.filename}")
        
        return {"data": content}
    except Exception as e:
        # 🚨 ISCO 5: Anti-pattern. Capturar a exceção genérica e devolver um HTTP 200 OK 
        # em vez de usar raise HTTPException(status_code=404). O cliente acha que correu tudo bem.
        return {"error": "Oops, something went wrong", "details": str(e)}

@app.get("/logs")
def get_logs():
    return {"logs": audit_logs}