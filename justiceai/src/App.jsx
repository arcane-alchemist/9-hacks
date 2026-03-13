import { useState, useEffect } from 'react';
import { useT } from './i18n';
import Header from './components/Header';
import SituationCards from './components/SituationCards';
import ChatInterface from './components/ChatInterface';
import LetterModal from './components/LetterModal';

export default function App() {
  const { t } = useT();
  const [situationType, setSituationType] = useState('');
  const [letterModal, setLetterModal] = useState(null);
  const [dark, setDark] = useState(() => {
    if (typeof window !== 'undefined') {
      const saved = localStorage.getItem('justiceai-dark');
      if (saved !== null) return saved === 'true';
      return window.matchMedia('(prefers-color-scheme: dark)').matches;
    }
    return false;
  });

  useEffect(() => {
    document.documentElement.classList.toggle('dark', dark);
    localStorage.setItem('justiceai-dark', String(dark));
  }, [dark]);

  return (
    <div className="min-h-screen bg-slate-50 dark:bg-[#080f1c] transition-colors duration-300 font-sans">
      <Header dark={dark} onToggleDark={() => setDark((d) => !d)} />

      <main className="pb-12">
        {/* Hero Banner */}
        <section className="hero-pattern bg-white dark:bg-[#0b1120] border-b border-slate-200/60 dark:border-slate-700/30 transition-colors">
          <div className="max-w-4xl mx-auto px-4 py-10 sm:py-14">
            <div className="flex flex-col sm:flex-row items-start sm:items-center gap-5">
              <div className="flex-shrink-0 w-14 h-14 rounded-2xl bg-teal-600 flex items-center justify-center shadow-lg shadow-teal-500/25">
                <svg className="w-7 h-7 text-white" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" d="M12 3v17.25m0 0c-1.472 0-2.882.265-4.185.75M12 20.25c1.472 0 2.882.265 4.185.75M18.75 4.97A48.416 48.416 0 0012 4.5c-2.291 0-4.545.16-6.75.47m13.5 0c1.01.143 2.01.317 3 .52m-3-.52l2.62 10.726c.122.499-.106 1.028-.589 1.202a5.988 5.988 0 01-2.031.352 5.988 5.988 0 01-2.031-.352c-.483-.174-.711-.703-.59-1.202L18.75 4.971zm-16.5.52c.99-.203 1.99-.377 3-.52m0 0l2.62 10.726c.122.499-.106 1.028-.589 1.202a5.989 5.989 0 01-2.031.352 5.989 5.989 0 01-2.031-.352c-.483-.174-.711-.703-.59-1.202L5.25 4.971z" />
                </svg>
              </div>
              <div className="flex-1">
                <h2 className="text-2xl sm:text-3xl font-bold text-slate-900 dark:text-slate-100 text-balance leading-tight">
                  Know Your Rights.{' '}
                  <span className="text-teal-600">Get Legal Help.</span>
                </h2>
                <p className="mt-1.5 text-sm sm:text-base text-slate-500 dark:text-slate-400 leading-relaxed max-w-xl">
                  Free legal guidance for workers, families, and communities in India — powered by AI, available in your language.
                </p>
              </div>
              <div className="flex flex-wrap gap-2 sm:flex-nowrap sm:flex-col sm:items-end shrink-0">
                <div className="inline-flex items-center gap-1.5 text-xs font-medium text-teal-700 dark:text-teal-400 bg-teal-50 dark:bg-teal-900/30 border border-teal-200 dark:border-teal-800 rounded-full px-3 py-1.5">
                  <span className="w-1.5 h-1.5 rounded-full bg-teal-500 animate-pulse"></span>
                  Free Legal Aid
                </div>
                <div className="inline-flex items-center gap-1.5 text-xs font-medium text-blue-700 dark:text-blue-400 bg-blue-50 dark:bg-blue-900/30 border border-blue-200 dark:border-blue-800 rounded-full px-3 py-1.5">
                  <svg className="w-3 h-3" fill="none" viewBox="0 0 24 24" strokeWidth={2.5} stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" d="M10.5 21l5.25-11.25L21 21m-9-3h7.5M3 5.621a48.474 48.474 0 016-.371m0 0c1.12 0 2.233.038 3.334.114M9 5.25V3m3.334 2.364C11.176 10.658 7.69 15.08 3 17.502m9.334-12.138c.896.061 1.785.147 2.666.257m-4.589 8.495a18.023 18.023 0 01-3.827-5.802" />
                  </svg>
                  5 Languages
                </div>
              </div>
            </div>
          </div>
        </section>

        <SituationCards onSelectSituation={setSituationType} />

        <ChatInterface
          situationType={situationType}
          onOpenLetterModal={(type) => setLetterModal(type)}
        />
      </main>

      <footer className="text-center py-6 px-4 text-xs text-slate-400 dark:text-slate-600 border-t border-slate-200/60 dark:border-slate-800/60 bg-white dark:bg-[#0b1120] transition-colors">
        {t('footer.disclaimer')}
      </footer>

      {letterModal && (
        <LetterModal
          letterType={letterModal}
          onClose={() => setLetterModal(null)}
        />
      )}
    </div>
  );
}
