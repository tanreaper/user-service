from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, User
from . import student_user

# SQLite for now; swap with PostgreSQL URI when needed
# engine = create_engine('sqlite:///users.db', echo=True)
engine = create_engine('postgresql://postgresql:secret@localhost:5432/postgresql')

# Create tables
Base.metadata.create_all(engine)

# Create a DB session
Session = sessionmaker(bind=engine)
session = Session()

# Create a new user

# Add and commit
session.add(student_user)
session.commit()

# Query to confirm
users = session.query(User).all()
for user in users:
    print(user)
