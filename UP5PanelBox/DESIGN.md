# UP5PanelBox — Design Notes

Mounting box for the Digitrax UP5 Universal LocoNet Panel.
**Two-piece design (V4, Rev3):** Front Panel Bezel + single-piece Component Box.
Frame attachment via screw tabs on box side walls, #6 wood screws driven vertically (Y axis) from below into 1×2 frame bottom face.

---

## Coordinate System

```
X = width  (0 = left/end-cap,  82 = right/entry)
Y = height (0 = bottom, 64 = top / frame face)
Z = depth  (0 = front face / brim face, positive into module)
```

---

## UP5 Physical Shape

The UP5 is T-shaped when viewed from above (XZ plane):

```
Top view (XZ plane):

X=0                X=82
  ┌──────────────────┐   Z=0   ← front panel face (1.5mm thick)
  └──┬────────────┬──┘   Z=1.5 ← panel back / box brim face
     │            │
     │   board    │            ← circuit board (65mm wide, ~57mm deep)
     │            │
     └────────────┘   Z=~58
  X=9.5          X=74.5

Panel (crossbar of T): 80mm wide × 60mm tall × 1.5mm thick
Board (stem of T):     65mm wide × ~26mm tall × ~57mm deep
```

- **Panel width (X=80mm)** → drives bezel outer width (82mm with 2mm border each side)
- **Board width (X=65mm)** → drives component box interior width

---

## Two-Part Design (V4)

### Part 1 — Front Panel Bezel

Holds the UP5 panel by its edges. Mounts permanently to the underside of the layout frame.
Assembly (panel + box) slides into the bezel from the **open end** (X=82 face, −X direction).

```
Front face (Z=0):
┌──────────────────────────────────────────────────────────────────┐  Y=64
│  border                                                           │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │  74×54mm inner window (8mm triangle corners)              │   │
│  │  (UP5 panel face visible here)                            │   │
│  └──────────────────────────────────────────────────────────┘   │
│  border                                                           │
└──────────────────────────────────────────────────────────────────┘  Y=0
X=0 (end cap)                                               X=82 (open)

Side view (YZ cross-section at centre):
        ┌──────────┐  Z=5.6 ← back wall start (brim slot + tol)
        │          │
        │  slots   │  Z=2.0–5.6: panel slot (Z=2.0–3.7) + brim slot (Z=3.5–5.6)
        │          │
┌───────┘          │  Z=2.0
│  front face ring │  Z=0–2
└────────────────────────── Y
        OPEN at X=82 (assembly entry from short side)
        CLOSED at X=0 (end cap / assembly stop)
```

**Bezel geometry:**
| Feature | Value | Notes |
|---|---|---|
| Outer (nominal) | 82×64×10mm | Full corners, +2mm bow on Y faces |
| Y-face bow | ±2mm at X=41 | Gentle convex arc on Y=0 and Y=64 outer faces |
| Front ring depth | 2mm | Z=0–2 |
| Inner window | 74×54mm | 8mm triangle corners |
| Front border | 3mm | All sides |
| Panel slot | 60.6mm Y × 1.7mm Z | Z=2.0–3.7; +0.3mm/edge Y tol, +0.2mm Z tol |
| Brim slot | 36mm Y × 2.1mm Z | Z=3.5–5.6; +0.1mm Z tol |
| Brim slot width | X=4.5–82 (77.5mm) | Open at X=82 |
| Back wall opening | 65×26mm | X=9.5–82, Y=18–44; box body passes through |
| Brim back support | 5mm each side | Solid bezel backs the brim overhang → Z-lock |
| Gusset clearance | X=4.5–9.5 (left), X=74.5–79.5 (right), Y=34–44, Z=5.5–10 | Clears box tab gussets |
| Back wall total | Z=5.6–10 | 4.4mm remaining |
| Entry | Short side, X=82 | Assembly slides in −X direction |
| Stop | End cap at X=0 | |

