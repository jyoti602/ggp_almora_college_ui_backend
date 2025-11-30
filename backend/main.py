from fastapi import FastAPI, Form
from fastapi.middleware.cors import CORSMiddleware
import mysql.connector

from routers.student_router import router as student_router
from routers.teacher_router import router as teacher_router
from routers.user_router import router as user_router

app = FastAPI()

# ✅ Allow frontend connection
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Include API routers
app.include_router(student_router)
app.include_router(teacher_router)
app.include_router(user_router)

# ✅ Database connection (legacy contact form)
conn = mysql.connector.connect(
    host="localhost",
    user="root",           # your MySQL username
    password="sohan@9761",           # your MySQL password (if any)
    database="college_db"  # your database name
)
cursor = conn.cursor()


@app.post("/api/contact")
async def contact(name: str = Form(...), email: str = Form(...), message: str = Form(...)):
    """Simple contact endpoint saving to contact_form table (existing behavior)."""
    try:
        sql = "INSERT INTO contact_form (name, email, message) VALUES (%s, %s, %s)"
        cursor.execute(sql, (name, email, message))
        conn.commit()
        return {"status": "success", "message": "Message saved successfully"}
    except Exception as e:
        print("Database Error:", e)
        return {"status": "error", "message": str(e)}
