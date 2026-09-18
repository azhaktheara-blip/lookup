"use client";

import React from "react";
import Link from "next/link";
import Navbar from "@/components/Navbar";
import BeforeAfterSlider from "@/components/generator/BeforeAfterSlider";
import {
  Sparkles,
  Sliders,
  Download,
  Dna,
  Layers,
  ArrowRight,
  CheckCircle2,
  Check,
  Zap,
  Film,
  Camera,
  Compass,
} from "lucide-react";

export default function HomePage() {
  const plans = [
    {
      name: "Free",
      price: "$0",
      period: "forever",
      desc: "For exploring and casual creative testing",
      credits: "50 credits / mo",
      features: [
        "AI style generation",
        "Interactive Before/After preview",
        "Basic color grading controls",
        "Standard .cube LUT export",
        "Community explore access",
      ],
      cta: "Get Started Free",
      highlight: false,
    },
    {
      name: "Creator",
      price: "$19",
      period: "/ month",
      desc: "For filmmakers, photographers, and content creators",
      credits: "500 credits / mo",
      features: [
        "Everything in Free",
        "Visual Reference Matching",
        "Adobe .cube 33×33×33 3D LUTs",
        "Adobe Lightroom .xmp presets",
        "Look DNA deep breakdown",
        "Unlimited saved looks",
      ],
      cta: "Start Creator Plan",
      highlight: true,
    },
    {
      name: "Pro",
      price: "$49",
      period: "/ month",
      desc: "For production studios, colorists, and commercial directors",
      credits: "2,000 credits / mo",
      features: [
        "Everything in Creator",
        "Advanced 3-Way Color Wheels",
        "Cubic Spline Tone Curves",
        "8-Band Vector HSL Tuning",
        "Film Grain & Matte Halation",
        "Commercial usage rights",
      ],
      cta: "Start Pro Plan",
      highlight: false,
    },
    {
      name: "Studio",
      price: "$149",
      period: "/ month",
      desc: "For creative agencies and high-volume post-production teams",
      credits: "10,000 credits / mo",
      features: [
        "Everything in Pro",
        "Team shared brand libraries",
        "Priority GPU processing",
        "Batch generation queue",
        "Dedicated account support",
      ],
      cta: "Contact Studio Sales",
      highlight: false,
    },
  ];

  const faqs = [
    {
      q: "How does THEARA COLOR differ from a standard LUT marketplace?",
      a: "Generic LUT packs are static files that often break when applied to different lighting conditions. THEARA COLOR is an AI creative color grading engine: you describe your artistic intent or upload a reference, and the engine mathematically tailors a custom structured color grade specifically to your scene before compiling it into an industry-standard 3D LUT.",
    },
    {
      q: "What editing software supports the exported LUTs and presets?",
      a: "Our .cube files are industry-standard 33×33×33 3D LUTs compatible with DaVinci Resolve, Adobe Premiere Pro, Final Cut Pro, CapCut Desktop, Photoshop, and monitor hardware. Our .xmp presets import natively into Adobe Lightroom and Adobe Camera Raw.",
    },
    {
      q: "Does reference matching copy pixels from the reference image?",
      a: "No. Reference matching performs statistical colorimetric analysis (CIE L*a*b* luminance distribution, chromatic differentials, and shadow/highlight split toning) to formulate a non-destructive mathematical color transformation.",
    },
    {
      q: "What are Look DNAs?",
      a: "Look DNA is THEARA COLOR's signature feature: an analytical fingerprint of each generated look, breaking down its temperature shift, contrast profile, shadow/highlight toning, and a 5-color harmonic palette.",
    },
  ];

  return (
    <div className="min-h-screen bg-[#09090b] text-zinc-100 selection:bg-amber-500 selection:text-zinc-950">
      <Navbar credits={250} />

      {/* 1. HERO SECTION */}
      <section className="relative pt-20 pb-20 px-4 sm:px-6 lg:px-8 max-w-7xl mx-auto flex flex-col items-center text-center">
        {/* Subtle glowing backdrop */}
        <div className="absolute top-1/4 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[600px] h-[350px] bg-amber-500/10 blur-[130px] rounded-full pointer-events-none" />

        <div className="inline-flex items-center gap-2 px-3 py-1.5 rounded-full bg-zinc-900 border border-amber-500/30 text-xs font-semibold text-amber-400 mb-6 shadow-sm">
          <Sparkles className="w-3.5 h-3.5" />
          <span>Next-Generation AI Color Grading Engine</span>
        </div>

        <h1 className="text-5xl sm:text-7xl font-black tracking-tight max-w-4xl text-white">
          CREATE YOUR LOOK.
        </h1>

        <p className="mt-6 text-lg sm:text-xl text-zinc-400 max-w-2xl font-normal leading-relaxed">
          Generate cinematic 3D LUTs and photo presets from your ideas, images, and visual references.
          Professional colorist software powered by deterministic mathematics.
        </p>

        {/* CTAs */}
        <div className="mt-8 flex flex-wrap items-center justify-center gap-4">
          <Link
            href="/generator"
            className="flex items-center gap-2 px-7 py-3.5 rounded-xl bg-amber-500 hover:bg-amber-400 text-zinc-950 font-bold text-base transition-all shadow-lg shadow-amber-500/25 hover:shadow-amber-500/40 hover:-translate-y-0.5"
          >
            <Sliders className="w-5 h-5" />
            <span>CREATE A LOOK</span>
          </Link>

          <Link
            href="/explore"
            className="flex items-center gap-2 px-7 py-3.5 rounded-xl bg-zinc-900 hover:bg-zinc-800 border border-white/10 text-zinc-200 font-semibold text-base transition-all hover:-translate-y-0.5"
          >
            <Compass className="w-5 h-5 text-amber-400" />
            <span>EXPLORE LOOKS</span>
          </Link>
        </div>

        {/* Founder Tag */}
        <div className="mt-8 text-xs text-zinc-500 font-mono tracking-wider uppercase">
          Crafted by Founder <span className="text-zinc-400 font-semibold">Krai Theara</span>
        </div>

        {/* 2. BEFORE/AFTER LIVE HERO DEMONSTRATION */}
        <div className="w-full mt-14 max-w-5xl rounded-2xl overflow-hidden border border-white/15 shadow-2xl bg-zinc-950/80 p-2">
          <div className="text-left px-3 py-2 text-xs text-zinc-400 font-mono flex items-center justify-between border-b border-white/5 mb-2">
            <span>LIVE DEMO: Golden Hour Cinema (33×33×33 3D LUT)</span>
            <span className="text-amber-400">Drag Slider to Compare</span>
          </div>
          <BeforeAfterSlider
            originalUrl="/storage/uploads/demo_original.jpg"
            gradedUrl="/storage/previews/demo_graded.webp"
          />
        </div>
      </section>

      {/* 3. HOW IT WORKS */}
      <section className="py-24 border-t border-white/5 bg-zinc-950/40">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center max-w-3xl mx-auto">
            <span className="text-xs uppercase font-bold tracking-widest text-amber-400">Workflow</span>
            <h2 className="text-3xl sm:text-4xl font-extrabold text-white mt-2">
              From Thought to Camera-Ready Grade
            </h2>
            <p className="text-zinc-400 mt-3 text-sm sm:text-base">
              The AI is not a gimmick. It translates natural language and reference lighting into structured color science.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mt-16">
            <div className="p-6 rounded-2xl bg-zinc-900/40 border border-white/5 hover:border-amber-500/30 transition-all flex flex-col">
              <div className="w-10 h-10 rounded-xl bg-amber-500/10 text-amber-400 flex items-center justify-center font-bold text-base mb-4 border border-amber-500/20">
                1
              </div>
              <h3 className="text-base font-bold text-zinc-100">Upload Source</h3>
              <p className="text-xs text-zinc-400 mt-2 leading-relaxed">
                Upload your raw photograph or video still frame. Optionally upload a reference image to match lighting.
              </p>
            </div>

            <div className="p-6 rounded-2xl bg-zinc-900/40 border border-white/5 hover:border-amber-500/30 transition-all flex flex-col">
              <div className="w-10 h-10 rounded-xl bg-amber-500/10 text-amber-400 flex items-center justify-center font-bold text-base mb-4 border border-amber-500/20">
                2
              </div>
              <h3 className="text-base font-bold text-zinc-100">Describe Your Look</h3>
              <p className="text-xs text-zinc-400 mt-2 leading-relaxed">
                Type natural language: &ldquo;Warm luxury resort during golden hour with muted greens and deep cinematic shadows.&rdquo;
              </p>
            </div>

            <div className="p-6 rounded-2xl bg-zinc-900/40 border border-white/5 hover:border-amber-500/30 transition-all flex flex-col">
              <div className="w-10 h-10 rounded-xl bg-amber-500/10 text-amber-400 flex items-center justify-center font-bold text-base mb-4 border border-amber-500/20">
                3
              </div>
              <h3 className="text-base font-bold text-zinc-100">Deterministic Engine</h3>
              <p className="text-xs text-zinc-400 mt-2 leading-relaxed">
                The Color Engine applies 3-way color wheels, spline curves, and 8-channel HSL in sub-second preview time.
              </p>
            </div>

            <div className="p-6 rounded-2xl bg-zinc-900/40 border border-white/5 hover:border-amber-500/30 transition-all flex flex-col">
              <div className="w-10 h-10 rounded-xl bg-amber-500/10 text-amber-400 flex items-center justify-center font-bold text-base mb-4 border border-amber-500/20">
                4
              </div>
              <h3 className="text-base font-bold text-zinc-100">Export .CUBE & .XMP</h3>
              <p className="text-xs text-zinc-400 mt-2 leading-relaxed">
                Download mathematically validated 33×33×33 .cube LUTs for DaVinci/Premiere and .xmp presets for Lightroom.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* 4. LOOK DNA SHOWCASE */}
      <section className="py-24 border-t border-white/5">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 grid grid-cols-1 lg:grid-cols-2 gap-12 items-center">
          <div>
            <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-amber-500/10 text-amber-400 text-xs font-semibold mb-3 border border-amber-500/20">
              <Dna className="w-3.5 h-3.5" />
              <span>Signature Feature</span>
            </div>
            <h2 className="text-3xl sm:text-4xl font-extrabold text-white">
              Every Look Has a Genetic Fingerprint.
            </h2>
            <p className="text-zinc-400 mt-4 text-sm sm:text-base leading-relaxed">
              Never wonder why a grade looks the way it does. The <strong>Look DNA</strong> decomposes every aesthetic into explicit color science metrics: temperature shift, contrast profile, shadow cyan toning, highlight roll-off, and extracted hex color palettes.
            </p>

            <div className="mt-8 space-y-3">
              <div className="flex items-start gap-3">
                <CheckCircle2 className="w-5 h-5 text-amber-400 shrink-0 mt-0.5" />
                <div>
                  <h4 className="text-sm font-bold text-zinc-200">5-Color Harmonic Swatches</h4>
                  <p className="text-xs text-zinc-400">Click any palette swatch to copy exact hex values for production design.</p>
                </div>
              </div>
              <div className="flex items-start gap-3">
                <CheckCircle2 className="w-5 h-5 text-amber-400 shrink-0 mt-0.5" />
                <div>
                  <h4 className="text-sm font-bold text-zinc-200">Independent Creative Control</h4>
                  <p className="text-xs text-zinc-400">Tweak exposure, saturation, or 3-way wheels while preserving the DNA mood.</p>
                </div>
              </div>
            </div>
          </div>

          <div className="p-6 rounded-2xl bg-zinc-900/60 border border-white/10 shadow-2xl space-y-4">
            <div className="flex items-center justify-between border-b border-white/10 pb-3">
              <div className="flex items-center gap-2">
                <div className="p-2 rounded-lg bg-amber-500/10 text-amber-400">
                  <Dna className="w-5 h-5" />
                </div>
                <div>
                  <span className="text-[10px] uppercase font-bold tracking-widest text-zinc-400">Look DNA</span>
                  <h3 className="text-base font-bold text-white">Warm Luxury Cinema</h3>
                </div>
              </div>
              <span className="text-xs px-2.5 py-1 rounded bg-amber-500/10 text-amber-400 font-mono">
                33×33×33 .CUBE
              </span>
            </div>

            <div className="space-y-1.5">
              <span className="text-[11px] uppercase font-bold text-zinc-400 tracking-wider">Characteristic Palette</span>
              <div className="grid grid-cols-5 gap-2">
                {["#131e24", "#5c554e", "#485344", "#c89474", "#f5ebd4"].map((hex, i) => (
                  <div key={i} className="h-10 rounded-md flex items-center justify-center border border-white/10" style={{ backgroundColor: hex }}>
                    <span className="text-[9px] font-mono text-white/80 bg-black/40 px-1 rounded">{hex}</span>
                  </div>
                ))}
              </div>
            </div>

            <div className="grid grid-cols-2 gap-3 pt-2 text-xs">
              <div className="bg-zinc-950 p-2.5 rounded-lg border border-white/5">
                <span className="text-[10px] text-zinc-400 block font-medium">Temperature</span>
                <span className="font-semibold text-zinc-200">Golden Warm (+32K)</span>
              </div>
              <div className="bg-zinc-950 p-2.5 rounded-lg border border-white/5">
                <span className="text-[10px] text-zinc-400 block font-medium">Contrast</span>
                <span className="font-semibold text-zinc-200">Punchy S-Curve (+22)</span>
              </div>
              <div className="bg-zinc-950 p-2.5 rounded-lg border border-white/5">
                <span className="text-[10px] text-zinc-400 block font-medium">Highlights</span>
                <span className="font-semibold text-zinc-200">Soft Amber Glow</span>
              </div>
              <div className="bg-zinc-950 p-2.5 rounded-lg border border-white/5">
                <span className="text-[10px] text-zinc-400 block font-medium">Shadows</span>
                <span className="font-semibold text-zinc-200">Deep Cinematic Teal</span>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* 5. PRICING & PLANS */}
      <section id="pricing" className="py-24 border-t border-white/5 bg-zinc-950/60">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center max-w-3xl mx-auto">
            <span className="text-xs uppercase font-bold tracking-widest text-amber-400">Pricing</span>
            <h2 className="text-3xl sm:text-4xl font-extrabold text-white mt-2">
              Transparent, Creator-Friendly Plans
            </h2>
            <p className="text-zinc-400 mt-3 text-sm sm:text-base">
              Every generation and reference match consumes credits with automatic refund protection.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mt-16">
            {plans.map((p, idx) => (
              <div
                key={idx}
                className={`p-6 rounded-2xl flex flex-col justify-between transition-all ${
                  p.highlight
                    ? "bg-zinc-900 border-2 border-amber-400/80 shadow-2xl shadow-amber-500/10 scale-[1.02]"
                    : "bg-zinc-900/40 border border-white/5 hover:border-white/15"
                }`}
              >
                <div>
                  {p.highlight && (
                    <div className="inline-block px-2.5 py-0.5 rounded-full bg-amber-500 text-zinc-950 text-[10px] font-black uppercase tracking-wider mb-3">
                      Most Popular
                    </div>
                  )}
                  <h3 className="text-lg font-bold text-white">{p.name}</h3>
                  <div className="flex items-baseline gap-1 mt-2">
                    <span className="text-3xl font-black text-white">{p.price}</span>
                    <span className="text-xs text-zinc-400">{p.period}</span>
                  </div>
                  <p className="text-xs text-zinc-400 mt-2">{p.desc}</p>
                  <div className="mt-3 py-1.5 px-2.5 rounded bg-zinc-950 border border-white/5 text-xs font-semibold text-amber-400 flex items-center gap-1.5">
                    <Zap className="w-3.5 h-3.5 fill-amber-400 text-amber-400" />
                    <span>{p.credits}</span>
                  </div>

                  <ul className="mt-6 space-y-2.5 text-xs text-zinc-300">
                    {p.features.map((f, fi) => (
                      <li key={fi} className="flex items-center gap-2">
                        <Check className="w-3.5 h-3.5 text-amber-400 shrink-0" />
                        <span>{f}</span>
                      </li>
                    ))}
                  </ul>
                </div>

                <div className="mt-8">
                  <Link
                    href="/generator"
                    className={`w-full py-2.5 rounded-lg text-xs font-bold flex items-center justify-center transition-all ${
                      p.highlight
                        ? "bg-amber-500 hover:bg-amber-400 text-zinc-950 shadow-md shadow-amber-500/20"
                        : "bg-zinc-800 hover:bg-zinc-700 text-white"
                    }`}
                  >
                    {p.cta}
                  </Link>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* 6. FAQ */}
      <section className="py-24 border-t border-white/5">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <span className="text-xs uppercase font-bold tracking-widest text-amber-400">Questions & Answers</span>
            <h2 className="text-3xl font-extrabold text-white mt-2">Frequently Asked Questions</h2>
          </div>

          <div className="space-y-6">
            {faqs.map((faq, i) => (
              <div key={i} className="p-6 rounded-2xl bg-zinc-900/40 border border-white/5 space-y-2">
                <h4 className="text-base font-bold text-zinc-100">{faq.q}</h4>
                <p className="text-xs sm:text-sm text-zinc-400 leading-relaxed">{faq.a}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* 7. FINAL CTA & FOOTER */}
      <footer className="border-t border-white/10 bg-zinc-950 py-16">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 flex flex-col items-center text-center">
          <div className="w-12 h-12 rounded-xl bg-gradient-to-br from-amber-400 to-amber-600 flex items-center justify-center text-zinc-950 font-black text-xl mb-4 shadow-xl shadow-amber-500/20">
            TC
          </div>
          <h2 className="text-3xl font-extrabold text-white">THEARA COLOR</h2>
          <p className="text-sm font-semibold tracking-widest text-amber-400 uppercase mt-1">
            Create Your Look.
          </p>
          <p className="text-xs text-zinc-500 max-w-md mt-3">
            Founded by Krai Theara. Built for creators, cinematographers, and photographers worldwide.
          </p>

          <div className="mt-8 flex gap-4">
            <Link
              href="/generator"
              className="px-6 py-2.5 rounded-lg bg-amber-500 hover:bg-amber-400 text-zinc-950 font-bold text-xs shadow-md shadow-amber-500/20"
            >
              Open Studio Now
            </Link>
            <Link
              href="/explore"
              className="px-6 py-2.5 rounded-lg bg-zinc-900 hover:bg-zinc-800 border border-white/10 text-white font-medium text-xs"
            >
              Explore Public Looks
            </Link>
          </div>

          <div className="mt-12 text-xs text-zinc-600">
            © {new Date().getFullYear()} THEARA COLOR. All rights reserved. Professional 33×33×33 .CUBE & .XMP formats.
          </div>
        </div>
      </footer>
    </div>
  );
}

