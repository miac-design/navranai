import type { Config } from "tailwindcss";

const config: Config = {
  content: ["./app/**/*.{ts,tsx}", "./components/**/*.{ts,tsx}"],
  theme: {
    extend: {
      colors: {
        dawn: "#FBF7ED",
        parchment: "#F2EBD9",
        saffron: "#C67C3E",
        clay: "#A85A3A",
        twilight: "#3D2B5C",
        ink: "#2B2419",
      },
      fontFamily: {
        display: ["var(--font-fraunces)", "serif"],
        sans: ["var(--font-instrument)", "system-ui", "sans-serif"],
      },
      letterSpacing: {
        tightest: "-0.06em",
        wordmark: "-0.04em",
      },
    },
  },
  plugins: [],
};

export default config;
