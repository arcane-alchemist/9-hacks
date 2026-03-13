export default function LoadingSkeleton() {
  return (
    <div className="max-w-lg w-full bg-white dark:bg-slate-800/60 rounded-2xl rounded-tl-sm p-5 shadow-sm border border-slate-100 dark:border-slate-700/50 space-y-3.5 transition-colors">
      {/* Pill placeholder */}
      <div className="skeleton-bar h-5 w-20 rounded-full" />

      {/* Text lines */}
      <div className="space-y-2">
        <div className="skeleton-bar h-3.5 w-full" />
        <div className="skeleton-bar h-3.5 w-[92%]" />
        <div className="skeleton-bar h-3.5 w-4/5" />
      </div>

      {/* Steps placeholder */}
      <div className="space-y-2 pt-1">
        <div className="skeleton-bar h-3 w-24" />
        <div className="flex items-center gap-2">
          <div className="skeleton-bar h-5 w-5 rounded-full shrink-0" />
          <div className="skeleton-bar h-3.5 w-full" />
        </div>
        <div className="flex items-center gap-2">
          <div className="skeleton-bar h-5 w-5 rounded-full shrink-0" />
          <div className="skeleton-bar h-3.5 w-[85%]" />
        </div>
        <div className="flex items-center gap-2">
          <div className="skeleton-bar h-5 w-5 rounded-full shrink-0" />
          <div className="skeleton-bar h-3.5 w-[70%]" />
        </div>
      </div>

      {/* Typing dots */}
      <div className="flex items-center gap-1 pt-1">
        <div className="pulse-dot w-2 h-2 rounded-full bg-teal-400 dark:bg-teal-600"></div>
        <div className="pulse-dot w-2 h-2 rounded-full bg-teal-400 dark:bg-teal-600"></div>
        <div className="pulse-dot w-2 h-2 rounded-full bg-teal-400 dark:bg-teal-600"></div>
      </div>
    </div>
  );
}
