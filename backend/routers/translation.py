from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from backend.services.seamless_model import SeamlessTranslator
import shutil
import os
import torchaudio
import uuid

router = APIRouter()

# Initialize model (lazy loading recommended in production, but here global for simplicity)
# We will initialize it inside the function or globally with a check to avoid slow startup blocking
# For this demo, let's keep it global but instantiated on first request or main startup?
# Better to instantiate once.
try:
    translator = SeamlessTranslator()
except Exception as e:
    print(f"Warning: Model could not be loaded immediately: {e}")
    translator = None

@router.post("/translate-audio")
async def translate_audio(
    file: UploadFile = File(...),
    source_lang: str = Form(...),
    target_lang: str = Form(...)
):
    if not translator:
        raise HTTPException(status_code=503, detail="Translation model is not loaded.")

    temp_path = ""
    output_audio_path = ""
    try:
        # Save temp file
        temp_dir = "temp_uploads"
        output_dir = "static/audio" # Ensure this exists/served
        os.makedirs(temp_dir, exist_ok=True)
        os.makedirs(output_dir, exist_ok=True)
        
        file_ext = file.filename.split('.')[-1]
        filename = f"{uuid.uuid4()}.{file_ext}"
        temp_path = os.path.join(temp_dir, filename)
        
        with open(temp_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
            
        # Call Model
        # TODO: Handle Mina routing here
        if source_lang == "mina" or target_lang == "mina":
             # Placeholder for connection to Mina 3rd party model
             return {
                "source_lang": source_lang,
                "target_lang": target_lang,
                "original_text": "[Audio Source Mina]",
                "translation_text": "Mina translation integration coming soon.",
                "audio_url": None
             }

        translated_text, audio_waveform, sample_rate = translator.predict(temp_path, source_lang, target_lang)
        
        # Save generated audio
        output_filename = f"trans_{filename}.wav" # Save as WAV
        output_audio_path = os.path.join(output_dir, output_filename)
        
        torchaudio.save(output_audio_path, audio_waveform.unsqueeze(0), sample_rate)
        
        # Generate URL
        # For localhost, we need to serve static files. 
        audio_url = f"http://localhost:8000/static/audio/{output_filename}"
        
        return {
            "source_lang": source_lang,
            "target_lang": target_lang,
            "original_text": "(Audio Processed)",
            "translation_text": translated_text,
            "audio_url": audio_url
        }

    except Exception as e:
        print(f"Error processing: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        # Cleanup input temp
        if os.path.exists(temp_path):
            os.remove(temp_path)

@router.get("/languages")
async def get_languages():
    return [
        {"code": "mina", "name": "Mina", "type": "audio-only"},
        {"code": "ewe", "name": "Éwé", "type": "audio-text"},
        {"code": "fr", "name": "Français", "type": "audio-text"},
        {"code": "en", "name": "English", "type": "audio-text"},
    ]
