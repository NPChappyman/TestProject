# api.py

from pathlib import Path
import shutil

from fastapi import FastAPI, File, UploadFile

from services.pipeline import run_pipeline

app = FastAPI(title="UMUX ETL")


UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

@app.post("/process")
async def process(files: list[UploadFile] = File(...)):

    paths = []

    for file in files:

        path = UPLOAD_DIR / file.filename

        with open(path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        paths.append(str(path))

    result = run_pipeline(paths)

    return {
        "valid": result["valid"],
        "invalid": result["invalid"],
        "rejected_share": round(result["rejected_share"] * 100, 2),
    }