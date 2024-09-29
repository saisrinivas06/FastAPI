from fastapi import APIRouter,Depends,status,HTTPException
import schemas,database,models
from typing import List
from sqlalchemy.orm import Session

get_db = database.get_db

router = APIRouter(
    prefix='/blog',
    tags=['Blog']
)


@router.get('/',response_model=List[schemas.ShowBlog])
def all(db:Session = Depends(database.get_db)):
    blogs = db.query(models.Blog).all()
    return blogs


@router.post('/',status_code=status.HTTP_201_CREATED)
def create(request :schemas.Blog, db:Session= Depends(get_db)):
    new_blog = models.Blog(title=request.title, body = request.body)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


@router.get('/{id}',status_code=status.HTTP_201_CREATED,response_model=schemas.ShowBlog)
def show(id, db:Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id==id).first()
    if not blog:
        # response.status_code=status.HTTP_404_NOT_FOUND
        # return {'details':'not available'}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail='not available')
    return blog


@router.delete('/{id}',status_code=status.HTTP_204_NO_CONTENT)
def destroy(id,db:Session = Depends(get_db)):
    db.query(models.Blog).filter(models.Blog.id==id).delete(synchronize_session=False)
    db.commit()
    return {'done'}



@router.put('/{id}',status_code=status.HTTP_202_ACCEPTED)
def update(id, request:schemas.Blog,db:Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="not available")
    blog.title = request.title
    blog.body = request.body
    db.commit()
    return "updated"