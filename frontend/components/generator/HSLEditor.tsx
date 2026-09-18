"use client";

import React, { useState } from "react";
import { HSLSettings, HSLChannel } from "@/lib/types";

interface HSLEditorProps {
  hsl: HSLSettings;
  onChange: (updated: HSLSettings) => void;
}

const HSL_COLOR_MAP: Record<keyof HSLSettings, string> = {
  red: "#ef4444",
  orange: "#f97316",
  yellow: "#eab308",
  green: "#22c55e",
  aqua: "#06b6d4",
  blue: "#3b82f6",
  purple: "#a855f7",
  magenta: "#ec4899",
};

export default function HSLEditor({ hsl, onChange }: HSLEditorProps) {
  const [selectedChannel, setSelectedChannel] = useState<keyof HSLSettings>("red");

  const channelData = hsl[selectedChannel];

  const updateChannel = (key: keyof HSLChannel, val: number) => {
    onChange({
      ...hsl,
      [selectedChannel]: {
        ...channelData,
        [key]: val,
      },
    });
  };

  const resetCurrent = () => {
    onChange({
      ...hsl,
      [selectedChannel]: { hue: 0, saturation: 0, luminance: 0 },
    });
  };

  return (
    <div className="p-3 bg-zinc-900/40 rounded-xl border border-white/5 space-y-3">
      <div className="flex items-center justify-between">
        <span className="text-[11px] font-bold uppercase tracking-wider text-zinc-400">
          8-Band HSL Tuning
        </span>
        <button
          onClick={resetCurrent}
          className="text-[10px] text-zinc-500 hover:text-amber-400 font-mono"
        >
          Reset {selectedChannel}
        </button>
      </div>

      {/* Color Channel Pills */}
      <div className="flex items-center justify-between gap-1 bg-zinc-950 p-1 rounded-lg border border-white/5">
        {(Object.keys(HSL_COLOR_MAP) as (keyof HSLSettings)[]).map((key) => {
          const isSelected = selectedChannel === key;
          return (
            <button
              key={key}
              onClick={() => setSelectedChannel(key)}
              className={`flex-1 py-1 rounded-md flex flex-col items-center gap-1 transition-all ${
                isSelected ? "bg-zinc-800 ring-1 ring-white/20" : "hover:bg-zinc-900"
              }`}
              title={key}
            >
              <div
                className="w-3 h-3 rounded-full shadow-sm"
                style={{ backgroundColor: HSL_COLOR_MAP[key] }}
              />
            </button>
          );
        })}
      </div>

      {/* Channel Adjustments */}
      <div className="space-y-2 text-xs">
        <div>
          <div className="flex justify-between text-zinc-400 mb-0.5">
            <span>Hue Shift</span>
            <span className="font-mono text-zinc-300">
              {channelData.hue > 0 ? `+${channelData.hue}` : channelData.hue}°
            </span>
          </div>
          <input
            type="range"
            min={-100}
            max={100}
            value={channelData.hue}
            onChange={(e) => updateChannel("hue", parseFloat(e.target.value))}
            className="w-full h-1.5 bg-zinc-800 rounded-lg appearance-none cursor-pointer accent-amber-400"
          />
        </div>

        <div>
          <div className="flex justify-between text-zinc-400 mb-0.5">
            <span>Saturation</span>
            <span className="font-mono text-zinc-300">
              {channelData.saturation > 0 ? `+${channelData.saturation}` : channelData.saturation}%
            </span>
          </div>
          <input
            type="range"
            min={-100}
            max={100}
            value={channelData.saturation}
            onChange={(e) => updateChannel("saturation", parseFloat(e.target.value))}
            className="w-full h-1.5 bg-zinc-800 rounded-lg appearance-none cursor-pointer accent-amber-400"
          />
        </div>

        <div>
          <div className="flex justify-between text-zinc-400 mb-0.5">
            <span>Luminance</span>
            <span className="font-mono text-zinc-300">
              {channelData.luminance > 0 ? `+${channelData.luminance}` : channelData.luminance}%
            </span>
          </div>
          <input
            type="range"
            min={-100}
            max={100}
            value={channelData.luminance}
            onChange={(e) => updateChannel("luminance", parseFloat(e.target.value))}
            className="w-full h-1.5 bg-zinc-800 rounded-lg appearance-none cursor-pointer accent-amber-400"
          />
        </div>
      </div>
    </div>
  );
}

