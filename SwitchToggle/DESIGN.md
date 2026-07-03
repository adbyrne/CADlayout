# SwitchToggle — Design Specification

Fascia-mounted seesaw lever to throw a BluePoint under-table switch machine
via a Sullivan Gold-N-Rod #504 R/C Bowden cable with 2-56 threaded rod ends.

---

## Overview

The SwitchToggle mounts on the 1/8" plastic fascia surface via four M3 corner screws.
The outer R/C cable sheath is fixed in the module foam; only the inner 2-56 threaded
rod slides. The operator pushes the lever paddle up or down to drive the rod 5mm and
throw the BluePoint. Two red 5mm LEDs in the shell side walls (top-left and bottom-right) indicate which
route is set (one LED lit at a time). Wiring exits through the back face via a 5mm
cable hole.

---

## Four-Part Design (v9 — current)

| Part | Qty | Description |
|------|-----|-------------|
| Shell | 1 | 50×50×12mm hollow tray, open front face |
| FrontPlate | 1 | 50×50×3mm plate + 4×4mm mortise pockets (no integral posts) |
| Lever | 1 | 20×35×6mm paddle with Ø8mm cylinder + Ø4mm stub axles |
| PivotClip | 2 | 4×6×10mm snap-capture clip; press-fits into FrontPlate mortise |
| 2-56 stud | 1 | Short cut section of 2-56 rod (~10mm) |
| 2-56 nut | 1 | Pre-assembled on stud; slides into T-slot from bottom |
| 5mm LED (red) | 2 | Left wall near top (Y=38), right wall near bottom (Y=12) |
| JST-XH 2.5mm 3-pin plug | 1 | LED1, LED2, GND — at control panel end |
| JST-XH 2.5mm 3-pin socket | 1 | On LED cable at SwitchToggle end |
| Resistor (470Ω) | 1 | At control panel end |
| M3×? screw | 4 | Corner fascia mount |

No external pivot pin or rod required — PivotClips capture the lever stubs.

**Assembly sequence:**
1. Install LEDs through shell side wall holes — top LED in left wall (Y=38), bottom LED in right wall (Y=12) — press fit or glue
2. Route LED wires through shell interior; exit through 5mm cable hole in back wall
3. Crimp JST-XH socket onto LED cable
4. Place FrontPlate onto shell (alignment pegs register it); glue with CA
5. Position lever between the two mortise pockets with stubs pointing left and right
6. Press each PivotClip straight down over its stub — stub snaps through the 3.0mm entry slot into the Ø4.2mm bore; tang seats in FrontPlate mortise
7. Pre-assemble 2-56 stud+nut (thread nut a few turns onto cut stud)
8. Slide stud+nut into T-slot from Y=0 bottom edge — nut into wide pocket, stud into narrow slot
9. Route Gold-N-Rod inner rod through fascia, shell rod slot, FrontPlate slot; thread onto stud

**PivotClip replacement:** If a clip breaks, press a new clip down over the stub — no shell disassembly required.

**Print orientation note:** The lever STL has the cylinder protruding below Z=0.
**Flip the lever 180° around the X axis in PrusaSlicer** (smooth operator face on bed).
The cylinder becomes the last 2mm to print — no supports required.
Print PivotClips upright (tang down, body up) — no supports required.

---

## Coordinate Frame

- **X** — left/right (width)
- **Y** — up/down (height)
- **Z** — depth (Z=0 back/fascia face, increasing toward operator)

---

## Part Geometry

### Shell — 50 × 50 × 12mm

Hollow tray, open at front face (Z=12). Prints open-face-up, zero bridging.

**Back face features:**

| Feature | Size | Position | Notes |
|---------|------|----------|-------|
| Rod slot | 5×14mm | X=22.5..27.5, Y=8..22 | Vertical slot, ±4mm install tolerance |
| Cable hole | Ø5mm | X=25, Y=28 | LED wires |
| M3 mount × 4 | Ø3.4mm | (5,5)(5,45)(45,5)(45,45) | Fascia corner screws |
| LED top | Ø5.2mm | Left wall (X=0..2), Y=38, Z=9 | 7mm clear of M3 at Y=45, faces left |
| LED bottom | Ø5.2mm | Right wall (X=48..50), Y=12, Z=9 | 7mm clear of M3 at Y=5, faces right |
| Alignment pegs | Ø2mm × 1.0mm | (5,1)(45,1)(5,49)(45,49) | On front rim (shortened v7 to clear fillet) |

