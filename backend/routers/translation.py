from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from typing import Optional
from services.audio_processor import AudioProcessor
import shutil
import os
import random

router = APIRouter()
audio_processor = AudioProcessor()

# Mock translations for demo
MOCK_TRANSLATIONS = {
    "ewe": {
        "fr": "Ceci est une traduction simulée de l'Éwé vers le Français.",
        "en": "This is a simulated translation from Ewe to English."
    },
    "mina": {
        "fr": "Traduction Mina vers Français (Mock).",
        "en": "Mina to English translation (Mock)."
    },
    "fr": {
        "ewe": "Ewe translation mock text.",
        "mina": "Mina translation mock text." # Should accept text/audio in but Mina out is audio only usually.
    }
}

@router.post("/translate-audio")
async def translate_audio(
    file: UploadFile = File(...),
    source_lang: str = Form(...),
    target_lang: str = Form(...)
):
    try:
        # Save temp file
        temp_dir = "temp_uploads"
        os.makedirs(temp_dir, exist_ok=True)
        temp_path = os.path.join(temp_dir, file.filename)
        
        with open(temp_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
            
        # Process audio (convert/validate)
        # processed_path = await audio_processor.convert_audio(temp_path)
        
        # Mock Logic
        translation_text = MOCK_TRANSLATIONS.get(source_lang, {}).get(target_lang, "Translation unavailable for this pair.")
        
        # Return result
        return {
            "source_lang": source_lang,
            "target_lang": target_lang,
            "original_text": "(Transcription simulée de l'audio)",
            "translation_text": translation_text,
            "audio_url": None # TODO: Return URL to synthesized audio (TTS)
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        # Cleanup
        if 'temp_path' in locals() and os.path.exists(temp_path):
            os.remove(temp_path)

@router.get("/languages")
async def get_languages():
    return [
        {"code": "mina", "name": "Mina", "type": "audio-only"},
        {"code": "ewe", "name": "Éwé", "type": "audio-text"},
        {"code": "fr", "name": "Français", "type": "audio-text"},
        {"code": "en", "name": "English", "type": "audio-text"},
    ]
