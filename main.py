from datetime import datetime, timedelta, time

from uuid import UUID

from fastapi import FastAPI, Body, Path, Query, File, UploadFile, Form, Depends, Header
from enum import Enum
from typing import Optional

from fastapi.exceptions import RequestValidationError, HTTPException
from pydantic import HttpUrl, BaseModel, Field
from starlette.requests import Request
from starlette.responses import JSONResponse, PlainTextResponse

app = FastAPI()
"""
@app.get("/",description="this is get route from fast api")
async def root():
    return {"message": "Hello World"}


@app.post("/")
async def post():
    return {"message": "Hello World"}

@app.put("/")
async def put():
    return {"message": "Hello World"}

@app.get("/user")
async def list_user():
    return {"message": "List of items"}

@app.get("/user/me")
async def list_user():
    return {"message": "it is myself user"}

@app.get("/user/{user_id}")
async def get_user(user_id:str):
    return {"message": user_id}

class FoodEnum(str, Enum):
    fruits = "fruits",
    vegetables = "vegetables"
    dairy = "dairy"

@app.get("/foods/{food_name}")
async def get_food(food_name:FoodEnum):
    if food_name == FoodEnum.vegetables:
        return {"food_name" : food_name, "message":"you are healthy"}

    if food_name.value == "fruits" :
        return {"food_name" : food_name, "message":"Nice Pracctice to be healthy"}

    return {"food_name" : food_name, "message":" Pracctice to be healthy"}
    
"""

"""
class Image(BaseModel):
    url:HttpUrl
    name:str

class Item(BaseModel):
    name:str
    description :  str | None = None
    price : float
    tax : float | None = None
    Tags: set[str] = set()
    image: list[Image] | None = None

class Offer(BaseModel):
    name:str
    description: str | None = None
    price:float
    items : list[Item]

@app.put("/items/{item_id}")
async def update_item(item_id : int , item :Item):
    results = {"item_id": item_id, "item": item}
    return results

@app.post("/images/multiple")
async def create_multile_images(images:list(Image)= Body(...,embed=True)):
    return  images
    


"""

"""
class Item(BaseModel):
    name: str = Field(...,example="Me")
    description: str = Field(...,example="Very Good Description")
    price : float = Field(...,example=16.5)
    tax : float | None = Field(...,example=2.5)


@app.put("/items/{item_id}")
async  def update_item(item_id:int, item:Item):
    results = {"item_id":item_id, "item":item}
    return results
    



class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price : float
    tax : float | None = None

@app.Post("/items")
async def create_item(item:Item):
    item_dict = item.dict()
    if item.tax:
        price_with_tax = item.price + item.tax
        item_dict.update({"prictice_with_tax": price_with_tax})
    return item_dict

@app.put("/items/{item_id}")
async def create_item_with_put(item_id:int, item:Item,q:str | None = None):
    result = {"item_id":item_id,**item.dict()}
    if q:
        result.update({"q":q})
    return result

@app.get("/items_validation/{item_id}")
async def reading_item_validation(
        item_id : int  = Path(..., title="The id of the item", max_length=100 ),
        q: str | None  = Query(None, alias="item-query")
):
    results={"item_id":item_id}
    if q:
        q.update({"q":q})
    return results


"""
"""@app.put("item/{item_id}")
async def read_item(
  item_id : UUID,
  start_date : datetime | None =  Body(None),
  end_date :    datetime | None = Body(None),
  repeat_at : time | None = Body(None),
  process_after :  timedelta |  None = Body(None)
):
    start_process = start_date + process_after
    duration = end_date - start_process
    return{
        "item_id": item_id,
        "start_date": start_date,
        "end_date": end_date,
        "repeat_at": repeat_at,
        "process_after": process_after,
        "start_process": start_process,
        "duration": duration

    }
"""



"""
class UserBase(BaseModel):
    username: str
    email: str | None = None
    full_name: str | None = None


class UserIn(UserBase):
    password:str

class Userout(UserBase):
    pass

@app.post("/users/", response_model=Userout)
async def create_user(user: UserIn):
    return user


"""

"""
@app.post("/files")
async def create_file(
    file: bytes = File(...),
    fileb: UploadFile = File(...),
    token: str = Form(...),
    hello: str = Body(...),
):
    return {
        "file_size": len(file),
        "token": token,
        "hello": hello,
        "File-content-type": fileb.content_type,
    }
"""
"""
class UnicornException(Exception):
    def __init__(self, name: str):
        self.name = name

@app.exception_handler(UnicornException)
async def uncorn_exception_handler(request : Request, exc: UnicornException):
    return JSONResponse(status_code=418, content={"message": f"Hello {exc.name}"})

@app.get("/unicorn/{name}")
async def read_unicorns(name: str):
    if name == "yolo":
        raise UnicornException(name=name)
    return {"unicorn_name": name}

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request : Request, exc: RequestValidationError):
    return PlainTextResponse(status_code=400, content=exc.errors())


"""
"""

fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]


class CommonQueryParams:
    def __init__(self, q: str | None = None, skip: int = 0, limit: int = 100):
        self.q = q
        self.skip = skip
        self.limit = limit


@app.get("/items/{item_id}")
async def read_items(commons = Depends(CommonQueryParams)):
    response = {}
    if commons.q:
        response.update({"q": commons.q})
    items = fake_items_db[commons.skip : commons.skip + commons.limit]
    response.update({"items": items})
    return response
"""

async def verify_token(x_token: str = Header(...)):
    if x_token != "fake-super-secret-token":
        raise HTTPException(status_code=400, detail="X-Token header invalid")


async def verify_key(x_key: str = Header(...)):
    if x_key != "fake-super-secret-key":
        raise HTTPException(status_code=400, detail="X-Key header invalid")
    return x_key

@app.get("/items/", dependencies=[Depends(verify_token), Depends(verify_key)])
async def read_items(blah : str = Depends(verify_token), blah2 : str = Depends(verify_key)):
    return [{"item": "Foo"}, {"item": "Bar"}]
