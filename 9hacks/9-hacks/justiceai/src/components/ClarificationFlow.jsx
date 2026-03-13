import { useState } from 'react';
import { useT } from '../i18n';

export default function ClarificationFlow({ question, onSubmit }) {
  const { t } = useT();
  const [answer, setAnswer] = useState('');

  function handleSubmit(e) {
    e.preventDefault();
    if (!answer.trim()) return;
    onSubmit(answer.trim());
    setAnswer('');
  }

  return (
    <div className="max-w-lg space-y-2.5">
      <div className="bg-white dark:bg-slate-800/60 rounded-2xl rounded-tl-sm shadow-sm border border-slate-100 dark:border-slate-700/50 px-5 py-4 transition-colors">
        <div className="flex items-center gap-2 mb-2.5">
          <span className="inline-flex items-center gap-1.5 text-xs font-semibold bg-amber-50 dark:bg-amber-900/30 text-amber-700 dark:text-amber-300 border border-amber-200 dark:border-amber-800/60 px-2.5 py-1 rounded-full">
            <svg className="w-3 h-3" fill="none" viewBox="0 0 24 24" strokeWidth={2.5} stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" d="M9.879 7.519c1.171-1.025 3.071-1.025 4.242 0 1.172 1.025 1.172 2.687 0 3.712-.203.179-.43.326-.67.442-.745.361-1.45.999-1.45 1.827v.75M21 12a9 9 0 11-18 0 9 9 0 0118 0zm-9 5.25h.008v.008H12v-.008z" />
            </svg>
            {t('clarification.badge')}
          </span>
        </div>
        <p className="text-sm text-slate-700 dark:text-slate-200 leading-relaxed">{question}</p>
      </div>
      <form onSubmit={handleSubmit} className="flex gap-2">
        <input
          type="text"
          value={answer}
          onChange={(e) => setAnswer(e.target.value)}
          placeholder={t('clarification.placeholder')}
          className="flex-1 rounded-xl border border-slate-200 dark:border-slate-600/60 bg-white dark:bg-slate-800/60 text-slate-900 dark:text-slate-100 px-4 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-teal-500 focus:border-transparent placeholder:text-slate-400 dark:placeholder:text-slate-500 transition-all"
          autoFocus
        />
        <button
          type="submit"
          disabled={!answer.trim()}
          className="bg-teal-600 text-white rounded-xl px-4 py-2.5 text-sm font-medium hover:bg-teal-700 disabled:opacity-40 disabled:cursor-not-allowed transition-all duration-200 flex items-center gap-1.5 active:scale-95"
        >
          <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" strokeWidth={2.5} stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" d="M6 12L3.269 3.126A59.768 59.768 0 0121.485 12 59.77 59.77 0 013.27 20.876L5.999 12zm0 0h7.5" />
          </svg>
          {t('chat.send')}
        </button>
      </form>
    </div>
  );
}
