from fastapi import FastAPI, Depends, status, Response, HTTPException
from schemas import Blog,ShowBlog, User, ShowUser, Login
from typing import List
from models import Blog as blog_model, Base, User as user_model
from database import engine, SessionLocal, get_db
from sqlalchemy.orm import Session
from hashing import Hash
from tokens import create_access_token
from oauth2 import get_current_user
from fastapi.security import OAuth2PasswordRequestForm

from passlib.context import CryptContext
# from routers import user, blog


app = FastAPI()

Base.metadata.create_all(bind=engine)

# app.include_router(blog.router)
# app.include_router(user.router)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/blog", status_code=status.HTTP_201_CREATED, tags=["Blogs"])
def create(request: Blog, db: Session = Depends(get_db)):
    new_blog = blog_model(title=request.title, body=request.body, user_id=1)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog

@app.get("/blog",response_model=List[ShowBlog],tags=["Blogs"])
# def all(db: Session = Depends(get_db)):
def all(db: Session = Depends(get_db),get_current_user: str = Depends(get_current_user)):
    blogs = db.query(blog_model).all()
    return blogs

@app.get("/blog/{id}",status_code=status.HTTP_200_OK, response_model=ShowBlog,tags=["Blogs"])
def GetById(id,response : Response, db: Session = Depends(get_db)):
    blog = db.query(blog_model).filter(blog_model.id == id).first()
    if not blog:
        # response.status_code = status.HTTP_404_NOT_FOUND      # return {"detail": f"Blog with id {id} not found"}
         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with id {id} not found")
    return blog

@app.delete("/blog/{id}",status_code=status.HTTP_204_NO_CONTENT,tags=["Blogs"])
def destroyer(id, db: Session = Depends(get_db)):
    blog = db.query(blog_model).filter(blog_model.id == id)
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with id {id} not found")
    blog.delete(synchronize_session=False)
    db.commit()
    return 'done'

@app.put("/blog/{id}",status_code=status.HTTP_202_ACCEPTED,tags=["Blogs"])
def update(id, request: Blog, db: Session = Depends(get_db)):
    blog = db.query(blog_model).filter(blog_model.id == id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with id {id} not found")
    blog.title = request.title
    blog.body = request.body
    db.commit()
    db.refresh(blog)
    return blog


# @app.put("/blog/{id}", status_code=status.HTTP_202_ACCEPTED)
# def update(id, request: Blog, db: Session = Depends(get_db)):
#     # Use .filter to specify the condition
#     query = db.query(blog_model).filter(blog_model.id == id)
#     updated_count = query.update(request.dict())
#     if updated_count == 0:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with id {id} not found")
#     db.commit()
#     db.refresh(query.first())
#     return query.first()



    #Not Working
# @app.put("/blog/{id}",status_code=status.HTTP_202_ACCEPTED)
# def update(id, request: Blog, db: Session = Depends(get_db)):
#     blog = db.query(blog_model).filter(blog_model.id == id)
#     if not blog.first():
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with id {id} not found")
#     blog.update(request.dict(), synchronize_session=False)
#     db.commit()
#     db.refresh(blog)
#     return blog



@app.post("/User", response_model=ShowUser, status_code=status.HTTP_201_CREATED,tags=["Users"])
def create_user(request: User, db: Session = Depends(get_db)):
    new_user = user_model(name=request.name, email=request.email, password=Hash.bcrypt(request.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@app.get("/User/{id}",  response_model=ShowUser,tags=["Users"])
def get_user(id:int, db: Session = Depends(get_db)):
    user = db.query(user_model).filter(user_model.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {id} not found")
    return user




@app.post('/login')
def login(request:OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):  #def login(request:Login = Depends(), db: Session = Depends(get_db)):
    user = db.query(user_model).filter(user_model.email == request.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Invalid Credentials")
    if not Hash.verify(user.password, request.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Incorrect password")
    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}