import Section from "./Section";
import { screenshots } from "../app/content";

export default function Showcase() {
  return (
    <Section id="showcase" title="See it in action">
      <div className="grid grid-cols-1 items-start gap-8 md:grid-cols-2">
        {screenshots.map((shot) => (
          <figure key={shot.src} className="min-w-0">
            <div
              className="overflow-hidden rounded-xl border border-line bg-surface"
              style={{ aspectRatio: `${shot.width} / ${shot.height}` }}
            >
              {/* eslint-disable-next-line @next/next/no-img-element -- static export with unoptimised images; the screenshots are remote GitHub URLs */}
              <img
                src={shot.src}
                alt={shot.alt}
                width={shot.width}
                height={shot.height}
                loading="lazy"
                className="h-auto w-full"
              />
            </div>
            <figcaption className="mt-3 text-center text-sm text-muted">{shot.caption}</figcaption>
          </figure>
        ))}
      </div>
    </Section>
  );
}
