"use client";

import { motion } from "framer-motion";

const steps = [
  { n: "01", label: "Scan", detail: "12 verified sources · Reuters, AP, DOJ, Polaris" },
  { n: "02", label: "Plan", detail: "GPT-4o selects the week's story" },
  { n: "03", label: "Write", detail: "5 posts, 5 purposes, 5 audiences" },
  { n: "04", label: "Check", detail: "Ethics + compliance · auto-fix" },
  { n: "05", label: "Approve", detail: "Human-in-the-loop · nothing ships alone" },
];

const week = [
  { day: "Mon", type: "Breaking", score: 8.4, audience: "General Public", color: "#C67C3E" },
  { day: "Tue", type: "Stat Card", score: 9.1, audience: "Educators", color: "#C67C3E" },
  { day: "Wed", type: "Explainer", score: 8.8, audience: "Parents", color: "#C67C3E" },
  { day: "Thu", type: "Action", score: 9.0, audience: "Students", color: "#C67C3E" },
  { day: "Fri", type: "Hope", score: 9.3, audience: "General Public", color: "#C67C3E" },
];

export default function HowItsMade() {
  return (
    <section
      className="relative overflow-hidden py-32 md:py-40"
      style={{ backgroundColor: "var(--twilight)", color: "var(--dawn)" }}
    >
      <div
        aria-hidden
        className="pointer-events-none absolute inset-0 opacity-40"
        style={{
          background:
            "radial-gradient(55% 60% at 18% 18%, rgba(198,124,62,0.18) 0%, rgba(198,124,62,0) 60%), radial-gradient(60% 50% at 82% 88%, rgba(168,90,58,0.16) 0%, rgba(168,90,58,0) 70%)",
        }}
      />

      <div className="relative mx-auto max-w-6xl px-6">
        <motion.div
          initial={{ opacity: 0, x: -12 }}
          whileInView={{ opacity: 1, x: 0 }}
          viewport={{ once: true, amount: 0.6 }}
          transition={{ duration: 0.8 }}
          className="mb-6 font-sans text-xs uppercase tracking-[0.35em] text-saffron"
        >
          III. How it's made
        </motion.div>

        <motion.h2
          initial={{ opacity: 0, y: 14 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true, amount: 0.4 }}
          transition={{ duration: 1, ease: [0.2, 0.6, 0.2, 1] }}
          className="max-w-4xl font-display font-light leading-[1.02] tracking-tight"
          style={{ fontSize: "clamp(2rem, 4.8vw, 4rem)" }}
        >
          A command center for the work.{" "}
          <span className="italic text-saffron">Not a headline generator.</span>
        </motion.h2>

        <motion.p
          initial={{ opacity: 0 }}
          whileInView={{ opacity: 1 }}
          viewport={{ once: true, amount: 0.4 }}
          transition={{ duration: 1, delay: 0.3 }}
          className="mt-8 max-w-2xl font-sans text-dawn/65"
          style={{ fontSize: "clamp(1rem, 1.2vw, 1.1rem)", lineHeight: 1.65 }}
        >
          redM Command is the tool we built with Austin AI Hub. It turns a
          single verified news story into a week of ethical, audience-tuned
          social posts — written, illustrated, scored, and compliance-checked
          by AI, with a human signing off every single post.
        </motion.p>

        <div className="relative mt-20 md:mt-28">
          <motion.div
            initial="hidden"
            whileInView="show"
            viewport={{ once: true, amount: 0.2 }}
            variants={{
              hidden: {},
              show: { transition: { staggerChildren: 0.14 } },
            }}
            className="relative grid gap-6 md:grid-cols-5 md:gap-4"
          >
            <motion.div
              aria-hidden
              initial={{ scaleX: 0 }}
              whileInView={{ scaleX: 1 }}
              viewport={{ once: true, amount: 0.4 }}
              transition={{ duration: 1.6, delay: 0.2, ease: [0.2, 0.6, 0.2, 1] }}
              className="absolute left-0 right-0 top-8 hidden h-px origin-left bg-dawn/20 md:block"
            />

            {steps.map((s) => (
              <motion.div
                key={s.n}
                variants={{
                  hidden: { opacity: 0, y: 18 },
                  show: {
                    opacity: 1,
                    y: 0,
                    transition: { duration: 0.8, ease: [0.2, 0.6, 0.2, 1] },
                  },
                }}
                className="relative"
              >
                <div className="flex items-center gap-3 md:block">
                  <span
                    className="relative z-10 inline-flex h-16 w-16 items-center justify-center rounded-full border border-dawn/20 font-display text-saffron"
                    style={{ backgroundColor: "var(--twilight)" }}
                  >
                    {s.n}
                  </span>
                </div>
                <div className="mt-5 font-display text-xl text-dawn">
                  {s.label}
                </div>
                <div className="mt-2 font-sans text-xs leading-relaxed text-dawn/50">
                  {s.detail}
                </div>
              </motion.div>
            ))}
          </motion.div>
        </div>

        <div className="mt-28 md:mt-36">
          <div className="mb-8 flex flex-wrap items-end justify-between gap-4">
            <div>
              <div className="font-sans text-[11px] uppercase tracking-[0.3em] text-saffron">
                This week's campaign
              </div>
              <div className="mt-3 font-display font-light text-dawn" style={{ fontSize: "clamp(1.3rem, 2vw, 1.7rem)" }}>
                From one story: <span className="italic">five posts</span>, five audiences.
              </div>
            </div>
            <div className="font-sans text-xs text-dawn/50">
              Source: DOJ · AI confidence: High · 5/5 ready
            </div>
          </div>

          <motion.div
            initial="hidden"
            whileInView="show"
            viewport={{ once: true, amount: 0.2 }}
            variants={{
              hidden: {},
              show: { transition: { staggerChildren: 0.1 } },
            }}
            className="grid gap-3 md:grid-cols-5"
          >
            {week.map((p, i) => (
              <motion.div
                key={p.day}
                variants={{
                  hidden: { opacity: 0, y: 18 },
                  show: {
                    opacity: 1,
                    y: 0,
                    transition: { duration: 0.7, ease: [0.2, 0.6, 0.2, 1] },
                  },
                }}
                whileHover={{ y: -4 }}
                className="flex flex-col justify-between border border-dawn/15 bg-dawn/[0.03] p-5 backdrop-blur-sm"
                style={{ minHeight: "14rem" }}
              >
                <div>
                  <div className="flex items-center justify-between font-sans text-[10px] uppercase tracking-[0.3em] text-dawn/50">
                    <span>{p.day}</span>
                    <span className="text-saffron">{p.score}</span>
                  </div>
                  <div
                    className="mt-5 font-display text-dawn"
                    style={{ fontSize: "1.15rem" }}
                  >
                    {p.type}
                  </div>
                  <div className="mt-1 font-sans text-[11px] text-dawn/45">
                    {p.audience}
                  </div>
                </div>
                <div className="mt-6 flex items-center justify-between">
                  <motion.span
                    initial={{ scaleX: 0 }}
                    whileInView={{ scaleX: 1 }}
                    viewport={{ once: true, amount: 0.6 }}
                    transition={{
                      duration: 0.9,
                      delay: 0.3 + i * 0.08,
                      ease: [0.2, 0.6, 0.2, 1],
                    }}
                    className="block h-px w-16 origin-left bg-saffron"
                  />
                  <span className="font-sans text-[10px] uppercase tracking-[0.3em] text-dawn/60">
                    Compliant
                  </span>
                </div>
              </motion.div>
            ))}
          </motion.div>
        </div>

        <div className="mt-24 grid gap-10 border-t border-dawn/15 pt-12 md:grid-cols-3">
          {[
            {
              stat: "98%",
              label: "Compliance score",
              body: "Every post runs through a regex guardrail and an AI deep-check. Flagged terms like 'rescued' are auto-corrected to 'identified' before a human ever sees them.",
            },
            {
              stat: "0 to 5 in 3 min",
              label: "Campaign speed",
              body: "One approved story in — five platform-ready posts out in under three minutes. Each with a generated image and per-platform character counts.",
            },
            {
              stat: "EN · ES · FR · PT",
              label: "One-click translation",
              body: "Campaigns ship in English and can be translated to Spanish, French, or Portuguese from the calendar view.",
            },
          ].map((item) => (
            <motion.div
              key={item.label}
              initial={{ opacity: 0, y: 14 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true, amount: 0.5 }}
              transition={{ duration: 0.9, ease: [0.2, 0.6, 0.2, 1] }}
            >
              <div
                className="font-display text-saffron"
                style={{ fontSize: "clamp(1.8rem, 3vw, 2.4rem)" }}
              >
                {item.stat}
              </div>
              <div className="mt-2 font-sans text-[11px] uppercase tracking-[0.3em] text-dawn/60">
                {item.label}
              </div>
              <div className="mt-4 font-sans text-sm leading-relaxed text-dawn/70">
                {item.body}
              </div>
            </motion.div>
          ))}
        </div>
      </div>
    </section>
  );
}
