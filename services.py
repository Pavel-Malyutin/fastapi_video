from pathlib import Path

import aiofiles
import shutil

import ormar.exceptions
from fastapi import UploadFile
from uuid import uuid4
from fastapi import BackgroundTasks, UploadFile, HTTPException, Request
from schema import UploadVideo
from models import Video, User


async def save_video(
        user: User,
        file: UploadFile,
        title: str,
        description: str,
        background_tasks: BackgroundTasks
):
    file.filename = f"{user.id}-{uuid4()}.mp4"
    file_name = file.filename
    if file.content_type == 'video/mp4':
        # background_tasks.add_task(write_video, file.filename, file)
        await write_video(file_name, file)
    else:
        raise HTTPException(status_code=418, detail="isn't mp4")
    info = UploadVideo(title=title, description=description)
    return await Video.objects.create(file=file_name, user=user, **info.dict())


async def write_video(file_name: str, file: UploadFile):
    async with aiofiles.open(f'video/{file_name}', 'wb') as buffer:
        data = await file.read()
        await buffer.write(data)
    # with open(f'video/{file_name}', 'wb') as buffer:
    #     shutil.copyfileobj(file.file, buffer)


async def open_file(request: Request, video_pk: int) -> tuple:
    try:
        file = await Video.objects.get(pk=video_pk)
    except ormar.exceptions.NoMatch:
        raise HTTPException(status_code=404)
    path = Path(file.dict().get('file'))
    file = path.open('rb')
    file_size = path.stat().st_size

    content_length = file_size
    status_code = 200
    headers = {}
    content_range = request.headers.get('range')

    if content_range is not None:
        content_range = content_range.strip().lower()
        content_ranges = content_range.split('=')[-1]
        range_start = range_end, *_ = map(str.strip, (content_ranges + '-').split('-'))
        range_start = max(0, int(range_start)) if range_start else 0
        range_end = min(file_size - 1, int(range_end)) if range_end else file_size - 1
        content_length = (range_end - range_start) + 1
        file = ranged(file, start=range_start, end=range_end + 1)
        status_code = 206
        headers['Content-Range'] = f'bytes {range_start}-{range_end}/{file_size}'

    return file, status_code, content_length, headers