### FrontPlate — 50 × 50 × 3mm

Glued to shell front rim after electronics installed.

**Features:**
- Mortise pockets: 4×4mm through-holes at X=10..14 and X=36..40, Y=23..27 — accept PivotClip tangs
- Rod clearance slot: 5×14mm at X=22.5..27.5, Y=8..22 (matches shell slot)
- Peg holes: Ø2.1mm × 2mm at same XY as shell pegs
- M3 holes: Ø3.4mm at all four corners

### Lever — 20 × 35 × 6mm with Ø8mm cylinder

```
  Y=35 ┌──────────────────┐
       │                  │
       │   UPPER ARM      │  17.5mm above cylinder center
       │   (thumb grip)   │
       │                  │
  Y=21 ╠══════════════════╣  ← cylinder top
       ║   Ø8mm CYLINDER  ║  cylinder runs X-axis (left-right)
       ║   (fulcrum)      ║  flush at operator face (Z=6)
  Y=13 ╠══════════════════╣  2mm proud at fascia face (Z=-2..0)
       │                  │
       │   LOWER ARM      │  13.5mm below cylinder center
       │   (rod conn.)    │
  Y=0  └────────┬─────────┘
              T-SLOT
         (stud+nut entry)
```

**Cylinder:** Ø8mm × 20mm, X-axis through lever at Y=17.5, Z=2 (local center).
Flush at operator face (Z=6), 2mm proud toward fascia (Z=-2..0). No pin hole (v8).

**Stub axles (v8):** Ø4mm × 5mm, protruding from each cylinder end outward in X.
Left stub: local X=−5..0 → world X=10..15. Right stub: local X=20..25 → world X=35..40.
Stub fills PivotClip bore (Ø4.2mm × 4mm deep) with 1mm in the lever-to-clip gap.

**T-slot** (at Y=0 bottom edge, fascia face):
- Narrow stud slot: 3mm wide, Z=0..1, open at back face (Z=0) — stud protrudes into shell
- Wide nut pocket: 5.5mm wide, Z=1..3, open at bottom (Y=0) — nut captured, can't pass back
- Front wall: Z=3..6 = 3mm solid — nut hidden from operator

**Arm lengths from cylinder center (Y=17.5):**
- Upper thumb arm: 17.5mm
- Lower cable arm: 17.5mm to pivot, rod hole at Y≈3 → effective arm ≈ 14.5mm
- Cable travel: 5mm at 14.5mm arm → swing = arcsin(5/14.5) ≈ 20°

### PivotClip — 4 × 6 × 10mm body + 3.95 × 3.95 × 3mm tang (print × 2)

Replaces the integral pivot posts from v7. Both clips are identical — mirror placement only.

```
  Z=10┌──────────────────┐
      │    BODY (4×6mm)  │  bore at Z=5 (mid-height)
  Z=5 ├──────(O)─────────┤  ← Ø4.2mm bore (X-axis)
      │    entry slot    │  3.0mm wide in Y, open at Z=0
  Z=0 └──────────────────┘  ← rests on FrontPlate front face
      │   TANG (3.95sq)  │  press-fits into FrontPlate 4×4mm mortise
  Z=-3└──────────────────┘
```

**Snap walls:** (CLIP_BODY_Y − CLIP_SNAP_W) / 2 = (6 − 3.0) / 2 = **1.5mm** each side.
Stub (Ø4mm) squeezes through 3.0mm slot → snap feel → seated in Ø4.2mm bore.

**Tang/wall overlap:** (CLIP_TANG_W − CLIP_SNAP_W) / 2 = (3.95 − 3.0) / 2 = **0.475mm** each side —
the solid material bridging the tang to the snap-wall pillars at the Z=0 transition (v9: was
0.2mm with CLIP_TANG_W=3.9/CLIP_SNAP_W=3.5 — thinner than one nozzle line, a print/breakage risk).

