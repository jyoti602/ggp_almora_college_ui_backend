from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Use same credentials as main.py: user=root, password="sohan@9761"
# '@' must be URL-encoded as '%40' in the connection string
SQLALCHEMY_DATABASE_URL = (
    "mysql+mysqlconnector://root:sohan%409761@localhost/college_db"
)

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
