import Section from "./Section";
import { faq } from "../app/content";

export default function Faq() {
  return (
    <Section id="faq" title="FAQ">
      <div className="space-y-3">
        {faq.map((item) => (
          <details key={item.question} className="group rounded-lg border border-line bg-surface">
            <summary className="flex cursor-pointer list-none items-center justify-between gap-4 px-5 py-4 font-medium text-fg [&::-webkit-details-marker]:hidden">
              <span>{item.question}</span>
              <span
                aria-hidden="true"
                className="shrink-0 text-xl leading-none text-brand transition-transform group-open:rotate-45"
              >
                +
              </span>
            </summary>
            <p className="px-5 pb-4 text-muted">{item.answer}</p>
          </details>
        ))}
      </div>
    </Section>
  );
}
