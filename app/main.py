from fastapi import FastAPI, UploadFile, Form, File
from fastapi.responses import StreamingResponse
from typing import Annotated
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from models.models import save_mp3, save_user, get_mp3
from tools.audio import convert_to_mp3, generate_link
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
    """create_user gets username from POST request body and returns it's id and token"""
    result = save_user(user_data.username)
    
    if result["error"] != "":
        status = 409

    return JSONResponse(result, status_code=status)

@app.post("/upload/audio")
async def upload_audio(
    user_token: Annotated[str, Form()],
    wav_file: Annotated[UploadFile, File()]
):
    """upload_audio gets user_token and wav_file in body of POST request, returns link to download mp3 audio file"""
    if not user_token:
        return JSONResponse("No user token", 400)
    if not wav_file:
        return JSONResponse("No file sent", 400)

    content = wav_file.file.read()
    mp3_file = convert_to_mp3(io.BytesIO(content))
    result = save_mp3(user_token, mp3_file.read())
    if result["error"] != "":
        return JSONResponse(result, 409)

    link = generate_link(result["audio_id"], result["user_id"])

    return {"id": result["audio_id"], "link": link}

@app.get("/record")
async def get_record(id: int, user: int):
    """get_record parse audio_id and user_id from link query, returns audio file was saved with this parameters"""
    result = get_mp3(audio_id=id, user_id=user)
    if result["error"] != "":
        return JSONResponse(result["error"], 409)
    
    audio = result["raw_audio"]
    response = StreamingResponse(io.BytesIO(audio), media_type="audio/mpeg")
    response.headers["Content-Disposition"] = f"attachment; filename=audio_{id}"

    return response