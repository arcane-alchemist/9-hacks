import { useState } from 'react';
import { colorMap } from '../data/situationData';
import { useT } from '../i18n';

const situationKeys = ['labour', 'domestic_violence', 'land_property', 'sc_st'];
const situationTypeMap = {
  labour: 'labour',
  domestic_violence: 'family_dv',
  land_property: 'civil',
  sc_st: 'scst',
};
const colorKeys = {
  labour: 'green',
  domestic_violence: 'red',
  land_property: 'amber',
  sc_st: 'purple',
};

const icons = {
  labour: (
    <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" strokeWidth={1.8} stroke="currentColor">
      <path strokeLinecap="round" strokeLinejoin="round" d="M11.42 15.17L17.25 21A2.652 2.652 0 0021 17.25l-5.877-5.877M11.42 15.17l2.496-3.03c.317-.384.74-.626 1.208-.766M11.42 15.17l-4.655 5.653a2.548 2.548 0 11-3.586-3.586l6.837-5.63m5.108-.233c.55-.164 1.163-.188 1.743-.14a4.5 4.5 0 004.486-6.336l-3.276 3.277a3.004 3.004 0 01-2.25-2.25l3.276-3.276a4.5 4.5 0 00-6.336 4.486c.049.58.025 1.193-.14 1.743" />
    </svg>
  ),
  domestic_violence: (
    <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" strokeWidth={1.8} stroke="currentColor">
      <path strokeLinecap="round" strokeLinejoin="round" d="M9 12.75L11.25 15 15 9.75m-3-7.036A11.959 11.959 0 013.598 6 11.99 11.99 0 003 9.749c0 5.592 3.824 10.29 9 11.623 5.176-1.332 9-6.03 9-11.622 0-1.31-.21-2.571-.598-3.751h-.152c-3.196 0-6.1-1.248-8.25-3.285z" />
    </svg>
  ),
  land_property: (
    <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" strokeWidth={1.8} stroke="currentColor">
      <path strokeLinecap="round" strokeLinejoin="round" d="M2.25 21h19.5m-18-18v18m10.5-18v18m6-13.5V21M6.75 6.75h.75m-.75 3h.75m-.75 3h.75m3-6h.75m-.75 3h.75m-.75 3h.75M6.75 21v-3.375c0-.621.504-1.125 1.125-1.125h2.25c.621 0 1.125.504 1.125 1.125V21M3 3h12m-.75 4.5H21m-3.75 3H21" />
    </svg>
  ),
  sc_st: (
    <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" strokeWidth={1.8} stroke="currentColor">
      <path strokeLinecap="round" strokeLinejoin="round" d="M12 3v17.25m0 0c-1.472 0-2.882.265-4.185.75M12 20.25c1.472 0 2.882.265 4.185.75M18.75 4.97A48.416 48.416 0 0012 4.5c-2.291 0-4.545.16-6.75.47m13.5 0c1.01.143 2.01.317 3 .52m-3-.52l2.62 10.726c.122.499-.106 1.028-.589 1.202a5.988 5.988 0 01-2.031.352 5.988 5.988 0 01-2.031-.352c-.483-.174-.711-.703-.59-1.202L18.75 4.971zm-16.5.52c.99-.203 1.99-.377 3-.52m0 0l2.62 10.726c.122.499-.106 1.028-.589 1.202a5.989 5.989 0 01-2.031.352 5.989 5.989 0 01-2.031-.352c-.483-.174-.711-.703-.59-1.202L5.25 4.971z" />
    </svg>
  ),
};

