"use client";

import React from "react";
import { ColorGradeModel } from "@/lib/types";
import ToneCurveCanvas from "./ToneCurveCanvas";
import ColorWheelsCanvas from "./ColorWheelsCanvas";
import HSLEditor from "./HSLEditor";

interface AdvancedControlsProps {
  grade: ColorGradeModel;
  onChange: (updated: ColorGradeModel) => void;
}

export default function AdvancedControls({ grade, onChange }: AdvancedControlsProps) {
  return (
    <div className="space-y-4">
      <ToneCurveCanvas
        curves={grade.curves}
        onChange={(c) => onChange({ ...grade, curves: c })}
      />
      <ColorWheelsCanvas
        wheels={grade.color_wheels}
        onChange={(w) => onChange({ ...grade, color_wheels: w })}
      />
      <HSLEditor
        hsl={grade.hsl}
        onChange={(h) => onChange({ ...grade, hsl: h })}
      />
    </div>
  );
}