**Print orientation:** X=0 end-cap face on print bed. Grows in +X direction. Cross-section 64×10mm.

**3-sided channel** (open at X=82):
- Side 1: front face (Z=0–2)
- Side 2: back wall (Z=5.5+)
- Side 3: left end cap (X=0)
- Open: right face (X=82) — assembly entry

---

### Part 2 — Box (single piece)

Component enclosure that slides into the bezel. Brim captures in brim slot; box body passes through back wall opening.

```
Print orientation: Z=0 brim face on build plate, grows in +Z direction.

Front view (XY at Z=0 — brim face, on build plate):

X=4.5                                         X=79.5
  ┌─────────────────────────────────────────────┐  Y=49  ← brim top
  │                  BRIM                        │
  │     ┌───────────────────────────────────┐   │  Y=44  ← box top / tab top
  │     │                                   │   │
  │  ◉  │         box body front            │  ◉│  ← screw tabs (left & right)
  │     │                                   │   │
  │     └───────────────────────────────────┘   │  Y=18  ← box bottom
  │                  BRIM                        │
  └─────────────────────────────────────────────┘  Y=13  ← brim bottom
X=4.5  X=9.5                         X=74.5  X=79.5
         left tab ─────────────────────── right tab
         X=1.5-9.5                       X=74.5-82.5
```

**Box geometry:**
| Feature | Value | Notes |
|---|---|---|
| Brim | 75×36×2mm | X=4.5–79.5, Y=13–49, Z=0–2 |
| Body | 65×26×59mm | X=9.5–74.5, Y=18–44, Z=0–59 |
| Interior | 58×21.5×57mm | X=13–71, Y=19–40.5, Z=2–59 |
| Side walls | 3.5mm | X direction |
| Floor | 1mm | Y=18–19 |
| Ceiling | 3.5mm | Y=40.5–44 |
| Clearance hole | 58×21.5mm | Through brim face at Z=0–2 (board pass-through) |
| Screw tabs | 8×10×6mm each | Left X=1.5–9.5, Right X=74.5–82.5, Y=34–44, Z=11–17 |
| Screw bore | Ø3.5mm | Centred in tab at Z=14 |
| Countersink | Ø7mm×2mm | From Y=34 face (bottom of tab) |
| Gussets | 45°, Z=3→11 | On brim side of tabs; fills overhang when printing Z-up |
| RJ12 cutout | 3.5×16×18mm | Left wall X=9.5–13, Y=22–38, Z=18.5–36.5 |
| Power cutout | 3.5×16×13mm | Right wall X=71–74.5, Y=21–37, Z=34–47 |

**Print orientation:** Z=0 brim face on build plate. Grows in +Z (59mm tall). No supports needed — gussets bridge the tab overhang.

---

## Assembly Sequence

1. Place UP5 panel (80×60×1.5mm) flat against box brim face (Z=0)
2. Slide assembly (panel + box) into bezel from X=82 (short side) in −X direction:
   - Panel enters panel slot (Z=2.0–3.7)
   - Box brim enters brim slot (Z=3.5–5.6)
3. Assembly stops at X=0 end cap
4. Press assembly up against 1×2 frame bottom face (Y=64)
5. Drive #6 wood screws from below through box tabs → into frame

---

## Frame Mounting Tabs

| Parameter | Value | Notes |
|---|---|---|
| Tab position | Left X=1.5–9.5, Right X=74.5–82.5 | Outside box side walls |
| Tab Y span | Y=34–44 | Top flush with box top |
| Tab Z span | Z=11–17 | 6mm wide |
| Screw centre Z | 14mm | Centre of 1×2 (Z=5–24 approx) |
| Screw bore | Ø3.5mm | #6 clearance, Y-axis |
| Countersink | Ø7mm×2mm | From Y=34 (bottom face) |
| Gusset | 45° triangle, Z=3→11 | Fills brim-side overhang; bezel back wall cleared to match |

---

## Side Wall Connector Cutouts

