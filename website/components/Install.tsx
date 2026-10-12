"use client";

import { useRef, useState, useSyncExternalStore, type KeyboardEvent } from "react";
import { installMethods } from "@/app/content";
import CopyButton from "./CopyButton";

const noopSubscribe = () => () => {};

/**
 * False on the server and during hydration, true afterwards. Until JS has run every panel stays
 * visible, so the install steps are readable with JavaScript disabled and hydration matches.
 */
function useMounted() {
  return useSyncExternalStore(
    noopSubscribe,
    () => true,
    () => false,
  );
}

export default function Install() {
  const [selected, setSelected] = useState(installMethods[0].id);
  const mounted = useMounted();
  const tabRefs = useRef<(HTMLButtonElement | null)[]>([]);

  function selectIndex(index: number) {
    const count = installMethods.length;
    const next = (index + count) % count;
    setSelected(installMethods[next].id);
    tabRefs.current[next]?.focus();
  }

  function handleKeyDown(event: KeyboardEvent<HTMLButtonElement>, index: number) {
    switch (event.key) {
      case "ArrowRight":
        selectIndex(index + 1);
        break;
      case "ArrowLeft":
        selectIndex(index - 1);
        break;
      case "Home":
        selectIndex(0);
        break;
      case "End":
        selectIndex(installMethods.length - 1);
        break;
      default:
        return;
    }
    event.preventDefault();
  }

  return (
    <section id="install" aria-labelledby="install-title" className="py-16 sm:py-24">
      <h2 id="install-title" className="text-2xl font-semibold tracking-tight sm:text-3xl">
        Install
      </h2>
      <p className="mt-3 max-w-2xl text-muted">Pick the way that suits you.</p>
      <div className="mt-10">
        <div
          role="tablist"
          aria-label="Install methods"
          className="flex flex-wrap gap-x-2 border-b border-line"
        >
          {installMethods.map((method, index) => {
            const isSelected = method.id === selected;
            return (
              <button
                key={method.id}
                ref={(el) => {
                  tabRefs.current[index] = el;
                }}
                type="button"
                role="tab"
                id={`tab-${method.id}`}
                aria-selected={isSelected}
                aria-controls={`panel-${method.id}`}
                tabIndex={isSelected ? 0 : -1}
                onClick={() => setSelected(method.id)}
                onKeyDown={(event) => handleKeyDown(event, index)}
                className={`-mb-px border-b-2 px-3 py-2 text-sm font-medium transition-colors ${
                  isSelected
                    ? "border-brand text-fg"
                    : "border-transparent text-muted hover:text-fg"
                }`}
              >
                {method.label}
              </button>
            );
          })}
        </div>

        {installMethods.map((method) => (
          <div
            key={method.id}
            role="tabpanel"
            id={`panel-${method.id}`}
            aria-labelledby={`tab-${method.id}`}
            tabIndex={0}
            hidden={mounted && method.id !== selected}
            className="mt-6 rounded-md"
          >
            <ol className="list-decimal space-y-4 pl-6">
              {method.steps.map((step, stepIndex) => (
                <li key={stepIndex} className="min-w-0 pl-1">
                  {step.text && <p className="text-fg">{step.text}</p>}
                  {step.code && (
                    <div
                      className={`flex max-w-full items-start gap-3 rounded-lg bg-terminal p-4 text-terminal-fg ${
                        step.text ? "mt-2" : ""
                      }`}
                    >
                      <pre className="min-w-0 flex-1 overflow-x-auto font-mono text-sm whitespace-pre">
                        <code>{step.code}</code>
                      </pre>
                      <CopyButton
                        text={step.code}
                        label={`${method.label} step ${stepIndex + 1} command`}
                      />
                    </div>
                  )}
                </li>
              ))}
            </ol>
          </div>
        ))}
      </div>
    </section>
  );
}
