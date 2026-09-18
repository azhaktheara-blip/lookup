"use client";

import React, { useRef, useState, useEffect, useCallback } from "react";
import { CurvePoint, CurveSettings } from "@/lib/types";

interface ToneCurveCanvasProps {
  curves: CurveSettings;
  onChange: (updated: CurveSettings) => void;
}

export default function ToneCurveCanvas({ curves, onChange }: ToneCurveCanvasProps) {
  const [activeChannel, setActiveChannel] = useState<"master" | "red" | "green" | "blue">("master");
  const [draggedPointIdx, setDraggedPointIdx] = useState<number | null>(null);
  const canvasRef = useRef<HTMLCanvasElement>(null);

  const points = curves[activeChannel];

  const channelColors = {
    master: "#f4f4f5",
    red: "#ef4444",
    green: "#22c55e",
    blue: "#3b82f6",
  };

  const drawCanvas = useCallback(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext("2d");
    if (!ctx) return;

    const width = canvas.width;
    const height = canvas.height;

    // Clear
    ctx.clearRect(0, 0, width, height);

    // Background grid
    ctx.strokeStyle = "#27272a";
    ctx.lineWidth = 1;

    // 4x4 Grid
    for (let i = 1; i < 4; i++) {
      const pos = (i / 4) * width;
      ctx.beginPath();
      ctx.moveTo(pos, 0);
      ctx.lineTo(pos, height);
      ctx.stroke();

      ctx.beginPath();
      ctx.moveTo(0, pos);
      ctx.lineTo(width, pos);
      ctx.stroke();
    }

    // Diagonal reference
    ctx.strokeStyle = "#3f3f46";
    ctx.setLineDash([4, 4]);
    ctx.beginPath();
    ctx.moveTo(0, height);
    ctx.lineTo(width, 0);
    ctx.stroke();
    ctx.setLineDash([]);

    // Draw curve line through points
    const sorted = [...points].sort((a, b) => a.x - b.x);
    ctx.strokeStyle = channelColors[activeChannel];
    ctx.lineWidth = 2.5;
    ctx.beginPath();

    // Spline through sorted points
    for (let i = 0; i < sorted.length; i++) {
      const px = sorted[i].x * width;
      const py = (1 - sorted[i].y) * height;
      if (i === 0) {
        ctx.moveTo(px, py);
      } else {
        const prev = sorted[i - 1];
        const prevX = prev.x * width;
        const prevY = (1 - prev.y) * height;
        const cpx = (prevX + px) / 2;
        ctx.bezierCurveTo(cpx, prevY, cpx, py, px, py);
      }
    }
    ctx.stroke();

    // Draw control point handles
    sorted.forEach((pt, idx) => {
      const px = pt.x * width;
      const py = (1 - pt.y) * height;

      ctx.fillStyle = idx === draggedPointIdx ? "#e6b042" : "#ffffff";
      ctx.strokeStyle = "#09090b";
      ctx.lineWidth = 2;

      ctx.beginPath();
      ctx.arc(px, py, 5.5, 0, Math.PI * 2);
      ctx.fill();
      ctx.stroke();
    });
  }, [points, activeChannel, draggedPointIdx]);

  useEffect(() => {
    drawCanvas();
  }, [drawCanvas]);

  const handleMouseDown = (e: React.MouseEvent<HTMLCanvasElement>) => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const rect = canvas.getBoundingClientRect();
    const clickX = (e.clientX - rect.left) / rect.width;
    const clickY = 1 - (e.clientY - rect.top) / rect.height;

    // Check if clicked close to an existing point
    const threshold = 0.08;
    const hitIdx = points.findIndex(
      (p) => Math.hypot(p.x - clickX, p.y - clickY) < threshold
    );

    if (hitIdx !== -1) {
      setDraggedPointIdx(hitIdx);
    } else {
      // Add new control point
      const newPoints = [...points, { x: Math.max(0, Math.min(1, clickX)), y: Math.max(0, Math.min(1, clickY)) }];
      onChange({ ...curves, [activeChannel]: newPoints });
      setDraggedPointIdx(newPoints.length - 1);
    }
  };

  const handleMouseMove = (e: React.MouseEvent<HTMLCanvasElement>) => {
    if (draggedPointIdx === null || !canvasRef.current) return;
    const rect = canvasRef.current.getBoundingClientRect();
    const x = Math.max(0, Math.min(1, (e.clientX - rect.left) / rect.width));
    const y = Math.max(0, Math.min(1, 1 - (e.clientY - rect.top) / rect.height));

    const updated = [...points];
    updated[draggedPointIdx] = { x, y };
    onChange({ ...curves, [activeChannel]: updated });
  };

  const handleMouseUp = () => {
    setDraggedPointIdx(null);
  };

  const resetCurve = () => {
    onChange({
      ...curves,
      [activeChannel]: [{ x: 0, y: 0 }, { x: 1, y: 1 }],
    });
  };

  return (
    <div className="p-3 bg-zinc-900/40 rounded-xl border border-white/5 space-y-2">
      {/* Channel Switcher */}
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-1 bg-zinc-950 p-1 rounded-lg border border-white/5">
          {(["master", "red", "green", "blue"] as const).map((ch) => (
            <button
              key={ch}
              onClick={() => setActiveChannel(ch)}
              className={`px-2 py-0.5 rounded text-[11px] font-bold capitalize transition-colors ${
                activeChannel === ch ? "bg-zinc-800 text-white" : "text-zinc-500 hover:text-zinc-300"
              }`}
              style={{ color: activeChannel === ch ? channelColors[ch] : undefined }}
            >
              {ch}
            </button>
          ))}
        </div>
        <button
          onClick={resetCurve}
          className="text-[10px] text-zinc-500 hover:text-amber-400 font-mono"
        >
          Reset Curve
        </button>
      </div>

      {/* Canvas */}
      <div className="relative w-full aspect-square bg-zinc-950 rounded-lg border border-white/10 overflow-hidden flex items-center justify-center">
        <canvas
          ref={canvasRef}
          width={220}
          height={220}
          className="w-full h-full cursor-crosshair"
          onMouseDown={handleMouseDown}
          onMouseMove={handleMouseMove}
          onMouseUp={handleMouseUp}
          onMouseLeave={handleMouseUp}
        />
      </div>
      <p className="text-[10px] text-zinc-500 text-center">
        Click to add control point. Drag to adjust S-curve or matte lift.
      </p>
    </div>
  );
}

