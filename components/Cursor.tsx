"use client";

import { motion, useMotionValue, useSpring } from "framer-motion";
import { useEffect, useState } from "react";

export default function Cursor() {
  const x = useMotionValue(-100);
  const y = useMotionValue(-100);
  const sx = useSpring(x, { stiffness: 260, damping: 28, mass: 0.4 });
  const sy = useSpring(y, { stiffness: 260, damping: 28, mass: 0.4 });

  const [enabled, setEnabled] = useState(false);
  const [hovered, setHovered] = useState(false);
  const [visible, setVisible] = useState(false);

  useEffect(() => {
    const canHover = window.matchMedia("(hover: hover) and (pointer: fine)");
    const wide = window.matchMedia("(min-width: 1024px)");
    const reduce = window.matchMedia("(prefers-reduced-motion: reduce)");
    setEnabled(canHover.matches && wide.matches && !reduce.matches);
  }, []);

  useEffect(() => {
    if (!enabled) return;

    const onMove = (e: MouseEvent) => {
      x.set(e.clientX);
      y.set(e.clientY);
      setVisible(true);
    };
    const onLeave = () => setVisible(false);
    const onOver = (e: MouseEvent) => {
      const t = e.target as HTMLElement | null;
      if (!t) return;
      const interactive = t.closest(
        "a, button, input, [data-cursor-target]",
      );
      setHovered(Boolean(interactive));
    };

    window.addEventListener("mousemove", onMove);
    window.addEventListener("mouseover", onOver);
    document.body.addEventListener("mouseleave", onLeave);
    return () => {
      window.removeEventListener("mousemove", onMove);
      window.removeEventListener("mouseover", onOver);
      document.body.removeEventListener("mouseleave", onLeave);
    };
  }, [enabled, x, y]);

  if (!enabled) return null;

  return (
    <motion.div
      aria-hidden
      className="pointer-events-none fixed left-0 top-0 z-[60]"
      style={{
        x: sx,
        y: sy,
        opacity: visible ? 1 : 0,
      }}
    >
      <motion.div
        className="rounded-full bg-saffron"
        animate={{
          width: hovered ? 36 : 10,
          height: hovered ? 36 : 10,
          opacity: hovered ? 0.25 : 0.85,
        }}
        transition={{ type: "spring", stiffness: 240, damping: 22 }}
        style={{ translateX: "-50%", translateY: "-50%" }}
      />
    </motion.div>
  );
}
