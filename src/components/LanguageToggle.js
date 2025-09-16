import React from 'react';
import { Globe } from 'lucide-react';
import './LanguageToggle.css';

const LanguageToggle = ({ language, onLanguageChange }) => {
  const toggleLanguage = () => {
    const newLanguage = language === 'en' ? 'hi' : 'en';
    onLanguageChange(newLanguage);
  };

  return (
    <button 
      className={`language-toggle ${language}`}
      onClick={toggleLanguage}
      title={`Switch to ${language === 'en' ? 'Hindi' : 'English'}`}
    >
      <Globe size={16} />
      <span className="language-text">
        {language === 'en' ? 'EN' : 'हिं'}
      </span>
    </button>
  );
};

export default LanguageToggle;