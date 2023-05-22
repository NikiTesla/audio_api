from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
from tempfile import NamedTemporaryFile
from pydantic import BaseModel
from models.models import Audio, User, save_mp3, save_user
from tools.audio import convert_to_mp3
import requests
import json
import io

app = FastAPI(
    title="audio api"
)

class UserCreateRequest(BaseModel):
    username: str


@app.get("/")
def index():
    return "hello, world"

@app.post("/create_user")

async def create_user(user_data: UserCreateRequest):
    msg = save_user(user_data.username)
    
    if msg["error"] != "":
        status = 409
    else:
        status = 200

    return JSONResponse(msg, status_code=status)

@app.post("/upload/audio")
async def upload_audio(wav_file: bytes = File(...)):

    if not wav_file:
        return JSONResponse("No file sent", 400)

    wav_io = io.BytesIO(wav_file)
    mp3_file = convert_to_mp3(wav_io)
    mp3_data = mp3_file.read()

    id = -1
    link = "lol"

    return {"mp3_data": mp3_data, "id": id, "link": link}

