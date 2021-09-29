from datetime import datetime
import random
from typing import List
from fastapi import APIRouter, UploadFile, File, Form
import shutil
from schema import UploadVideo, GetVideo
from models import Video, User

video_router = APIRouter()


@video_router.post('/')
async def create_video(title: str = Form(...), description: str = Form(...), file: UploadFile = File(...)):
    info = UploadVideo(title=title, description=description)
    file.filename = f"{datetime.now().timestamp()}-{random.randint(1, 999999999999)}.mp4"
    with open(f'video/{file.filename}', 'wb') as buffer:
        shutil.copyfileobj(file.file, buffer)
    user = await User.objects.first()
    return await Video.objects.create(file=file.filename, user=user, **info.dict())


@video_router.get('/video/{vid_pk}', response_model=Video)
async def get_video(vid_pk: int):
    return await Video.objects.select_related('user').get(pk=vid_pk)
