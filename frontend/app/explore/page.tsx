"use client";

import React, { useState, useEffect } from "react";
import Link from "next/link";
import Navbar from "@/components/Navbar";
import {
  Compass,
  Download,
  Dna,
  Sliders,
  Filter,
  Sparkles,
} from "lucide-react";
import { Look } from "@/lib/types";
import { fetchPublicLooks } from "@/lib/api";

const CATEGORIES = [
  "All",
  "Cinematic",
  "Moody",
  "Fashion",
  "Vintage",
  "Luxury",
  "Travel",
  "Wedding",
  "Sunset",
  "Clean",
  "Commercial",
];

export default function ExplorePage() {
  const [selectedCategory, setSelectedCategory] = useState<string>("All");
  const [looks, setLooks] = useState<Look[]>([]);
  const [isLoading, setIsLoading] = useState<boolean>(true);

  useEffect(() => {
    setIsLoading(true);
    fetchPublicLooks(selectedCategory)
      .then((data) => setLooks(data))
      .finally(() => setIsLoading(false));
  }, [selectedCategory]);

  return (
    <div className="min-h-screen bg-[#09090b] text-zinc-100 flex flex-col">
      <Navbar credits={250} />

      <main className="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-8">
        {/* Header */}
        <div className="text-center max-w-2xl mx-auto space-y-2">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-amber-500/10 text-amber-400 text-xs font-semibold border border-amber-500/20">
            <Compass className="w-3.5 h-3.5" />
            <span>Community Color Library</span>
          </div>
          <h1 className="text-3xl sm:text-4xl font-black text-white">
            Explore Cinematic Looks
          </h1>
          <p className="text-sm text-zinc-400">
            Browse structured looks created with THEARA COLOR. Test any look directly on your footage with &ldquo;Try This Look&rdquo;.
          </p>
        </div>

        {/* Category Filter Pills */}
        <div className="flex items-center justify-center gap-1.5 overflow-x-auto pb-2">
          {CATEGORIES.map((cat) => (
            <button
              key={cat}
              onClick={() => setSelectedCategory(cat)}
              className={`px-3.5 py-1.5 rounded-full text-xs font-semibold whitespace-nowrap transition-all ${
                selectedCategory === cat
                  ? "bg-amber-500 text-zinc-950 shadow-md shadow-amber-500/20"
                  : "bg-zinc-900 hover:bg-zinc-800 text-zinc-400 hover:text-zinc-200 border border-white/5"
              }`}
            >
              {cat}
            </button>
          ))}
        </div>

        {/* Looks Grid */}
        {isLoading ? (
          <div className="text-center py-16 text-sm text-zinc-500">Loading looks...</div>
        ) : looks.length === 0 ? (
          <div className="text-center py-16 text-sm text-zinc-500">No looks found in this category.</div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {looks.map((look) => (
              <div
                key={look.id}
                className="rounded-xl bg-zinc-900/50 border border-white/10 overflow-hidden flex flex-col hover:border-amber-500/30 transition-all shadow-lg group"
              >
                {/* Preview Thumbnail */}
                <div className="relative aspect-video bg-zinc-950 overflow-hidden">
                  {/* eslint-disable-next-line @next/next/no-img-element */}
                  <img
                    src={look.preview_url || "/storage/previews/demo_graded.webp"}
                    alt={look.title}
                    className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300"
                  />
                  <div className="absolute top-2.5 right-2.5 px-2 py-0.5 rounded bg-zinc-950/80 text-[10px] font-mono font-bold text-amber-400 border border-white/10">
                    {look.category || "Cinematic"}
                  </div>
                  <div className="absolute bottom-2.5 left-2.5 px-2 py-0.5 rounded bg-zinc-950/80 text-[10px] font-mono text-zinc-400 border border-white/10">
                    By {look.creator_name || "Krai Theara"}
                  </div>
                </div>

                {/* Details */}
                <div className="p-4 flex-1 flex flex-col justify-between space-y-3">
                  <div>
                    <h3 className="text-base font-bold text-white">{look.title}</h3>
                    <p className="text-xs text-zinc-400 line-clamp-2 mt-1">{look.prompt}</p>
                  </div>

                  {/* Look DNA Swatches */}
                  {look.look_dna?.color_palette && (
                    <div className="space-y-1 pt-2 border-t border-white/5">
                      <div className="flex justify-between text-[10px] text-zinc-400">
                        <span>Look DNA: {look.look_dna.mood || "Balanced"}</span>
                        <span>{look.downloads_count} downloads</span>
                      </div>
                      <div className="grid grid-cols-5 gap-1">
                        {look.look_dna.color_palette.map((hex, i) => (
                          <div
                            key={i}
                            className="h-4 rounded-sm border border-white/5"
                            style={{ backgroundColor: hex }}
                            title={hex}
                          />
                        ))}
                      </div>
                    </div>
                  )}

                  {/* CTAs */}
                  <div className="flex items-center justify-between pt-3">
                    <Link
                      href={`/generator?look=${look.slug}`}
                      className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-amber-500 hover:bg-amber-400 text-zinc-950 font-bold text-xs shadow-sm transition-all"
                    >
                      <Sparkles className="w-3.5 h-3.5" />
                      <span>Try This Look</span>
                    </Link>

                    <Link
                      href={`/look/${look.slug}`}
                      className="text-xs text-zinc-400 hover:text-white transition-colors"
                    >
                      Share / Details
                    </Link>
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}
      </main>
    </div>
  );
}

