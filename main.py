from fastapi import FastAPI,HTTPException, Depends
from database import SessionLocal, Author, User, Post, Comment
from schemas import CreateAuthor, CreateUser, CreatePost, CreateComment, UserOut
from sqlalchemy.exc import IntegrityError
from auth import hash_password

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
app = FastAPI()

@app.get("/authors")
def get_authors(db= Depends(get_db)):
    authors = db.query(Author).all()
    return authors

@app.post("/authors")
def create_author(author:CreateAuthor, db = Depends(get_db)):
    new_author = Author(name = author.name, email = author.email)
    db.add(new_author)
    db.commit()
    db.refresh(new_author)
    return new_author

@app.get("/users")
def get_users(db = Depends(get_db)):
    users = db.query(User).all()    
    return users
@app.post("/users", response_model=UserOut)
def create_user(user: CreateUser, db=Depends(get_db)):
    new_user = User(
        name=user.name,
        email=user.email,
        hashed_password=hash_password(user.password)
    )
    db.add(new_user)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Email already registered")
    db.refresh(new_user)
    return new_user


@app.get("/posts")
def get_posts(db = Depends(get_db)):
    posts = db.query(Post).all()    
    return posts
@app.post("/posts")
def create_post(post: CreatePost, db = Depends(get_db)):
    new_post = Post(title = post.title, content = post.content, author_id = post.author_id)
    db.add(new_post)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=404, detail="Author not found")
    db.refresh(new_post)
    return new_post
    

@app.get("/comments")
def get_comment(db = Depends(get_db)):
    comments = db.query(Comment).all()    
    return comments
@app.post("/comments")
def create_comment(comment: CreateComment, db = Depends(get_db)):
    new_comment = Comment(content = comment.content, post_id=comment.post_id, user_id = comment.user_id)
    db.add(new_comment)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=404, detail="Post not found")
    db.refresh(new_comment)
    return new_comment

