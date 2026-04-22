"use client";

import { motion, useScroll, useTransform } from "framer-motion";
import { useRef } from "react";

const articles = [
  {
    kicker: "Field report",
    topic: "Labor trafficking",
    headline: "The fishing fleets that don't come home",
    dek: "How forced labor survives in the blank spaces between jurisdictions — and who is quietly mapping them.",
    byline: "Ava Okonkwo · 14 min",
  },
  {
    kicker: "Analysis",
    topic: "Climate displacement",
    headline: "A country without a coastline",
    dek: "When a nation is promised to disappear, its people become a category no passport office has a name for.",
    byline: "Reyes Martín · 9 min",
  },
  {
    kicker: "Investigation",
    topic: "Digital exclusion",
    headline: "Offline by design",
    dek: "Millions are locked out of benefits, banking, and identity itself — not by accident, but by the shape of the system.",
    byline: "Priya Banerjee · 12 min",
  },
  {
    kicker: "Dispatch",
    topic: "Anti-trafficking",
    headline: "The hotline that nobody answers",
    dek: "Why the infrastructure built to receive cries for help is often the first thing traffickers learn to silence.",
    byline: "Jonah Lister · 11 min",
  },
  {
    kicker: "Essay",
    topic: "Mental health",
    headline: "What care looks like without a clinic",
    dek: "In the places where psychiatry never arrived, communities are building something it couldn't have imagined.",
    byline: "Tess Nambale · 8 min",
  },
];

function Card({ a, index }: { a: (typeof articles)[number]; index: number }) {
  return (
    <motion.article
      data-cursor-target
      initial={{ opacity: 0, y: 24 }}
      whileInView={{ opacity: 1, y: 0 }}
      viewport={{ once: true, amount: 0.2 }}
      transition={{
        duration: 0.8,
        delay: index * 0.08,
        ease: [0.2, 0.6, 0.2, 1],
      }}
      className="group relative flex w-[78vw] shrink-0 flex-col justify-between overflow-hidden border border-ink/10 bg-dawn p-8 md:w-[32rem] md:p-10"
      style={{ minHeight: "28rem" }}
    >
      <div>
        <div className="mb-8 flex items-center justify-between font-sans text-[11px] uppercase tracking-[0.3em]">
          <span className="text-twilight transition-colors duration-500 group-hover:text-saffron">
            {a.kicker}
          </span>
          <span className="text-ink/40">{a.topic}</span>
        </div>
        <h3
          className="font-display font-light text-ink leading-[1.08] tracking-tight"
          style={{ fontSize: "clamp(1.6rem, 2.4vw, 2.15rem)" }}
        >
          {a.headline}
          <motion.span
            aria-hidden
            initial={{ opacity: 0, x: -6 }}
            whileHover={{ opacity: 1, x: 0 }}
            className="ml-2 inline-block text-saffron opacity-0 transition-all duration-500 group-hover:opacity-100"
          >
            →
          </motion.span>
        </h3>
        <p className="mt-5 font-sans text-[0.98rem] leading-relaxed text-ink/70">
          {a.dek}
        </p>
      </div>
      <div className="mt-10 font-sans text-xs uppercase tracking-[0.28em] text-ink/45">
        {a.byline}
      </div>
    </motion.article>
  );
}

export default function Articles() {
  const ref = useRef<HTMLElement>(null);
  const { scrollYProgress } = useScroll({
    target: ref,
    offset: ["start end", "end start"],
  });

  const x = useTransform(scrollYProgress, [0.1, 0.9], ["8%", "-45%"]);

  return (
    <section
      ref={ref}
      className="relative overflow-hidden py-32 md:py-40"
      style={{ backgroundColor: "var(--dawn)" }}
    >
      <div className="mx-auto mb-16 max-w-6xl px-6">
        <motion.div
          initial={{ opacity: 0, x: -12 }}
          whileInView={{ opacity: 1, x: 0 }}
          viewport={{ once: true, amount: 0.6 }}
          transition={{ duration: 0.8 }}
          className="mb-6 font-sans text-xs uppercase tracking-[0.35em] text-clay"
        >
          III. Dispatches
        </motion.div>
        <h2
          className="max-w-2xl font-display font-light text-ink leading-[1.08] tracking-tight"
          style={{ fontSize: "clamp(1.75rem, 3.6vw, 3rem)" }}
        >
          A few things we&rsquo;re <span className="italic text-twilight">working on</span>.
        </h2>
      </div>

      <div className="md:hidden">
        <div className="hide-scroll flex snap-x snap-mandatory gap-5 overflow-x-auto px-6 pb-6">
          {articles.map((a, i) => (
            <div key={a.headline} className="snap-start">
              <Card a={a} index={i} />
            </div>
          ))}
        </div>
      </div>

      <div className="hidden md:block">
        <motion.div
          style={{ x }}
          className="flex gap-8 px-6 will-change-transform"
        >
          {articles.map((a, i) => (
            <Card key={a.headline} a={a} index={i} />
          ))}
        </motion.div>
      </div>
    </section>
  );
}
