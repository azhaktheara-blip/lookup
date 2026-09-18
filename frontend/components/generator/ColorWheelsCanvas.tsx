"use client";

import React, { useRef, useEffect, useCallback } from "react";
import { ColorWheelsSettings, ColorWheel } from "@/lib/types";

interface ColorWheelsCanvasProps {
  wheels: ColorWheelsSettings;
  onChange: (updated: ColorWheelsSettings) => void;
}

interface SingleWheelProps {
  title: string;
  wheel: ColorWheel;
  onChange: (w: ColorWheel) => void;
}

function SingleWheel({ title, wheel, onChange }: SingleWheelProps) {
  const canvasRef = useRef<HTMLCanvasElement>(null);

  const drawWheel = useCallback(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext("2d");
    if (!ctx) return;

    const width = canvas.width;
    const height = canvas.height;
    const cx = width / 2;
    const cy = height / 2;
    const radius = width / 2 - 4;

    ctx.clearRect(0, 0, width, height);

    // Draw chromatic circle
    for (let angle = 0; angle < 360; angle += 2) {
      const startAngle = ((angle - 1) * Math.PI) / 180;
      const endAngle = ((angle + 1) * Math.PI) / 180;
      ctx.beginPath();
      ctx.moveTo(cx, cy);
      ctx.arc(cx, cy, radius, startAngle, endAngle);
      ctx.closePath();
      const grad = ctx.createRadialGradient(cx, cy, 0, cx, cy, radius);
      grad.addColorStop(0, "rgba(40, 40, 45, 1)");
      grad.addColorStop(1, `hsl(${angle}, 75%, 50%)`);
      ctx.fillStyle = grad;
      ctx.fill();
    }

    // Outer ring
    ctx.strokeStyle = "#27272a";
    ctx.lineWidth = 1.5;
    ctx.beginPath();
    ctx.arc(cx, cy, radius, 0, Math.PI * 2);
    ctx.stroke();

    // Crosshairs
    ctx.strokeStyle = "rgba(255, 255, 255, 0.15)";
    ctx.lineWidth = 1;
    ctx.beginPath();
    ctx.moveTo(cx - 6, cy);
    ctx.lineTo(cx + 6, cy);
    ctx.moveTo(cx, cy - 6);
    ctx.lineTo(cx, cy + 6);
    ctx.stroke();

    // Position of current reticle
    const angleRad = (wheel.hue * Math.PI) / 180;
    const rDist = wheel.saturation * radius;
    const reticleX = cx + rDist * Math.cos(angleRad);
    const reticleY = cy + rDist * Math.sin(angleRad);

    // Reticle
    ctx.fillStyle = "#ffffff";
    ctx.strokeStyle = "#09090b";
    ctx.lineWidth = 2;
    ctx.beginPath();
    ctx.arc(reticleX, reticleY, 4.5, 0, Math.PI * 2);
    ctx.fill();
    ctx.stroke();
  }, [wheel]);

  useEffect(() => {
    drawWheel();
  }, [drawWheel]);

  const handlePointer = (e: React.MouseEvent<HTMLCanvasElement>) => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const rect = canvas.getBoundingClientRect();
    const cx = rect.width / 2;
    const cy = rect.height / 2;
    const dx = e.clientX - rect.left - cx;
    const dy = e.clientY - rect.top - cy;
    const maxRadius = cx - 4;

    const dist = Math.hypot(dx, dy);
    const sat = Math.min(1.0, dist / maxRadius);
    let hue = (Math.atan2(dy, dx) * 180) / Math.PI;
    if (hue < 0) hue += 360;

    onChange({
      ...wheel,
      hue: Math.round(hue),
      saturation: parseFloat(sat.toFixed(3)),
    });
  };

  return (
    <div className="flex flex-col items-center bg-zinc-950/60 p-2.5 rounded-xl border border-white/5">
      <div className="flex items-center justify-between w-full mb-1">
        <span className="text-[10px] font-bold uppercase tracking-wider text-zinc-400">{title}</span>
        <button
          onClick={() => onChange({ hue: 0, saturation: 0, luminance: 0 })}
          className="text-[9px] text-zinc-500 hover:text-amber-400 font-mono"
        >
          Reset
        </button>
      </div>

      <div className="relative my-1">
        <canvas
          ref={canvasRef}
          width={100}
          height={100}
          className="rounded-full cursor-pointer hover:ring-1 hover:ring-white/20 transition-all"
          onClick={handlePointer}
        />
      </div>

      {/* Luminance slider */}
      <div className="w-full mt-1">
        <div className="flex justify-between text-[9px] text-zinc-500 font-mono">
          <span>Lum</span>
          <span>{wheel.luminance > 0 ? `+${wheel.luminance.toFixed(2)}` : wheel.luminance.toFixed(2)}</span>
        </div>
        <input
          type="range"
          min={-1}
          max={1}
          step={0.02}
          value={wheel.luminance}
          onChange={(e) => onChange({ ...wheel, luminance: parseFloat(e.target.value) })}
          className="w-full h-1 bg-zinc-800 rounded-lg appearance-none cursor-pointer accent-amber-400"
        />
      </div>
    </div>
  );
}

export default function ColorWheelsCanvas({ wheels, onChange }: ColorWheelsCanvasProps) {
  return (
    <div className="p-3 bg-zinc-900/40 rounded-xl border border-white/5 space-y-2">
      <div className="text-[11px] font-bold uppercase tracking-wider text-zinc-400">
        3-Way Color Wheels (Lift / Gamma / Gain)
      </div>
      <div className="grid grid-cols-3 gap-2">
        <SingleWheel
          title="Lift (Shadows)"
          wheel={wheels.lift}
          onChange={(w) => onChange({ ...wheels, lift: w })}
        />
        <SingleWheel
          title="Gamma (Mids)"
          wheel={wheels.gamma}
          onChange={(w) => onChange({ ...wheels, gamma: w })}
        />
        <SingleWheel
          title="Gain (Highlights)"
          wheel={wheels.gain}
          onChange={(w) => onChange({ ...wheels, gain: w })}
        />
      </div>
    </div>
  );
}

