from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from gtts import gTTS
import os
from fastapi.responses import FileResponse, JSONResponse

app = FastAPI()

# CORS Middleware Add Kiya
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Specific domains ke liye ["https://toolart.site"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def home():
    return {"message": "FastAPI Text-to-Speech API is running with multiple languages & download feature!"}

@app.get("/text-to-speech/")
async def text_to_speech(text: str, lang: str = Query(default="en", description="Language code (e.g., 'en' for English, 'hi' for Hindi)")):
    try:
        file_path = "output.mp3"
        tts = gTTS(text=text, lang=lang)
        tts.save(file_path)

        return JSONResponse(content={"message": "Speech generated successfully!", "download_url": "/download-audio"})
    
    except Exception as e:
        return {"error": str(e)}

@app.get("/download-audio")
async def download_audio():
    file_path = "output.mp3"
    if os.path.exists(file_path):
        return FileResponse(file_path, media_type="audio/mpeg", filename="speech.mp3")
    return {"error": "File not found"}