| Wall | Connector | Z range | Y range | Size (X×Y×Z) |
|---|---|---|---|---|
| Left (X=9.5–13) | RJ12 | Z=18.5–36.5 | Y=22–38 | 3.5×16×18mm |
| Right (X=71–74.5) | Power | Z=34–47 | Y=21–37 | 3.5×16×13mm |

---

## Print Settings (Prusa Core One)

| Setting | Bezel | Box |
|---|---|---|
| Orientation | X=0 end-cap face down | Z=0 brim face down |
| Print height | 82mm (X direction) | 59mm (Z direction) |
| Layer height | 0.2mm | 0.2mm |
| Infill | 25% | 25% |
| Perimeters | 3 | 3 |
| Material | PETG | PETG |
| Supports | None | None |

---

## Tolerance Values (Rev3 — from test print)

| Feature | Nominal | Printed tolerance | Notes |
|---|---|---|---|
| Panel slot Y | 60.0mm | +0.6mm (±0.3/edge) | Panel was tight in Y |
| Panel slot Z | 1.5mm | +0.2mm | Channel too shallow |
| Brim slot Z | 2.0mm | +0.1mm | Brim fit well; minor margin |
| Brim slot Y/X | 36×77.5mm | none | Fit good |

---

## Edge Fillets / Chamfers (Final)

Applied via `generate_up5panelbox.py`. Conservative set — all verified to produce correct volumes.

| Part | Operation | Edges | Notes |
|---|---|---|---|
| Bezel | C0.5 | X=0 end-cap perimeter (4 edges) | Applied pre-bow; bed face |
| Bezel | R0.5 | Z=10 back face outer (2 edges) | Outer perimeter only |
| Box | C0.5 | Z=0 brim outer perimeter (4 edges) | Bed face |
| Box | R0.5 | Z=2 brim top outer (4 edges) | Outer perimeter only |
| Box | R0.5 | Z=59 body top outer (4 edges) | Outer perimeter only |

Note: bezel Z=0 front face and box body vertical corner fillets omitted — complex topology after boolean ops caused degenerate geometry. Can revisit if needed.

---

## Open Items

1. Connector cutout positions — verify against physical board if prints are ever revised

---

## File Locations

| File | Path |
|---|---|
| **Production script** | `scripts/generate_up5panelbox.py` |
| **FreeCAD source** | `freecad/UP5PanelBox_V4.FCStd` |
| **Print STLs** | `printed_files/UP5_V4_Final-Bezel.stl` / `UP5_V4_Final-Box.stl` |
| **Slicer file** | `printed_files/UP5_V4_Final.3mf` |
| **TechDraw drawing** | `drawings/UP5PanelBox_V4.svg` |

---

## Version History

| Version | Date | Description |
|---|---|---|
| V1 | 2026-03-25 | Full 80×60mm box — incorrect |
| V2 | 2026-03-25 | Shelf-bracket + corner bosses — superseded |
| V3 | 2026-03-26 | Two-piece T-shape concept confirmed |
| V3d | 2026-03-27 | Locked: T-shape, split Y=28, cylinder on top half, 1mm floor |
| V4 concept | 2026-03-30 | Three-piece: Bezel + Bottom half + Top half (superseded) |
| V4 Rev1 | 2026-03-30 | Corrected bezel (82×64mm), back wall opening, connector cutouts |
| V4 Rev2 | 2026-03-30 | Pivoted to two-piece: Bezel + single-piece box with brim. Screw tabs on side walls. 45° gussets brim-side. Test printed. |
| V4 Rev3 | 2026-03-31 | Tolerance pass from test print: +0.6mm Y / +0.2mm Z panel slot, +0.1mm Z brim slot. Added 2mm outward arc bow on bezel Y faces. Bezel print orientation confirmed X=0-face-down. |
| V4 Final | 2026-04-01 | Edge fillets/chamfers applied. Production script written. TechDraw 6-view page created (A3 landscape). STLs and SVG exported. |
