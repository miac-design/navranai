"use client";

import { motion } from "framer-motion";

const quote =
  "Awareness, when it works, is the act of making the hidden visible — and giving people a way to move from seeing to doing.";

export default function Mission() {
  const words = quote.split(" ");

  return (
    <section
      className="relative py-32 md:py-48"
      style={{ backgroundColor: "var(--parchment)" }}
    >
      <div className="mx-auto grid max-w-6xl grid-cols-12 gap-10 px-6">
        <motion.div
          initial={{ opacity: 0, x: -12 }}
          whileInView={{ opacity: 1, x: 0 }}
          viewport={{ once: true, amount: 0.6 }}
          transition={{ duration: 0.8 }}
          className="col-span-12 mb-4 font-sans text-xs uppercase tracking-[0.35em] text-clay md:col-span-12"
        >
          IV. The mission
        </motion.div>

        <div className="col-span-12 md:col-span-7">
          <motion.p
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true, amount: 0.4 }}
            transition={{ duration: 1, ease: [0.2, 0.6, 0.2, 1] }}
            className="drop-cap font-display font-light text-ink leading-[1.35] md:leading-[1.3]"
            style={{ fontSize: "clamp(1.15rem, 1.6vw, 1.4rem)" }}
          >
            Navran was built on a simple premise: harm that is invisible cannot
            be addressed. Most of the world&rsquo;s most persistent injuries
            &mdash; human trafficking, forced displacement, exclusion from the
            systems that decide who counts &mdash; survive because they happen
            quietly, in places and to people that existing media does not
            cover. We are assembling an editorial practice that pairs original
            reporting with structured context, and we are using AI where it
            helps us see patterns that would otherwise stay buried. The point
            is not the technology. The point is the noticing.
          </motion.p>
        </div>

        <div className="col-span-12 md:col-span-5 md:pt-10">
          <div className="relative pl-6 md:pl-8">
            <motion.span
              aria-hidden
              className="absolute left-0 top-0 block w-[3px] rounded-full"
              style={{
                backgroundColor: "var(--saffron)",
                height: "100%",
                transformOrigin: "top",
              }}
              initial={{ scaleY: 0 }}
              whileInView={{ scaleY: 1 }}
              viewport={{ once: true, amount: 0.5 }}
              transition={{ duration: 1.1, ease: [0.2, 0.6, 0.2, 1] }}
            />
            <motion.blockquote
              initial="hidden"
              whileInView="show"
              viewport={{ once: true, amount: 0.5 }}
              variants={{
                hidden: {},
                show: { transition: { staggerChildren: 0.05, delayChildren: 0.6 } },
              }}
              className="font-display font-light italic text-twilight leading-[1.2]"
              style={{ fontSize: "clamp(1.4rem, 2.2vw, 1.9rem)" }}
            >
              {words.map((w, i) => (
                <motion.span
                  key={i}
                  variants={{
                    hidden: { opacity: 0, y: 8 },
                    show: {
                      opacity: 1,
                      y: 0,
                      transition: { duration: 0.5, ease: "easeOut" },
                    },
                  }}
                  className="inline-block"
                >
                  {w}&nbsp;
                </motion.span>
              ))}
            </motion.blockquote>
          </div>
        </div>
      </div>
    </section>
  );
}
