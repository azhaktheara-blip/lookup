"use client";

import React, { useState, useEffect, useRef } from "react";
import Navbar from "@/components/Navbar";
import BeforeAfterSlider from "@/components/generator/BeforeAfterSlider";
import LookDNACard from "@/components/generator/LookDNACard";
import BasicControls from "@/components/generator/BasicControls";
import AdvancedControls from "@/components/generator/AdvancedControls";
import {
  Sparkles,
  Upload,
  Download,
  Save,
  Share2,
  RefreshCw,
  Image as ImageIcon,
  Check,
  Zap,
  Sliders,
  Dna,
  Layers,
  AlertCircle,
  FileCode,
} from "lucide-react";
import {
  ColorGradeModel,
  LookDNA,
  DEFAULT_COLOR_GRADE,
  DEFAULT_LOOK_DNA,
  Asset,
} from "@/lib/types";
import {
  uploadAsset,
  generateLook,
  renderLivePreview,
  saveLook,
  fetchUserCredits,
} from "@/lib/api";

export default function GeneratorPage() {
  // Image assets state
  const [originalAsset, setOriginalAsset] = useState<Asset | null>({
    id: "demo-asset-001",
    user_id: "demo",
    asset_type: "original",
    storage_path: "uploads/demo_original.jpg",
    filename: "demo_original.jpg",
    mime_type: "image/jpeg",
    file_size: 85000,
    url: "/storage/uploads/demo_original.jpg",
  });
  const [referenceAsset, setReferenceAsset] = useState<Asset | null>(null);

  // Look generation & controls state
  const [prompt, setPrompt] = useState<string>(
    "Warm luxury resort commercial during golden hour, with warm highlights, natural skin tones, muted greens and deep cinematic shadows."
  );
  const [grade, setGrade] = useState<ColorGradeModel>(DEFAULT_COLOR_GRADE);
  const [lookDna, setLookDna] = useState<LookDNA>(DEFAULT_LOOK_DNA);
  const [previewUrl, setPreviewUrl] = useState<string>("/storage/previews/demo_graded.webp");

  // UI state
  const [activeTab, setActiveTab] = useState<"basic" | "advanced">("basic");
  const [isGenerating, setIsGenerating] = useState<boolean>(false);
  const [isRenderingPreview, setIsRenderingPreview] = useState<boolean>(false);
  const [isSaving, setIsSaving] = useState<boolean>(false);
  const [saveSuccess, setSaveSuccess] = useState<boolean>(false);
  const [credits, setCredits] = useState<number>(250);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);
  const [lookTitle, setLookTitle] = useState<string>("Golden Hour Cinema");

  const origInputRef = useRef<HTMLInputElement>(null);
  const refInputRef = useRef<HTMLInputElement>(null);

  useEffect(() => {
    fetchUserCredits()
      .then((data) => setCredits(data.balance))
      .catch(() => {});
  }, []);

  // Quick Inspiration Prompts
  const inspirationPrompts = [
    { label: "Golden Hour Cinema", text: "Warm luxury resort commercial during golden hour, with warm highlights, natural skin tones, muted greens and deep cinematic shadows." },
    { label: "Moody Nordic Thriller", text: "Moody cold Nordic thriller aesthetic with slate blue shadows, desaturated greens, and high contrast drama." },
    { label: "35mm Portra Vintage", text: "Analog 35mm film emulation with creamy lifted matte shadows, warm skin tones, and organic silver grain." },
    { label: "Teal & Orange Blockbuster", text: "Classic Hollywood cinematic blockbuster with deep cyan teal shadows and vibrant amber skin highlights." },
    { label: "Vogue Luxury Editorial", text: "High-end luxury fashion editorial with pristine clean tones, soft highlight roll-off, and velvet blacks." },
  ];

  // Handle Original Upload
  const handleOriginalUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;
    try {
      setErrorMessage(null);
      const uploaded = await uploadAsset(file, "original");
      setOriginalAsset(uploaded);
      setPreviewUrl(uploaded.url); // Initially raw
    } catch (err: any) {
      setErrorMessage(err.message || "Failed to upload original image");
    }
  };

  // Handle Reference Upload
  const handleReferenceUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;
    try {
      setErrorMessage(null);
      const uploaded = await uploadAsset(file, "reference");
      setReferenceAsset(uploaded);
    } catch (err: any) {
      setErrorMessage(err.message || "Failed to upload reference image");
    }
  };

  // Trigger AI Look Generation
  const handleGenerate = async () => {
    if (!originalAsset) {
      setErrorMessage("Please upload an original source image first.");
      return;
    }
    try {
      setIsGenerating(true);
      setErrorMessage(null);

      const result = await generateLook(
        prompt,
        originalAsset.id,
        referenceAsset?.id,
        grade.intensity
      );

      setGrade(result.parameters);
      setLookDna(result.look_dna);
      setPreviewUrl(result.preview_url);
      setCredits(result.credits_remaining);
    } catch (err: any) {
      setErrorMessage(err.message || "Look generation failed.");
    } finally {
      setIsGenerating(false);
    }
  };

  // Real-time render preview on slider change (debounce)
  useEffect(() => {
    if (!originalAsset) return;
    const timer = setTimeout(async () => {
      try {
        setIsRenderingPreview(true);
        const newUrl = await renderLivePreview(originalAsset.id, grade);
        setPreviewUrl(newUrl);
      } catch (err) {
        // silent fallback
      } finally {
        setIsRenderingPreview(false);
      }
    }, 400);

    return () => clearTimeout(timer);
  }, [grade, originalAsset]);

  // Handle Save Look
  const handleSaveLook = async () => {
    try {
      setIsSaving(true);
      setErrorMessage(null);
      await saveLook({
        title: lookTitle || "Custom Look",
        prompt,
        parameters: grade,
        look_dna: lookDna,
        original_asset_id: originalAsset?.id,
        preview_url: previewUrl,
        is_public: true,
      });
      setSaveSuccess(true);
      setTimeout(() => setSaveSuccess(false), 2500);
    } catch (err: any) {
      setErrorMessage(err.message || "Failed to save look.");
    } finally {
      setIsSaving(false);
    }
  };

  // Handle Export Download (.cube or .xmp)
  const handleExportDownload = async (format: "cube" | "xmp") => {
    try {
      // First save or ensure look exists
      const saved = await saveLook({
        title: lookTitle || "Custom Look",
        prompt,
        parameters: grade,
        look_dna: lookDna,
        original_asset_id: originalAsset?.id,
        preview_url: previewUrl,
      });

      // Trigger export download
      const downloadUrl = `/api/v1/looks/${saved.id}/export`;
      const res = await fetch(downloadUrl, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ format, lut_size: 33 }),
      });

      if (!res.ok) throw new Error("Export failed");

      const blob = await res.blob();
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = `${lookTitle.replace(/\s+/g, "_")}.${format === "cube" ? "cube" : "xmp"}`;
      document.body.appendChild(a);
      a.click();
      a.remove();
      window.URL.revokeObjectURL(url);
    } catch (err: any) {
      setErrorMessage(err.message || "Failed to download export file.");
    }
  };

  return (
    <div className="min-h-screen bg-[#09090b] text-zinc-100 flex flex-col">
      <Navbar credits={credits} />

      {/* Main Studio Workstation Layout: 3 Columns */}
      <div className="flex-1 max-w-[1720px] w-full mx-auto p-3 sm:p-4 grid grid-cols-1 lg:grid-cols-12 gap-4">
        {/* =========================================================================
            LEFT COLUMN (Col 1-3): Uploads & Reference Info
        ========================================================================= */}
        <aside className="lg:col-span-3 flex flex-col gap-4">
          {/* Original Source Image Card */}
          <div className="p-4 rounded-xl bg-zinc-900/50 border border-white/10 shadow-lg flex flex-col">
            <div className="flex items-center justify-between mb-2.5">
              <span className="text-xs font-bold uppercase tracking-wider text-zinc-300 flex items-center gap-1.5">
                <ImageIcon className="w-3.5 h-3.5 text-amber-400" />
                Original Source
              </span>
              {originalAsset && (
                <span className="text-[10px] text-zinc-500 font-mono truncate max-w-[120px]">
                  {originalAsset.filename}
                </span>
              )}
            </div>

            <div
              onClick={() => origInputRef.current?.click()}
              className="relative group cursor-pointer aspect-video rounded-lg border-2 border-dashed border-white/10 hover:border-amber-500/50 bg-zinc-950 flex flex-col items-center justify-center overflow-hidden transition-all"
            >
              {originalAsset ? (
                <>
                  {/* eslint-disable-next-line @next/next/no-img-element */}
                  <img
                    src={originalAsset.url}
                    alt="Original source thumbnail"
                    className="w-full h-full object-cover"
                  />
                  <div className="absolute inset-0 bg-black/60 opacity-0 group-hover:opacity-100 transition-opacity flex flex-col items-center justify-center text-xs font-medium text-white gap-1">
                    <Upload className="w-4 h-4 text-amber-400" />
                    <span>Replace Source</span>
                  </div>
                </>
              ) : (
                <div className="flex flex-col items-center gap-2 p-4 text-center">
                  <div className="w-10 h-10 rounded-full bg-zinc-900 flex items-center justify-center text-amber-400">
                    <Upload className="w-5 h-5" />
                  </div>
                  <span className="text-xs font-medium text-zinc-300">Click or drag image</span>
                  <span className="text-[10px] text-zinc-500">JPEG, PNG, WebP (up to 25MB)</span>
                </div>
              )}
              <input
                ref={origInputRef}
                type="file"
                accept="image/jpeg,image/png,image/webp"
                onChange={handleOriginalUpload}
                className="hidden"
              />
            </div>
          </div>

          {/* Reference Image Card (Optional Matching) */}
          <div className="p-4 rounded-xl bg-zinc-900/50 border border-white/10 shadow-lg flex flex-col">
            <div className="flex items-center justify-between mb-2.5">
              <span className="text-xs font-bold uppercase tracking-wider text-zinc-300 flex items-center gap-1.5">
                <Layers className="w-3.5 h-3.5 text-amber-400" />
                Reference Look (Optional)
              </span>
              {referenceAsset && (
                <button
                  onClick={() => setReferenceAsset(null)}
                  className="text-[10px] text-rose-400 hover:text-rose-300 font-mono"
                >
                  Clear
                </button>
              )}
            </div>

            <div
              onClick={() => refInputRef.current?.click()}
              className="relative group cursor-pointer aspect-video rounded-lg border-2 border-dashed border-white/10 hover:border-amber-500/50 bg-zinc-950 flex flex-col items-center justify-center overflow-hidden transition-all"
            >
              {referenceAsset ? (
                <>
                  {/* eslint-disable-next-line @next/next/no-img-element */}
                  <img
                    src={referenceAsset.url}
                    alt="Reference thumbnail"
                    className="w-full h-full object-cover"
                  />
                  <div className="absolute inset-0 bg-black/60 opacity-0 group-hover:opacity-100 transition-opacity flex flex-col items-center justify-center text-xs font-medium text-white gap-1">
                    <Upload className="w-4 h-4 text-amber-400" />
                    <span>Replace Reference</span>
                  </div>
                </>
              ) : (
                <div className="flex flex-col items-center gap-2 p-4 text-center">
                  <div className="w-8 h-8 rounded-full bg-zinc-900 flex items-center justify-center text-zinc-400">
                    <Layers className="w-4 h-4" />
                  </div>
                  <span className="text-xs font-medium text-zinc-400">Upload visual reference</span>
                  <span className="text-[10px] text-zinc-500">AI extracts lighting & colorimetry</span>
                </div>
              )}
              <input
                ref={refInputRef}
                type="file"
                accept="image/jpeg,image/png,image/webp"
                onChange={handleReferenceUpload}
                className="hidden"
              />
            </div>
            {referenceAsset && (
              <p className="text-[10px] text-zinc-400 mt-2 italic">
                Reference match active (Costs 15 credits). Will transfer tone curve and chromatic cast.
              </p>
            )}
          </div>

          {/* Project & Title Metadata */}
          <div className="p-4 rounded-xl bg-zinc-900/50 border border-white/10 shadow-lg space-y-3">
            <div className="text-xs font-bold uppercase tracking-wider text-zinc-400">
              Look Title
            </div>
            <input
              type="text"
              value={lookTitle}
              onChange={(e) => setLookTitle(e.target.value)}
              className="w-full px-3 py-2 rounded-lg bg-zinc-950 border border-white/10 text-sm font-semibold text-zinc-100 focus:outline-none focus:border-amber-400"
              placeholder="e.g. Golden Sunset Cinema"
            />
          </div>

          {/* Look DNA Panel */}
          <LookDNACard lookDna={lookDna} />
        </aside>

        {/* =========================================================================
            CENTER COLUMN (Col 4-8): Large Preview & Before/After Comparison
        ========================================================================= */}
        <main className="lg:col-span-5 flex flex-col gap-3">
          {/* Error Banner if any */}
          {errorMessage && (
            <div className="p-3 rounded-lg bg-rose-500/10 border border-rose-500/30 text-xs text-rose-300 flex items-center gap-2">
              <AlertCircle className="w-4 h-4 shrink-0" />
              <span>{errorMessage}</span>
            </div>
          )}

          {/* Comparison Slider Component */}
          <div className="flex-1 min-h-[560px]">
            <BeforeAfterSlider
              originalUrl={originalAsset ? originalAsset.url : "/storage/uploads/demo_original.jpg"}
              gradedUrl={previewUrl}
              className="h-full"
            />
          </div>

          {/* Bottom Action Bar: Export & Save */}
          <div className="p-3 rounded-xl bg-zinc-900/80 border border-white/10 shadow-lg flex flex-wrap items-center justify-between gap-2">
            <div className="flex items-center gap-2">
              <button
                onClick={() => handleExportDownload("cube")}
                className="flex items-center gap-2 px-4 py-2 rounded-lg bg-amber-500 hover:bg-amber-400 text-zinc-950 font-bold text-xs shadow-md shadow-amber-500/20 transition-all"
                title="Export standard 33×33×33 3D LUT"
              >
                <Download className="w-4 h-4" />
                <span>Export .CUBE (33×)</span>
              </button>

              <button
                onClick={() => handleExportDownload("xmp")}
                className="flex items-center gap-2 px-3.5 py-2 rounded-lg bg-zinc-800 hover:bg-zinc-700 text-zinc-200 font-semibold text-xs border border-white/10 transition-all"
                title="Export Adobe Lightroom .xmp Preset"
              >
                <FileCode className="w-4 h-4 text-amber-400" />
                <span>Export .XMP</span>
              </button>
            </div>

            <div className="flex items-center gap-2">
              <button
                onClick={handleSaveLook}
                disabled={isSaving}
                className="flex items-center gap-1.5 px-3 py-2 rounded-lg bg-zinc-950 hover:bg-zinc-800 border border-white/10 text-xs font-medium text-zinc-300 transition-all"
              >
                {saveSuccess ? (
                  <>
                    <Check className="w-3.5 h-3.5 text-emerald-400" />
                    <span className="text-emerald-400">Saved!</span>
                  </>
                ) : (
                  <>
                    <Save className="w-3.5 h-3.5 text-zinc-400" />
                    <span>Save to Library</span>
                  </>
                )}
              </button>
            </div>
          </div>
        </main>

        {/* =========================================================================
            RIGHT COLUMN (Col 9-12): AI Prompt & Color Controls (Basic + Advanced)
        ========================================================================= */}
        <aside className="lg:col-span-4 flex flex-col gap-4">
          {/* AI Style Prompt Card */}
          <div className="p-4 rounded-xl bg-zinc-900/50 border border-white/10 shadow-lg space-y-3">
            <div className="flex items-center justify-between">
              <span className="text-xs font-bold uppercase tracking-wider text-zinc-300 flex items-center gap-1.5">
                <Sparkles className="w-4 h-4 text-amber-400" />
                AI Style Prompt
              </span>
              <span className="text-[10px] text-zinc-500 font-mono">Natural Language</span>
            </div>

            <textarea
              rows={3}
              value={prompt}
              onChange={(e) => setPrompt(e.target.value)}
              placeholder="Describe your desired look (e.g. 'Warm cinematic golden hour with deep shadows and muted greens')..."
              className="w-full p-3 rounded-lg bg-zinc-950 border border-white/10 text-xs text-zinc-200 leading-relaxed focus:outline-none focus:border-amber-400 resize-none"
            />

            {/* Inspiration Chips */}
            <div className="flex flex-wrap gap-1.5">
              {inspirationPrompts.map((chip, idx) => (
                <button
                  key={idx}
                  onClick={() => setPrompt(chip.text)}
                  className="px-2 py-0.5 rounded bg-zinc-950 hover:bg-zinc-800 border border-white/5 text-[10px] font-medium text-zinc-400 hover:text-amber-400 transition-colors"
                >
                  {chip.label}
                </button>
              ))}
            </div>

            {/* Generate Action Button */}
            <button
              onClick={handleGenerate}
              disabled={isGenerating}
              className="w-full py-3 rounded-xl bg-amber-500 hover:bg-amber-400 text-zinc-950 font-black text-sm tracking-wide shadow-lg shadow-amber-500/25 transition-all flex items-center justify-center gap-2 disabled:opacity-50"
            >
              {isGenerating ? (
                <>
                  <RefreshCw className="w-4 h-4 animate-spin" />
                  <span>Computing Color Grade...</span>
                </>
              ) : (
                <>
                  <Sparkles className="w-4 h-4" />
                  <span>
                    Generate Look ({referenceAsset ? "15" : "10"} Credits)
                  </span>
                </>
              )}
            </button>
          </div>

          {/* Intensity Slider */}
          <div className="p-3.5 rounded-xl bg-zinc-900/50 border border-white/10 shadow-lg space-y-1.5">
            <div className="flex items-center justify-between text-xs">
              <span className="font-bold text-zinc-300">Look Intensity</span>
              <span className="font-mono text-amber-400 font-semibold">
                {Math.round(grade.intensity * 100)}%
              </span>
            </div>
            <input
              type="range"
              min={0}
              max={2}
              step={0.05}
              value={grade.intensity}
              onChange={(e) => setGrade({ ...grade, intensity: parseFloat(e.target.value) })}
              className="w-full h-1.5 bg-zinc-800 rounded-lg appearance-none cursor-pointer accent-amber-400"
            />
          </div>

          {/* Creative Controls Tabs: Basic vs Advanced */}
          <div className="p-4 rounded-xl bg-zinc-900/50 border border-white/10 shadow-lg space-y-3 flex-1">
            <div className="flex items-center gap-2 border-b border-white/10 pb-2.5">
              <button
                onClick={() => setActiveTab("basic")}
                className={`flex items-center gap-1.5 px-3 py-1.5 rounded-md text-xs font-bold transition-colors ${
                  activeTab === "basic"
                    ? "bg-amber-500 text-zinc-950"
                    : "text-zinc-400 hover:text-zinc-200"
                }`}
              >
                <Sliders className="w-3.5 h-3.5" />
                <span>Basic Controls</span>
              </button>

              <button
                onClick={() => setActiveTab("advanced")}
                className={`flex items-center gap-1.5 px-3 py-1.5 rounded-md text-xs font-bold transition-colors ${
                  activeTab === "advanced"
                    ? "bg-amber-500 text-zinc-950"
                    : "text-zinc-400 hover:text-zinc-200"
                }`}
              >
                <Dna className="w-3.5 h-3.5" />
                <span>Advanced Wheels & Curves</span>
              </button>
            </div>

            {/* Tab Contents */}
            <div className="max-h-[580px] overflow-y-auto pr-1">
              {activeTab === "basic" ? (
                <BasicControls grade={grade} onChange={setGrade} />
              ) : (
                <AdvancedControls grade={grade} onChange={setGrade} />
              )}
            </div>
          </div>
        </aside>
      </div>
    </div>
  );
}

