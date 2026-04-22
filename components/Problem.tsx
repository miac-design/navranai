"use client";

import {
  motion,
  MotionValue,
  useScroll,
  useTransform,
} from "framer-motion";
import { useRef } from "react";

const COLS = 18;
const ROWS = 8;

const transforms = [
  { from: "hidden", to: "named" },
  { from: "silent", to: "heard" },
  { from: "alone", to: "counted" },
  { from: "invisible", to: "visible" },
];

function WordSwap({
  index,
  from,
  to,
  progress,
}: {
  index: number;
  from: string;
  to: string;
  progress: MotionValue<number>;
}) {
  const start = 0.35 + index * 0.08;
  const mid = start + 0.05;
  const end = mid + 0.05;

  const fromOpacity = useTransform(progress, [start, mid], [1, 0]);
  const fromBlur = useTransform(progress, [start, mid], [0, 8]);
  const fromFilter = useTransform(fromBlur, (b) => `blur(${b}px)`);
  const fromY = useTransform(progress, [start, mid], [0, -12]);

  const toOpacity = useTransform(progress, [mid, end], [0, 1]);
  const toBlur = useTransform(progress, [mid, end], [8, 0]);
  const toFilter = useTransform(toBlur, (b) => `blur(${b}px)`);
  const toY = useTransform(progress, [mid, end], [12, 0]);

  return (
    <div className="relative flex items-baseline justify-between border-b border-ink/15 py-6">
      <div className="relative h-[1.1em] w-full font-display font-light tracking-tight">
        <motion.span
          className="absolute inset-0 text-ink/40 line-through decoration-clay/50 decoration-1"
          style={{
            opacity: fromOpacity,
            filter: fromFilter,
            y: fromY,
            fontSize: "clamp(2rem, 5vw, 4.5rem)",
          }}
        >
          {from}
        </motion.span>
        <motion.span
          className="absolute inset-0 italic text-twilight"
          style={{
            opacity: toOpacity,
            filter: toFilter,
            y: toY,
            fontSize: "clamp(2rem, 5vw, 4.5rem)",
          }}
        >
          {to}
        </motion.span>
      </div>
    </div>
  );
}

function Tile({
  index,
  progress,
}: {
  index: number;
  progress: MotionValue<number>;
}) {
  const col = index % COLS;
  const row = Math.floor(index / COLS);
  const diag = (col + row) / (COLS + ROWS - 2);
  const threshold = 0.15 + diag * 0.65;

  const reveal = useTransform(
    progress,
    [threshold - 0.08, threshold + 0.08],
    [0, 1],
  );
  const baseOpacity = useTransform(reveal, (v) => 0.35 + v * 0.55);

  return (
    <span className="relative block h-2 w-full md:h-2.5">
      <motion.span
        className="absolute inset-0 rounded-full"
        style={{ backgroundColor: "var(--twilight)", opacity: baseOpacity }}
      />
      <motion.span
        className="absolute inset-0 rounded-full"
        style={{ backgroundColor: "var(--saffron)", opacity: reveal }}
      />
    </span>
  );
}

export default function Problem() {
  const ref = useRef<HTMLElement>(null);
  const { scrollYProgress } = useScroll({
    target: ref,
    offset: ["start end", "end start"],
  });

  const filter = useTransform(
    scrollYProgress,
    [0, 0.45, 0.7],
    ["blur(14px)", "blur(0px)", "blur(0px)"],
  );
  const opacity = useTransform(scrollYProgress, [0, 0.3, 0.6], [0.3, 0.85, 1]);

  return (
    <section
      ref={ref}
      className="relative overflow-hidden py-40 md:py-56"
      style={{ backgroundColor: "var(--dawn)" }}
    >
      <div className="mx-auto max-w-6xl px-6">
        <motion.div
          initial={{ opacity: 0, x: -12 }}
          whileInView={{ opacity: 1, x: 0 }}
          viewport={{ once: true, amount: 0.5 }}
          transition={{ duration: 0.8 }}
          className="mb-20 font-sans text-xs uppercase tracking-[0.35em] text-clay"
        >
          I. The problem
        </motion.div>

        <motion.p
          style={{ filter, opacity }}
          className="font-display font-light text-ink leading-[1.12] tracking-tightest"
        >
          <span style={{ fontSize: "clamp(1.75rem, 4.6vw, 4rem)" }}>
            Harm hides. Trafficking, displacement, exclusion &mdash; most of
            what damages people most survives because it&rsquo;s never named.{" "}
            <span className="italic text-twilight">
              Navran exists to change what gets seen.
            </span>
          </span>
        </motion.p>

        <div className="mt-24 md:mt-32">
          <div className="mb-8 font-sans text-[11px] uppercase tracking-[0.3em] text-clay">
            What we change
          </div>
          <div>
            {transforms.map((t, i) => (
              <WordSwap
                key={t.from}
                index={i}
                from={t.from}
                to={t.to}
                progress={scrollYProgress}
              />
            ))}
          </div>
        </div>

        <div className="relative mt-32 md:mt-40">
          <div
            className="grid gap-[6px] md:gap-2"
            style={{ gridTemplateColumns: `repeat(${COLS}, minmax(0, 1fr))` }}
            aria-hidden
          >
            {Array.from({ length: COLS * ROWS }).map((_, i) => (
              <Tile key={i} index={i} progress={scrollYProgress} />
            ))}
          </div>

          <div className="mt-6 flex justify-between font-sans text-[11px] uppercase tracking-[0.3em] text-ink/40">
            <span>hidden</span>
            <span>seen</span>
          </div>
        </div>
      </div>
    </section>
  );
}
