"use client";

import { motion } from "framer-motion";

export default function BuiltBy() {
  return (
    <section
      className="relative py-24 md:py-32"
      style={{ backgroundColor: "var(--dawn)" }}
    >
      <div className="mx-auto max-w-3xl px-6 text-center">
        <motion.div
          initial={{ opacity: 0, y: 8 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true, amount: 0.6 }}
          transition={{ duration: 0.8 }}
          className="mb-6 font-sans text-[11px] uppercase tracking-[0.35em] text-clay"
        >
          Built by
        </motion.div>

        <motion.p
          initial={{ opacity: 0, y: 14 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true, amount: 0.4 }}
          transition={{ duration: 0.9, ease: [0.2, 0.6, 0.2, 1] }}
          className="font-display font-light text-ink/80 leading-[1.4]"
          style={{ fontSize: "clamp(1.05rem, 1.4vw, 1.25rem)" }}
        >
          An editorial project incubated at the{" "}
          <span className="text-twilight">Austin AI Hub</span>, developed in
          partnership with{" "}
          <span className="text-twilight">UN Human Rights</span>, and grounded
          in three years of research on what moves readers from awareness to
          action.
        </motion.p>
      </div>
    </section>
  );
}
