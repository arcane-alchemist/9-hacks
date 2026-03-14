const langLabels = {
  hindi: 'Hindi',
  english: 'English',
  tamil: 'Tamil',
  telugu: 'Telugu',
  bengali: 'Bengali',
  hi: 'Hindi',
  en: 'English',
  ta: 'Tamil',
  te: 'Telugu',
  bn: 'Bengali',
};

export default function LanguageBadge({ language }) {
  if (!language) return null;
  const label = langLabels[language.toLowerCase()] || language;

  return (
    <span className="inline-flex items-center gap-1 text-xs font-medium bg-blue-50 dark:bg-blue-900/40 text-blue-700 dark:text-blue-300 px-2.5 py-1 rounded-full border border-blue-200 dark:border-blue-800">
      <svg className="w-3 h-3" fill="none" viewBox="0 0 24 24" strokeWidth={2} stroke="currentColor">
        <path strokeLinecap="round" strokeLinejoin="round" d="M10.5 21l5.25-11.25L21 21m-9-3h7.5M3 5.621a48.474 48.474 0 016-.371m0 0c1.12 0 2.233.038 3.334.114M9 5.25V3m3.334 2.364C11.176 10.658 7.69 15.08 3 17.502m9.334-12.138c.896.061 1.785.147 2.666.257m-4.589 8.495a18.023 18.023 0 01-3.827-5.802" />
      </svg>
      Responding in {label}
    </span>
  );
}
