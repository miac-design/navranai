"use client";

import {
  motion,
  MotionValue,
  useScroll,
  useSpring,
  useTransform,
} from "framer-motion";
import { useMemo, useRef } from "react";

const STAR_COUNT = 120;
const TARGET = 82000;

function seeded(i: number) {
  const x = Math.sin(i * 928.5471) * 43758.5453;
  return x - Math.floor(x);
}

type Star = { x: number; y: number; size: number; delay: number };

function buildStars(): Star[] {
  return Array.from({ length: STAR_COUNT }).map((_, i) => {
    const x = seeded(i + 1) * 100;
    const y = seeded(i + 200) * 100;
    const size = 1 + seeded(i + 300) * 2.6;
    const delay = seeded(i + 400);
    return { x, y, size, delay };
  });
}

function Star({
  star,
  progress,
}: {
  star: Star;
  progress: MotionValue<number>;
}) {
  const start = 0.1 + star.delay * 0.55;
  const end = start + 0.1;
  const opacity = useTransform(progress, [start, end], [0, 1]);
  const scale = useTransform(progress, [start, end], [0.2, 1]);

  return (
    <motion.span
      className="absolute block rounded-full bg-dawn"
      style={{
        left: `${star.x}%`,
        top: `${star.y}%`,
        width: star.size,
        height: star.size,
        opacity,
        scale,
        boxShadow: "0 0 6px rgba(251,247,237,0.8)",
      }}
    />
  );
}

function Counter({ progress }: { progress: MotionValue<number> }) {
  const raw = useTransform(progress, [0.15, 0.8], [0, TARGET]);
  const smoothed = useSpring(raw, { stiffness: 80, damping: 22, mass: 0.4 });
  const display = useTransform(smoothed, (v) =>
    Math.round(v).toLocaleString("en-US"),
  );
  return (
    <motion.span
      className="font-display font-light text-dawn"
      style={{ fontSize: "clamp(4rem, 12vw, 10rem)", lineHeight: 0.9 }}
    >
      {display}
    </motion.span>
  );
}

export default function Constellation() {
  const ref = useRef<HTMLElement>(null);
  const stars = useMemo(buildStars, []);

  const { scrollYProgress } = useScroll({
    target: ref,
    offset: ["start end", "end start"],
  });

  const bgOpacity = useTransform(
    scrollYProgress,
    [0, 0.15, 0.85, 1],
    [0, 1, 1, 0],
  );
  const haloOpacity = useTransform(
    scrollYProgress,
    [0.05, 0.3, 0.7, 1],
    [0, 0.5, 0.5, 0],
  );
  const textOpacity = useTransform(
    scrollYProgress,
    [0.25, 0.45, 0.75, 0.9],
    [0, 1, 1, 0],
  );

  return (
    <section ref={ref} className="relative" style={{ height: "260vh" }}>
      <div className="sticky top-0 flex h-screen w-full items-center justify-center overflow-hidden">
        <motion.div
          aria-hidden
          className="absolute inset-0"
          style={{ backgroundColor: "#0F0A1C", opacity: bgOpacity }}
        />
        <motion.div
          aria-hidden
          className="absolute inset-0"
          style={{
            opacity: haloOpacity,
            background:
              "radial-gradient(50% 50% at 50% 50%, rgba(198,124,62,0.20) 0%, rgba(61,43,92,0) 60%)",
          }}
        />

        <motion.div
          aria-hidden
          className="absolute inset-0"
          style={{ opacity: bgOpacity }}
        >
          {stars.map((s, i) => (
            <Star key={i} star={s} progress={scrollYProgress} />
          ))}
        </motion.div>

        <motion.div
          className="relative z-10 flex flex-col items-center px-6 text-center"
          style={{ opacity: textOpacity }}
        >
          <div className="mb-6 font-sans text-xs uppercase tracking-[0.35em] text-saffron">
            V. Impact
          </div>

          <div className="flex items-baseline gap-3">
            <Counter progress={scrollYProgress} />
            <span
              className="font-display font-light text-saffron"
              style={{ fontSize: "clamp(2rem, 5vw, 4rem)" }}
            >
              +
            </span>
          </div>

          <p
            className="mt-8 max-w-2xl font-display font-light italic text-dawn/85"
            style={{ fontSize: "clamp(1.15rem, 1.8vw, 1.5rem)", lineHeight: 1.4 }}
          >
            Survivors identified through the National Human Trafficking
            Hotline since 2007.
          </p>

          <p className="mt-6 font-sans text-[11px] uppercase tracking-[0.3em] text-dawn/50">
            Source · Polaris Project · 2025
          </p>

          <p
            className="mt-12 max-w-xl font-sans text-dawn/60"
            style={{ fontSize: "clamp(0.95rem, 1.1vw, 1.05rem)", lineHeight: 1.6 }}
          >
            Every one of those numbers is a person. Every call started with
            someone noticing. The work of this platform is to make that
            noticing easier, faster, and more frequent.
          </p>
        </motion.div>
      </div>
    </section>
  );
}
