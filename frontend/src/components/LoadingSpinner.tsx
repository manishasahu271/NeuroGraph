export function LoadingSpinner({ label }: { label?: string }) {
  return (
    <div className="flex items-center gap-3 text-[14px] text-text-secondary">
      <div
        className="h-5 w-5 animate-spin rounded-full border-2 border-almond-silk/30 border-t-almond-silk"
        aria-hidden
      />
      <span>{label || "Loading…"}</span>
    </div>
  );
}
