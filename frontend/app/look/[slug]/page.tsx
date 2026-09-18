"use client";

import React, { useState, useEffect } from "react";
import Link from "next/link";
import { useParams } from "next/navigation";
import Navbar from "@/components/Navbar";
import BeforeAfterSlider from "@/components/generator/BeforeAfterSlider";
import LookDNACard from "@/components/generator/LookDNACard";
import {
  Download,
  Share2,
  Sparkles,
  Sliders,
  Check,
  FileCode,
  ArrowLeft,
  Eye,
} from "lucide-react";
import { Look } from "@/lib/types";
import { fetchLookBySlug } from "@/lib/api";

export default function PublicLookDetailPage() {
  const params = useParams();
  const slug = params.slug as string;

  const [look, setLook] = useState<Look | null>(null);
  const [isLoading, setIsLoading] = useState<boolean>(true);
  const [isCopied, setIsCopied] = useState<boolean>(false);

  useEffect(() => {
    if (!slug) return;
    setIsLoading(true);
    fetchLookBySlug(slug)
      .then((data) => setLook(data))
      .finally(() => setIsLoading(false));
  }, [slug]);

  const copyShareLink = () => {
    if (typeof window !== "undefined") {
      navigator.clipboard.writeText(window.location.href);
      setIsCopied(true);
      setTimeout(() => setIsCopied(false), 2000);
    }
  };

  const handleDownload = (format: "cube" | "xmp") => {
    if (!look) return;
    window.location.href = `/api/v1/looks/${look.id}/export`;
  };

  if (isLoading) {
    return (
      <div className="min-h-screen bg-[#09090b] text-zinc-100 flex flex-col">
        <Navbar credits={250} />
        <div className="flex-1 flex items-center justify-center text-zinc-500 text-sm">
          Loading Look...
        </div>
      </div>
    );
  }

  if (!look) {
    return (
      <div className="min-h-screen bg-[#09090b] text-zinc-100 flex flex-col">
        <Navbar credits={250} />
        <div className="flex-1 flex flex-col items-center justify-center gap-4 text-center p-4">
          <h1 className="text-xl font-bold text-white">Look Not Found</h1>
          <p className="text-xs text-zinc-400">The requested look may have been deleted or made private.</p>
          <Link href="/explore" className="px-4 py-2 rounded-lg bg-amber-500 text-zinc-950 font-bold text-xs">
            Back to Explore
          </Link>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-[#09090b] text-zinc-100 flex flex-col">
      <Navbar credits={250} />

      <main className="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-8">
        {/* Back Link */}
        <Link
          href="/explore"
          className="inline-flex items-center gap-1.5 text-xs text-zinc-400 hover:text-white transition-colors"
        >
          <ArrowLeft className="w-3.5 h-3.5" />
          <span>Back to Explore</span>
        </Link>

        {/* Top Header */}
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 pb-6 border-b border-white/10">
          <div>
            <div className="flex items-center gap-2">
              <span className="px-2 py-0.5 rounded bg-amber-500/10 text-amber-400 text-[10px] font-mono font-bold border border-amber-500/20">
                {look.category || "Cinematic"}
              </span>
              <span className="text-xs text-zinc-500">By {look.creator_name || "Krai Theara"}</span>
            </div>
            <h1 className="text-3xl sm:text-4xl font-black text-white mt-1">{look.title}</h1>
            <p className="text-sm text-zinc-400 max-w-2xl mt-2 leading-relaxed">{look.prompt}</p>
          </div>

          <div className="flex items-center gap-2 self-start md:self-auto">
            <button
              onClick={copyShareLink}
              className="flex items-center gap-1.5 px-3 py-2 rounded-lg bg-zinc-900 hover:bg-zinc-800 border border-white/10 text-xs font-semibold text-zinc-200 transition-all"
            >
              {isCopied ? <Check className="w-4 h-4 text-emerald-400" /> : <Share2 className="w-4 h-4" />}
              <span>{isCopied ? "Link Copied!" : "Share"}</span>
            </button>

            <Link
              href={`/generator?look=${look.slug}`}
              className="flex items-center gap-2 px-5 py-2 rounded-lg bg-amber-500 hover:bg-amber-400 text-zinc-950 font-bold text-xs shadow-md shadow-amber-500/20 transition-all"
            >
              <Sparkles className="w-4 h-4" />
              <span>Try This Look</span>
            </Link>
          </div>
        </div>

        {/* Visual Inspection Grid */}
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">
          {/* Main Visual Comparison Slider */}
          <div className="lg:col-span-8 flex flex-col gap-4">
            <div className="rounded-2xl overflow-hidden border border-white/10 shadow-2xl min-h-[520px]">
              <BeforeAfterSlider
                originalUrl="/storage/uploads/demo_original.jpg"
                gradedUrl={look.preview_url || "/storage/previews/demo_graded.webp"}
              />
            </div>

            {/* Export Bar */}
            <div className="p-4 rounded-xl bg-zinc-900/40 border border-white/10 flex flex-wrap items-center justify-between gap-3">
              <div>
                <h4 className="text-xs font-bold text-zinc-200 uppercase tracking-wider">Export Look</h4>
                <p className="text-[11px] text-zinc-400">Download for DaVinci Resolve, Premiere Pro, or Lightroom.</p>
              </div>

              <div className="flex items-center gap-2">
                <button
                  onClick={() => handleDownload("cube")}
                  className="flex items-center gap-1.5 px-4 py-2 rounded-lg bg-amber-500 hover:bg-amber-400 text-zinc-950 font-bold text-xs shadow-sm transition-all"
                >
                  <Download className="w-4 h-4" />
                  <span>Download .CUBE (33×)</span>
                </button>
                <button
                  onClick={() => handleDownload("xmp")}
                  className="flex items-center gap-1.5 px-3.5 py-2 rounded-lg bg-zinc-800 hover:bg-zinc-700 text-zinc-200 font-semibold text-xs border border-white/10 transition-all"
                >
                  <FileCode className="w-4 h-4 text-amber-400" />
                  <span>Download .XMP</span>
                </button>
              </div>
            </div>
          </div>

          {/* Sidebar: Look DNA & Specs */}
          <div className="lg:col-span-4 space-y-4">
            {look.look_dna && <LookDNACard lookDna={look.look_dna} />}

            {/* Parameter Snapshot Card */}
            <div className="p-4 rounded-xl bg-zinc-900/40 border border-white/10 space-y-3">
              <h4 className="text-xs font-bold uppercase tracking-wider text-zinc-400">
                Grading Parameters Snapshot
              </h4>
              <div className="grid grid-cols-2 gap-2 text-xs font-mono">
                <div className="bg-zinc-950 p-2 rounded border border-white/5 flex justify-between">
                  <span className="text-zinc-500">Exposure:</span>
                  <span className="text-zinc-200">{look.parameters?.exposure?.toFixed(2) || "0.00"} EV</span>
                </div>
                <div className="bg-zinc-950 p-2 rounded border border-white/5 flex justify-between">
                  <span className="text-zinc-500">Contrast:</span>
                  <span className="text-zinc-200">{look.parameters?.contrast?.toFixed(0) || "0"}</span>
                </div>
                <div className="bg-zinc-950 p-2 rounded border border-white/5 flex justify-between">
                  <span className="text-zinc-500">Temp:</span>
                  <span className="text-zinc-200">{look.parameters?.temperature?.toFixed(0) || "0"}</span>
                </div>
                <div className="bg-zinc-950 p-2 rounded border border-white/5 flex justify-between">
                  <span className="text-zinc-500">Sat:</span>
                  <span className="text-zinc-200">{look.parameters?.saturation?.toFixed(0) || "0"}</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}

