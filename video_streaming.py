from fastapi import HTTPException, Request
from fastapi.responses import StreamingResponse, FileResponse
import os
import json


DATA_DIR = {
    'body': './body',
    'leg': './leg_data',
    'speed': './speed_data',
    'torso': './torso'
}


async def video_stream(request: Request, category: str, video_name: str):
    if category not in DATA_DIR:
        raise HTTPException(status_code=404, detail="Category not found")
    
    video_directory = os.path.join(DATA_DIR[category], 'videos')
    video_path = os.path.join(video_directory, video_name)
    
    if not os.path.isfile(video_path):
        raise HTTPException(status_code=404, detail="Video not found")

    file_size = os.path.getsize(video_path)
    range_header = request.headers.get("Range")
    
    if range_header:
        start, end = 0, file_size - 1
        range_match = re.match(r"bytes=(\d+)-(\d*)", range_header)
        if range_match:
            start = int(range_match.group(1))
            end = int(range_match.group(2)) if range_match.group(2) else file_size - 1

        if start >= file_size or end >= file_size or start > end:
            raise HTTPException(status_code=416, detail="Requested Range Not Satisfiable")

        content_length = end - start + 1
        headers = {
            'Content-Range': f'bytes {start}-{end}/{file_size}',
            'Accept-Ranges': 'bytes',
            'Content-Length': str(content_length),
            'Content-Type': 'video/mp4',
        }

        def file_iterator(file_path, start, content_length):
            with open(file_path, 'rb') as video_file:
                video_file.seek(start)
                remaining_bytes = content_length
                while remaining_bytes > 0:
                    chunk_size = min(remaining_bytes, 2048)
                    chunk = video_file.read(chunk_size)
                    if not chunk:
                        break
                    remaining_bytes -= chunk_size
                    yield chunk

        return StreamingResponse(file_iterator(video_path, start, content_length), status_code=206, headers=headers)
    else:
        return StreamingResponse(video_path, media_type='video/mp4')
        # return FileResponse(video_path, media_type='video/mp4')