**Fillets/chamfers (v9 — previously none):**
- Outer body corners + top cap edges: R0.5mm fillet (cosmetic; scaled down from the 1.5mm used
  on Shell/FrontPlate/Lever to suit the 4×6mm cross-section)
- Bore mouths (both ends): 0.3mm chamfer — eases stub engagement, reduces edge scrape against
  the stub during lever rotation
- Tang leading edge: 0.4mm chamfer — lead-in for the FrontPlate mortise press-fit
- Snap wall root (Z=0, at Y=bore_y−CLIP_SNAP_W/2 and Y=bore_y+CLIP_SNAP_W/2 — the entry
  slot's own wall boundary, not the tang's edge): R0.2mm fillet. This is the root of the
  wall's inner (slot-facing) surface — the face actually pushed by the stub during
  snap-through, fixed at its base — the real bending stress-concentration point (kept
  small so it doesn't widen the slot)

**Assembly:** press clip straight down; bore descends to stub height (world Z=20) at full insertion.

| Feature | Dimension |
|---------|-----------|
| Body | 4×6×10mm (X×Y×Z) |
| Tang | 3.95×3.95×3mm, centred in body XY |
| Bore | Ø4.2mm, X-axis, at Y=3 Z=5 (clip local) = Y=25 Z=20 (world) |
| Entry slot | 3.0mm wide (Y), full X width, Z=0..5 |
| Snap wall | 1.5mm each Y side |
| Tang/wall overlap | 0.475mm each Y side |
| Outer corner/top fillet | R0.5mm |
| Bore mouth chamfer | 0.3mm |
| Tang lead-in chamfer | 0.4mm |
| Snap wall root fillet | R0.2mm |
| Left placement | world X=10, Y=22, Z=15 |
| Right placement | world X=36, Y=22, Z=15 |

---

## Cable Connection

```
  Foam → Fascia → Shell back wall → Shell interior → FrontPlate → Lever T-slot
                  (rod slot 5×14mm)                 (rod slot)    stud protrudes ←→ rod threads on
```

Installation: pre-assemble stud+nut, drop into T-slot from bottom edge, route rod from foam
through slots and thread onto stud. Install: set position in slot, thread rod on.
Disconnect: unthread rod from stud (stud+nut stays in lever).

---

## LED Electrical Design

```
  5V ─── switch COM
         NC ─── R(470Ω) ─── [LED1 wire] ─── LED_TOP(+) ─── GND
         NO ─── R(470Ω) ─── [LED2 wire] ─── LED_BOT(+) ─── GND

  JST-XH 2.5mm 3-pin: Pin1=LED1, Pin2=LED2, Pin3=GND
```

Resistors at control panel end — adjust brightness without disturbing toggle.

---

## Fritzing Schematic

`SwitchToggle_LED_circuit.fzz` — to be created.

---

## Dimensions Summary

| Feature | Dimension |
|---------|-----------|
| Shell | 50 × 50 × 12mm |
| FrontPlate | 50 × 50 × 3mm |
| PivotClip body | 4×6×10mm, world Z=15..25 |
| PivotClip tang | 3.95×3.95×3mm, world Z=12..15 |
| Mortise pockets | 4×4mm, X=10..14 and X=36..40, Y=23..27 |
| Lever stub | Ø4mm×5mm, world X=10..15 (L) and X=35..40 (R) |
| Pivot world position | X=25, Y=25, Z=20 |
| Rod slot (shell + plate) | 5×14mm, X=22.5..27.5, Y=8..22 |
| Cable hole | Ø5mm, X=25, Y=28, back wall |
| LED top | Ø5.2mm, left wall X=0..2, Y=38, Z=9 |
| LED bottom | Ø5.2mm, right wall X=48..50, Y=12, Z=9 |
| M3 mount holes | Ø3.4mm, (5,5)(5,45)(45,5)(45,45) |
| Lever | 20mm W × 35mm H × 6mm T |
| Cylinder | Ø8mm × 20mm, center at Y=17.5, Z=2 |
| T-slot stud | 3mm W × Z=0..1, open at back face |
| T-slot nut | 5.5mm W × Z=1..3, open at bottom |
| Effective cable arm | ~14.5mm → 20° swing for 5mm travel |
| PivotClip snap walls | 1.5mm each side (6mm body − 3.0mm slot) / 2 |
| PivotClip tang/wall overlap | 0.475mm each side (3.95mm tang − 3.0mm slot) / 2 |

---

## Design Decisions Log

| # | Decision | Rationale |
|---|----------|-----------|
| 1 | Three-part split (Shell/FrontPlate/Lever) | Electronics access; no bridging |
| 2 | Single rod slot (5×14mm vertical) | ±4mm install tolerance; unit orientation set at install |
| 3 | Cylinder as fulcrum (Ø8mm, X-axis) | Clean pivot, visible feature, symmetric in Y |
| 11 | Stub axles + PivotClip (v8) | Eliminates M2 pivot pin; no external hardware; clip replaceable without shell disassembly |
| 12 | Snap entry slot 3.0mm < Ø4mm stub (v8; narrowed v9) | Snap-feel install confirms seating; once in bore, requires deliberate force to remove |
| 13 | Clip body 6mm Y vs 4mm mortise (v8) | Extra 2mm each side provides 1.5mm snap walls — adequate flex in PLA/PETG |
| 4 | T-slot rod connection | Pre-assembled stud+nut slides in; no front-face hardware |
| 5 | JST-XH 2.5mm 3-pin | From existing PEBA brand inventory |
| 6 | Resistor at control panel end | Brightness adjustment without touching toggle |
| 7 | Both LEDs red | Single color, one lit at a time |
| 8 | 4×M3 corner screws for fascia mount | Simple v1 fastening |
| 9 | Lever print orientation | Flip 180° in slicer (operator face on bed) |
| 10 | LED diagonal placement (v6) | Top-left + bottom-right: LEDs face opposite sides, clear route indication without obscuring fascia center |
| 14 | Nut pocket height reduced to 2mm (Z=1..3) | Thickens front wall to 3mm (was 2mm) — more material hiding/retaining the nut |
| 15 | PivotClip body height 8mm → 10mm (v9) | Pivot bore centre moves 1mm further from FrontPlate face (world Z=19 → 20) — extra swing clearance so lever doesn't rub against plate/clip base through its ~20° travel |
| 16 | PivotClip tang 3.9→3.95mm, entry slot 3.5→3.0mm (v9) | Tang/wall overlap at Z=0 was 0.2mm — thinner than one nozzle line, a print/breakage risk. Widened to 0.475mm each side |
| 17 | PivotClip fillets/chamfers added (v9) | Previously had none, unlike the other 3 parts. Cosmetic R0.5mm on outer corners/top cap; functional chamfers at bore mouths and tang lead-in; R0.2mm fillet at the snap wall's Z=0 root (inner slot-facing surface, fixed end) — the real bending stress-concentration point during snap-through, distinct from the tang/wall overlap fixed in decision #16 |

---

## v2 Improvement Candidates

See `PLAN_v2.md`.

---

## Reference Screenshots (`docs/`)

| File | Shows |
|------|-------|
| `assembly_isometric.png` | Full three-part assembly, isometric |
| `assembly_side.png` | Assembly side view — lever cylinder + post relationship |
| `shell_back.png` | Shell back face — rod slot, cable hole, M3 holes |
| `shell_left.png` | Shell left side — top LED hole in left wall (Y=38) |
| `shell_right.png` | Shell right side — bottom LED hole in right wall (Y=12) |
| `frontplate_front.png` | FrontPlate front face — posts, pin holes, rod clearance slot |
| `lever_isometric.png` | Lever — T-slot entry visible |
| `lever_back.png` | Lever — smooth operator face |
| `lever_fascia.png` | Lever — cylinder protrusion + T-slot profile |

---

*Created: 2026-03-16 | v5 CAD: 2026-03-17 | v6 CAD (baseline): 2026-03-18 | v7 CAD (fillets): 2026-03-18 | v8 CAD (PivotClip, no external pin): 2026-04-28 | v9 CAD (PivotClip swing clearance + tang/wall reinforcement + fillets/chamfers): 2026-07-03*
