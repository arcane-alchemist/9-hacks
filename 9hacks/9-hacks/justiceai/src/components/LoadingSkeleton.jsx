export default function LoadingSkeleton() {
  return (
    <div className="max-w-lg w-full rounded-2xl rounded-tl-sm p-5 space-y-3.5 border border-white/[0.07] bg-white/[0.03]">
      {/* Pill placeholder */}
      <div className="skeleton-dark h-5 w-24 rounded-full" />

      {/* Text lines */}
      <div className="space-y-2">
        <div className="skeleton-dark h-3.5 w-full rounded-md" />
        <div className="skeleton-dark h-3.5 w-[90%] rounded-md" />
        <div className="skeleton-dark h-3.5 w-4/5 rounded-md" />
      </div>

      {/* Steps */}
      <div className="space-y-2 pt-1">
        <div className="skeleton-dark h-3 w-24 rounded-md" />
        {[100, 85, 70].map((w, i) => (
          <div key={i} className="flex items-center gap-2">
            <div className="skeleton-dark h-5 w-5 rounded-full shrink-0" />
            <div className={`skeleton-dark h-3.5 rounded-md`} style={{ width: `${w}%` }} />
          </div>
        ))}
      </div>

      {/* Animated typing dots */}
      <div className="flex items-center gap-1.5 pt-1">
        <div className="pulse-dot w-2 h-2 rounded-full bg-teal-500/60" />
        <div className="pulse-dot w-2 h-2 rounded-full bg-teal-500/60" style={{ animationDelay: '0.2s' }} />
        <div className="pulse-dot w-2 h-2 rounded-full bg-teal-500/60" style={{ animationDelay: '0.4s' }} />
        <span className="text-xs text-gray-500 ml-1 font-light">Analysing your situation...</span>
      </div>
    </div>
  );
}
