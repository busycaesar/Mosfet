import CopyButton from "@/components/CopyButton";
import { banner, site } from "@/app/content";

export default function Hero() {
  return (
    <section aria-labelledby="hero-title" className="mx-auto w-full max-w-5xl px-4 pt-20 pb-16 sm:px-6 sm:pt-28">
      <div className="flex min-w-0 flex-col items-start gap-6">
        <span className="inline-flex items-center gap-2 rounded-full border border-line px-3 py-1 text-xs font-medium text-muted">
          <span aria-hidden="true" className="h-2 w-2 rounded-full bg-brand" />
          {site.status}
        </span>

        <pre role="img" aria-label="Mosfet" className="w-full max-w-full overflow-x-auto rounded-xl bg-terminal p-4 font-mono text-[8px] leading-tight text-brand sm:p-6 sm:text-xs md:text-sm">
          {banner}
        </pre>

        <h1 id="hero-title" className="text-4xl font-bold tracking-tight text-fg sm:text-5xl">
          {site.tagline}
        </h1>

        <p className="max-w-2xl text-lg text-muted">{site.description}</p>

        <div className="flex w-full max-w-full items-center gap-3 rounded-lg bg-terminal px-4 py-3 font-mono text-sm text-terminal-fg sm:w-auto">
          <div className="flex min-w-0 flex-1 overflow-x-auto whitespace-nowrap">
            <span aria-hidden="true" className="mr-2 select-none text-brand">
              $
            </span>
            <code>{site.installCommand}</code>
          </div>
          <CopyButton text={site.installCommand} label="install command" />
        </div>

        <div className="flex w-full flex-col gap-3 sm:w-auto sm:flex-row">
          <a href="#install" className="rounded-lg bg-brand px-5 py-2.5 text-center font-medium text-brand-ink transition-opacity hover:opacity-90">
            Install
          </a>
          <a href={site.githubUrl} target="_blank" rel="noopener noreferrer" className="rounded-lg border border-line px-5 py-2.5 text-center font-medium text-fg transition-colors hover:bg-surface">
            View on GitHub
          </a>
        </div>
      </div>
    </section>
  );
}
