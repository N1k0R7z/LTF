from fastapi import FastAPI, UploadFile, File
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import uvicorn
import os

app = FastAPI()

SAVE_DIR = "./uploads"
os.makedirs(SAVE_DIR, exist_ok=True)

@app.get("/", response_class=HTMLResponse)
async def home():
    with open("./templates/index.html", "r") as f:
        return f.read()

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    file_path = os.path.join(SAVE_DIR, file.filename)
    with open(file_path, "wb") as buffer:
        while chunk := await file.read(1024 * 1024):
            buffer.write(chunk)
    return {"status": "ok", "filename": file.filename}
    
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=7070)
