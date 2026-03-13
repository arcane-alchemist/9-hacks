import { useState, useRef, useEffect } from 'react';
import { postQuery, getDLSA } from '../api';
import { useT } from '../i18n';
import ResponseCard from './ResponseCard';
import LoadingSkeleton from './LoadingSkeleton';
import ClarificationFlow from './ClarificationFlow';

const QUICK_PROMPTS = [
  { label: 'My employer hasn\'t paid my wages', icon: '💼' },
  { label: 'I need protection from domestic abuse', icon: '🛡️' },
  { label: 'My land is being taken illegally', icon: '🏠' },
  { label: 'I faced caste discrimination', icon: '⚖️' },
];

export default function ChatInterface({ situationType, onOpenLetterModal }) {
  const { t } = useT();
  const [messages, setMessages] = useState([]);
  const [query, setQuery] = useState('');
  const [loading, setLoading] = useState(false);
  const [showPincode, setShowPincode] = useState(false);
  const [pincode, setPincode] = useState('');
  const [pincodeLoading, setPincodeLoading] = useState(false);
  const [isFocused, setIsFocused] = useState(false);
  const messagesEndRef = useRef(null);
  const pincodeInputRef = useRef(null);
  const inputRef = useRef(null);
  const pendingClarificationRef = useRef(null);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, loading, showPincode]);

  useEffect(() => {
    if (showPincode) pincodeInputRef.current?.focus();
  }, [showPincode]);

  async function sendQuery(text, extraContext) {
    const fullText = extraContext ? `${text}\n\nAdditional info: ${extraContext}` : text;
    setMessages((prev) => [...prev, { role: 'user', text: fullText }]);
    setLoading(true);

    try {
      const data = await postQuery({ text: fullText, situation_type: situationType || undefined });
      if (data.clarification_needed) {
        pendingClarificationRef.current = fullText;
        setMessages((prev) => [...prev, { role: 'clarification', question: data.clarification_question, data }]);
      } else {
        pendingClarificationRef.current = null;
        setMessages((prev) => [...prev, { role: 'ai', data }]);
      }
    } catch (err) {
      const detail = err.response?.data?.detail || t('chat.errorFallback');
      setMessages((prev) => [...prev, { role: 'error', text: detail }]);
    } finally {
      setLoading(false);
    }
  }

  function handleSubmit(e) {
    e.preventDefault();
    if (!query.trim() || loading) return;
    const text = query.trim();
    setQuery('');
    setShowPincode(false);
    setPincode('');
    sendQuery(text);
  }

  function handleQuickPrompt(label) {
    if (loading) return;
    setQuery('');
    sendQuery(label);
  }

  function handleClarificationAnswer(answer) {
    sendQuery(pendingClarificationRef.current || '', answer);
  }

  async function handlePincodeSubmit(e) {
    e.preventDefault();
    if (!pincode.trim() || pincode.length < 6 || pincodeLoading) return;
    setPincodeLoading(true);
    try {
      const dlsa = await getDLSA(pincode.trim());
      setMessages((prev) => [...prev, { role: 'dlsa', data: dlsa }]);
      setShowPincode(false);
      setPincode('');
    } catch (err) {
      const detail = err.response?.data?.detail || t('chat.pincodeError');
      setMessages((prev) => [...prev, { role: 'error', text: detail }]);
    } finally {
      setPincodeLoading(false);
    }
  }

  const isEmpty = messages.length === 0 && !loading;

  return (
    <section className="max-w-4xl mx-auto px-4 pb-6">
      <div className={`bg-white dark:bg-[#0d1929] rounded-2xl border transition-all duration-200 overflow-hidden shadow-sm ${
        isFocused
          ? 'border-teal-400 dark:border-teal-600 shadow-teal-500/10'
          : 'border-slate-200 dark:border-slate-700/50'
      }`}>

        {/* Chat header bar */}
        <div className="flex items-center gap-2 px-4 py-3 border-b border-slate-100 dark:border-slate-700/50 bg-slate-50/80 dark:bg-slate-800/30">
          <div className="flex gap-1.5">
            <div className="w-2.5 h-2.5 rounded-full bg-red-400/70"></div>
            <div className="w-2.5 h-2.5 rounded-full bg-amber-400/70"></div>
            <div className="w-2.5 h-2.5 rounded-full bg-green-400/70"></div>
          </div>
          <div className="flex-1 text-center">
            <span className="text-xs font-medium text-slate-400 dark:text-slate-500">
              JusticeAI Legal Assistant
            </span>
          </div>
          {messages.length > 0 && (
            <button
              onClick={() => setMessages([])}
              className="text-xs text-slate-400 dark:text-slate-500 hover:text-red-500 dark:hover:text-red-400 transition-colors flex items-center gap-1"
              title="Clear conversation"
            >
              <svg className="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" strokeWidth={2} stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" d="M14.74 9l-.346 9m-4.788 0L9.26 9m9.968-3.21c.342.052.682.107 1.022.166m-1.022-.165L18.16 19.673a2.25 2.25 0 01-2.244 2.077H8.084a2.25 2.25 0 01-2.244-2.077L4.772 5.79m14.456 0a48.108 48.108 0 00-3.478-.397m-12 .562c.34-.059.68-.114 1.022-.165m0 0a48.11 48.11 0 013.478-.397m7.5 0v-.916c0-1.18-.91-2.164-2.09-2.201a51.964 51.964 0 00-3.32 0c-1.18.037-2.09 1.022-2.09 2.201v.916m7.5 0a48.667 48.667 0 00-7.5 0" />
              </svg>
              Clear
            </button>
          )}
        </div>

        {/* Messages area */}
        <div className="min-h-[240px] max-h-[58vh] overflow-y-auto p-4 space-y-4">
          {isEmpty && (
            <div className="flex flex-col items-center justify-center py-8 text-center">
              <div className="w-16 h-16 rounded-2xl bg-teal-50 dark:bg-teal-900/30 border border-teal-100 dark:border-teal-800/50 flex items-center justify-center mb-4 shadow-inner">
                <svg className="w-8 h-8 text-teal-600 dark:text-teal-400" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" d="M12 18v-5.25m0 0a6.01 6.01 0 001.5-.189m-1.5.189a6.01 6.01 0 01-1.5-.189m3.75 7.478a12.06 12.06 0 01-4.5 0m3.75 2.383a14.406 14.406 0 01-3 0M14.25 18v-.192c0-.983.658-1.823 1.508-2.316a7.5 7.5 0 10-7.517 0c.85.493 1.509 1.333 1.509 2.316V18" />
                </svg>
              </div>
              <h3 className="text-sm font-semibold text-slate-700 dark:text-slate-300 mb-1">
                How can I help you today?
              </h3>
              <p className="text-xs text-slate-400 dark:text-slate-500 max-w-xs mb-6 leading-relaxed">
                {t('chat.emptyState')}
              </p>

              {/* Quick prompt chips */}
              <div className="flex flex-wrap gap-2 justify-center max-w-sm">
                {QUICK_PROMPTS.map((prompt) => (
                  <button
                    key={prompt.label}
                    onClick={() => handleQuickPrompt(prompt.label)}
                    className="inline-flex items-center gap-1.5 text-xs font-medium text-slate-600 dark:text-slate-300 bg-slate-100 dark:bg-slate-700/60 border border-slate-200 dark:border-slate-600/60 rounded-full px-3 py-1.5 hover:bg-teal-50 dark:hover:bg-teal-900/30 hover:border-teal-300 dark:hover:border-teal-700 hover:text-teal-700 dark:hover:text-teal-300 transition-all duration-200"
                  >
                    <span>{prompt.icon}</span>
                    {prompt.label}
                  </button>
                ))}
              </div>
            </div>
          )}

          {messages.map((msg, i) => {
            if (msg.role === 'user') return (
              <div key={i} className="flex justify-end msg-enter">
                <div className="max-w-xs sm:max-w-sm">
                  <div className="bg-teal-600 text-white rounded-2xl rounded-br-sm px-4 py-3 text-sm leading-relaxed shadow-sm">
                    {msg.text}
                  </div>
                  <p className="text-[10px] text-slate-400 dark:text-slate-600 mt-1 text-right pr-1">You</p>
                </div>
              </div>
            );
            if (msg.role === 'ai') return (
              <div key={i} className="flex justify-start gap-2.5 msg-enter">
                <div className="w-7 h-7 rounded-xl bg-teal-600 flex items-center justify-center shrink-0 mt-1 shadow-sm shadow-teal-500/20">
                  <svg className="w-3.5 h-3.5 text-white" fill="none" viewBox="0 0 24 24" strokeWidth={2} stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" d="M12 18v-5.25m0 0a6.01 6.01 0 001.5-.189m-1.5.189a6.01 6.01 0 01-1.5-.189m3.75 7.478a12.06 12.06 0 01-4.5 0m3.75 2.383a14.406 14.406 0 01-3 0M14.25 18v-.192c0-.983.658-1.823 1.508-2.316a7.5 7.5 0 10-7.517 0c.85.493 1.509 1.333 1.509 2.316V18" />
                  </svg>
                </div>
                <ResponseCard data={msg.data} onGenerateLetter={onOpenLetterModal} onLiked={() => setShowPincode(true)} />
              </div>
            );
            if (msg.role === 'clarification') return (
              <div key={i} className="flex justify-start gap-2.5 msg-enter">
                <div className="w-7 h-7 rounded-xl bg-amber-500 flex items-center justify-center shrink-0 mt-1">
                  <svg className="w-3.5 h-3.5 text-white" fill="none" viewBox="0 0 24 24" strokeWidth={2} stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" d="M9.879 7.519c1.171-1.025 3.071-1.025 4.242 0 1.172 1.025 1.172 2.687 0 3.712-.203.179-.43.326-.67.442-.745.361-1.45.999-1.45 1.827v.75M21 12a9 9 0 11-18 0 9 9 0 0118 0zm-9 5.25h.008v.008H12v-.008z" />
                  </svg>
                </div>
                <ClarificationFlow question={msg.question} onSubmit={handleClarificationAnswer} />
              </div>
            );
            if (msg.role === 'dlsa') return (
              <div key={i} className="flex justify-start gap-2.5 msg-enter">
                <div className="w-7 h-7 rounded-xl bg-teal-600 flex items-center justify-center shrink-0 mt-1">
                  <svg className="w-3.5 h-3.5 text-white" fill="none" viewBox="0 0 24 24" strokeWidth={2} stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" d="M15 10.5a3 3 0 11-6 0 3 3 0 016 0z" /><path strokeLinecap="round" strokeLinejoin="round" d="M19.5 10.5c0 7.142-7.5 11.25-7.5 11.25S4.5 17.642 4.5 10.5a7.5 7.5 0 1115 0z" />
                  </svg>
                </div>
                <DLSACard data={msg.data} />
              </div>
            );
            if (msg.role === 'error') return (
              <div key={i} className="flex justify-start gap-2.5 msg-enter">
                <div className="w-7 h-7 rounded-xl bg-red-500 flex items-center justify-center shrink-0 mt-1">
                  <svg className="w-3.5 h-3.5 text-white" fill="none" viewBox="0 0 24 24" strokeWidth={2} stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" d="M12 9v3.75m9-.75a9 9 0 11-18 0 9 9 0 0118 0zm-9 3.75h.008v.008H12v-.008z" />
                  </svg>
                </div>
                <div className="max-w-lg bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800/60 text-red-700 dark:text-red-300 rounded-2xl rounded-tl-sm px-4 py-3 text-sm leading-relaxed">
                  {msg.text}
                </div>
              </div>
            );
            return null;
          })}

          {loading && (
            <div className="flex justify-start gap-2.5 msg-enter">
              <div className="w-7 h-7 rounded-xl bg-teal-600 flex items-center justify-center shrink-0 mt-1">
                <svg className="w-3.5 h-3.5 text-white" fill="none" viewBox="0 0 24 24" strokeWidth={2} stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" d="M12 18v-5.25m0 0a6.01 6.01 0 001.5-.189m-1.5.189a6.01 6.01 0 01-1.5-.189m3.75 7.478a12.06 12.06 0 01-4.5 0m3.75 2.383a14.406 14.406 0 01-3 0M14.25 18v-.192c0-.983.658-1.823 1.508-2.316a7.5 7.5 0 10-7.517 0c.85.493 1.509 1.333 1.509 2.316V18" />
                </svg>
              </div>
              <LoadingSkeleton />
            </div>
          )}
          <div ref={messagesEndRef} />
        </div>

        {/* Pincode finder */}
        {showPincode && (
          <div className="border-t border-teal-100 dark:border-teal-900/50 bg-teal-50/60 dark:bg-teal-950/30 px-3 sm:px-4 py-3">
            <p className="text-xs font-medium text-teal-700 dark:text-teal-400 mb-2 flex items-center gap-1.5">
              <svg className="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" strokeWidth={2} stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" d="M15 10.5a3 3 0 11-6 0 3 3 0 016 0z" /><path strokeLinecap="round" strokeLinejoin="round" d="M19.5 10.5c0 7.142-7.5 11.25-7.5 11.25S4.5 17.642 4.5 10.5a7.5 7.5 0 1115 0z" />
              </svg>
              Find your nearest free legal aid office
            </p>
            <form onSubmit={handlePincodeSubmit} className="flex items-center gap-2">
              <input
                ref={pincodeInputRef}
                type="text"
                value={pincode}
                onChange={(e) => setPincode(e.target.value.replace(/\D/g, '').slice(0, 6))}
                placeholder={t('chat.pincodePlaceholder')}
                className="flex-1 rounded-xl border border-teal-200 dark:border-teal-800/70 bg-white dark:bg-slate-800/80 text-slate-900 dark:text-slate-100 px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-teal-500 focus:border-transparent placeholder:text-slate-400 dark:placeholder:text-slate-500 transition-colors"
                disabled={pincodeLoading}
              />
              <button
                type="submit"
                disabled={pincode.length < 6 || pincodeLoading}
                className="bg-teal-600 text-white rounded-xl px-4 py-2 text-sm font-medium hover:bg-teal-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors flex items-center gap-1.5 shrink-0"
              >
                {pincodeLoading ? (
                  <svg className="w-4 h-4 animate-spin" viewBox="0 0 24 24" fill="none">
                    <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
                    <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" />
                  </svg>
                ) : (
                  <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" strokeWidth={2} stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" d="M21 21l-5.197-5.197m0 0A7.5 7.5 0 105.196 5.196a7.5 7.5 0 0010.607 10.607z" />
                  </svg>
                )}
                {t('chat.findOffice')}
              </button>
              <button
                type="button"
                onClick={() => { setShowPincode(false); setPincode(''); }}
                className="p-2 rounded-lg text-slate-400 hover:bg-slate-200 dark:hover:bg-slate-700 transition-colors"
                aria-label="Dismiss"
              >
                <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" strokeWidth={2} stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" d="M6 18L18 6M6 6l12 12" />
                </svg>
              </button>
            </form>
          </div>
        )}

        {/* Input area */}
        <form
          onSubmit={handleSubmit}
          className="border-t border-slate-100 dark:border-slate-700/50 bg-white dark:bg-[#0d1929] p-3 sm:p-4 transition-colors"
        >
          <div className="flex gap-2 items-end">
            <div className="flex-1 relative">
              <input
                ref={inputRef}
                type="text"
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                onFocus={() => setIsFocused(true)}
                onBlur={() => setIsFocused(false)}
                placeholder={t('chat.placeholder')}
                className="w-full rounded-xl border border-slate-200 dark:border-slate-600/60 bg-slate-50 dark:bg-slate-800/60 text-slate-900 dark:text-slate-100 px-4 py-3 text-sm focus:outline-none focus:ring-2 focus:ring-teal-500 focus:border-transparent placeholder:text-slate-400 dark:placeholder:text-slate-500 transition-all pr-10"
                disabled={loading}
              />
              {query && (
                <button
                  type="button"
                  onClick={() => setQuery('')}
                  className="absolute right-3 top-1/2 -translate-y-1/2 text-slate-300 dark:text-slate-600 hover:text-slate-500 dark:hover:text-slate-400 transition-colors"
                  tabIndex={-1}
                >
                  <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" strokeWidth={2} stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" d="M6 18L18 6M6 6l12 12" />
                  </svg>
                </button>
              )}
            </div>
            <button
              type="submit"
              disabled={!query.trim() || loading}
              className="bg-teal-600 text-white rounded-xl w-11 h-11 flex items-center justify-center hover:bg-teal-700 disabled:opacity-40 disabled:cursor-not-allowed transition-all duration-200 shadow-sm hover:shadow-md hover:shadow-teal-500/20 shrink-0 active:scale-95"
              aria-label={t('chat.send')}
            >
              {loading ? (
                <svg className="w-4 h-4 animate-spin" viewBox="0 0 24 24" fill="none">
                  <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
                  <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" />
                </svg>
              ) : (
                <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" strokeWidth={2.5} stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" d="M6 12L3.269 3.126A59.768 59.768 0 0121.485 12 59.77 59.77 0 013.27 20.876L5.999 12zm0 0h7.5" />
                </svg>
              )}
            </button>
          </div>

          {situationType && (
            <div className="flex items-center gap-1.5 mt-2 pl-1">
              <div className="w-1.5 h-1.5 rounded-full bg-teal-500"></div>
              <p className="text-xs text-slate-400 dark:text-slate-500">
                {t('chat.context')}:{' '}
                <span className="font-medium text-teal-600 dark:text-teal-400 capitalize">
                  {situationType.replace(/_/g, ' ')}
                </span>
              </p>
            </div>
          )}
        </form>
      </div>
    </section>
  );
}

