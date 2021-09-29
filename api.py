from typing import List
from fastapi import APIRouter, UploadFile, File, Form
import shutil
from schema import UploadVideo, GetVideo, User

video_router = APIRouter()


@video_router.post('/')
async def upload_video(title: str = Form(...), description: str = Form(...), file: UploadFile = File(...)):
    info = UploadVideo(title=title, description=description)
    with open(f'video/test12.mp4', 'wb') as buffer:
        shutil.copyfileobj(file.file, buffer)
    return {'file_name': file.filename, 'info': info}


@video_router.post('/img')
async def upload_image(files: List[UploadFile] = File(...)):
    for img in files:
        with open(f'img/test12.mp4', 'wb') as buffer:
            shutil.copyfileobj(img.file, buffer)
    return {'file_name': 'ok'}


@video_router.get('/video')
async def get_video():
    user = {
        'id': 1123,
        'name': 'qwertyy'
    }
    video = {
        'title': 'test',
        'description': 'Deesc'
    }
    return GetVideo(user=user, video=video)
