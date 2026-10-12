import { site } from "../app/content";

const external = { target: "_blank", rel: "noopener noreferrer" } as const;

export default function Footer() {
  return (
    <footer className="border-t border-line">
      <div className="mx-auto flex max-w-5xl flex-col items-center gap-2 px-4 py-8 text-center text-sm text-muted sm:flex-row sm:justify-between sm:px-6 sm:text-left">
        <p>
          Released under the{" "}
          <a href={site.licenseUrl} className="link" {...external}>
            {site.licenseName}
          </a>{" "}
          License · Made by{" "}
          <a href={site.authorUrl} className="link" {...external}>
            {site.authorName}
          </a>
        </p>
        <p>
          <a href={site.githubUrl} className="link" {...external}>
            GitHub
          </a>
        </p>
      </div>
    </footer>
  );
}
