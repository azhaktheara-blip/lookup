"use client";

import React from "react";
import { ColorGradeModel } from "@/lib/types";

interface BasicControlsProps {
  grade: ColorGradeModel;
  onChange: (updated: ColorGradeModel) => void;
}

interface SliderRowProps {
  label: string;
  value: number;
  min: number;
  max: number;
  step: number;
  unit?: string;
  onChange: (val: number) => void;
  onReset: () => void;
  defaultValue?: number;
}

function SliderRow({
  label,
  value,
  min,
  max,
  step,
  unit = "",
  onChange,
  onReset,
  defaultValue = 0,
}: SliderRowProps) {
  const isModified = value !== defaultValue;

  return (
    <div className="flex flex-col gap-1 py-1.5">
      <div className="flex items-center justify-between text-xs">
        <span className={`font-medium ${isModified ? "text-amber-400" : "text-zinc-400"}`}>
          {label}
        </span>
        <div className="flex items-center gap-1.5">
          <button
            onClick={onReset}
            className={`text-[10px] font-mono px-1 rounded transition-colors ${
              isModified ? "text-zinc-200 hover:text-amber-400 hover:bg-zinc-800" : "text-zinc-500"
            }`}
            title="Click to reset"
          >
            {value > 0 ? `+${value.toFixed(step < 1 ? 2 : 0)}` : value.toFixed(step < 1 ? 2 : 0)}
            {unit}
          </button>
        </div>
      </div>
      <input
        type="range"
        min={min}
        max={max}
        step={step}
        value={value}
        onChange={(e) => onChange(parseFloat(e.target.value))}
        className="w-full h-1.5 bg-zinc-800 rounded-lg appearance-none cursor-pointer accent-amber-400 hover:accent-amber-300"
      />
    </div>
  );
}

export default function BasicControls({ grade, onChange }: BasicControlsProps) {
  const update = (key: keyof ColorGradeModel, val: any) => {
    onChange({ ...grade, [key]: val });
  };

  return (
    <div className="space-y-4 text-zinc-300">
      {/* Tone & Exposure Section */}
      <div className="p-3 bg-zinc-900/40 rounded-xl border border-white/5 space-y-1">
        <div className="text-[11px] font-bold uppercase tracking-wider text-zinc-400 mb-2">
          Tone & Exposure
        </div>
        <SliderRow
          label="Exposure"
          value={grade.exposure}
          min={-4.0}
          max={4.0}
          step={0.05}
          unit=" EV"
          onChange={(v) => update("exposure", v)}
          onReset={() => update("exposure", 0.0)}
        />
        <SliderRow
          label="Contrast"
          value={grade.contrast}
          min={-100}
          max={100}
          step={1}
          onChange={(v) => update("contrast", v)}
          onReset={() => update("contrast", 0)}
        />
        <SliderRow
          label="Highlights"
          value={grade.highlights}
          min={-100}
          max={100}
          step={1}
          onChange={(v) => update("highlights", v)}
          onReset={() => update("highlights", 0)}
        />
        <SliderRow
          label="Shadows"
          value={grade.shadows}
          min={-100}
          max={100}
          step={1}
          onChange={(v) => update("shadows", v)}
          onReset={() => update("shadows", 0)}
        />
        <SliderRow
          label="Whites"
          value={grade.whites}
          min={-100}
          max={100}
          step={1}
          onChange={(v) => update("whites", v)}
          onReset={() => update("whites", 0)}
        />
        <SliderRow
          label="Blacks"
          value={grade.blacks}
          min={-100}
          max={100}
          step={1}
          onChange={(v) => update("blacks", v)}
          onReset={() => update("blacks", 0)}
        />
      </div>

      {/* White Balance Section */}
      <div className="p-3 bg-zinc-900/40 rounded-xl border border-white/5 space-y-1">
        <div className="text-[11px] font-bold uppercase tracking-wider text-zinc-400 mb-2">
          White Balance
        </div>
        <SliderRow
          label="Temperature (Warm / Cool)"
          value={grade.temperature}
          min={-100}
          max={100}
          step={1}
          onChange={(v) => update("temperature", v)}
          onReset={() => update("temperature", 0)}
        />
        <SliderRow
          label="Tint (Green / Magenta)"
          value={grade.tint}
          min={-100}
          max={100}
          step={1}
          onChange={(v) => update("tint", v)}
          onReset={() => update("tint", 0)}
        />
      </div>

      {/* Saturation & Vibrance Section */}
      <div className="p-3 bg-zinc-900/40 rounded-xl border border-white/5 space-y-1">
        <div className="text-[11px] font-bold uppercase tracking-wider text-zinc-400 mb-2">
          Color Presence
        </div>
        <SliderRow
          label="Master Saturation"
          value={grade.saturation}
          min={-100}
          max={100}
          step={1}
          onChange={(v) => update("saturation", v)}
          onReset={() => update("saturation", 0)}
        />
        <SliderRow
          label="Vibrance (Skin Protect)"
          value={grade.vibrance}
          min={-100}
          max={100}
          step={1}
          onChange={(v) => update("vibrance", v)}
          onReset={() => update("vibrance", 0)}
        />
        <SliderRow
          label="Matte Film Fade"
          value={grade.fade}
          min={0}
          max={100}
          step={1}
          onChange={(v) => update("fade", v)}
          onReset={() => update("fade", 0)}
        />
      </div>

      {/* Film Texture Section */}
      <div className="p-3 bg-zinc-900/40 rounded-xl border border-white/5 space-y-1">
        <div className="text-[11px] font-bold uppercase tracking-wider text-zinc-400 mb-2">
          Film Emulation
        </div>
        <SliderRow
          label="Film Grain"
          value={grade.grain}
          min={0}
          max={100}
          step={1}
          onChange={(v) => update("grain", v)}
          onReset={() => update("grain", 0)}
        />
        <SliderRow
          label="Vignette"
          value={grade.vignette}
          min={-100}
          max={100}
          step={1}
          onChange={(v) => update("vignette", v)}
          onReset={() => update("vignette", 0)}
        />
      </div>
    </div>
  );
}

