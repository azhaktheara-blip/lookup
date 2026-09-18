export interface CurvePoint {
  x: number;
  y: number;
}

export interface CurveSettings {
  master: CurvePoint[];
  red: CurvePoint[];
  green: CurvePoint[];
  blue: CurvePoint[];
}

export interface HSLChannel {
  hue: number;
  saturation: number;
  luminance: number;
}

export interface HSLSettings {
  red: HSLChannel;
  orange: HSLChannel;
  yellow: HSLChannel;
  green: HSLChannel;
  aqua: HSLChannel;
  blue: HSLChannel;
  purple: HSLChannel;
  magenta: HSLChannel;
}

export interface ColorWheel {
  hue: number;
  saturation: number;
  luminance: number;
}

export interface ColorWheelsSettings {
  lift: ColorWheel;
  gamma: ColorWheel;
  gain: ColorWheel;
}

export interface ColorGradeModel {
  exposure: number;
  contrast: number;
  highlights: number;
  shadows: number;
  whites: number;
  blacks: number;
  temperature: number;
  tint: number;
  saturation: number;
  vibrance: number;
  fade: number;
  curves: CurveSettings;
  hsl: HSLSettings;
  color_wheels: ColorWheelsSettings;
  grain: number;
  vignette: number;
  intensity: number;
}

export interface LookDNA {
  mood: string;
  temperature_profile: string;
  contrast_profile: string;
  saturation_profile: string;
  highlight_character: string;
  shadow_character: string;
  color_palette: string[];
  key_tags: string[];
}

export interface Asset {
  id: string;
  project_id?: string;
  user_id: string;
  asset_type: "original" | "reference" | "preview";
  storage_path: string;
  filename: string;
  mime_type: string;
  file_size: number;
  width?: number;
  height?: number;
  url: string;
}

export interface Look {
  id: string;
  project_id?: string;
  user_id: string;
  title: string;
  slug: string;
  prompt: string;
  parameters: ColorGradeModel;
  look_dna: LookDNA;
  original_asset_id?: string;
  preview_url?: string;
  is_public: boolean;
  category: string;
  downloads_count: number;
  creator_name?: string;
  created_at: string;
}

export interface Project {
  id: string;
  user_id: string;
  title: string;
  description: string;
  created_at: string;
  updated_at: string;
}

export interface GenerationResult {
  generation_id: string;
  preview_url: string;
  parameters: ColorGradeModel;
  look_dna: LookDNA;
  credits_remaining: number;
}

export const DEFAULT_COLOR_GRADE: ColorGradeModel = {
  exposure: 0.0,
  contrast: 0.0,
  highlights: 0.0,
  shadows: 0.0,
  whites: 0.0,
  blacks: 0.0,
  temperature: 0.0,
  tint: 0.0,
  saturation: 0.0,
  vibrance: 0.0,
  fade: 0.0,
  curves: {
    master: [{ x: 0, y: 0 }, { x: 1, y: 1 }],
    red: [{ x: 0, y: 0 }, { x: 1, y: 1 }],
    green: [{ x: 0, y: 0 }, { x: 1, y: 1 }],
    blue: [{ x: 0, y: 0 }, { x: 1, y: 1 }],
  },
  hsl: {
    red: { hue: 0, saturation: 0, luminance: 0 },
    orange: { hue: 0, saturation: 0, luminance: 0 },
    yellow: { hue: 0, saturation: 0, luminance: 0 },
    green: { hue: 0, saturation: 0, luminance: 0 },
    aqua: { hue: 0, saturation: 0, luminance: 0 },
    blue: { hue: 0, saturation: 0, luminance: 0 },
    purple: { hue: 0, saturation: 0, luminance: 0 },
    magenta: { hue: 0, saturation: 0, luminance: 0 },
  },
  color_wheels: {
    lift: { hue: 0, saturation: 0, luminance: 0 },
    gamma: { hue: 0, saturation: 0, luminance: 0 },
    gain: { hue: 0, saturation: 0, luminance: 0 },
  },
  grain: 0.0,
  vignette: 0.0,
  intensity: 1.0,
};

export const DEFAULT_LOOK_DNA: LookDNA = {
  mood: "Natural Raw",
  temperature_profile: "Neutral 5600K (0)",
  contrast_profile: "Standard Linear (0)",
  saturation_profile: "Natural True Color (0)",
  highlight_character: "Clean Specular",
  shadow_character: "Natural Black",
  color_palette: ["#18181b", "#3f3f46", "#71717a", "#a1a1aa", "#f4f4f5"],
  key_tags: ["Raw", "Neutral", "Unprocessed"],
};

