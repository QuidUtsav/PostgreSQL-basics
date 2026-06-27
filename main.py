from fastapi import FastAPI
from database import SessionLocal, Author

app = FastAPI()

@app.get("/authors")
def get_authors():
    db = SessionLocal()
    authors = db.query(Author).all()
    db.close()
    return authors