from sqlalchemy import create_engine # Establish connection to the database
from sqlalchemy.orm import sessionmaker # Create session objects for interacting with the database efficiently

DATABASE_URL = "postgresql://yourname:pw@localhost/url_monitor"

engine = create_engine(DATABASE_URL) # initialize the database connection
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# The SessionLocal class is a factory for creating new Session objects.
# The autocommit=False parameter means that changes are not committed automatically to the database.
# The autoflush=False parameter means that the Session does not automatically flush pending changes to the database.
# The bind=engine parameter means that the SessionLocal class will use the engine object to interact with the database.

def get_db():
    db = SessionLocal() # create a new Session object
    try:
        yield db # Temporarily gives control to calling functions, enabling database interactions
    finally:
        db.close() # Ensures session closure once operations are completed, even if excepetions occur.

# The get_db function provides a clean way of generating batabase session for API endpoints for tasks.
