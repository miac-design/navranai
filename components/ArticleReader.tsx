"use client";

import Link from "next/link";
import { motion, useScroll, useSpring } from "framer-motion";
import type { Article } from "@/lib/articles";

export default function ArticleReader({
  article,
  others,
}: {
  article: Article;
  others: Article[];
}) {
  const { scrollYProgress } = useScroll();
  const progress = useSpring(scrollYProgress, {
    stiffness: 120,
    damping: 28,
    mass: 0.3,
  });

  return (
    <>
      <motion.div
        aria-hidden
        className="fixed left-0 right-0 top-0 z-40 h-[2px] origin-left bg-saffron"
        style={{ scaleX: progress }}
      />

      <article className="relative">
        <header className="px-6 pb-12 pt-40 md:pt-48">
          <div className="mx-auto max-w-3xl">
            <motion.div
              initial={{ opacity: 0, y: 8 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6 }}
              className="mb-6 flex flex-wrap items-center gap-x-5 gap-y-2 font-sans text-[11px] uppercase tracking-[0.3em]"
            >
              <span className="text-saffron">{article.kicker}</span>
              <span className="text-ink/50">{article.topic}</span>
              <span className="text-ink/40">{article.date}</span>
              <span className="text-ink/40">{article.readTime}</span>
            </motion.div>

            <motion.h1
              initial={{ opacity: 0, y: 14 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.9, ease: [0.2, 0.6, 0.2, 1] }}
              className="font-display font-light text-ink leading-[1.05] tracking-tight"
              style={{ fontSize: "clamp(2.25rem, 5.5vw, 4.5rem)" }}
            >
              {article.headline}
            </motion.h1>

            <motion.p
              initial={{ opacity: 0, y: 14 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.9, delay: 0.15, ease: [0.2, 0.6, 0.2, 1] }}
              className="mt-8 font-display font-light italic text-twilight"
              style={{ fontSize: "clamp(1.2rem, 1.8vw, 1.5rem)", lineHeight: 1.4 }}
            >
              {article.dek}
            </motion.p>

            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ duration: 0.8, delay: 0.4 }}
              className="mt-10 flex items-center justify-between border-t border-ink/10 pt-6 font-sans text-xs uppercase tracking-[0.3em]"
            >
              <span className="text-ink/70">By {article.byline}</span>
              <span className="text-ink/50">{article.location}</span>
            </motion.div>
          </div>
        </header>

        <section className="px-6">
          <div className="mx-auto max-w-3xl">
            <motion.p
              initial={{ opacity: 0, y: 10 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true, amount: 0.5 }}
              transition={{ duration: 0.9, ease: [0.2, 0.6, 0.2, 1] }}
              className="drop-cap font-display font-light text-ink"
              style={{
                fontSize: "clamp(1.3rem, 1.9vw, 1.6rem)",
                lineHeight: 1.45,
              }}
            >
              {article.lead}
            </motion.p>

            <div className="mt-16 space-y-10">
              {article.body.map((block, i) => {
                if (block.type === "h2") {
                  return (
                    <motion.h2
                      key={i}
                      initial={{ opacity: 0, y: 10 }}
                      whileInView={{ opacity: 1, y: 0 }}
                      viewport={{ once: true, amount: 0.5 }}
                      transition={{ duration: 0.7 }}
                      className="pt-6 font-display font-light italic text-twilight"
                      style={{ fontSize: "clamp(1.5rem, 2.2vw, 1.9rem)" }}
                    >
                      {block.text}
                    </motion.h2>
                  );
                }
                if (block.type === "pull") {
                  return (
                    <motion.blockquote
                      key={i}
                      initial={{ opacity: 0 }}
                      whileInView={{ opacity: 1 }}
                      viewport={{ once: true, amount: 0.5 }}
                      transition={{ duration: 0.9 }}
                      className="relative my-12 pl-6 md:pl-8"
                    >
                      <motion.span
                        aria-hidden
                        initial={{ scaleY: 0 }}
                        whileInView={{ scaleY: 1 }}
                        viewport={{ once: true, amount: 0.5 }}
                        transition={{
                          duration: 1,
                          ease: [0.2, 0.6, 0.2, 1],
                        }}
                        className="absolute left-0 top-0 block h-full w-[3px] rounded-full bg-saffron"
                        style={{ transformOrigin: "top" }}
                      />
                      <p
                        className="font-display font-light italic text-twilight"
                        style={{
                          fontSize: "clamp(1.35rem, 2.1vw, 1.8rem)",
                          lineHeight: 1.3,
                        }}
                      >
                        {block.text}
                      </p>
                    </motion.blockquote>
                  );
                }
                return (
                  <motion.p
                    key={i}
                    initial={{ opacity: 0, y: 12 }}
                    whileInView={{ opacity: 1, y: 0 }}
                    viewport={{ once: true, amount: 0.2 }}
                    transition={{ duration: 0.7, ease: [0.2, 0.6, 0.2, 1] }}
                    className="font-sans text-ink/85"
                    style={{
                      fontSize: "clamp(1.05rem, 1.2vw, 1.15rem)",
                      lineHeight: 1.7,
                    }}
                  >
                    {block.text}
                  </motion.p>
                );
              })}
            </div>

            <motion.div
              initial={{ opacity: 0, y: 10 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true, amount: 0.4 }}
              transition={{ duration: 0.8 }}
              className="mt-20 border-t border-ink/10 pt-10"
            >
              <div className="mb-3 font-sans text-[11px] uppercase tracking-[0.3em] text-clay">
                Act on what you learn
              </div>
              <p
                className="font-display font-light text-ink"
                style={{ fontSize: "clamp(1.15rem, 1.5vw, 1.35rem)", lineHeight: 1.45 }}
              >
                Three verified organizations working on this story.
              </p>
              <ul className="mt-6 grid gap-4 md:grid-cols-3">
                {["Sea Watch Labs", "Human Rights at Sea", "Stella Maris"].map(
                  (name) => (
                    <li
                      key={name}
                      className="border border-ink/15 p-5 transition-colors hover:border-saffron"
                    >
                      <div className="font-display text-twilight">{name}</div>
                      <div className="mt-1 font-sans text-xs text-ink/55">
                        Vetted · Direct support
                      </div>
                    </li>
                  ),
                )}
              </ul>
            </motion.div>
          </div>
        </section>

        <section className="mt-32 border-t border-ink/10 px-6 py-24">
          <div className="mx-auto max-w-6xl">
            <div className="mb-10 font-sans text-xs uppercase tracking-[0.35em] text-clay">
              Keep reading
            </div>
            <div className="grid gap-8 md:grid-cols-2">
              {others.map((a) => (
                <Link
                  key={a.slug}
                  href={`/dispatches/${a.slug}`}
                  data-cursor-target
                  className="group block border border-ink/10 p-8 transition-colors hover:border-saffron md:p-10"
                >
                  <div className="mb-6 flex items-center justify-between font-sans text-[11px] uppercase tracking-[0.3em]">
                    <span className="text-twilight transition-colors group-hover:text-saffron">
                      {a.kicker}
                    </span>
                    <span className="text-ink/40">{a.topic}</span>
                  </div>
                  <h3
                    className="font-display font-light text-ink leading-[1.08]"
                    style={{ fontSize: "clamp(1.5rem, 2.2vw, 1.9rem)" }}
                  >
                    {a.headline}
                  </h3>
                  <p className="mt-4 font-sans text-[0.95rem] text-ink/65">
                    {a.dek}
                  </p>
                </Link>
              ))}
            </div>

            <div className="mt-16 flex items-center justify-between">
              <Link
                href="/dispatches"
                data-cursor-target
                className="group font-sans text-xs uppercase tracking-[0.3em] text-twilight"
              >
                <span className="border-b border-twilight/40 pb-1 transition-colors group-hover:border-saffron group-hover:text-saffron">
                  All dispatches
                </span>
              </Link>
              <Link
                href="/"
                data-cursor-target
                className="font-sans text-xs uppercase tracking-[0.3em] text-ink/50 transition-colors hover:text-saffron"
              >
                ← Navran
              </Link>
            </div>
          </div>
        </section>
      </article>
    </>
  );
}
