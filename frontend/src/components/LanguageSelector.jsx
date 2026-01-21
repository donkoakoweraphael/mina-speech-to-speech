import React from 'react';

const languages = [
    { code: 'mina', name: 'Mina', type: 'audio-only' },
    { code: 'ewe', name: 'Éwé', type: 'audio-text' },
    { code: 'fr', name: 'Français', type: 'audio-text' },
    { code: 'en', name: 'English', type: 'audio-text' },
];

const LanguageSelector = ({ selected, onChange, label, excludeMina = false }) => {
    const availableLanguages = excludeMina
        ? languages.filter(l => l.code !== 'mina')
        : languages;

    return (
        <div className="flex flex-col gap-2 w-full max-w-sm">
            <label className="text-sm font-medium text-slate-500 uppercase tracking-wider">{label}</label>
            <div className="relative">
                <select
                    value={selected}
                    onChange={(e) => onChange(e.target.value)}
                    className="appearance-none w-full bg-white border border-gray-200 text-gray-700 py-3 px-4 pr-8 rounded-xl leading-tight focus:outline-none focus:bg-white focus:border-primary focus:ring-2 focus:ring-primary/20 transition-all font-medium"
                >
                    {availableLanguages.map((lang) => (
                        <option key={lang.code} value={lang.code}>
                            {lang.name} {lang.type === 'audio-only' ? '(Audio Only)' : ''}
                        </option>
                    ))}
                </select>
                <div className="pointer-events-none absolute inset-y-0 right-0 flex items-center px-2 text-gray-700">
                    <svg className="fill-current h-4 w-4" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20"><path d="M9.293 12.95l.707.707L15.657 8l-1.414-1.414L10 10.828 5.757 6.586 4.343 8z" /></svg>
                </div>
            </div>
        </div>
    );
};

export default LanguageSelector;
