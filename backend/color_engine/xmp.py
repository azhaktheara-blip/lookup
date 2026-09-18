"""
THEARA COLOR — Adobe Camera Raw & Lightroom .xmp Preset Generator
Founder: Krai Theara | "Create Your Look"
"""

from xml.etree import ElementTree as ET
from .models import ColorGradeModel


def generate_xmp_preset(
    grade: ColorGradeModel,
    preset_name: str = "THEARA COLOR LOOK",
) -> str:
    """
    Generates a valid Adobe Camera Raw / Lightroom XMP preset XML file.
    Maps internal ColorGradeModel parameters to crs:* Camera Raw settings.
    """
    # Scale parameters to Adobe Camera Raw ranges
    # Exposure in EV: -5.0 to +5.0 -> float
    # Contrast: -100 to +100 -> int
    # Highlights, Shadows, Whites, Blacks: -100 to +100 -> int
    # Saturation, Vibrance: -100 to +100 -> int
    # Temperature: map from -100..100 to relative offset or kelvin shift
    # Tint: -100 to 100 -> int

    hsl = grade.hsl
    wheels = grade.color_wheels

    xmp_template = f"""<x:xmpmeta xmlns:x="adobe:ns:meta/" x:xmptk="Adobe XMP Core 7.0-c000 1.000000, 2024/01/01-00:00:00">
 <rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about=""
    xmlns:crs="http://ns.adobe.com/camera-raw-settings/1.0/"
    crs:PresetType="Normal"
    crs:Cluster=""
    crs:UUID=""
    crs:SupportsAmount="True"
    crs:Amount="{grade.intensity:.2f}"
    crs:ProcessVersion="15.4"
    crs:Exposure2012="{grade.exposure:+.2f}"
    crs:Contrast2012="{int(round(grade.contrast))}"
    crs:Highlights2012="{int(round(grade.highlights))}"
    crs:Shadows2012="{int(round(grade.shadows))}"
    crs:Whites2012="{int(round(grade.whites))}"
    crs:Blacks2012="{int(round(grade.blacks))}"
    crs:Temperature="{int(round(grade.temperature * 15))}"
    crs:Tint="{int(round(grade.tint))}"
    crs:Saturation="{int(round(grade.saturation))}"
    crs:Vibrance="{int(round(grade.vibrance))}"
    crs:GrainAmount="{int(round(grade.grain))}"
    crs:PostCropVignetteAmount="{int(round(-grade.vignette))}"
    crs:HueAdjustmentRed="{int(round(hsl.red.hue))}"
    crs:HueAdjustmentOrange="{int(round(hsl.orange.hue))}"
    crs:HueAdjustmentYellow="{int(round(hsl.yellow.hue))}"
    crs:HueAdjustmentGreen="{int(round(hsl.green.hue))}"
    crs:HueAdjustmentAqua="{int(round(hsl.aqua.hue))}"
    crs:HueAdjustmentBlue="{int(round(hsl.blue.hue))}"
    crs:HueAdjustmentPurple="{int(round(hsl.purple.hue))}"
    crs:HueAdjustmentMagenta="{int(round(hsl.magenta.hue))}"
    crs:SaturationAdjustmentRed="{int(round(hsl.red.saturation))}"
    crs:SaturationAdjustmentOrange="{int(round(hsl.orange.saturation))}"
    crs:SaturationAdjustmentYellow="{int(round(hsl.yellow.saturation))}"
    crs:SaturationAdjustmentGreen="{int(round(hsl.green.saturation))}"
    crs:SaturationAdjustmentAqua="{int(round(hsl.aqua.saturation))}"
    crs:SaturationAdjustmentBlue="{int(round(hsl.blue.saturation))}"
    crs:SaturationAdjustmentPurple="{int(round(hsl.purple.saturation))}"
    crs:SaturationAdjustmentMagenta="{int(round(hsl.magenta.saturation))}"
    crs:LuminanceAdjustmentRed="{int(round(hsl.red.luminance))}"
    crs:LuminanceAdjustmentOrange="{int(round(hsl.orange.luminance))}"
    crs:LuminanceAdjustmentYellow="{int(round(hsl.yellow.luminance))}"
    crs:LuminanceAdjustmentGreen="{int(round(hsl.green.luminance))}"
    crs:LuminanceAdjustmentAqua="{int(round(hsl.aqua.luminance))}"
    crs:LuminanceAdjustmentBlue="{int(round(hsl.blue.luminance))}"
    crs:LuminanceAdjustmentPurple="{int(round(hsl.purple.luminance))}"
    crs:LuminanceAdjustmentMagenta="{int(round(hsl.magenta.luminance))}"
    crs:SplitToningShadowHue="{int(round(wheels.lift.hue))}"
    crs:SplitToningShadowSaturation="{int(round(wheels.lift.saturation * 100))}"
    crs:SplitToningHighlightHue="{int(round(wheels.gain.hue))}"
    crs:SplitToningHighlightSaturation="{int(round(wheels.gain.saturation * 100))}"
    crs:HasSettings="True">
   <crs:Name>
    <rdf:Alt>
     <rdf:li xml:lang="x-default">{preset_name}</rdf:li>
    </rdf:Alt>
   </crs:Name>
  </rdf:Description>
 </rdf:RDF>
</x:xmpmeta>"""
    return xmp_template.strip()

