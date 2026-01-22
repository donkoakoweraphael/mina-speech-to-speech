from transformers import SeamlessM4TModel, AutoProcessor
import torch
import torchaudio
import os

class SeamlessTranslator:
    def __init__(self, model_name="facebook/seamless-m4t-v2-large"):
        # Detect device
        self.device = "cuda:0" if torch.cuda.is_available() else "cpu"
        print(f"Loading SeamlessM4T model on {self.device}...")
        
        try:
            self.processor = AutoProcessor.from_pretrained(model_name)
            self.model = SeamlessM4TModel.from_pretrained(model_name).to(self.device)
            print("Model loaded successfully.")
        except Exception as e:
            print(f"Error loading model: {e}")
            raise e

    def predict(self, audio_path: str, src_lang: str, tgt_lang: str):
        """
        Performs S2ST (Speech-to-Speech) or S2T (Speech-to-Text).
        """
        # Load and resample audio
        audio_input, original_sample_rate = torchaudio.load(audio_path)
        
        # Resample to 16000Hz if needed (SeamlessM4T requires 16kHz)
        if original_sample_rate != 16000:
            resampler = torchaudio.transforms.Resample(orig_freq=original_sample_rate, new_freq=16000)
            audio_input = resampler(audio_input)
            
        audio_inputs = self.processor(audios=audio_input, sampling_rate=16000, return_tensors="pt").to(self.device)

        # Map simplified language codes to Seamless codes
        # ewe -> ewe, fr -> fra, en -> eng, mina (not supported directly, routed to external or Ewe)
        lang_map = {
            "ewe": "ewe",
            "fr": "fra",
            "en": "eng"
        }
        
        src_code = lang_map.get(src_lang)
        tgt_code = lang_map.get(tgt_lang)
        
        if not src_code or not tgt_code:
            raise ValueError(f"Language pair {src_lang}->{tgt_lang} not supported by SeamlessM4T internally.")

        # Generate translation
        # S2ST (Audio Output) + S2T (Text Output)
        output_tokens = self.model.generate(**audio_inputs, tgt_lang=tgt_code, generate_speech=True)
        
        # Decode Text
        translated_text = self.processor.decode(output_tokens[0].tolist()[0], skip_special_tokens=True)
        
        # Get Audio Array
        # waveform = output_tokens.waveform[0].cpu().numpy()
        # sample_rate = self.model.config.sampling_rate
        
        # Save Audio to temporary file or return bytes
        # For now, we return parts to be handled by the router
        
        audio_waveform = output_tokens[0].waveform.squeeze().cpu()
        sample_rate = self.model.config.sampling_rate

        return translated_text, audio_waveform, sample_rate
