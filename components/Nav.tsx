"use client";

import Link from "next/link";
import { motion } from "framer-motion";
import CompassStar from "./CompassStar";

export default function Nav({ variant = "dawn" }: { variant?: "dawn" | "twilight" }) {
  const textColor = variant === "twilight" ? "text-dawn" : "text-ink";
  const accent = variant === "twilight" ? "text-saffron" : "text-twilight";
  const hover = variant === "twilight" ? "hover:text-saffron" : "hover:text-saffron";

  return (
    <motion.header
      initial={{ opacity: 0, y: -8 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.7, ease: [0.2, 0.6, 0.2, 1] }}
      className={`absolute inset-x-0 top-0 z-30 ${textColor}`}
    >
      <div className="mx-auto flex max-w-6xl items-center justify-between px-6 py-6 md:py-8">
        <Link
          href="/"
          data-cursor-target
          className="group flex items-center gap-3"
          aria-label="Navran home"
        >
          <CompassStar size={22} />
          <span
            className={`font-display font-light tracking-wordmark transition-colors ${accent} group-hover:text-saffron`}
            style={{ fontSize: "1.2rem" }}
          >
            Navran
          </span>
        </Link>
        <nav className="flex items-center gap-8 font-sans text-[11px] uppercase tracking-[0.3em]">
          <Link
            data-cursor-target
            href="/#how-its-made"
            className={`hidden opacity-75 transition-opacity ${hover} hover:opacity-100 md:inline`}
          >
            How it works
          </Link>
          <Link
            data-cursor-target
            href="/dispatches"
            className={`opacity-75 transition-opacity ${hover} hover:opacity-100`}
          >
            Dispatches
          </Link>
          <Link
            data-cursor-target
            href="/#mission"
            className={`hidden opacity-75 transition-opacity ${hover} hover:opacity-100 md:inline`}
          >
            Mission
          </Link>
          <Link
            data-cursor-target
            href="/#subscribe"
            className={`border px-4 py-2 transition-colors ${
              variant === "twilight"
                ? "border-dawn/30 hover:border-saffron hover:text-saffron"
                : "border-ink/20 hover:border-saffron hover:text-saffron"
            }`}
          >
            Subscribe
          </Link>
        </nav>
      </div>
    </motion.header>
  );
}
