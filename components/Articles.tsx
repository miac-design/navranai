"use client";

import { motion, useScroll, useTransform } from "framer-motion";
import Link from "next/link";
import { useRef } from "react";
import { articles, type Article } from "@/lib/articles";

function Card({ a, index }: { a: Article; index: number }) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 24 }}
      whileInView={{ opacity: 1, y: 0 }}
      viewport={{ once: true, amount: 0.2 }}
      transition={{
        duration: 0.8,
        delay: index * 0.08,
        ease: [0.2, 0.6, 0.2, 1],
      }}
      className="w-[78vw] shrink-0 md:w-[32rem]"
    >
      <Link
        href={`/dispatches/${a.slug}`}
        data-cursor-target
        className="group relative flex h-full flex-col justify-between overflow-hidden border border-ink/10 bg-dawn p-8 md:p-10"
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
            <span
              aria-hidden
              className="ml-2 inline-block text-saffron opacity-0 transition-all duration-500 group-hover:translate-x-1 group-hover:opacity-100"
            >
              →
            </span>
          </h3>
          <p className="mt-5 font-sans text-[0.98rem] leading-relaxed text-ink/70">
            {a.dek}
          </p>
        </div>
        <div className="mt-10 font-sans text-xs uppercase tracking-[0.28em] text-ink/45">
          {a.byline} · {a.readTime}
        </div>
      </Link>
    </motion.div>
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
        <div className="flex flex-wrap items-end justify-between gap-6">
          <h2
            className="max-w-2xl font-display font-light text-ink leading-[1.08] tracking-tight"
            style={{ fontSize: "clamp(1.75rem, 3.6vw, 3rem)" }}
          >
            A few things we&rsquo;re{" "}
            <span className="italic text-twilight">working on</span>.
          </h2>
          <Link
            href="/dispatches"
            data-cursor-target
            className="group inline-flex items-center gap-2 font-sans text-xs uppercase tracking-[0.3em] text-twilight"
          >
            <span className="border-b border-twilight/40 pb-1 transition-colors group-hover:border-saffron group-hover:text-saffron">
              All dispatches
            </span>
            <span className="transition-transform group-hover:translate-x-1">
              →
            </span>
          </Link>
        </div>
      </div>

      <div className="md:hidden">
        <div className="hide-scroll flex snap-x snap-mandatory gap-5 overflow-x-auto px-6 pb-6">
          {articles.map((a, i) => (
            <div key={a.slug} className="snap-start">
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
            <Card key={a.slug} a={a} index={i} />
          ))}
        </motion.div>
      </div>
    </section>
  );
}
