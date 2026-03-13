import { useState } from 'react';
import { useT } from '../i18n';

export default function FeedbackBar({ onLiked }) {
  const { t } = useT();
  const [feedback, setFeedback] = useState(null);

  function handleFeedback(type) {
    setFeedback(type);
    if (type === 'up') onLiked();
  }

  if (feedback) {
    return (
      <div className="flex items-center gap-2 pt-1 msg-enter">
        <span className={`inline-flex items-center gap-1.5 text-xs font-medium px-3 py-1.5 rounded-full ${
          feedback === 'up'
            ? 'bg-green-50 dark:bg-green-900/30 text-green-700 dark:text-green-300 border border-green-200 dark:border-green-800/60'
            : 'bg-slate-100 dark:bg-slate-700 text-slate-500 dark:text-slate-400 border border-slate-200 dark:border-slate-600'
        }`}>
          {feedback === 'up' ? (
            <>
              <svg className="w-3.5 h-3.5" fill="currentColor" viewBox="0 0 24 24">
                <path d="M2 20h2V8H2v12zm22-9a2 2 0 00-2-2h-6.31l.95-4.57.03-.32c0-.41-.17-.79-.44-1.06L14.17 1 7.59 7.59C7.22 7.95 7 8.45 7 9v10a2 2 0 002 2h9c.83 0 1.54-.5 1.84-1.22l3.02-7.05c.09-.23.14-.47.14-.73v-2z" />
              </svg>
              {t('feedback.likedMsg')}
            </>
          ) : (
            <>
              <svg className="w-3.5 h-3.5" fill="currentColor" viewBox="0 0 24 24">
                <path d="M22 4h-2v12h2V4zm-4 12V6c0-1.1-.9-2-2-2H7c-.83 0-1.54.5-1.84 1.22l-3.02 7.05c-.09.23-.14.47-.14.73v2a2 2 0 002 2h6.31l-.95 4.57-.03.32c0 .41.17.79.44 1.06L9.83 23l6.59-6.59c.36-.36.58-.86.58-1.41z" />
              </svg>
              {t('feedback.dislikedMsg')}
            </>
          )}
        </span>
      </div>
    );
  }

  return (
    <div className="flex items-center gap-3 pt-3 border-t border-white/[0.06] mt-1">
      <span className="text-xs text-slate-400 dark:text-slate-500">{t('feedback.question')}</span>
      <div className="flex gap-1">
        <button
          onClick={() => handleFeedback('up')}
          className="p-1.5 rounded-lg text-slate-300 dark:text-slate-600 hover:text-green-600 dark:hover:text-green-400 hover:bg-green-50 dark:hover:bg-green-900/30 transition-all duration-150 active:scale-90"
          aria-label="Helpful"
        >
          <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" strokeWidth={2} stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" d="M6.633 10.5c.806 0 1.533-.446 2.031-1.08a9.041 9.041 0 012.861-2.4c.723-.384 1.35-.956 1.653-1.715a4.498 4.498 0 00.322-1.672V3a.75.75 0 01.75-.75A2.25 2.25 0 0116.5 4.5c0 1.152-.26 2.243-.723 3.218-.266.558.107 1.282.725 1.282h3.126c1.026 0 1.945.694 2.054 1.715.045.422.068.85.068 1.285a11.95 11.95 0 01-2.649 7.521c-.388.482-.987.729-1.605.729H14.23c-.483 0-.964-.078-1.423-.23l-3.114-1.04a4.501 4.501 0 00-1.423-.23H5.904M14.25 9h2.25M5.904 18.75c.083.205.173.405.27.602.197.4-.078.898-.523.898h-.908c-.889 0-1.713-.518-1.972-1.368a12 12 0 01-.521-3.507c0-1.553.295-3.036.831-4.398C3.387 10.203 4.167 9.75 5 9.75h1.053c.472 0 .745.556.5.96a8.958 8.958 0 00-1.302 4.665c0 1.194.232 2.333.654 3.375z" />
          </svg>
        </button>
        <button
          onClick={() => handleFeedback('down')}
          className="p-1.5 rounded-lg text-slate-300 dark:text-slate-600 hover:text-red-500 dark:hover:text-red-400 hover:bg-red-50 dark:hover:bg-red-900/30 transition-all duration-150 active:scale-90"
          aria-label="Not helpful"
        >
          <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" strokeWidth={2} stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" d="M7.5 15h2.25m8.024-9.75c.011.05.028.1.052.148.591 1.2.924 2.55.924 3.977a8.96 8.96 0 01-1.302 4.666c-.245.403.028.959.5.959h1.053c.832 0 1.612-.453 1.918-1.227C20.705 12.16 21 10.87 21 9.504c0-1.553-.295-3.036-.831-4.398C19.84 4.33 19.06 3.75 18.175 3.75h-.908c-.445 0-.72.498-.523.898.197.4.41.805.577 1.227M7.5 15l-3.114 1.04a4.501 4.501 0 00-1.423.23H2.25A.75.75 0 011.5 15.5v-.628c0-1.026.694-1.945 1.715-2.054A12.07 12.07 0 014.5 12.5c1.285 0 2.524.19 3.701.546a4.5 4.5 0 001.423.23h.681" />
          </svg>
        </button>
      </div>
    </div>
  );
}
