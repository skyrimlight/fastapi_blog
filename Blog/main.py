from typing import List

from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from Blog import crud, schemas
from Blog.database import engine, Base, SessionLocal
# from Blog.models import City, Data
from fastapi.templating import Jinja2Templates

application = APIRouter()
templates = Jinja2Templates(directory='./Blog/templates')
Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@application.post('/create_city', response_model=schemas.CreateCity)
def create_city(city: schemas.CreateCity, db: Session = Depends(get_db)):
    # db_city = crud.get_city_by_name(db=db, name=city.province)
    # if not db_city:
    #     crud.create_city(db=db, city=city)
    #     return {'msg': "添加成功"}
    # raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='城市已存在')
    db_city = crud.get_city_by_name(db, name=city.province)
    if db_city:
        raise HTTPException(status_code=400, detail="City already registered")
    return crud.create_city(db=db, city=city)


@application.get('/get_city/{city}', response_model=schemas.CreateCity)
def get_city(city: str, db: Session = Depends(get_db)):
    db_city = crud.get_city_by_name(db=db, name=city)
    if db_city is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='未找到此城市')
    return db_city


@application.get('/get_cities', response_model=List[schemas.ReadCity])
def get_cities(skip: int = 0, limit: int = 5, db: Session = Depends(get_db)):
    cities = crud.get_cities(db=db, skip=skip, limit=limit)
    return cities


@application.post('/create_data', response_model=schemas.CreateData)
def create_data_for_city(city: str, data: schemas.CreateData, db: Session = Depends(get_db)):
    db_city = crud.get_city_by_name(db=db, name=city)
    data = crud.create_city_data(db=db, data=data, city=db_city)
    return data


# @application.get('/get_data')
# def get_data(city: str = None, db: Session = Depends(get_db), skip: int = 0, limit: int = 0):
#     data = crud.get_data(db=db, skip=skip, limit=limit, city=city)
#     return data

@application.get("/get_data")
def get_data(city: str = None, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    data = crud.get_data(db, city=city, skip=skip, limit=limit)
    return data


@application.get('/')
def Blog(request: Request, city: str = None, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    data = crud.get_data(db, city=city, skip=skip, limit=limit)
    return templates.TemplateResponse("home.html", {
        "request": request,
        "data": data,
        "sync_data_url": "/Blog/sync_Blog_data/jhu"
    })
