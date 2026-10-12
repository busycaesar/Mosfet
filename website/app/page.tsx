import Header from "@/components/Header";
import Hero from "@/components/Hero";
import Features from "@/components/Features";
import Showcase from "@/components/Showcase";
import Install from "@/components/Install";
import Faq from "@/components/Faq";
import Footer from "@/components/Footer";

export default function Home() {
  return (
    <>
      <Header />
      <main className="flex-1">
        <Hero />
        <div className="mx-auto w-full max-w-5xl px-4 sm:px-6">
          <Features />
          <Showcase />
          <Install />
          <Faq />
        </div>
      </main>
      <Footer />
    </>
  );
}
