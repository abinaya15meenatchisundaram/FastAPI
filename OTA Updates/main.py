from fastapi import FastAPI, Form, UploadFile, File, HTTPException, Depends
from fastapi.responses import FileResponse
import os

app = FastAPI()

# Hardcoded users: username -> {"password": ..., "role": ...}
USERS = {
    "Abinaya": {"password": "mypassword", "role": "uploader"},
    "pranav": {"password": "pranavpassword", "role": "downloader"}
}

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# ---------------- AUTH ----------------
def authenticate(username: str = Form(...), password: str = Form(...)):
    user = USERS.get(username)
    if not user or user["password"] != password:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return {"username": username, "role": user["role"]}

# ---------------- ENDPOINTS ----------------
@app.post("/upload")
async def upload_file(
    file: UploadFile = File(...),
    user=Depends(authenticate)
):
    if user["role"] != "uploader":
        raise HTTPException(status_code=403, detail="You are not allowed to upload files")

    path = os.path.join(UPLOAD_DIR, file.filename)
    with open(path, "wb") as f:
        f.write(await file.read())
    return {"message": f"File '{file.filename}' uploaded by {user['username']}"}


@app.post("/download")
async def download_file(
    filename: str = Form(...),
    user=Depends(authenticate)
):
    if user["role"] != "downloader":
        raise HTTPException(status_code=403, detail="You are not allowed to download files")

    path = os.path.join(UPLOAD_DIR, filename)
    if not os.path.exists(path):
        raise HTTPException(status_code=404, detail="File not found")

    return FileResponse(path, filename=filename)
