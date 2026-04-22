"use client";

import { motion } from "framer-motion";

type Props = {
  size?: number;
  className?: string;
};

export default function CompassStar({ size = 56, className }: Props) {
  const rays = [
    { d: "M50 6 L50 30", delay: 0.1 },
    { d: "M94 50 L70 50", delay: 0.18 },
    { d: "M50 94 L50 70", delay: 0.26 },
    { d: "M6 50 L30 50", delay: 0.34 },
    { d: "M81 19 L66 34", delay: 0.42 },
    { d: "M81 81 L66 66", delay: 0.5 },
    { d: "M19 81 L34 66", delay: 0.58 },
    { d: "M19 19 L34 34", delay: 0.66 },
  ];

  return (
    <svg
      width={size}
      height={size}
      viewBox="0 0 100 100"
      fill="none"
      className={className}
      aria-hidden
    >
      {rays.map((r, i) => (
        <motion.path
          key={i}
          d={r.d}
          stroke="#C67C3E"
          strokeWidth={1.25}
          strokeLinecap="round"
          initial={{ pathLength: 0, opacity: 0 }}
          animate={{ pathLength: 1, opacity: 1 }}
          transition={{
            duration: 0.8,
            delay: r.delay,
            ease: [0.2, 0.6, 0.2, 1],
          }}
        />
      ))}
      <motion.circle
        cx={50}
        cy={50}
        r={10}
        fill="#3D2B5C"
        initial={{ scale: 0, opacity: 0 }}
        animate={{ scale: 1, opacity: 1 }}
        transition={{ duration: 0.6, delay: 0.85, ease: [0.2, 0.6, 0.2, 1] }}
      />
      <motion.circle
        cx={50}
        cy={50}
        r={2.25}
        fill="#C67C3E"
        initial={{ scale: 0, opacity: 0 }}
        animate={{ scale: 1, opacity: 1 }}
        transition={{ duration: 0.45, delay: 1.15, ease: "easeOut" }}
      />
    </svg>
  );
}
