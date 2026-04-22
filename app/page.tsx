import Hero from "@/components/Hero";
import Problem from "@/components/Problem";
import WhatWeDo from "@/components/WhatWeDo";
import Articles from "@/components/Articles";
import Mission from "@/components/Mission";
import BuiltBy from "@/components/BuiltBy";
import Footer from "@/components/Footer";
import Cursor from "@/components/Cursor";
import Nav from "@/components/Nav";

export default function Home() {
  return (
    <main className="relative">
      <Cursor />
      <Nav variant="dawn" />
      <Hero />
      <Problem />
      <WhatWeDo />
      <Articles />
      <section id="mission">
        <Mission />
      </section>
      <BuiltBy />
      <section id="subscribe">
        <Footer />
      </section>
    </main>
  );
}
