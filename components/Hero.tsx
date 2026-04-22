"use client";

import { motion } from "framer-motion";
import CompassStar from "./CompassStar";

export default function Hero() {
  const letters = "Navran".split("");

  return (
    <section className="relative flex min-h-[100svh] items-center justify-center overflow-hidden px-6">
      <div
        aria-hidden
        className="pointer-events-none absolute inset-0"
        style={{
          background:
            "radial-gradient(55% 50% at 50% 30%, rgba(198,124,62,0.14) 0%, rgba(198,124,62,0) 65%), radial-gradient(60% 50% at 50% 85%, rgba(61,43,92,0.12) 0%, rgba(61,43,92,0) 70%)",
        }}
      />

      <div className="relative z-10 flex flex-col items-center text-center">
        <motion.div
          initial={{ opacity: 0, y: 8 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8, delay: 0.05 }}
          className="mb-10 md:mb-14"
        >
          <CompassStar size={64} />
        </motion.div>

        <h1
          aria-label="Navran"
          className="font-display font-light text-twilight leading-[0.9] tracking-wordmark"
          style={{ fontSize: "clamp(4.5rem, 16vw, 14rem)" }}
        >
          <span className="inline-flex">
            {letters.map((l, i) => (
              <motion.span
                key={i}
                initial={{ opacity: 0, y: 18, letterSpacing: "-0.12em" }}
                animate={{ opacity: 1, y: 0, letterSpacing: "-0.04em" }}
                transition={{
                  duration: 1.1,
                  delay: 0.9 + i * 0.06,
                  ease: [0.2, 0.6, 0.2, 1],
                }}
                className="inline-block"
              >
                {l}
              </motion.span>
            ))}
          </span>
        </h1>

        <motion.p
          initial={{ opacity: 0, y: 12 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 1.2, delay: 1.7, ease: [0.2, 0.6, 0.2, 1] }}
          className="mt-6 font-display italic text-ink/70"
          style={{ fontSize: "clamp(1.1rem, 2.2vw, 1.65rem)" }}
        >
          Navigate what&rsquo;s hidden
        </motion.p>

        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ duration: 1.5, delay: 2.4 }}
          className="mt-24 flex flex-col items-center gap-3 text-xs uppercase tracking-[0.35em] text-ink/40"
        >
          <span>Scroll</span>
          <motion.span
            aria-hidden
            className="block h-10 w-px bg-ink/30"
            animate={{ scaleY: [0.3, 1, 0.3] }}
            transition={{
              duration: 2.4,
              repeat: Infinity,
              ease: "easeInOut",
            }}
            style={{ transformOrigin: "top" }}
          />
        </motion.div>
      </div>
    </section>
  );
}
