from fastapi import FastAPI, Path
from typing import Optional
from pydantic import BaseModel

app = FastAPI()



stu = {
    1 : {
        "name" : "abc",
        "phn" : 123
    }
}

class blog(BaseModel):
    title : str
    body : str
    published : Optional[bool]




@app.get("/")
def index():
    return {"name":"sai srinivas"}

@app.post('/blog')
def create(request:blog):
    return {'data': f"Blog is created with {request.title}"}


@app.get("/get_student/{stu_id}")
def get_stud(stu_id:int = Path(description="enter id",gt=0)):
    return stu[stu_id]