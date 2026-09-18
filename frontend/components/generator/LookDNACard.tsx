"use client";

import React, { useState } from "react";
import { Dna, Check, Copy } from "lucide-react";
import { LookDNA } from "@/lib/types";

interface LookDNACardProps {
  lookDna: LookDNA;
  className?: string;
}

export default function LookDNACard({ lookDna, className = "" }: LookDNACardProps) {
  const [copiedHex, setCopiedHex] = useState<string | null>(null);

  const copyHex = (hex: string) => {
    navigator.clipboard.writeText(hex);
    setCopiedHex(hex);
    setTimeout(() => setCopiedHex(null), 1500);
  };

  return (
    <div className={`p-4 rounded-xl bg-zinc-900/60 border border-white/10 shadow-lg ${className}`}>
      {/* Header */}
      <div className="flex items-center justify-between pb-3 border-b border-white/5">
        <div className="flex items-center gap-2">
          <div className="p-1.5 rounded-lg bg-amber-500/10 text-amber-400 border border-amber-500/20">
            <Dna className="w-4 h-4" />
          </div>
          <div>
            <h4 className="text-xs font-bold uppercase tracking-wider text-zinc-400">Look DNA</h4>
            <p className="text-sm font-semibold text-zinc-100">{lookDna.mood}</p>
          </div>
        </div>
      </div>

      {/* 5 Color Palette Swatches */}
      {lookDna.color_palette && lookDna.color_palette.length > 0 && (
        <div className="mt-3">
          <div className="text-[10px] uppercase font-bold tracking-wider text-zinc-400 mb-1.5">
            Characteristic Color Palette
          </div>
          <div className="grid grid-cols-5 gap-1.5">
            {lookDna.color_palette.map((hex, i) => (
              <button
                key={i}
                onClick={() => copyHex(hex)}
                className="group relative h-9 rounded-md border border-white/10 transition-transform hover:scale-105 flex flex-col items-center justify-center overflow-hidden"
                style={{ backgroundColor: hex }}
                title={`Click to copy ${hex}`}
              >
                <div className="absolute inset-0 bg-black/40 opacity-0 group-hover:opacity-100 transition-opacity flex items-center justify-center text-[9px] font-mono text-white">
                  {copiedHex === hex ? <Check className="w-3 h-3 text-emerald-400" /> : <Copy className="w-3 h-3" />}
                </div>
              </button>
            ))}
          </div>
        </div>
      )}

      {/* Grid of DNA Attributes */}
      <div className="grid grid-cols-2 gap-2 mt-3 pt-3 border-t border-white/5 text-xs">
        <div className="bg-zinc-950/60 p-2 rounded-lg border border-white/5">
          <span className="block text-[10px] text-zinc-400 font-medium">Temperature</span>
          <span className="font-semibold text-zinc-200">{lookDna.temperature_profile}</span>
        </div>
        <div className="bg-zinc-950/60 p-2 rounded-lg border border-white/5">
          <span className="block text-[10px] text-zinc-400 font-medium">Contrast</span>
          <span className="font-semibold text-zinc-200">{lookDna.contrast_profile}</span>
        </div>
        <div className="bg-zinc-950/60 p-2 rounded-lg border border-white/5">
          <span className="block text-[10px] text-zinc-400 font-medium">Highlights</span>
          <span className="font-semibold text-zinc-200">{lookDna.highlight_character}</span>
        </div>
        <div className="bg-zinc-950/60 p-2 rounded-lg border border-white/5">
          <span className="block text-[10px] text-zinc-400 font-medium">Shadows</span>
          <span className="font-semibold text-zinc-200">{lookDna.shadow_character}</span>
        </div>
      </div>

      {/* Tags */}
      {lookDna.key_tags && lookDna.key_tags.length > 0 && (
        <div className="flex flex-wrap gap-1.5 mt-3 pt-2">
          {lookDna.key_tags.map((tag, idx) => (
            <span
              key={idx}
              className="px-2 py-0.5 rounded-full bg-zinc-800/80 text-[10px] font-medium text-zinc-300 border border-white/5"
            >
              #{tag}
            </span>
          ))}
        </div>
      )}
    </div>
  );
}

