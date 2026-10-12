import Section from "./Section";
import { features } from "../app/content";

export default function Features() {
  return (
    <Section id="features" title="Features" intro="Everything it can do today.">
      <ul className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3">
        {features.map((feature) => (
          <li key={feature.title} className="rounded-xl border border-line bg-surface p-6">
            <span aria-hidden="true" className="block h-1 w-8 rounded-full bg-brand" />
            <h3 className="mt-4 font-semibold text-fg">{feature.title}</h3>
            <p className="mt-2 text-muted">{feature.body}</p>
          </li>
        ))}
      </ul>
    </Section>
  );
}
