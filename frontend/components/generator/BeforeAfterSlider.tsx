"use client";

import React, { useState, useRef, useEffect, useCallback } from "react";
import { Maximize2, Minimize2, Columns, Eye, ZoomIn, ZoomOut, RotateCcw } from "lucide-react";

interface BeforeAfterSliderProps {
  originalUrl: string;
  gradedUrl: string;
  aspectRatio?: string;
  className?: string;
}

export default function BeforeAfterSlider({
  originalUrl,
  gradedUrl,
  className = "",
}: BeforeAfterSliderProps) {
  const [sliderPos, setSliderPos] = useState<number>(50); // percentage 0 to 100
  const [isDragging, setIsDragging] = useState<boolean>(false);
  const [viewMode, setViewMode] = useState<"split" | "side-by-side" | "hold">("split");
  const [isHoldingOriginal, setIsHoldingOriginal] = useState<boolean>(false);
  const [zoomLevel, setZoomLevel] = useState<number>(1); // 1 = fit, 1.5, 2
  const [isFullscreen, setIsFullscreen] = useState<boolean>(false);

  const containerRef = useRef<HTMLDivElement>(null);

  const handleMove = useCallback(
    (clientX: number) => {
      if (!containerRef.current) return;
      const rect = containerRef.current.getBoundingClientRect();
      const x = clientX - rect.left;
      const percentage = Math.max(0, Math.min(100, (x / rect.width) * 100));
      setSliderPos(percentage);
    },
    []
  );

  const handleTouchMove = useCallback(
    (e: TouchEvent) => {
      if (!isDragging) return;
      handleMove(e.touches[0].clientX);
    },
    [isDragging, handleMove]
  );

  const handleMouseMove = useCallback(
    (e: MouseEvent) => {
      if (!isDragging) return;
      handleMove(e.clientX);
    },
    [isDragging, handleMove]
  );

  const handleMouseUp = useCallback(() => {
    setIsDragging(false);
  }, []);

  useEffect(() => {
    if (isDragging) {
      window.addEventListener("mousemove", handleMouseMove);
      window.addEventListener("mouseup", handleMouseUp);
      window.addEventListener("touchmove", handleTouchMove);
      window.addEventListener("touchend", handleMouseUp);
    }
    return () => {
      window.removeEventListener("mousemove", handleMouseMove);
      window.removeEventListener("mouseup", handleMouseUp);
      window.removeEventListener("touchmove", handleTouchMove);
      window.removeEventListener("touchend", handleMouseUp);
    };
  }, [isDragging, handleMouseMove, handleMouseUp, handleTouchMove]);

  const toggleFullscreen = () => {
    if (!containerRef.current) return;
    if (!document.fullscreenElement) {
      containerRef.current.requestFullscreen().catch(() => {});
      setIsFullscreen(true);
    } else {
      document.exitFullscreen().catch(() => {});
      setIsFullscreen(false);
    }
  };

  return (
    <div className={`flex flex-col h-full bg-zinc-950 rounded-xl border border-white/10 overflow-hidden ${className}`}>
      {/* Top Toolbar */}
      <div className="flex items-center justify-between px-4 py-2.5 bg-zinc-900/90 border-b border-white/10 text-xs text-zinc-300">
        {/* Mode Selectors */}
        <div className="flex items-center gap-1 bg-zinc-950 p-0.5 rounded-lg border border-white/10">
          <button
            onClick={() => setViewMode("split")}
            className={`flex items-center gap-1.5 px-2.5 py-1 rounded-md transition-colors ${
              viewMode === "split" ? "bg-amber-500 text-zinc-950 font-bold" : "hover:text-white"
            }`}
            title="Interactive Split Slider"
          >
            <Columns className="w-3.5 h-3.5" />
            <span>Split Slider</span>
          </button>
          <button
            onClick={() => setViewMode("side-by-side")}
            className={`flex items-center gap-1.5 px-2.5 py-1 rounded-md transition-colors ${
              viewMode === "side-by-side" ? "bg-amber-500 text-zinc-950 font-bold" : "hover:text-white"
            }`}
            title="Side-by-Side Comparison"
          >
            <Columns className="w-3.5 h-3.5 rotate-90" />
            <span>Side by Side</span>
          </button>
          <button
            onMouseDown={() => setIsHoldingOriginal(true)}
            onMouseUp={() => setIsHoldingOriginal(false)}
            onTouchStart={() => setIsHoldingOriginal(true)}
            onTouchEnd={() => setIsHoldingOriginal(false)}
            className={`flex items-center gap-1.5 px-2.5 py-1 rounded-md transition-colors select-none ${
              isHoldingOriginal ? "bg-rose-500 text-white font-bold" : "hover:text-white"
            }`}
            title="Hold to temporarily view original"
          >
            <Eye className="w-3.5 h-3.5" />
            <span>Hold for Original</span>
          </button>
        </div>

        {/* Zoom & View Controls */}
        <div className="flex items-center gap-2">
          <div className="flex items-center gap-1 bg-zinc-950 px-2 py-1 rounded-md border border-white/10">
            <button
              onClick={() => setZoomLevel((z) => Math.max(0.75, z - 0.25))}
              className="hover:text-white transition-colors"
              title="Zoom out"
            >
              <ZoomOut className="w-3.5 h-3.5" />
            </button>
            <span className="font-mono text-[11px] text-zinc-400 w-10 text-center">
              {Math.round(zoomLevel * 100)}%
            </span>
            <button
              onClick={() => setZoomLevel((z) => Math.min(2.5, z + 0.25))}
              className="hover:text-white transition-colors"
              title="Zoom in"
            >
              <ZoomIn className="w-3.5 h-3.5" />
            </button>
            <button
              onClick={() => setZoomLevel(1)}
              className="ml-1 pl-1 border-l border-white/10 hover:text-white"
              title="Fit to screen"
            >
              <RotateCcw className="w-3 h-3" />
            </button>
          </div>

          <button
            onClick={toggleFullscreen}
            className="p-1.5 bg-zinc-950 hover:bg-zinc-800 rounded-md border border-white/10 text-zinc-400 hover:text-white transition-colors"
            title="Toggle fullscreen"
          >
            {isFullscreen ? <Minimize2 className="w-3.5 h-3.5" /> : <Maximize2 className="w-3.5 h-3.5" />}
          </button>
        </div>
      </div>

      {/* Main Visual Canvas Container */}
      <div
        ref={containerRef}
        className="relative flex-1 w-full h-full min-h-[420px] bg-zinc-950 checkerboard flex items-center justify-center overflow-hidden select-none"
      >
        <div
          className="relative max-w-full max-h-full flex items-center justify-center transition-transform duration-100"
          style={{ transform: `scale(${zoomLevel})` }}
        >
          {viewMode === "split" && (
            <div className="relative inline-block max-w-[85vw] max-h-[72vh] overflow-hidden rounded-lg shadow-2xl border border-white/10">
              {/* Underneath: Original Image */}
              {/* eslint-disable-next-line @next/next/no-img-element */}
              <img
                src={originalUrl}
                alt="Original source frame"
                className="block max-h-[72vh] w-auto object-contain pointer-events-none"
              />

              {/* Overlaid: Graded Image with clip path */}
              <div
                className="absolute inset-0 overflow-hidden pointer-events-none"
                style={{
                  clipPath: isHoldingOriginal
                    ? "polygon(0 0, 0 0, 0 100%, 0% 100%)"
                    : `polygon(0 0, ${sliderPos}% 0, ${sliderPos}% 100%, 0 100%)`,
                }}
              >
                {/* eslint-disable-next-line @next/next/no-img-element */}
                <img
                  src={gradedUrl}
                  alt="Graded color look"
                  className="block max-h-[72vh] w-auto object-contain pointer-events-none"
                />
              </div>

              {/* Comparison Split Line & Draggable Handle */}
              {!isHoldingOriginal && (
                <div
                  className="absolute top-0 bottom-0 w-0.5 bg-white cursor-ew-resize z-20 shadow-[0_0_10px_rgba(0,0,0,0.8)]"
                  style={{ left: `${sliderPos}%` }}
                  onMouseDown={(e) => {
                    e.preventDefault();
                    setIsDragging(true);
                  }}
                  onTouchStart={(e) => {
                    setIsDragging(true);
                  }}
                >
                  {/* Circular Grabber Reticle */}
                  <div className="absolute top-1/2 -translate-y-1/2 -translate-x-1/2 w-8 h-8 rounded-full bg-zinc-900/90 border-2 border-amber-400 flex items-center justify-center shadow-lg cursor-grab active:cursor-grabbing">
                    <div className="flex items-center gap-0.5 text-zinc-300">
                      <span className="text-[9px] font-bold text-amber-400">◄</span>
                      <span className="text-[9px] font-bold text-amber-400">►</span>
                    </div>
                  </div>
                </div>
              )}

              {/* Top Corner Labels */}
              <div className="absolute top-3 left-3 px-2.5 py-1 rounded-md bg-zinc-950/80 backdrop-blur-md border border-white/10 text-[11px] font-bold tracking-wider text-amber-400 uppercase pointer-events-none shadow-md">
                Graded
              </div>
              <div className="absolute top-3 right-3 px-2.5 py-1 rounded-md bg-zinc-950/80 backdrop-blur-md border border-white/10 text-[11px] font-bold tracking-wider text-zinc-400 uppercase pointer-events-none shadow-md">
                Original
              </div>
            </div>
          )}

          {viewMode === "side-by-side" && (
            <div className="grid grid-cols-2 gap-3 max-w-[90vw] max-h-[72vh] p-2">
              <div className="relative rounded-lg overflow-hidden border border-white/10 shadow-xl">
                {/* eslint-disable-next-line @next/next/no-img-element */}
                <img
                  src={originalUrl}
                  alt="Original source"
                  className="max-h-[68vh] w-auto object-contain"
                />
                <div className="absolute top-3 left-3 px-2 py-0.5 rounded bg-zinc-950/80 text-[10px] font-bold tracking-wider text-zinc-400 uppercase border border-white/10">
                  Original
                </div>
              </div>
              <div className="relative rounded-lg overflow-hidden border border-amber-500/30 shadow-xl">
                {/* eslint-disable-next-line @next/next/no-img-element */}
                <img
                  src={gradedUrl}
                  alt="Graded result"
                  className="max-h-[68vh] w-auto object-contain"
                />
                <div className="absolute top-3 left-3 px-2 py-0.5 rounded bg-amber-500 text-zinc-950 text-[10px] font-black tracking-wider uppercase shadow-md">
                  Graded
                </div>
              </div>
            </div>
          )}

          {viewMode === "hold" && (
            <div className="relative inline-block max-w-[85vw] max-h-[72vh] overflow-hidden rounded-lg shadow-2xl border border-white/10">
              {/* eslint-disable-next-line @next/next/no-img-element */}
              <img
                src={isHoldingOriginal ? originalUrl : gradedUrl}
                alt="Frame comparison"
                className="block max-h-[72vh] w-auto object-contain"
              />
              <div className="absolute top-3 left-3 px-3 py-1 rounded-md bg-zinc-950/80 text-xs font-bold uppercase tracking-wider text-white border border-white/10">
                {isHoldingOriginal ? "Showing: Original (Raw)" : "Showing: Graded (Look Applied)"}
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

