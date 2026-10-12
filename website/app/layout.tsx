import type { Metadata } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import { site } from "./content";
import "./globals.css";

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

const title = "Mosfet — your own AI agent, on your own machine";

export const metadata: Metadata = {
  title,
  description: site.description,
  openGraph: { title, description: site.description, type: "website" },
};

// Runs before first paint so the page never flashes the wrong theme.
const themeScript = `(function(){var d=document.documentElement;var dark;try{var t=localStorage.getItem("mosfet-theme");dark=t==="dark"?true:t==="light"?false:window.matchMedia("(prefers-color-scheme: dark)").matches;}catch(e){try{dark=window.matchMedia("(prefers-color-scheme: dark)").matches;}catch(e2){dark=false;}}d.classList.toggle("dark",dark);})();`;

export default function RootLayout({ children }: LayoutProps<"/">) {
  return (
    <html
      lang="en"
      suppressHydrationWarning
      className={`${geistSans.variable} ${geistMono.variable} h-full antialiased`}
    >
      <head>
        <script dangerouslySetInnerHTML={{ __html: themeScript }} />
      </head>
      <body className="min-h-full flex flex-col bg-bg text-fg">{children}</body>
    </html>
  );
}
