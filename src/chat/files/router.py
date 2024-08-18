from fastapi import File, UploadFile, HTTPException, APIRouter
from fastapi.responses import FileResponse
import os
import shutil
import uuid


router = APIRouter(
    prefix="/files",
    tags=["Files"]
)

# Папка для хранения загруженных файлов
UPLOAD_DIRECTORY = "uploads/"

if not os.path.exists(UPLOAD_DIRECTORY):
    os.makedirs(UPLOAD_DIRECTORY)


@router.post("/upload_file")
async def upload_file(file: UploadFile = File(...)):
    file_id = str(uuid.uuid4())
    file_path = os.path.join(UPLOAD_DIRECTORY, f"{file_id}_{file.filename}")

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return {
        "file_id": file_id,
        "filename": file.filename,
        "file_path": file_path,
        "file_size": file.size,
        "file_type": file.content_type
    }


@router.get("/{file_id}")
async def get_file(file_id: str):
    file_path = None
    for file in os.listdir(UPLOAD_DIRECTORY):
        if file.startswith(file_id):
            file_path = os.path.join(UPLOAD_DIRECTORY, file)
            break

    if file_path and os.path.exists(file_path):
        return FileResponse(file_path)

    raise HTTPException(status_code=404, detail="File not found")
