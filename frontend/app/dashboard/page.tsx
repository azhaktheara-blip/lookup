"use client";

import React, { useState, useEffect } from "react";
import Link from "next/link";
import Navbar from "@/components/Navbar";
import {
  Sparkles,
  Sliders,
  Download,
  Dna,
  Zap,
  FolderPlus,
  ArrowRight,
  Clock,
  Layers,
} from "lucide-react";
import { Look } from "@/lib/types";
import { fetchMyLooks, fetchUserCredits } from "@/lib/api";

export default function DashboardPage() {
  const [looks, setLooks] = useState<Look[]>([]);
  const [credits, setCredits] = useState<number>(250);
  const [lifetimeUsed, setLifetimeUsed] = useState<number>(0);
  const [isLoading, setIsLoading] = useState<boolean>(true);

  useEffect(() => {
    Promise.all([fetchMyLooks(), fetchUserCredits()])
      .then(([myLooks, creditData]) => {
        setLooks(myLooks);
        setCredits(creditData.balance);
        setLifetimeUsed(creditData.lifetime_used);
      })
      .finally(() => setIsLoading(false));
  }, []);

  return (
    <div className="min-h-screen bg-[#09090b] text-zinc-100 flex flex-col">
      <Navbar credits={credits} />

      <main className="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-8">
        {/* Dashboard Header */}
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 pb-6 border-b border-white/10">
          <div>
            <h1 className="text-2xl sm:text-3xl font-black text-white">Creator Dashboard</h1>
            <p className="text-sm text-zinc-400 mt-1">
              Manage your projects, saved looks, and 3D LUT exports.
            </p>
          </div>

          <Link
            href="/generator"
            className="flex items-center gap-2 px-5 py-2.5 rounded-xl bg-amber-500 hover:bg-amber-400 text-zinc-950 font-bold text-sm shadow-md shadow-amber-500/20 transition-all self-start"
          >
            <Sliders className="w-4 h-4" />
            <span>Open Studio</span>
          </Link>
        </div>

        {/* Credit & Analytics Metric Cards */}
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
          <div className="p-5 rounded-xl bg-zinc-900/40 border border-white/10 flex flex-col justify-between">
            <div className="flex items-center justify-between text-xs text-zinc-400 font-semibold uppercase">
              <span>Credits Available</span>
              <Zap className="w-4 h-4 text-amber-400" />
            </div>
            <div className="text-3xl font-black text-white mt-3">{credits}</div>
            <span className="text-[11px] text-zinc-500 mt-1">Auto-refills with plan tier</span>
          </div>

          <div className="p-5 rounded-xl bg-zinc-900/40 border border-white/10 flex flex-col justify-between">
            <div className="flex items-center justify-between text-xs text-zinc-400 font-semibold uppercase">
              <span>Saved Looks</span>
              <Dna className="w-4 h-4 text-amber-400" />
            </div>
            <div className="text-3xl font-black text-white mt-3">{looks.length}</div>
            <span className="text-[11px] text-zinc-500 mt-1">Ready for .cube & .xmp export</span>
          </div>

          <div className="p-5 rounded-xl bg-zinc-900/40 border border-white/10 flex flex-col justify-between">
            <div className="flex items-center justify-between text-xs text-zinc-400 font-semibold uppercase">
              <span>Generations Created</span>
              <Sparkles className="w-4 h-4 text-amber-400" />
            </div>
            <div className="text-3xl font-black text-white mt-3">{Math.round(lifetimeUsed / 10)}</div>
            <span className="text-[11px] text-zinc-500 mt-1">Total lifetime AI interpretations</span>
          </div>
        </div>

        {/* My Saved Looks Gallery */}
        <div className="space-y-4">
          <div className="flex items-center justify-between">
            <h2 className="text-lg font-bold text-white">Recent Saved Looks</h2>
            <Link href="/generator" className="text-xs text-amber-400 hover:underline flex items-center gap-1">
              Create New Look <ArrowRight className="w-3.5 h-3.5" />
            </Link>
          </div>

          {isLoading ? (
            <div className="text-sm text-zinc-500 py-12 text-center">Loading your library...</div>
          ) : looks.length === 0 ? (
            <div className="p-12 rounded-2xl bg-zinc-900/20 border border-white/5 text-center flex flex-col items-center">
              <Sliders className="w-10 h-10 text-zinc-600 mb-3" />
              <h3 className="text-base font-bold text-zinc-300">No saved looks yet</h3>
              <p className="text-xs text-zinc-500 max-w-sm mt-1">
                Open the Studio to generate your first custom color grade and export a 3D LUT.
              </p>
              <Link
                href="/generator"
                className="mt-4 px-4 py-2 rounded-lg bg-amber-500 text-zinc-950 font-bold text-xs"
              >
                Create a Look
              </Link>
            </div>
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
                  </div>

                  {/* Look Info & DNA Palette */}
                  <div className="p-4 flex-1 flex flex-col justify-between space-y-3">
                    <div>
                      <h3 className="text-base font-bold text-white">{look.title}</h3>
                      <p className="text-xs text-zinc-400 line-clamp-2 mt-1">{look.prompt}</p>
                    </div>

                    {/* DNA Palette */}
                    {look.look_dna?.color_palette && (
                      <div className="grid grid-cols-5 gap-1 pt-2 border-t border-white/5">
                        {look.look_dna.color_palette.map((hex, i) => (
                          <div
                            key={i}
                            className="h-5 rounded-sm border border-white/5"
                            style={{ backgroundColor: hex }}
                            title={hex}
                          />
                        ))}
                      </div>
                    )}

                    {/* Actions */}
                    <div className="flex items-center justify-between pt-2">
                      <Link
                        href={`/look/${look.slug}`}
                        className="text-xs text-zinc-400 hover:text-white transition-colors"
                      >
                        View Details
                      </Link>

                      <div className="flex items-center gap-1.5">
                        <a
                          href={`/api/v1/looks/${look.id}/export`}
                          download
                          className="px-2.5 py-1 rounded bg-zinc-800 hover:bg-zinc-700 text-[11px] font-semibold text-zinc-200 border border-white/5 flex items-center gap-1"
                        >
                          <Download className="w-3 h-3 text-amber-400" />
                          <span>.CUBE</span>
                        </a>
                      </div>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </main>
    </div>
  );
}

