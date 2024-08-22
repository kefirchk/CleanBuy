from fastapi import File, UploadFile, HTTPException, APIRouter, BackgroundTasks
from fastapi.responses import FileResponse
import os
import shutil
import uuid

from src.chat.files.file_repo import FileRepo
from src.s3 import s3_client

router = APIRouter(
    prefix="/files",
    tags=["Files"]
)

# Папка для временного хранения загруженных файлов перед отправкой на S3
TEMP_DIRECTORY = "temp_uploads/"

if not os.path.exists(TEMP_DIRECTORY):
    os.makedirs(TEMP_DIRECTORY)


@router.post("/upload_file")
async def upload_file(file: UploadFile = File(...)):
    # Генерируем уникальный идентификатор файла
    file_id = str(uuid.uuid4())
    temp_file_path = os.path.join(TEMP_DIRECTORY, f"{file_id}_{file.filename}")

    # Сохраняем файл временно на диск, чтобы затем загрузить его в S3
    with open(temp_file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Загружаем файл в S3
    await s3_client.upload_file(temp_file_path)

    # Удаляем временный файл
    os.remove(temp_file_path)

    return {
        "file_id": file_id,
        "filename": file.filename,
        "file_size": file.size,
        "file_type": file.content_type
    }


@router.get("/{file_id}")
async def get_file(file_id: str, background_tasks: BackgroundTasks):
    # Определяем имя файла в S3 по file_id (здесь file_id - это file_url без префикса '/files/')
    print(f"[INFO] Get file (id={file_id})")

    file_orm = await FileRepo.get_file_by_url(f'/files/{file_id}')
    file_name = file_orm.filename

    s3_filename = f'{file_id}_{file_name}'

    print(f"[INFO] S3_Filename={s3_filename} (file_id={file_id}) ")

    if not s3_filename:
        raise HTTPException(status_code=404, detail="File not found")

    # Загружаем файл из S3
    temp_file_path = os.path.join(TEMP_DIRECTORY, s3_filename)
    await s3_client.get_file(s3_filename, temp_file_path)

    print(f"[INFO] Temp_file_path={temp_file_path})")

    # Добавляем задачу удаления временного файла после ответа
    background_tasks.add_task(os.remove, temp_file_path)

    # Отправляем файл в ответе и удаляем временный файл
    response = FileResponse(
        path=temp_file_path,
        media_type=file_orm.file_type,
        filename=file_name
    )

    return response
