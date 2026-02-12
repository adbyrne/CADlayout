# CurrentLimitBox Design Specification

## Purpose

3D-printable box to hold three DCC current-limiting components for a model railroad layout module. The box installs into foam under the layout. A 55-degree angled tab extends from the front edge, making the bulb and switch visible and accessible from below.

## Components

| Component | Key Dimensions | Mounting |
|-----------|---------------|----------|
| 1156 (BA15S) taillight bulb | 26.5mm glass dia, 15mm base dia, ~52mm long, 2mm bayonet pins | Friction-fit clips on angled tab |
| Large panel-mount slide switch | 50mm total X length, 11.8mm x 6.3mm slide opening, 37.5mm screw hole centers | M3 screws through angled tab |
| 5-position terminal strip | 64.7mm wide, 57mm screw hole centers, 9.1mm pitch, 22mm Y-body, 13mm Z-body | Friction-fit cylindrical posts (ElectricBox pattern) |

## Coordinate System

- **X-axis**: Box width (80mm)
- **Y-axis**: Box length (49mm outer). Y=0 is the front edge (tab side).
- **Z-axis**: Box depth (17mm). Z=0 is the floor (presses into foam). Open face at Z=17 (faces downward when mounted).
- 55-degree tab extends from front edge (Y=0) going in +Y and +Z directions.

## Box Dimensions

| Feature | Value | Notes |
|---------|-------|-------|
| Outer width (X) | 80mm | |
| Internal width | 76mm | 2mm walls each side |
| Outer length (Y) | 49mm | |
| Internal cavity length (Y) | 45mm | Terminal strip body (22mm) + wiring clearance |
| Internal depth (Z) | 15mm | |
| Wall/floor thickness | 2mm | |
| Tab angle | 55 deg from horizontal | 35 deg overhang - safe for PETG on Prusa Core One |
| Tab face length | 35mm | Along the angled surface |
| Tab wall thickness | 5mm | Normal to face, for clip/switch mount strength |

## Terminal Strip Placement

- Strip center Y = 24mm (strip body from Y=13 to Y=35)
- Back wall inner face at Y=47, giving 12mm clearance for wire lugs
- 4 cylindrical mounting posts in 2x2 grid (matching ElectricBox pattern):
  - X positions: 11.5mm and 68.5mm (57mm apart, centered on 80mm width)
  - Y positions: 20.06mm and 27.94mm (7.88mm apart, centered on strip)
  - Post diameter: 3.9mm, height: 6.35mm

## Angled Tab Features

All features centered at face midpoint (17.5mm along the 35mm face).

### Bulb Holder (X = 20mm)
- 15.5mm diameter through-hole (0.5mm clearance on 15mm base)
- Two 3mm-wide pin notches on opposite sides along face direction (for BA15S bayonet pins, 1mm tolerance)
- Two friction-fit clips on inner face:
  - 2mm thick (X) x 10mm wide (along face) x 12mm deep (protruding inward)
  - 0.5mm gap from hole edge
  - Positioned at X = 10.75 and X = 29.25

### Slide Switch (X = 55mm)
- 11.8mm x 6.3mm rectangular cutout (slide opening)
- Two M3 mounting holes (3.2mm dia) at X = 36.25 and X = 73.75 (37.5mm apart)

## Layout (looking at angled tab face)

```
         80mm (X)
    ┌──────────────────────────────────────┐
    │                                      │
    │   [clip]  ◯  [clip]   ●  ▬▬▬▬  ●   │  35mm face
    │        (bulb)        (screw)(sw)(screw)
    │                                      │
    └──────────────────────────────────────┘
         X=20              X=55
```

## Print Settings

- **Material**: PETG
- **Printer**: Prusa Core One
- **Orientation**: Floor (Z=0) on bed, tab grows upward
- **Supports**: None required (35 deg overhang)
- **Build plate**: 250mm x 210mm (part fits easily)

## Construction Method

Built with **Part primitives and boolean operations** (`Part.makeBox`, `Part.makeCylinder`, `Part.makePolygon` → `Part.Face` → `extrude`, then `fuse`/`cut`) in FreeCAD 1.0.2. This approach was chosen over PartDesign sketch-on-face because the `create_sketch` MCP tool crashes FreeCAD 1.0.2. See `scripts/generate_currentlimitbox.py` for the parametric build script.

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2026-02-12 | Initial design. Tab angle changed from 45 to 55 deg for PETG printability. Box length increased from 33mm to 49mm for terminal strip access. Switch cutout corrected to measured 11.8x6.3mm. Screw holes changed to cylindrical posts per ElectricBox pattern. |
