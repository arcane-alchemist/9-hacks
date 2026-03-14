import { createContext, useContext, useState, useCallback, useMemo } from 'react';
import en from './en';
import hi from './hi';
import ta from './ta';
import te from './te';
import bn from './bn';

const translations = { en, hi, ta, te, bn };

const I18nContext = createContext();

function getNestedValue(obj, path) {
  return path.split('.').reduce((acc, key) => acc?.[key], obj);
}

export function I18nProvider({ children }) {
  const [lang, setLang] = useState(() => {
    if (typeof window !== 'undefined') {
      return localStorage.getItem('justiceai-lang') || 'en';
    }
    return 'en';
  });

  const changeLang = useCallback((code) => {
    setLang(code);
    localStorage.setItem('justiceai-lang', code);
  }, []);

  const t = useCallback((key) => {
    return getNestedValue(translations[lang], key)
      ?? getNestedValue(translations.en, key)
      ?? key;
  }, [lang]);

  const value = useMemo(() => ({ lang, setLang: changeLang, t }), [lang, changeLang, t]);

  return (
    <I18nContext.Provider value={value}>
      {children}
    </I18nContext.Provider>
  );
}

export function useT() {
  const ctx = useContext(I18nContext);
  if (!ctx) throw new Error('useT must be used within I18nProvider');
  return ctx;
}
