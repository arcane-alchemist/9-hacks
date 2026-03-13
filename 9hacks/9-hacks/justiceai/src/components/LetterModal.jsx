import { useState } from 'react';
import { generateLetter } from '../api';
import { letterTypeLabels } from '../data/situationData';
import { useT } from '../i18n';

export default function LetterModal({ letterType, onClose }) {
  const { t } = useT();
  const displayName = letterTypeLabels[letterType] || letterType;

  const [form, setForm] = useState({
    user_name: '',
    district: '',
    date: new Date().toISOString().split('T')[0],
    details: '',
  });
  const [letter, setLetter] = useState('');
  const [loading, setLoading] = useState(false);
  const [copied, setCopied] = useState(false);
  const [error, setError] = useState('');

  function updateField(field, value) {
    setForm((prev) => ({ ...prev, [field]: value }));
  }

  async function handleGenerate() {
    setLoading(true);
    setError('');
    try {
      const data = await generateLetter({ type: letterType, ...form });
      setLetter(data.letter || data.content || JSON.stringify(data));
    } catch (err) {
      setError(err.response?.data?.detail || t('letter.error'));
    } finally {
      setLoading(false);
    }
  }

  async function handleCopy() {
    try {
      await navigator.clipboard.writeText(letter);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    } catch {
      const ta = document.createElement('textarea');
      ta.value = letter;
      document.body.appendChild(ta);
      ta.select();
      document.execCommand('copy');
      document.body.removeChild(ta);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    }
  }

  const inputClasses =
    'w-full rounded-xl border border-slate-200 dark:border-slate-600/60 bg-slate-50 dark:bg-slate-800/60 text-slate-900 dark:text-slate-100 px-3.5 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-teal-500 focus:border-transparent placeholder:text-slate-400 dark:placeholder:text-slate-500 transition-all';

  const canGenerate = form.user_name.trim() && form.district.trim();

  return (
    <div
      className="fixed inset-0 z-50 flex items-center justify-center bg-black/60 backdrop-blur-sm p-4"
      onClick={(e) => { if (e.target === e.currentTarget) onClose(); }}
    >
      <div className="bg-white dark:bg-[#0d1929] rounded-2xl shadow-2xl w-full max-w-2xl max-h-[92vh] flex flex-col overflow-hidden border border-slate-100 dark:border-slate-700/50 transition-colors msg-enter">

        {/* Modal header */}
        <div className="flex items-center justify-between px-6 py-4 border-b border-slate-100 dark:border-slate-700/50">
          <div className="flex items-center gap-3">
            <div className="w-9 h-9 rounded-xl bg-teal-50 dark:bg-teal-900/40 border border-teal-200 dark:border-teal-800/60 flex items-center justify-center">
              <svg className="w-5 h-5 text-teal-600 dark:text-teal-400" fill="none" viewBox="0 0 24 24" strokeWidth={2} stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" d="M19.5 14.25v-2.625a3.375 3.375 0 00-3.375-3.375h-1.5A1.125 1.125 0 0113.5 7.125v-1.5a3.375 3.375 0 00-3.375-3.375H8.25m0 12.75h7.5m-7.5 3H12M10.5 2.25H5.625c-.621 0-1.125.504-1.125 1.125v17.25c0 .621.504 1.125 1.125 1.125h12.75c.621 0 1.125-.504 1.125-1.125V11.25a9 9 0 00-9-9z" />
              </svg>
            </div>
            <div>
              <h2 className="text-base font-semibold text-slate-900 dark:text-slate-100">{t('letter.title')}</h2>
              <p className="text-xs text-slate-400 dark:text-slate-500 mt-0.5">{displayName}</p>
            </div>
          </div>
          <button
            onClick={onClose}
            className="p-2 rounded-xl hover:bg-slate-100 dark:hover:bg-slate-700/60 transition-colors text-slate-400 hover:text-slate-600 dark:hover:text-slate-300"
            aria-label="Close"
          >
            <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" strokeWidth={2} stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>

        {/* Modal body */}
        <div className="flex-1 overflow-y-auto p-6 space-y-5">

          {/* Form fields */}
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <div className="space-y-1.5">
              <label className="block text-xs font-semibold text-slate-600 dark:text-slate-400 uppercase tracking-wide">
                {t('letter.yourName')} <span className="text-red-500">*</span>
              </label>
              <input
                type="text"
                value={form.user_name}
                onChange={(e) => updateField('user_name', e.target.value)}
                placeholder={t('letter.namePlaceholder')}
                className={inputClasses}
              />
            </div>
            <div className="space-y-1.5">
              <label className="block text-xs font-semibold text-slate-600 dark:text-slate-400 uppercase tracking-wide">
                {t('letter.district')} <span className="text-red-500">*</span>
              </label>
              <input
                type="text"
                value={form.district}
                onChange={(e) => updateField('district', e.target.value)}
                placeholder={t('letter.districtPlaceholder')}
                className={inputClasses}
              />
            </div>
            <div className="space-y-1.5">
              <label className="block text-xs font-semibold text-slate-600 dark:text-slate-400 uppercase tracking-wide">
                {t('letter.date')}
              </label>
              <input
                type="date"
                value={form.date}
                onChange={(e) => updateField('date', e.target.value)}
                className={inputClasses}
              />
            </div>
          </div>

          <div className="space-y-1.5">
            <label className="block text-xs font-semibold text-slate-600 dark:text-slate-400 uppercase tracking-wide">
              {t('letter.details')}
            </label>
            <textarea
              value={form.details}
              onChange={(e) => updateField('details', e.target.value)}
              placeholder={t('letter.detailsPlaceholder')}
              rows={3}
              className={`${inputClasses} resize-none`}
            />
          </div>

          {/* Generate button */}
          <button
            onClick={handleGenerate}
            disabled={loading || !canGenerate}
            className="w-full bg-teal-600 text-white font-semibold py-3 rounded-xl hover:bg-teal-700 disabled:opacity-50 disabled:cursor-not-allowed transition-all duration-200 flex items-center justify-center gap-2 shadow-sm hover:shadow-md hover:shadow-teal-500/20 active:scale-[0.98]"
          >
            {loading ? (
              <>
                <svg className="w-4 h-4 animate-spin" viewBox="0 0 24 24" fill="none">
                  <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
                  <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" />
                </svg>
                {t('letter.generating')}
              </>
            ) : (
              <>
                <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" strokeWidth={2} stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" d="M9.813 15.904L9 18.75l-.813-2.846a4.5 4.5 0 00-3.09-3.09L2.25 12l2.846-.813a4.5 4.5 0 003.09-3.09L9 5.25l.813 2.846a4.5 4.5 0 003.09 3.09L15.75 12l-2.846.813a4.5 4.5 0 00-3.09 3.09zM18.259 8.715L18 9.75l-.259-1.035a3.375 3.375 0 00-2.455-2.456L14.25 6l1.036-.259a3.375 3.375 0 002.455-2.456L18 2.25l.259 1.035a3.375 3.375 0 002.456 2.456L21.75 6l-1.035.259a3.375 3.375 0 00-2.456 2.456zM16.894 20.567L16.5 21.75l-.394-1.183a2.25 2.25 0 00-1.423-1.423L13.5 18.75l1.183-.394a2.25 2.25 0 001.423-1.423l.394-1.183.394 1.183a2.25 2.25 0 001.423 1.423l1.183.394-1.183.394a2.25 2.25 0 00-1.423 1.423z" />
                </svg>
                {t('letter.generateBtn')}
              </>
            )}
          </button>

          {!canGenerate && !loading && (
            <p className="text-xs text-slate-400 dark:text-slate-500 text-center -mt-2">
              Fill in your name and district to generate the letter
            </p>
          )}

          {/* Error state */}
          {error && (
            <div className="flex items-start gap-2.5 bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800/60 rounded-xl p-3">
              <svg className="w-4 h-4 text-red-500 shrink-0 mt-0.5" fill="none" viewBox="0 0 24 24" strokeWidth={2} stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" d="M12 9v3.75m9-.75a9 9 0 11-18 0 9 9 0 0118 0zm-9 3.75h.008v.008H12v-.008z" />
              </svg>
              <p className="text-sm text-red-600 dark:text-red-400">{error}</p>
            </div>
          )}

          {/* Generated letter */}
          {letter && (
            <div className="space-y-3 msg-enter">
              <div className="flex items-center justify-between">
                <h3 className="text-xs font-semibold text-slate-600 dark:text-slate-400 uppercase tracking-wide flex items-center gap-1.5">
                  <svg className="w-3.5 h-3.5 text-teal-500" fill="none" viewBox="0 0 24 24" strokeWidth={2} stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" d="M4.5 12.75l6 6 9-13.5" />
                  </svg>
                  {t('letter.generatedTitle')}
                </h3>
                <button
                  onClick={handleCopy}
                  className={`inline-flex items-center gap-1.5 text-xs font-semibold rounded-xl px-3 py-1.5 border transition-all duration-200 active:scale-95 ${
                    copied
                      ? 'bg-green-50 dark:bg-green-900/30 text-green-700 dark:text-green-300 border-green-200 dark:border-green-800'
                      : 'bg-teal-50 dark:bg-teal-900/30 text-teal-700 dark:text-teal-300 border-teal-200 dark:border-teal-700 hover:bg-teal-100 dark:hover:bg-teal-900/50'
                  }`}
                >
                  {copied ? (
                    <>
                      <svg className="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" strokeWidth={2.5} stroke="currentColor">
                        <path strokeLinecap="round" strokeLinejoin="round" d="M4.5 12.75l6 6 9-13.5" />
                      </svg>
                      {t('letter.copied')}
                    </>
                  ) : (
                    <>
                      <svg className="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" strokeWidth={2} stroke="currentColor">
                        <path strokeLinecap="round" strokeLinejoin="round" d="M15.666 3.888A2.25 2.25 0 0013.5 2.25h-3c-1.03 0-1.9.693-2.166 1.638m7.332 0c.055.194.084.4.084.612v0a.75.75 0 01-.75.75H9.75a.75.75 0 01-.75-.75v0c0-.212.03-.418.084-.612m7.332 0c.646.049 1.288.11 1.927.184 1.1.128 1.907 1.077 1.907 2.185V19.5a2.25 2.25 0 01-2.25 2.25H6.75A2.25 2.25 0 014.5 19.5V6.257c0-1.108.806-2.057 1.907-2.185a48.208 48.208 0 011.927-.184" />
                      </svg>
                      {t('letter.copyLetter')}
                    </>
                  )}
                </button>
              </div>
              <textarea
                readOnly
                value={letter}
                rows={14}
                className="w-full rounded-xl border border-slate-200 dark:border-slate-600/60 bg-slate-50 dark:bg-slate-800/60 px-4 py-3 text-sm text-slate-800 dark:text-slate-200 leading-relaxed font-mono resize-none transition-colors focus:outline-none focus:ring-2 focus:ring-teal-500"
              />
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
