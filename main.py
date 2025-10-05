from fastapi import FastAPI
from pydantic import BaseModel
import json, os

app = FastAPI(title="Organisasi Turnamen API", version="1.0")

DATA_FILE = "data.json"

# ======================
# Model Data
# ======================
class Tournament(BaseModel):
    id: int
    name: str
    start_date: str
    match_duration: int = 30

# ======================
# Fungsi Bantu
# ======================
def load_data():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)

# ======================
# Endpoint API
# ======================
@app.get("/")
def home():
    return {"message": "Selamat datang di API Organisasi Sistem Pertandingan"}

@app.get("/tournaments")
def get_tournaments():
    return load_data()

@app.post("/tournaments")
def create_tournament(t: Tournament):
    data = load_data()
    data.append(t.dict())
    save_data(data)
    return {"message": "Turnamen berhasil ditambahkan", "data": t}

@app.delete("/tournaments/{tid}")
def delete_tournament(tid: int):
    data = load_data()
    new_data = [d for d in data if d["id"] != tid]
    save_data(new_data)
    return {"message": f"Turnamen dengan ID {tid} telah dihapus"}
