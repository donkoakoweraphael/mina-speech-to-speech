import React, { useState } from 'react';
import LanguageSelector from './components/LanguageSelector';
import AudioRecorder from './components/AudioRecorder';

// Placeholder for the actual backend API call
// In a real application, this would be an API utility function
const translateAudio = async (audioBlob, sourceLang, targetLang) => {
  console.log(`Translating from ${sourceLang} to ${targetLang}`);
  console.log("Audio Blob:", audioBlob);

  // Simulate API call
  return new Promise(resolve => {
    setTimeout(() => {
      resolve({
        translation_text: "Ceci est une traduction simulée depuis l'audio source. L'intégration réelle viendra bientôt.",
        audio_url: "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3" // Example audio URL
      });
    }, 2000);
  });
};

function App() {
  const [sourceLang, setSourceLang] = useState('ewe');
  const [targetLang, setTargetLang] = useState('fr');
  const [sourceAudio, setSourceAudio] = useState(null);
  const [translatedText, setTranslatedText] = useState('');
  const [translatedAudio, setTranslatedAudio] = useState(null);
  const [isProcessing, setIsProcessing] = useState(false);

  // Handle translation via Backend API
  const handleRecordingComplete = async (audioBlob) => {
    setSourceAudio(URL.createObjectURL(audioBlob));
    setIsProcessing(true);
    setTranslatedText(""); 
    setTranslatedAudio(null);

    try {
      const result = await translateAudio(audioBlob, sourceLang, targetLang);
      setTranslatedText(result.translation_text);
      if (result.audio_url) {
        setTranslatedAudio(result.audio_url);
        // Auto-play
        const audio = new Audio(result.audio_url);
        audio.play().catch(e => console.log("Auto-play blocked", e));
      }
    } catch (error) {
      console.error("Translation failed:", error);
      setTranslatedText("Error during translation. Please check backend.");
    } finally {
      setIsProcessing(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-slate-200 flex flex-col items-center py-10 px-4">
      <header className="mb-10 text-center">
        <h1 className="text-4xl font-black text-transparent bg-clip-text bg-gradient-to-r from-primary to-secondary mb-2">
          MinaTranslate
        </h1>
        <p className="text-slate-500 font-medium">Bridging languages, connecting people.</p>
      </header>

      <main className="w-full max-w-6xl flex flex-col md:flex-row gap-6">
        {/* Source Column (Left) */}
        <div className="flex-1 glass-panel p-6 flex flex-col gap-6">
          <div className="border-b border-gray-100 pb-4">
            <LanguageSelector
              label="Translate from"
              selected={sourceLang}
              onChange={setSourceLang}
            />
          </div>

          <div className="flex-1 flex flex-col items-center justify-center min-h-[300px]">
            {/* If Mina then only Audio allowed, if Ewe/Fr/En allow text toggle? For now Input is Audio predominantly */}
            <AudioRecorder onRecordingComplete={handleRecordingComplete} />

            {sourceAudio && (
              <div className="mt-6 w-full bg-slate-50 p-4 rounded-xl">
                <p className="text-xs font-bold text-slate-400 mb-2 uppercase">Your Input</p>
                <audio controls src={sourceAudio} className="w-full" />
              </div>
            )}
          </div>
        </div>

        {/* Swap Button (Decorational) */}
        <div className="flex items-center justify-center -my-3 md:-mx-3 z-10">
          <button className="bg-white p-3 rounded-full shadow-lg text-slate-400 hover:text-primary hover:scale-110 transition-all">
            <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 7h12m0 0l-4-4m4 4l-4 4m0 6H4m0 0l4 4m-4-4l4-4" />
            </svg>
          </button>
        </div>

        {/* Target Column (Right) */}
        <div className="flex-1 glass-panel p-6 flex flex-col gap-6">
          <div className="border-b border-gray-100 pb-4">
            <LanguageSelector
              label="Translate to"
              selected={targetLang}
              onChange={setTargetLang}
              excludeMina={true} // Output to Mina is Audio only, handled internally? User said "Mina...audio en sortie disponible"
            />
          </div>

          <div className="flex-1 flex flex-col min-h-[300px] relative">
            {isProcessing ? (
              <div className="absolute inset-0 flex items-center justify-center bg-white/50 backdrop-blur-sm z-10 rounded-xl">
                <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary"></div>
              </div>
            ) : null}

            <textarea 
              readOnly
              className="w-full h-full bg-slate-50 border-none rounded-xl p-6 text-xl text-slate-700 resize-none focus:ring-0"
              placeholder="Translation will appear here..."
              value={translatedText}
            />
            
            <div className="mt-4 flex flex-col gap-2">
               {translatedAudio && (
                 <audio controls src={translatedAudio} className="w-full" />
               )}
               <div className="flex justify-between items-center">
                   <button 
                     className="flex items-center gap-2 text-slate-500 hover:text-primary font-medium transition-colors"
                     onClick={() => translatedAudio && new Audio(translatedAudio).play()}
                   >
                     <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                       <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM9.555 7.168A1 1 0 008 8v4a1 1 0 001.555.832l3-2a1 1 0 000-1.664l-3-2z" clipRule="evenodd" />
                     </svg>
                     Replay Audio
                   </button>
                   {/* Translate button removed as flow is auto on record stop, or we can keep it for text-only input later */}
               </div>
            </div>
          </div>
        </div>
      </main>

      <footer className="mt-12 text-slate-400 text-sm">
        <p>&copy; 2026 Mina Project Team</p>
      </footer>
    </div>
  );
}

export default App;
