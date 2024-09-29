from fastapi import APIRouter,Depends,status,HTTPException
import schemas,database,models
from typing import List
from sqlalchemy.orm import Session

get_db = database.get_db

router = APIRouter(
    prefix='/user',
    tags=['User']
)


@router.post('/',response_model=schemas.ShowUser)
def create_user(request:schemas.User, db:Session = Depends(get_db)):
    # hashed_password = pwd_cxt.hash(request.password)
    # hashed_password = hash_password(request.password)
    new_user = models.User(name = request.name, email = request.email, password = request.password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return request


@router.get('/{id}',response_model=schemas.ShowUser)
def get_user(id:int,db:Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id==id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="not available")
    return user