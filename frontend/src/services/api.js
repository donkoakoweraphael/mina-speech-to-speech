const API_URL = 'http://localhost:8000';

export const translateAudio = async (audioBlob, sourceLang, targetLang) => {
    const formData = new FormData();
    formData.append('file', audioBlob, 'audio.webm');
    formData.append('source_lang', sourceLang);
    formData.append('target_lang', targetLang);

    try {
        const response = await fetch(`${API_URL}/translate-audio`, {
            method: 'POST',
            body: formData,
        });

        if (!response.ok) {
            throw new Error(`API Error: ${response.statusText}`);
        }

        return await response.json();
    } catch (error) {
        console.error("Translation error:", error);
        throw error;
    }
};
