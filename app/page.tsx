import Hero from "@/components/Hero";
import Problem from "@/components/Problem";
import WhatWeDo from "@/components/WhatWeDo";
import Articles from "@/components/Articles";
import Mission from "@/components/Mission";
import BuiltBy from "@/components/BuiltBy";
import Footer from "@/components/Footer";
import Cursor from "@/components/Cursor";

export default function Home() {
  return (
    <main className="relative">
      <Cursor />
      <Hero />
      <Problem />
      <WhatWeDo />
      <Articles />
      <Mission />
      <BuiltBy />
      <Footer />
    </main>
  );
}
