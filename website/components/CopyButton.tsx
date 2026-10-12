"use client";

import { useEffect, useRef, useState } from "react";

type CopyButtonProps = {
  text: string;
  /** What is being copied, used in the accessible name. */
  label?: string;
};

export default function CopyButton({ text, label = "command" }: CopyButtonProps) {
  const [copied, setCopied] = useState(false);
  const timer = useRef<ReturnType<typeof setTimeout> | null>(null);

  useEffect(() => {
    return () => {
      if (timer.current) clearTimeout(timer.current);
    };
  }, []);

  async function handleClick() {
    try {
      await navigator.clipboard.writeText(text);
    } catch {
      return;
    }
    setCopied(true);
    if (timer.current) clearTimeout(timer.current);
    timer.current = setTimeout(() => setCopied(false), 2000);
  }

  return (
    <>
      <button
        type="button"
        onClick={handleClick}
        aria-label={copied ? `Copied ${label}` : `Copy ${label}`}
        className="shrink-0 rounded-md border border-neutral-500 px-2 py-1 font-sans text-xs font-medium text-terminal-fg transition-colors hover:border-brand hover:text-brand"
      >
        {copied ? "Copied" : "Copy"}
      </button>
      <span className="sr-only" aria-live="polite">
        {copied ? `Copied ${label} to clipboard` : ""}
      </span>
    </>
  );
}
