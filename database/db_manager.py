from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database.models import Base

# Create SQLite engine (database file: cashier.db)
engine = create_engine('sqlite:///cashier.db', echo=True)

# Create a session factory
SessionLocal = sessionmaker(bind=engine)

def init_db():
    """Initialize the database and create all tables."""
    Base.metadata.create_all(engine)
    
if __name__ == "__main__":
    init_db()
    print("Database initialized!")
