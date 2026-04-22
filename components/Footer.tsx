"use client";

import { motion, useInView } from "framer-motion";
import { useRef, useState } from "react";

export default function Footer() {
  const ref = useRef<HTMLDivElement>(null);
  const inView = useInView(ref, { once: true, amount: 0.4 });
  const [email, setEmail] = useState("");
  const [submitted, setSubmitted] = useState(false);
  const letters = "NAVRAN".split("");

  return (
    <footer
      className="relative overflow-hidden"
      style={{ backgroundColor: "var(--twilight)" }}
    >
      <div className="mx-auto max-w-6xl px-6 py-28 md:py-40">
        <div className="grid gap-16 md:grid-cols-2 md:gap-24">
          <div>
            <motion.h2
              initial={{ opacity: 0, y: 14 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true, amount: 0.5 }}
              transition={{ duration: 1, ease: [0.2, 0.6, 0.2, 1] }}
              className="font-display font-light text-dawn leading-[1.05] tracking-tight"
              style={{ fontSize: "clamp(2rem, 4vw, 3.25rem)" }}
            >
              Read the first <span className="italic">dispatch</span>.
            </motion.h2>
            <motion.p
              initial={{ opacity: 0 }}
              whileInView={{ opacity: 1 }}
              viewport={{ once: true, amount: 0.5 }}
              transition={{ duration: 1, delay: 0.3 }}
              className="mt-5 max-w-md font-sans text-dawn/60"
            >
              One story a month. Carefully made. No tracking pixels, no clever
              copy, no calls to rage.
            </motion.p>

            <motion.div
              initial={{ opacity: 0, y: 10 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true, amount: 0.5 }}
              transition={{ duration: 0.8, delay: 0.5 }}
              className="mt-10"
            >
              <a
                data-cursor-target
                href="#"
                className="group relative inline-flex items-center overflow-hidden border border-dawn/30 px-8 py-4 font-sans text-sm uppercase tracking-[0.28em]"
              >
                <span
                  aria-hidden
                  className="absolute inset-0 origin-left scale-x-0 bg-saffron transition-transform duration-500 ease-[cubic-bezier(0.2,0.6,0.2,1)] group-hover:scale-x-100"
                />
                <span className="relative z-10 text-dawn transition-colors duration-500 group-hover:text-twilight">
                  Read the first dispatch
                </span>
              </a>
            </motion.div>
          </div>

          <div className="md:pt-4">
            <motion.form
              initial={{ opacity: 0, y: 10 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true, amount: 0.5 }}
              transition={{ duration: 0.9, delay: 0.4 }}
              onSubmit={(e) => {
                e.preventDefault();
                if (email) setSubmitted(true);
              }}
              className="relative"
            >
              <label className="mb-4 block font-sans text-[11px] uppercase tracking-[0.35em] text-dawn/50">
                Get the first dispatch
              </label>
              <div className="flex items-center border-b border-dawn/30 pb-3 transition-colors focus-within:border-saffron">
                <input
                  data-cursor-target
                  type="email"
                  required
                  placeholder="you@somewhere"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  disabled={submitted}
                  className="w-full bg-transparent font-sans text-lg text-dawn placeholder:text-dawn/30 focus:outline-none"
                />
                <button
                  data-cursor-target
                  type="submit"
                  disabled={submitted}
                  aria-label="Subscribe"
                  className="ml-4 font-sans text-sm uppercase tracking-[0.28em] text-saffron transition-opacity hover:opacity-70"
                >
                  {submitted ? "Received" : "Send →"}
                </button>
              </div>
              <p className="mt-3 font-sans text-xs text-dawn/40">
                No list sharing. Unsubscribe is one click.
              </p>
            </motion.form>
          </div>
        </div>

        <div ref={ref} className="mt-32 flex items-end justify-between">
          <div className="flex items-baseline gap-3 md:gap-5">
            {letters.map((l, i) => (
              <motion.span
                key={i}
                initial={{ opacity: 0, y: 8 }}
                animate={
                  inView ? { opacity: 1, y: 0 } : { opacity: 0, y: 8 }
                }
                transition={{
                  duration: 0.8,
                  delay: i * 0.12,
                  ease: [0.2, 0.6, 0.2, 1],
                }}
                className="font-display font-light text-dawn"
                style={{ fontSize: "clamp(1.4rem, 2.4vw, 2rem)" }}
              >
                {l}
              </motion.span>
            ))}
          </div>
          <div className="text-right font-sans text-xs uppercase tracking-[0.3em] text-dawn/40">
            <div>© {new Date().getFullYear()} Navran</div>
            <div className="mt-2">Austin · Geneva</div>
          </div>
        </div>
      </div>
    </footer>
  );
}
