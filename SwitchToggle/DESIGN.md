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

## Three-Part Design (v6 — current)

| Part | Qty | Description |
|------|-----|-------------|
| Shell | 1 | 50×50×12mm hollow tray, open front face |
| FrontPlate | 1 | 50×50×3mm plate + 8mm pivot posts, closes shell |
| Lever | 1 | 20×35×6mm paddle with Ø8mm cylinder fulcrum |
| M2 pivot pin | 1 | M2×25mm bolt or 2mm rod through posts + cylinder |
| 2-56 stud | 1 | Short cut section of 2-56 rod (~10mm) |
| 2-56 nut | 1 | Pre-assembled on stud; slides into T-slot from bottom |
| 5mm LED (red) | 2 | Left wall near top (Y=38), right wall near bottom (Y=12) |
| JST-XH 2.5mm 3-pin plug | 1 | LED1, LED2, GND — at control panel end |
| JST-XH 2.5mm 3-pin socket | 1 | On LED cable at SwitchToggle end |
| Resistor (470Ω) | 1 | At control panel end |
| M3×? screw | 4 | Corner fascia mount |

**Assembly sequence:**
1. Install LEDs through shell side wall holes — top LED in left wall (Y=38), bottom LED in right wall (Y=12) — press fit or glue
2. Route LED wires through shell interior; exit through 5mm cable hole in back wall
3. Crimp JST-XH socket onto LED cable
4. Place FrontPlate onto shell (alignment pegs register it); glue with CA
5. Insert lever between posts; pass M2 pin through posts + cylinder; retain with M2 nut
6. Pre-assemble 2-56 stud+nut (thread nut a few turns onto cut stud)
7. Slide stud+nut into T-slot from Y=0 bottom edge — nut into wide pocket, stud into narrow slot
8. Route Gold-N-Rod inner rod through fascia, shell rod slot, FrontPlate slot; thread onto stud

**Print orientation note:** The lever STL has the cylinder protruding below Z=0.
**Flip the lever 180° around the X axis in PrusaSlicer** (smooth operator face on bed).
The cylinder becomes the last 2mm to print — no supports required.

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
| Alignment pegs | Ø2mm × 1.5mm | (5,1)(45,1)(5,49)(45,49) | On front rim |

### FrontPlate — 50 × 50 × 3mm

Glued to shell front rim after electronics installed.

**Features:**
- Pivot posts: 4×4×8mm at X=10..14 and X=36..40, Y=23..27 (22mm gap for lever)
- Pin hole: Ø2.2mm, X-direction through both posts at local Z=7 (world Z=19)
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
Flush at operator face (Z=6), 2mm proud toward fascia (Z=-2..0). Pin hole Ø2.2mm through center.

**T-slot** (at Y=0 bottom edge, fascia face):
- Narrow stud slot: 3mm wide, Z=0..1, open at back face (Z=0) — stud protrudes into shell
- Wide nut pocket: 5.5mm wide, Z=1..4, open at bottom (Y=0) — nut captured, can't pass back
- Front wall: Z=4..6 = 2mm solid — nut hidden from operator

**Arm lengths from cylinder center (Y=17.5):**
- Upper thumb arm: 17.5mm
- Lower cable arm: 17.5mm to pivot, rod hole at Y≈3 → effective arm ≈ 14.5mm
- Cable travel: 5mm at 14.5mm arm → swing = arcsin(5/14.5) ≈ 20°

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
| Posts | 4×4×8mm, world Z=15..23 |
| Post gap | 22mm (X=14 to X=36) |
| Pivot world position | X=25, Y=25, Z=19 |
| Rod slot (shell + plate) | 5×14mm, X=22.5..27.5, Y=8..22 |
| Cable hole | Ø5mm, X=25, Y=28, back wall |
| LED top | Ø5.2mm, left wall X=0..2, Y=38, Z=9 |
| LED bottom | Ø5.2mm, right wall X=48..50, Y=12, Z=9 |
| M3 mount holes | Ø3.4mm, (5,5)(5,45)(45,5)(45,45) |
| Lever | 20mm W × 35mm H × 6mm T |
| Cylinder | Ø8mm × 20mm, center at Y=17.5, Z=2 |
| T-slot stud | 3mm W × Z=0..1, open at back face |
| T-slot nut | 5.5mm W × Z=1..4, open at bottom |
| Effective cable arm | ~14.5mm → 20° swing for 5mm travel |
| Pivot pin | M2 × 25mm (or 2mm rod) |

---

## Design Decisions Log

| # | Decision | Rationale |
|---|----------|-----------|
| 1 | Three-part split (Shell/FrontPlate/Lever) | Electronics access; no bridging |
| 2 | Single rod slot (5×14mm vertical) | ±4mm install tolerance; unit orientation set at install |
| 3 | Cylinder as fulcrum (Ø8mm, X-axis) | Clean pivot, visible feature, symmetric in Y |
| 4 | T-slot rod connection | Pre-assembled stud+nut slides in; no front-face hardware |
| 5 | JST-XH 2.5mm 3-pin | From existing PEBA brand inventory |
| 6 | Resistor at control panel end | Brightness adjustment without touching toggle |
| 7 | Both LEDs red | Single color, one lit at a time |
| 8 | 4×M3 corner screws for fascia mount | Simple v1 fastening |
| 9 | Lever print orientation | Flip 180° in slicer (operator face on bed) |
| 10 | LED diagonal placement (v6) | Top-left + bottom-right: LEDs face opposite sides, clear route indication without obscuring fascia center |

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

*Created: 2026-03-16 | v5 CAD: 2026-03-17 | v6 CAD (baseline): 2026-03-18*
