# FoamPowerBox — Design Plan

Foam-embedded power distribution tray for a layout module. Open-top, no lid — foam provides retention.
Files stay in the `PowerBox/` project folder, named `FoamPowerBox.*`.

## Concept

Press the tray into a foam cutout in the module surface. All components are accessible from the top.
Power connector barrel points straight up; plug the AC/DC adapter in from above.

## Components (all in InvenTree)

| Part | InvenTree pk | Notes |
|------|-------------|-------|
| Barrel power connector | — | Press-fit into boss on inner wall |
| 5V 3A 15W DC-DC Step-Down Module | 61 | BINZET/DWEII variants, input 6-28V |
| Barrier terminal strip (2-slot) | — | Same strip as ElectricBox; qty 2 (+5V and +12V) |

## Box Dimensions

| Property | Value | Notes |
|----------|-------|-------|
| Outer footprint | 100 × 90 mm | Widened from PowerBox to fit DC-DC + strips |
| Height | 25 mm (≤ 1") | |
| Wall thickness | 3 mm | |
| Corner radius | 3 mm | Same as PowerBox |
| Inner footprint | 94 × 84 mm | |
| Inner height | 22 mm | 25mm − 3mm floor |
| Lid | none | Open top — foam provides retention |

## Layout (top-down view into open box)

```
 ┌──────────────────────────────────┐  ← 100mm
 │  [ DC-DC converter  (64×53mm)  ] │  upper area, left side
 │                      [+5V strip] │  right side
 │                      [+12V strip]│  right side
 │  [↑barrel]                       │  bottom-left (boss on inner wall)
 └──────────────────────────────────┘
              90mm
```

## Feature Details

### Barrel Connector (bottom-left)

Connector sits in a **boss** (thickened block integral with the left or front inner wall).
Inserted from above; barrel points straight up; press-fit, no screws or snap tabs.
A small lip at the bottom of the housing pocket prevents the connector being pushed toward the box floor.

**Measured dimensions:**

| Feature | Dimension |
|---------|-----------|
| Housing cross-section | 12 × 14 mm |
| Total length (tip to wire end) | 37.2 mm |
| Barrel section length | 23.8 mm (protrudes above box rim) |
| Housing section length | 9.2 mm (captured in boss pocket) |
| Wire end block | 10 × 10 mm sq, 4.2 mm long (one face flush with housing) |

**Pocket / boss design:**

| Feature | Value | Notes |
|---------|-------|-------|
| Pocket cross-section | 12 × 14 mm | Sized for press-fit (slight undersize TBD) |
| Pocket depth | 9.2 mm | Captures full housing section |
| Lip position | 9.2 mm from box rim | Stops housing sliding down |
| Lip inward protrusion | ~1.5 mm on 14mm sides | Wire end (10mm sq) passes below lip |
| Below-lip cavity | ≥ 10 × 10 mm | Clears wire end block |
| Wire end clearance from inner floor | 8.6 mm | Exceeds 5 mm requirement ✓ |
| Boss footprint | ~16 × 14 mm | Housing + ~2 mm wall each side |
| Boss height | Full 25 mm | Integral with side wall |
| Barrel protrusion above box rim | 23.8 mm | Accessible from above foam |

**Note on standard wall:** The 3mm wall is far too thin for the 12×14mm housing.
The boss protrudes 14mm inward from the wall, forming a solid block with the pocket in it.

### DC-DC Converter (upper area, left side)

Sits in a floor pocket. Flanges rest at floor level; components fill most of the internal height.

**Measured dimensions:**

| Feature | Dimension |
|---------|-----------|
| Board body | 50 × 53 mm |
| Mounting flanges | 7 mm each side of 50mm width → 64 mm total width |
| Height (components above board) | 20 mm |

**Pocket design:**

| Feature | Value | Notes |
|---------|-------|-------|
| Pocket footprint | 64 × 53 mm | Full board including flanges |
| Pocket depth | 20 mm | Flush with or just below inner floor rim |
| Clearance above converter | 2 mm | (22mm inner height − 20mm) |
| Flange overlap with strip zone | 5.6 mm in X | Flanges at floor level (Z≈3mm); strip recesses at Z≈19mm — no physical conflict |
| No internal divider needed | — | Between DC-DC and strip areas in the overlap zone |

**Terminal routing:** input terminals face left wall (or front), output terminals face right/back.
Verify orientation on physical part before scripting pocket placement.

### Terminal Strips (right side, stacked in Y)

Two 2-slot barrier strips in recesses matching ElectricBox pocket geometry.
Stacked front-to-back along the right side of the box.

**Known dimensions from ElectricBox:**

| Parameter | Value |
|-----------|-------|
| Slot count per strip | 2 |
| Strip width | 35.58 mm (runs in X, inward from right wall) |
| Strip depth | 22.35 mm (runs in Y per strip) |
| Two strips total Y span | 44.7 mm |
| Recess depth | 6.35 mm from box rim |
| Slot pitch | 9.53 mm center-to-center |
| Slot width | 7.62 mm |
| End wall to first slot | 8.26 mm |

Recess bottom is at Z = 25 − 6.35 = 18.65 mm from box floor — well above DC-DC flanges ✓

## Layout Fit Verification (100 × 90 mm box)

| Component | X range (inner) | Y range (inner) | Z range |
|-----------|----------------|----------------|---------|
| DC-DC (with flanges) | 0 – 64 mm | 0 – 53 mm | floor (20mm tall) |
| Terminal strips (×2) | 58.4 – 94 mm | 0 – 44.7 mm | top 6.35mm recess |
| Barrel boss | left/front wall | 0 – 16 mm Y | full height |
| DC-DC / strip X overlap | 58.4 – 64 mm | — | different Z, no conflict |

All components fit within 94 × 84 mm inner footprint ✓

## Build Approach

Script-based (Python + MCP), same pattern as SwitchToggle.

| File | Purpose |
|------|---------|
| `scripts/generate_foampowerbox.py` | Parametric generate script |
| `printed_files/FoamPowerBox (Meshed).stl` | Print-ready STL export |

### Feature sequence

1. Base pad — 100 × 90 × 25 mm outer shell
2. Interior cavity pocket — full depth, leaving 3mm walls and floor
3. DC-DC converter pocket — 64 × 53 × 20 mm floor recess, upper-left area
4. Barrel connector boss + pocket — integral boss on left/front wall, 12 × 14 mm pocket, 9.2 mm deep, lip at bottom
5. Terminal strip recesses × 2 — right side, stacked in Y, ElectricBox geometry
6. Fillets on outer corners

## Build Approach (actual — Part module CSG)

Script: `scripts/generate_foampowerbox.py` (Part module, not PartDesign — CSG fuse/cut operations)
Run via MCP bridge: `proxy.execute(open('scripts/generate_foampowerbox.py').read())`

| File | Purpose |
|------|---------|
| `scripts/generate_foampowerbox.py` | Generate script |
| `freecad/FoamPowerBox.FCStd` | FreeCAD source |
| `printed_files/FoamPowerBox (Meshed).stl` | Print-ready STL |

### V3 feature summary (as-scripted)
- Outer box: 100×90×25mm, 3mm walls/floor, rounded outer corners R=3mm, open top
- Terminal strip shelves: 22.35mm (X) × 35.58mm (Y) each, inline in Y, shelf top at Z=18.65mm
  - Retention pegs: R=1.8mm, 2mm tall, at 3.56mm inset from each strip end, centred in shelf X
- Barrel U-channel: two 3mm tabs, 14mm gap in Y, 12mm deep in X, full-height
  - Z-stop lip: 2mm protrusion from inner left wall at Z=13.8–15.8mm
  - X-retention lips: 1.5mm×4mm protrusions from each tab face at X=14–18mm, Z=21–25mm
- DC-DC round pegs: R=1.35mm, 2mm tall at (7,68) and (63.4,68)
- DC-DC oval pegs: R=1.4mm stadium (2.8×3mm), 2mm tall at (14,41.5) and (56,41.5)

### V5 feature summary (as-scripted, 2026-03-20)
Changes from V3 test print feedback:
- **Barrel channel**: BC_HX=13mm, BC_HY=15mm (+1mm clearance in both directions)
- **DC-DC oval pegs**: 6mm total Y-length (DCDC_OVL_SEG=1.6mm, was 1.0mm)
- **Strip shelves**: SHELF_Y=42mm each — fill full 84mm interior Y (was 35.58mm each)
- **Strip pegs**: 4 per strip (was 2), R=1.95mm, H=3.175mm (half of 6.35mm recess)
  - Positions from ElectricBox Sketch001: (4.0,7.24), (4.0,15.11), (32.46,7.24), (32.46,15.11) rotated to box coords
- **Strip shelf height**: STRIP_SHELF_H=9.25mm (was 15.65mm) — actual strip depth = 12.75mm
  - Strip mounting surface at Z=12.25mm; strip occupies Z=12.25–25mm (12.75mm total depth)
- **Fillet fix**: outer corner fillets now applied to raw outer box before cavity cut (OCCT topology issue)
  - 4 rounded vertical corners R=3mm confirmed working (79 faces, 40 curved edges, 7184 STL triangles)

### V6 feature summary (as-scripted, 2026-03-21)
Changes from V5 test print feedback:
- **Strip dimensions**: STRIP_W=41.2mm, STRIP_D=22.0mm (from direct measurement; replaces ElectricBox-derived values)
- **Strip peg positions** (from direct measurement of physical strip):
  - STRIP_HOLE_LONG=[4.0, 36.4] — 4mm from short end, 32.4mm hole-to-hole along long axis
  - STRIP_HOLE_DEPTH=[5.8, 16.3] — 5.8mm from long edge, 10.5mm hole-to-hole across short axis
  - Note: strip body is 28mm wide at barriers but only 22mm at mounting base; barrier overhangs shelf
- **Barrel ribs**: 4 vertical press-fit ribs on Y-tab faces (2 per tab) + 2 ribs on inner left wall (X grip)
  - RIB_PROJ=0.35mm, RIB_W=4mm, RIB_H=9.2mm (full connector engagement zone z=15.8–25mm)
- Shape: 113 faces, 40 curved edges, 7292 STL triangles

Screenshots in `docs/`: `FoamPowerBox_iso.png`, `FoamPowerBox_top.png`

### V7 feature summary (as-scripted, 2026-03-21)
Changes from V6 test print feedback:
- **Strip shelf width**: STRIP_SHELF_D=26mm (was 22mm) — +4mm in -X to clear barrier tab overhang
  - STRIP_X_OUTER now 71mm (was 75mm); DC-DC footprint ends ~64mm, gap = 7mm ✓
- **Strip pegs**: R=2.25mm (4.5mm dia), H=8mm (was R=1.95mm, H=3.175mm)
- Shape: 113 faces, 40 curved edges, 7292 STL triangles

## Status

**Session 2026-03-20 (V3):** Test print sent.
**Session 2026-03-20 (V5):** Test print #2 sent.
**Session 2026-03-21 (V6):** Test print #3 sent.
**Session 2026-03-21 (V7):** Test print #4 sent.
**Session 2026-03-21 (V8):** Test print #5 sent (shelf +2mm, no other changes).
**Session 2026-03-21 (V9):** ✅ **Production release.** Test print confirmed. Internal fillets added, STL exported.

### V9 production summary
- Shelf leading top edge: R1.5mm fillet
- Shelf inner vertical corners at x=STRIP_X_OUTER: R1.0mm fillet
- Removed unused `import MeshPart`
- Fixed step numbering and shelf width comment (28mm)
- Shape: 121 faces, 53 curved edges, 11962 STL triangles
- FCStd: `freecad/FoamPowerBox.FCStd`
- STL: `printed_files/FoamPowerBox (Meshed).stl` ← production file
- Screenshots: `docs/FoamPowerBox_iso.png`, `docs/FoamPowerBox_top.png`