export default function SituationCards({ onSelectSituation }) {
  const { t } = useT();
  const [expanded, setExpanded] = useState(null);

  function handleClick(key) {
    const isExpanding = expanded !== key;
    setExpanded(isExpanding ? key : null);
    if (isExpanding) {
      onSelectSituation(situationTypeMap[key]);
    }
  }

  return (
    <section className="max-w-4xl mx-auto px-4 py-7">
      <div className="flex items-center justify-between mb-5">
        <div>
          <h2 className="text-base font-semibold text-slate-800 dark:text-slate-200">
            {t('cards.heading')}
          </h2>
          <p className="text-sm text-slate-400 dark:text-slate-500 mt-0.5">
            {t('cards.subheading')}
          </p>
        </div>
        {expanded && (
          <button
            onClick={() => { setExpanded(null); onSelectSituation(''); }}
            className="text-xs text-slate-400 dark:text-slate-500 hover:text-slate-600 dark:hover:text-slate-300 transition-colors flex items-center gap-1"
          >
            <svg className="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" strokeWidth={2} stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" d="M6 18L18 6M6 6l12 12" />
            </svg>
            Clear
          </button>
        )}
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
        {situationKeys.map((key) => {
          const c = colorMap[colorKeys[key]];
          const isOpen = expanded === key;
          const title = t(`situations.${key}.title`);
          const titleHi = t(`situations.${key}.titleHi`);
          const description = t(`situations.${key}.description`);
          const rights = t(`situations.${key}.rights`);

          return (
            <div key={key} className={`rounded-2xl border-2 overflow-hidden transition-all duration-300 card-hover bg-transparent ${isOpen ? c.border + ' shadow-lg' : 'border-transparent shadow-sm hover:' + c.border.split(' ')[0].replace('border-', 'border-')}`}>
              <button
                onClick={() => handleClick(key)}
                className="w-full text-left p-4"
                aria-expanded={isOpen}
              >
                <div className="flex items-start gap-3">
                  <div className={`p-2.5 rounded-xl ${c.accent} text-white shrink-0 shadow-sm`}>
                    {icons[key]}
                  </div>
                  <div className="flex-1 min-w-0">
                    <div className="flex items-center justify-between gap-2">
                      <div>
                        <h3 className={`font-semibold text-sm ${c.text}`}>{title}</h3>
                        {title !== titleHi && (
                          <p className="text-xs text-slate-400 dark:text-slate-500 mt-0.5">{titleHi}</p>
                        )}
                      </div>
                      <div className={`w-6 h-6 rounded-full flex items-center justify-center shrink-0 transition-all duration-300 ${isOpen ? c.accent + ' text-white' : 'bg-white/60 dark:bg-black/20 text-slate-400'}`}>
                        <svg
                          className={`w-3.5 h-3.5 transition-transform duration-300 ${isOpen ? 'rotate-180' : ''}`}
                          fill="none" viewBox="0 0 24 24" strokeWidth={2.5} stroke="currentColor"
                        >
                          <path strokeLinecap="round" strokeLinejoin="round" d="M19.5 8.25l-7.5 7.5-7.5-7.5" />
                        </svg>
                      </div>
                    </div>
                    <p className="text-xs text-slate-500 dark:text-slate-400 mt-1.5 leading-relaxed">{description}</p>
                  </div>
                </div>
              </button>

              {isOpen && Array.isArray(rights) && (
                <div className="px-4 pb-4 pt-1">
                  <div className="border-t border-black/5 dark:border-white/5 pt-3 space-y-2.5">
                    <p className="text-[11px] font-semibold uppercase tracking-wider text-slate-400 dark:text-slate-500 mb-3">
                      Your Rights
                    </p>
                    {rights.map((right, i) => (
                      <div key={i} className="flex items-start gap-2.5 msg-enter" style={{ animationDelay: `${i * 50}ms` }}>
                        <span className={`shrink-0 w-5 h-5 rounded-full ${c.accent} text-white text-[10px] font-bold flex items-center justify-center mt-0.5 shadow-sm`}>
                          {i + 1}
                        </span>
                        <p className="text-sm text-slate-700 dark:text-slate-300 leading-relaxed">{right}</p>
                      </div>
                    ))}
                    <button
                      onClick={() => handleClick(key)}
                      className={`mt-3 w-full flex items-center justify-center gap-2 py-2 rounded-xl text-sm font-medium transition-all duration-200 ${c.accent} text-white hover:opacity-90 shadow-sm`}
                    >
                      <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" strokeWidth={2} stroke="currentColor">
                        <path strokeLinecap="round" strokeLinejoin="round" d="M8.625 12a.375.375 0 11-.75 0 .375.375 0 01.75 0zm0 0H8.25m4.125 0a.375.375 0 11-.75 0 .375.375 0 01.75 0zm0 0H12m4.125 0a.375.375 0 11-.75 0 .375.375 0 01.75 0zm0 0h-.375M21 12c0 4.556-4.03 8.25-9 8.25a9.764 9.764 0 01-2.555-.337A5.972 5.972 0 015.41 20.97a5.969 5.969 0 01-.474-.065 4.48 4.48 0 00.978-2.025c.09-.457-.133-.901-.467-1.226C3.93 16.178 3 14.189 3 12c0-4.556 4.03-8.25 9-8.25s9 3.694 9 8.25z" />
                      </svg>
                      Ask about this situation
                    </button>
                  </div>
                </div>
              )}
            </div>
          );
        })}
      </div>
    </section>
  );
}
