import Link from "next/link";

export default function NotFound() {
  return (
    <div className="rounded-2xl border border-border bg-card-bg p-10 text-center shadow-card sm:p-14">
      <h1 className="text-[32px] font-semibold tracking-[-0.02em] text-text-primary">Page not found</h1>
      <p className="mx-auto mt-3 max-w-md text-[15px] text-text-secondary">
        The page you’re looking for doesn’t exist or may have moved.
      </p>
      <div className="mt-8">
        <Link
          href="/"
          className="ng-btn-scale inline-flex rounded-full bg-almond-silk px-8 py-3 text-[15px] font-medium text-white shadow-soft hover:brightness-95"
        >
          Go home
        </Link>
      </div>
    </div>
  );
}