function DLSACard({ data }) {
  const { t } = useT();
  const office = data?.office || data;
  const name = office?.name || office?.office_name || t('response.nearestOffice');
  const address = office?.address || '';
  const phone = office?.phone || office?.contact || '';
  const timings = office?.timings || office?.working_hours || '';
  const isFree = office?.free;

  return (
    <div className="max-w-lg bg-teal-50 dark:bg-teal-900/20 border border-teal-200 dark:border-teal-800/60 rounded-2xl rounded-tl-sm p-4 space-y-2 transition-colors shadow-sm">
      <div className="flex items-start justify-between gap-2">
        <h4 className="text-sm font-semibold text-teal-800 dark:text-teal-200 flex items-center gap-1.5">
          <svg className="w-4 h-4 shrink-0" fill="none" viewBox="0 0 24 24" strokeWidth={2} stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" d="M15 10.5a3 3 0 11-6 0 3 3 0 016 0z" /><path strokeLinecap="round" strokeLinejoin="round" d="M19.5 10.5c0 7.142-7.5 11.25-7.5 11.25S4.5 17.642 4.5 10.5a7.5 7.5 0 1115 0z" />
          </svg>
          {name}
        </h4>
        {isFree && (
          <span className="text-[10px] font-bold uppercase tracking-wider bg-green-100 dark:bg-green-900/50 text-green-700 dark:text-green-300 px-2 py-0.5 rounded-full border border-green-200 dark:border-green-800 shrink-0">
            {t('response.free')}
          </span>
        )}
      </div>
      {address && <p className="text-sm text-teal-700 dark:text-teal-300 leading-relaxed">{address}</p>}
      {phone && (
        <a
          href={`tel:${phone}`}
          className="inline-flex items-center gap-1.5 text-sm font-medium text-teal-800 dark:text-teal-200 hover:text-teal-600 dark:hover:text-teal-400 transition-colors"
        >
          <svg className="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" strokeWidth={2} stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" d="M2.25 6.75c0 8.284 6.716 15 15 15h2.25a2.25 2.25 0 002.25-2.25v-1.372c0-.516-.351-.966-.852-1.091l-4.423-1.106c-.44-.11-.902.055-1.173.417l-.97 1.293c-.282.376-.769.542-1.21.38a12.035 12.035 0 01-7.143-7.143c-.162-.441.004-.928.38-1.21l1.293-.97c.363-.271.527-.734.417-1.173L6.963 3.102a1.125 1.125 0 00-1.091-.852H4.5A2.25 2.25 0 002.25 4.5v2.25z" />
          </svg>
          {phone}
        </a>
      )}
      {timings && (
        <p className="text-xs text-teal-600 dark:text-teal-400 flex items-center gap-1">
          <svg className="w-3 h-3" fill="none" viewBox="0 0 24 24" strokeWidth={2} stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" d="M12 6v6h4.5m4.5 0a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
          {timings}
        </p>
      )}
    </div>
  );
}
