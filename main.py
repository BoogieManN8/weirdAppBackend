from fastapi import FastAPI, HTTPException, Response, File, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, StreamingResponse
from pydantic import BaseModel
from typing import List
import json
import os
from database import *
from UserModel import *
from video_streaming import video_stream, DATA_DIR


app = FastAPI()

BASE_DIR = './'
DATA_DIR = {
    'body': os.path.join(BASE_DIR, 'body'),
    'leg': os.path.join(BASE_DIR, 'leg_data'),
    'speed': os.path.join(BASE_DIR, 'speed_data'),
    'torso': os.path.join(BASE_DIR, 'torso')
}

app.mount("/videos", StaticFiles(directory="body/videos"), name="videos")
app.mount("/images", StaticFiles(directory="body/images"), name="images")

app.mount("/videos", StaticFiles(directory="leg_data/videos"), name="videos")
app.mount("/images", StaticFiles(directory="leg_data/images"), name="images")

app.mount("/videos", StaticFiles(directory="speed_data/videos"), name="videos")
app.mount("/images", StaticFiles(directory="speed_data/images"), name="images")

app.mount("/videos", StaticFiles(directory="torso/videos"), name="videos")
app.mount("/images", StaticFiles(directory="torso/images"), name="images")
# for category, path in DATA_DIR.items():
#     app.mount(f"/videos/{category}", StaticFiles(directory=f"{path}/videos"), name=f"videos_{category}")
#     app.mount(f"/images/{category}", StaticFiles(directory=f"{path}/images"), name=f"images_{category}")


async def read_json(category: str):
    with open(os.path.join(DATA_DIR[category], 'data.json'), 'r') as f:
        return json.load(f)


db_host = "localhost"
db_user = "root"
db_password = ""

db = "WeirdWorkoutApp"
db_manager = DatabaseManager(db_host,db_user,db_password,db)


@app.post("/users/")
def create_user(user: UserCreate):
    db_manager.create_user(user.id, user.isGuest, user.isPremium, user.userToken, user.userLevel)
    return {"message": "User created successfully"}

@app.get("/users/{user_id}")
def read_user(user_id: str):
    user = db_manager.read_user(user_id)
    if user:
        user_dict = {
            "id": user[0],
            "isGuest": user[1],
            "isPremium": user[2],
            "userToken": user[3],
            "userLevel": user[4]
        }
        return user_dict
    raise HTTPException(status_code=404,detail="User with id {user_id} was not found")

@app.put("/users/{user_id}")
def update_user(user_id: str, user: UserUpdate):
    db_manager.update_user(user_id, **user.dict(exclude_none=True))
    updated_user = db_manager.read_user(user_id)
    if updated_user:
        user_dict = {
            "id": updated_user[0],
            "isGuest": updated_user[1],
            "isPremium": updated_user[2],
            "userToken": updated_user[3],
            "userLevel": updated_user[4]
        }
        return user_dict
    
    raise HTTPException(status_code=404, detail="User not found after update")

@app.delete("/users/{user_id}")
def delete_user(user_id: str):
    db_manager.delete_user(user_id)
    return {"message": "deleted succesfully"}


@app.get("/data/body", response_model=List[dict])
async def get_body_data():
    return await read_json('body')

@app.get("/data/leg", response_model=List[dict])
async def get_leg_data():
    return await read_json('leg')

@app.get("/data/speed", response_model=List[dict])
async def get_speed_data():
    return await read_json('speed')

@app.get("/data/torso", response_model=List[dict])
async def get_torso_data():
    return await read_json('torso')

@app.get("/data/all", response_model=List[dict])
async def get_all_data():
    all_data = []
    for category in DATA_DIR:
        all_data.extend(await read_json(category))
    return all_data



@app.get("/videos/{category}/{video_name}")
async def video_stream(request: Request, category: str, video_name: str):
    print("\n\n\nTEST\n\n\n\n")
    return await video_stream(request, category, video_name)


@app.on_event("shutdown")
def shutdown_event():
    db_manager.close()
    

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
    

"""
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE
)
"""