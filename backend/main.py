from fastapi import FastAPI, UploadFile, File, Form
from pydantic import BaseModel
from backend.pipeline import run_pdf_pipeline, run_youtube_pipeline
import shutil
import os

app = FastAPI(title="Multi-Source AI Chatbot API")

UPLOAD_DIR = "data/pdf"
os.makedirs(UPLOAD_DIR, exist_ok=True)


# ── PDF Chat ──────────────────────────────────────────

@app.post("/chat/pdf")
async def chat_pdf(
    file: UploadFile = File(...),
    question: str = Form(...),
    chat_history: str = Form("")
):
    try:
        file_path = os.path.join(UPLOAD_DIR, file.filename)

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        answer, docs = run_pdf_pipeline(file_path, question, chat_history)

        return {
            "answer": answer,
            "sources": [doc.page_content[:300] for doc in docs[:3]]
        }

    except Exception as e:
        return {"error": str(e)}


# ── YouTube Chat ──────────────────────────────────────

class YouTubeRequest(BaseModel):
    video_id: str
    question: str
    chat_history: str = ""


@app.post("/chat/youtube")
def chat_youtube(request: YouTubeRequest):
    try:
        answer, docs = run_youtube_pipeline(
            video_id=request.video_id,
            query=request.question,
            chat_history=request.chat_history
        )

        return {
            "answer": answer,
            "sources": [doc.page_content[:300] for doc in docs[:3]]
        }

    except Exception as e:
        return {"error": str(e)}
