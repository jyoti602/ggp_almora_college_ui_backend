from database import engine, Base
from models.user import User

# Create the users table
Base.metadata.create_all(bind=engine)
print("Users table created successfully!")
