import { nav, site } from "@/app/content";
import ThemeToggle from "./ThemeToggle";

export default function Header() {
  return (
    <header className="sticky top-0 z-50 border-b border-line bg-bg/80 backdrop-blur">
      <div className="mx-auto flex h-14 max-w-5xl items-center justify-between gap-2 px-4 sm:px-6">
        <a href="#" className="font-mono font-semibold text-brand">
          {site.name}
        </a>
        <nav aria-label="Main" className="flex min-w-0 items-center gap-2.5 text-sm sm:gap-6">
          {nav.map((item) => (
            <a key={item.href} href={item.href} className="text-muted hover:text-fg">
              {item.label}
            </a>
          ))}
          <a
            href={site.githubUrl}
            target="_blank"
            rel="noopener noreferrer"
            className="text-muted hover:text-fg"
          >
            GitHub
          </a>
          <ThemeToggle />
        </nav>
      </div>
    </header>
  );
}
