import type { Metadata } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import "./globals.css";
import Link from "next/link";

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: "Autism Bias Research Dashboard",
  description: "Research tool studying implicit autism-related bias in LLMs.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html
      lang="en"
      className={`${geistSans.variable} ${geistMono.variable} h-full antialiased`}
    >
      <body className="min-h-full flex flex-col bg-slate-50">
        <header className="sticky top-0 z-50 w-full border-b bg-white/95 backdrop-blur supports-[backdrop-filter]:bg-white/60">
          <div className="container flex h-14 items-center gap-6 px-4">
            <Link href="/" className="font-bold">
              Autism Bias Research
            </Link>
            <nav className="flex gap-4 text-sm font-medium">
              <Link href="/conversations" className="text-muted-foreground hover:text-foreground transition-colors">
                Conversations
              </Link>
              <Link href="/classifier" className="text-muted-foreground hover:text-foreground transition-colors">
                Classifier
              </Link>
              <Link href="/features" className="text-muted-foreground hover:text-foreground transition-colors">
                Features
              </Link>
              <Link href="/benchmark" className="text-muted-foreground hover:text-foreground transition-colors">
                Benchmark
              </Link>
            </nav>
          </div>
        </header>
        <main className="flex-1 container mx-auto px-4 py-6">
          {children}
        </main>
      </body>
    </html>
  );
}
