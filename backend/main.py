from fastapi import FastAPI, Form
from fastapi.middleware.cors import CORSMiddleware
import mysql.connector

app = FastAPI()

# ✅ Allow frontend connection
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3001", "http://127.0.0.1:3001"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Database connection
conn = mysql.connector.connect(
    host="localhost",
    user="root",           # your MySQL username
    password="sohan@9761",           # your MySQL password (if any)
    database="college_db"  # your database name
)
cursor = conn.cursor()

# ✅ API endpoint for contact form
@app.post("/api/contact")
async def contact(name: str = Form(...), email: str = Form(...), message: str = Form(...)):
    try:
        sql = "INSERT INTO contact_form (name, email, message) VALUES (%s, %s, %s)"
        cursor.execute(sql, (name, email, message))
        conn.commit()
        return {"status": "success", "message": "Message saved successfully"}
    except Exception as e:
        print("Database Error:", e)
        return {"status": "error", "message": str(e)}
