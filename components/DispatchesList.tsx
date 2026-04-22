"use client";

import Link from "next/link";
import { motion } from "framer-motion";
import type { Article } from "@/lib/articles";

export default function DispatchesList({ articles }: { articles: Article[] }) {
  return (
    <section className="px-6 pb-32">
      <div className="mx-auto max-w-6xl">
        <motion.ul
          initial="hidden"
          whileInView="show"
          viewport={{ once: true, amount: 0.1 }}
          variants={{
            hidden: {},
            show: { transition: { staggerChildren: 0.08 } },
          }}
          className="divide-y divide-ink/10 border-y border-ink/10"
        >
          {articles.map((a) => (
            <motion.li
              key={a.slug}
              variants={{
                hidden: { opacity: 0, y: 16 },
                show: {
                  opacity: 1,
                  y: 0,
                  transition: { duration: 0.8, ease: [0.2, 0.6, 0.2, 1] },
                },
              }}
            >
              <Link
                href={`/dispatches/${a.slug}`}
                data-cursor-target
                className="group grid gap-6 py-10 md:grid-cols-12 md:gap-8 md:py-12"
              >
                <div className="md:col-span-3">
                  <div className="flex flex-wrap items-center gap-x-4 gap-y-2 font-sans text-[11px] uppercase tracking-[0.3em]">
                    <span className="text-twilight transition-colors group-hover:text-saffron">
                      {a.kicker}
                    </span>
                    <span className="text-ink/40">{a.topic}</span>
                  </div>
                  <div className="mt-3 font-sans text-xs text-ink/45">
                    {a.date} · {a.readTime}
                  </div>
                </div>

                <div className="md:col-span-7">
                  <h2
                    className="font-display font-light text-ink leading-[1.1] tracking-tight"
                    style={{ fontSize: "clamp(1.75rem, 3vw, 2.5rem)" }}
                  >
                    {a.headline}
                    <span
                      aria-hidden
                      className="ml-2 inline-block translate-x-0 text-saffron opacity-0 transition-all duration-500 group-hover:translate-x-1 group-hover:opacity-100"
                    >
                      →
                    </span>
                  </h2>
                  <p className="mt-4 font-sans text-base leading-relaxed text-ink/70">
                    {a.dek}
                  </p>
                </div>

                <div className="md:col-span-2 md:text-right">
                  <div className="font-sans text-xs uppercase tracking-[0.3em] text-ink/50">
                    {a.byline}
                  </div>
                  <div className="mt-1 font-sans text-xs text-ink/40">
                    {a.location}
                  </div>
                </div>
              </Link>
            </motion.li>
          ))}
        </motion.ul>
      </div>
    </section>
  );
}
