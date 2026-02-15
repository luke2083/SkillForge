from sqlalchemy import create_engine, URL
from sqlalchemy.orm import Session, sessionmaker

postgres_url = URL.create(
    "postgresql",
    username="postgres",
    password="admin",
    port=5432,
    database="skillforge"
)

engine = create_engine(postgres_url, echo=True)
Session = sessionmaker(engine)

def get_db():
    db = Session()
    try:
        yield db
    except:
        db.close()
        raise
    