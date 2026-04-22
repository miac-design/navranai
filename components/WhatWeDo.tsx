"use client";

import { motion } from "framer-motion";

const items = [
  {
    kicker: "01",
    title: "See what's hidden",
    body: "Navran surfaces the stories and data that most outlets miss — the patterns, the individuals, the systems that let harm continue.",
    icon: (
      <svg viewBox="0 0 60 60" fill="none" className="h-14 w-14">
        <motion.circle
          cx={30}
          cy={30}
          r={14}
          stroke="#C67C3E"
          strokeWidth={1.25}
          initial={{ pathLength: 0 }}
          whileInView={{ pathLength: 1 }}
          viewport={{ once: true, amount: 0.6 }}
          transition={{ duration: 1.4, ease: [0.2, 0.6, 0.2, 1] }}
        />
        <motion.circle
          cx={30}
          cy={30}
          r={4}
          fill="#3D2B5C"
          initial={{ scale: 0 }}
          whileInView={{ scale: 1 }}
          viewport={{ once: true, amount: 0.6 }}
          transition={{ duration: 0.5, delay: 0.6 }}
        />
      </svg>
    ),
  },
  {
    kicker: "02",
    title: "Understand what's happening",
    body: "Plain-spoken context from researchers, frontline workers, and survivors — not statistics alone, but the meaning behind them.",
    icon: (
      <svg viewBox="0 0 60 60" fill="none" className="h-14 w-14">
        {[12, 22, 32].map((y, i) => (
          <motion.line
            key={i}
            x1={10}
            x2={50}
            y1={y}
            y2={y}
            stroke="#C67C3E"
            strokeWidth={1.25}
            strokeLinecap="round"
            initial={{ pathLength: 0 }}
            whileInView={{ pathLength: 1 }}
            viewport={{ once: true, amount: 0.6 }}
            transition={{
              duration: 1,
              delay: 0.1 + i * 0.18,
              ease: [0.2, 0.6, 0.2, 1],
            }}
          />
        ))}
        <motion.circle
          cx={42}
          cy={44}
          r={5}
          fill="#3D2B5C"
          initial={{ scale: 0 }}
          whileInView={{ scale: 1 }}
          viewport={{ once: true, amount: 0.6 }}
          transition={{ duration: 0.5, delay: 0.9 }}
        />
      </svg>
    ),
  },
  {
    kicker: "03",
    title: "Act on what you learn",
    body: "Every dispatch ends with a door: a verified organization, a petition, a role, a way to move from reading to doing.",
    icon: (
      <svg viewBox="0 0 60 60" fill="none" className="h-14 w-14">
        <motion.path
          d="M14 30 L46 30"
          stroke="#C67C3E"
          strokeWidth={1.25}
          strokeLinecap="round"
          initial={{ pathLength: 0 }}
          whileInView={{ pathLength: 1 }}
          viewport={{ once: true, amount: 0.6 }}
          transition={{ duration: 1, ease: [0.2, 0.6, 0.2, 1] }}
        />
        <motion.path
          d="M38 22 L46 30 L38 38"
          stroke="#3D2B5C"
          strokeWidth={1.25}
          strokeLinecap="round"
          strokeLinejoin="round"
          fill="none"
          initial={{ pathLength: 0 }}
          whileInView={{ pathLength: 1 }}
          viewport={{ once: true, amount: 0.6 }}
          transition={{ duration: 0.8, delay: 0.6 }}
        />
      </svg>
    ),
  },
];

export default function WhatWeDo() {
  return (
    <section
      className="relative py-32 md:py-40"
      style={{ backgroundColor: "var(--parchment)" }}
    >
      <div className="mx-auto max-w-6xl px-6">
        <motion.div
          initial={{ opacity: 0, x: -12 }}
          whileInView={{ opacity: 1, x: 0 }}
          viewport={{ once: true, amount: 0.6 }}
          transition={{ duration: 0.8 }}
          className="mb-20 font-sans text-xs uppercase tracking-[0.35em] text-clay"
        >
          II. What Navran does
        </motion.div>

        <motion.div
          className="grid gap-14 md:grid-cols-3 md:gap-10"
          initial="hidden"
          whileInView="show"
          viewport={{ once: true, amount: 0.25 }}
          variants={{
            hidden: {},
            show: { transition: { staggerChildren: 0.18 } },
          }}
        >
          {items.map((item) => (
            <motion.div
              key={item.kicker}
              variants={{
                hidden: { opacity: 0, y: 28 },
                show: {
                  opacity: 1,
                  y: 0,
                  transition: {
                    duration: 0.9,
                    ease: [0.2, 0.6, 0.2, 1],
                  },
                },
              }}
              className="flex flex-col"
            >
              <div className="mb-6">{item.icon}</div>
              <div className="mb-3 font-sans text-xs uppercase tracking-[0.3em] text-clay">
                {item.kicker}
              </div>
              <h3
                className="mb-4 font-display font-light text-twilight leading-[1.05]"
                style={{ fontSize: "clamp(1.5rem, 2.6vw, 2rem)" }}
              >
                {item.title}
              </h3>
              <p className="font-sans text-base leading-relaxed text-ink/75 md:text-[1.05rem]">
                {item.body}
              </p>
            </motion.div>
          ))}
        </motion.div>
      </div>
    </section>
  );
}
