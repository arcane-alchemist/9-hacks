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
    <div className="relative min-h-screen bg-black text-white font-sans overflow-x-hidden">
      {/* Spline animated background */}
      <div className="fixed inset-0 z-0 pointer-events-none">
        <iframe
          src="https://my.spline.design/claritystream-a72K0KUwFoZV82QBzvu52Kai/"
          frameBorder="0"
          width="100%"
          height="100%"
          title="Background animation"
        />
      </div>

      {/* Content layer */}
      <div className="relative z-10 flex flex-col min-h-screen">
        <Header dark={dark} onToggleDark={() => setDark((d) => !d)} />

        <main className="flex-1 pb-12">
          {/* Hero Banner */}
          <section className="border-b border-white/10">
            <div className="max-w-4xl mx-auto px-6 py-12 sm:py-16">
              <div className="flex flex-col sm:flex-row items-start sm:items-center gap-5">
                <div className="flex-shrink-0 w-14 h-14 rounded-2xl bg-teal-600 flex items-center justify-center shadow-lg shadow-teal-500/25">
                  <svg className="w-7 h-7 text-white" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" d="M12 3v17.25m0 0c-1.472 0-2.882.265-4.185.75M12 20.25c1.472 0 2.882.265 4.185.75M18.75 4.97A48.416 48.416 0 0012 4.5c-2.291 0-4.545.16-6.75.47m13.5 0c1.01.143 2.01.317 3 .52m-3-.52l2.62 10.726c.122.499-.106 1.028-.589 1.202a5.988 5.988 0 01-2.031.352 5.988 5.988 0 01-2.031-.352c-.483-.174-.711-.703-.59-1.202L18.75 4.971zm-16.5.52c.99-.203 1.99-.377 3-.52m0 0l2.62 10.726c.122.499-.106 1.028-.589 1.202a5.989 5.989 0 01-2.031.352 5.989 5.989 0 01-2.031-.352c-.483-.174-.711-.703-.59-1.202L5.25 4.971z" />
                  </svg>
                </div>
                <div className="flex-1">
                  <h2 className="text-3xl sm:text-4xl font-light tracking-tight text-white text-balance leading-tight">
                    Know Your Rights.{' '}
                    <span className="bg-clip-text text-transparent bg-gradient-to-r from-teal-400 to-blue-400">Get Legal Help.</span>
                  </h2>
                  <p className="mt-2 text-sm sm:text-base text-gray-300 font-light leading-relaxed max-w-xl tracking-wide">
                    Free legal guidance for workers, families, and communities in India — powered by AI, available in your language.
                  </p>
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

        <footer className="text-center py-6 px-4 text-xs text-gray-500 border-t border-white/10">
          {t('footer.disclaimer')}
        </footer>
      </div>

      {letterModal && (
        <LetterModal
          letterType={letterModal}
          onClose={() => setLetterModal(null)}
        />
      )}
    </div>
  );
}
