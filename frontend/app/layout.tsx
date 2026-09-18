import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "THEARA COLOR — Create Your Look",
  description: "AI-powered color grading and LUT/preset generation platform for creators. Founded by Krai Theara.",
  openGraph: {
    title: "THEARA COLOR — Create Your Look",
    description: "Generate cinematic 3D LUTs and photo presets from your ideas, images, and references.",
    siteName: "THEARA COLOR",
  },
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" className="dark">
      <body className="min-h-screen bg-[#09090b] text-zinc-100 antialiased selection:bg-amber-500 selection:text-zinc-950">
        {children}
      </body>
    </html>
  );
}

