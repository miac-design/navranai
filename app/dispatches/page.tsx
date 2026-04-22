import Link from "next/link";
import { articles } from "@/lib/articles";
import Nav from "@/components/Nav";
import Cursor from "@/components/Cursor";
import DispatchesList from "@/components/DispatchesList";

export const metadata = {
  title: "Dispatches — Navran",
  description: "Field reports, analyses, and investigations from Navran.",
};

export default function DispatchesPage() {
  return (
    <main className="relative min-h-screen">
      <Cursor />
      <Nav variant="dawn" />

      <section className="relative overflow-hidden px-6 pb-16 pt-40 md:pt-48">
        <div className="mx-auto max-w-6xl">
          <div className="mb-4 font-sans text-xs uppercase tracking-[0.35em] text-clay">
            Dispatches
          </div>
          <h1
            className="max-w-4xl font-display font-light text-ink leading-[1.02] tracking-tight"
            style={{ fontSize: "clamp(2.5rem, 6vw, 5rem)" }}
          >
            One story a month.{" "}
            <span className="italic text-twilight">Carefully made.</span>
          </h1>
          <p
            className="mt-8 max-w-2xl font-sans text-ink/70"
            style={{ fontSize: "clamp(1rem, 1.2vw, 1.1rem)", lineHeight: 1.6 }}
          >
            Field reports, long-form analysis, and investigations on the
            issues that survive by going unnamed. Written by reporters,
            researchers, and people working on the inside of the systems
            we cover.
          </p>
        </div>
      </section>

      <DispatchesList articles={articles} />

      <footer className="border-t border-ink/10 py-12">
        <div className="mx-auto flex max-w-6xl flex-wrap items-center justify-between gap-4 px-6 font-sans text-xs uppercase tracking-[0.3em] text-ink/45">
          <Link href="/" data-cursor-target className="hover:text-saffron">
            ← Navran
          </Link>
          <span>© {new Date().getFullYear()} Navran · Austin · Geneva</span>
        </div>
      </footer>
    </main>
  );
}
