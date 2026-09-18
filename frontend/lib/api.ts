import { ColorGradeModel, GenerationResult, Look, Project, Asset } from "./types";

const API_BASE = "/api/v1";

export async function uploadAsset(file: File, assetType: "original" | "reference", projectId?: string): Promise<Asset> {
  const formData = new FormData();
  formData.append("file", file);
  formData.append("asset_type", assetType);
  if (projectId) formData.append("project_id", projectId);

  const res = await fetch(`${API_BASE}/assets/upload`, {
    method: "POST",
    body: formData,
  });

  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: "Upload failed" }));
    throw new Error(err.detail || "Upload failed");
  }

  return res.json();
}

export async function generateLook(
  prompt: string,
  originalAssetId: string,
  referenceAssetId?: string,
  intensity: number = 1.0,
  projectId?: string
): Promise<GenerationResult> {
  const res = await fetch(`${API_BASE}/generations`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      prompt,
      original_asset_id: originalAssetId,
      reference_asset_id: referenceAssetId || null,
      intensity,
      project_id: projectId || null,
    }),
  });

  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: "Generation failed" }));
    throw new Error(err.detail || "Generation failed");
  }

  return res.json();
}

export async function renderLivePreview(originalAssetId: string, parameters: ColorGradeModel): Promise<string> {
  const res = await fetch(`${API_BASE}/generations/render-preview`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      original_asset_id: originalAssetId,
      parameters,
    }),
  });

  if (!res.ok) {
    throw new Error("Failed to render preview");
  }

  const data = await res.json();
  return data.preview_url;
}

export async function saveLook(lookData: {
  title: string;
  prompt?: string;
  parameters: ColorGradeModel;
  look_dna: any;
  project_id?: string;
  original_asset_id?: string;
  preview_url?: string;
  is_public?: boolean;
  category?: string;
}): Promise<Look> {
  const res = await fetch(`${API_BASE}/looks`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(lookData),
  });

  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: "Failed to save look" }));
    throw new Error(err.detail || "Failed to save look");
  }

  return res.json();
}

export async function fetchMyLooks(): Promise<Look[]> {
  const res = await fetch(`${API_BASE}/looks`);
  if (!res.ok) return [];
  return res.json();
}

export async function fetchPublicLooks(category?: string): Promise<Look[]> {
  const url = category && category !== "All"
    ? `${API_BASE}/looks/public?category=${encodeURIComponent(category)}`
    : `${API_BASE}/looks/public`;
  const res = await fetch(url);
  if (!res.ok) return [];
  return res.json();
}

export async function fetchLookBySlug(slug: string): Promise<Look | null> {
  const res = await fetch(`${API_BASE}/looks/slug/${encodeURIComponent(slug)}`);
  if (!res.ok) return null;
  return res.json();
}

export async function fetchUserCredits(): Promise<{ balance: number; lifetime_used: number }> {
  const res = await fetch(`${API_BASE}/credits/balance`);
  if (!res.ok) return { balance: 50, lifetime_used: 0 };
  return res.json();
}

export function getExportUrl(lookId: string, format: "cube" | "xmp", lutSize: number = 33): string {
  return `${API_BASE}/looks/${lookId}/export`;
}

