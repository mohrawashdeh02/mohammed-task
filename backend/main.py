from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
import models, schemas
from database import engine, SessionLocal, Base
from datetime import datetime

app = FastAPI()

Base.metadata.create_all(bind=engine)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ================== Categories ==================

@app.post("/categories", response_model=schemas.CategoryOut, status_code=201)
def create_category(category: schemas.CategoryCreate, db: Session = Depends(get_db)):
    existing = db.query(models.Category).filter(models.Category.name == category.name).first()
    if existing:
        raise HTTPException(status_code=400, detail="Category already exists")

    new_category = models.Category(name=category.name)
    db.add(new_category)
    db.commit()
    db.refresh(new_category)
    return new_category


@app.get("/categories", response_model=list[schemas.CategoryOut])
def get_categories(db: Session = Depends(get_db)):
    return db.query(models.Category).all()


@app.get("/categories/{id}", response_model=schemas.CategoryOut)
def get_category(id: int, db: Session = Depends(get_db)):
    category = db.query(models.Category).get(id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category


@app.put("/categories/{id}", response_model=schemas.CategoryOut)
def update_category(id: int, data: schemas.CategoryCreate, db: Session = Depends(get_db)):
    category = db.query(models.Category).get(id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")

    category.name = data.name
    db.commit()
    db.refresh(category)
    return category


@app.delete("/categories/{id}")
def delete_category(id: int, db: Session = Depends(get_db)):
    category = db.query(models.Category).get(id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")

    db.delete(category)
    db.commit()
    return {"detail": "Category deleted"}


# ================== Posts ==================

@app.post("/posts", response_model=schemas.PostOut, status_code=201)
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db)):
    category = db.query(models.Category).get(post.category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")

    new_post = models.Post(
        category_id=post.category_id,
        title=post.title,
        body=post.body
    )
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@app.get("/posts", response_model=list[schemas.PostOut])
def get_posts(db: Session = Depends(get_db)):
    return db.query(models.Post).all()


@app.get("/posts/{id}", response_model=schemas.PostOut)
def get_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).get(id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return post


@app.put("/posts/{id}", response_model=schemas.PostOut)
def update_post(id: int, data: schemas.PostCreate, db: Session = Depends(get_db)):
    post = db.query(models.Post).get(id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    post.category_id = data.category_id
    post.title = data.title
    post.body = data.body
    post.updated_at = datetime.utcnow()

    db.commit()
    db.refresh(post)
    return post


@app.delete("/posts/{id}")
def delete_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).get(id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    db.delete(post)
    db.commit()
    return {"detail": "Post deleted"}


# ================== Comments ==================

@app.post("/posts/{post_id}/comments", response_model=schemas.CommentOut, status_code=201)
def create_comment(post_id: int, comment: schemas.CommentCreate, db: Session = Depends(get_db)):
    post = db.query(models.Post).get(post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    new_comment = models.Comment(post_id=post_id, body=comment.body)
    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)
    return new_comment


@app.get("/posts/{post_id}/comments", response_model=list[schemas.CommentOut])
def get_comments(post_id: int, db: Session = Depends(get_db)):
    return db.query(models.Comment).filter(models.Comment.post_id == post_id).all()


@app.delete("/comments/{id}")
def delete_comment(id: int, db: Session = Depends(get_db)):
    comment = db.query(models.Comment).get(id)
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")

    db.delete(comment)
    db.commit()
    return {"detail": "Comment deleted"}

