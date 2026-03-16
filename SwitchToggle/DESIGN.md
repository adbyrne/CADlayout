# SwitchToggle — Design Specification

Fascia-mounted seesaw lever to throw a BluePoint under-table switch machine
via a Sullivan Gold-N-Rod #504 R/C Bowden cable with 2-56 threaded rod ends.

---

## Overview

The SwitchToggle mounts on the 1/8" plastic fascia surface via four M3 corner screws.
The outer R/C cable sheath is fixed in the module foam; only the inner 2-56 threaded
rod slides. The operator pushes the lever paddle up or down to drive the rod 5mm and
throw the BluePoint. Two red 5mm LEDs in the shell top/bottom walls indicate which
route is set (one LED lit at a time). Wiring exits through the back face via a 6mm
cable hole.

---

## Three-Part Design (v1 — as built)

The assembly splits into three printed parts to allow electronics access before closing:

| Part | Qty | Description |
|------|-----|-------------|
| Shell | 1 | 50×50×12mm hollow tray, open front face |
| FrontPlate | 1 | 50×50×3mm plate + 8mm pivot posts, closes shell |
| Lever | 1 | 15×25×4mm seesaw paddle |
| M2 pivot pin | 1 | M2×25mm bolt or 2mm rod, retained with M2 nut |
| 2-56 nut | 1 | Slides into lever nut slot; locks rod |
| 5mm LED (red) | 2 | One in top wall, one in bottom wall |
| JST-XH 2.5mm 3-pin plug | 1 | LED1, LED2, GND — at control panel end |
| JST-XH 2.5mm 3-pin socket | 1 | On LED cable at SwitchToggle end |
| Resistor | 1 | At control panel (see electrical section) |
| M3×? screw | 4 | Corner fascia mount |

**Assembly sequence:**
1. Install LEDs through shell top/bottom wall holes (glue or press fit)
2. Route LED wires through shell interior; exit cable through 6mm back hole
3. Fit JST-XH socket on LED cable
4. Place FrontPlate onto shell (alignment pegs register it)
5. Glue shell + FrontPlate with CA
6. Insert lever between posts; pass M2 pin through posts and lever; retain with M2 nut
7. Thread 2-56 rod through back hole and lever slot; slide 2-56 nut into lever nut slot

---

## Coordinate Frame

- **X** — left/right along fascia (width)
- **Y** — up/down (height)
- **Z** — depth (Z=0 back/fascia face, Z=15 FrontPlate front face, outward toward operator)

---

## Part Geometry

### Shell — 50 × 50 × 12mm

Hollow tray, open at front face (Z=12). Prints open-face-up with zero bridging.

```
Back face (fascia side)                Front face (open, Z=12)
        ┌─────────────────────────────┐
        │  ○ M3   ╔═════════════╗   ○ M3  │  ← corners at (5,5),(5,45),(45,5),(45,45)
  LED ──│──○  ══>  CAVITY       ║         │
 top    │         ║  46×46×10   ║         │
        │         ║             ║         │  ← LED holes in top/bottom walls at Z=9
  LED ──│──○  ══>  ╚═════════════╝         │
 bot    │  ○ M3   (back wall 2mm)    ○ M3  │
        └─────────────────────────────┘
```

**Back face holes** (all Z-axis, through 2mm back wall):

| Feature | Dia | X | Y | Notes |
|---------|-----|---|---|-------|
| Rod hole A | 5mm | 25 | 15 | lever slot down → "normal = UP" |
| Rod hole B | 5mm | 25 | 35 | lever flipped → "normal = DOWN" |
| LED cable | 6mm | 25 | 25 | 3-wire cable exit, centered |
| M3 corner × 4 | 3.4mm | 5/45 | 5/45 | fascia mount clearance |

**LED holes:** Ø5.2mm in top wall (Y=48–50) and bottom wall (Y=0–2), at Z=9, centered X=25.

**Alignment pegs:** Ø2mm × 1.5mm, fused to front rim at (5,1), (45,1), (5,49), (45,49).

### FrontPlate — 50 × 50 × 3mm

Solid plate glued to shell front rim. Pivot posts extend 8mm toward operator.

**Pivot posts:** 4×4×8mm rectangular posts at X=10–14 and X=36–40, Y=23–27 (centered Y=25).
Gap between posts: 22mm — lever (15mm) fits with 3.5mm clearance each side.

**Pin hole:** Ø2.2mm, X-direction through both posts at local Z=7 (world Z=19 — post midpoint).

**Peg holes:** Ø2.1mm × 2mm deep at same XY as shell pegs; receive pegs for alignment.

**M3 holes:** Ø3.4mm, Z-direction through plate at all four corners (co-axial with shell).

### Lever — 15 × 25 × 4mm

```
     ┌──────────────┐
     │  THUMB PAD   │  12.5mm — upper arm
     │              │
─────┼──○ pivot ────┼─────  Y=12.5 (world Y=25 at assembly)
     │              │
     │ [===slot===] │  slot at Y=0..5, 2.5mm wide, open bottom edge
     │  └─nut slot  │  nut slot 5.5×3mm transverse, from Y=0 edge
     └──────────────┘
```

**Pivot hole:** Ø2.2mm, X-direction through full 15mm width at Y=12.5, Z=2 (mid-thickness).

**Cable slot:** 2.5×5mm, Z-direction through 4mm thickness, centered X=6.25..8.75, open at Y=0 edge.
The 2-56 rod passes through; slot length absorbs ~1.3mm vertical rod travel during 30° swing.

**Nut slot:** 5.5mm W × 5mm D × 3mm T, from Y=0 edge, centered at Z=2 (Z=0.5..3.5).
2-56 nut (5.50mm corner-to-corner, 2.38mm thick) slides in transversely, rod threads through nut.

**Orientation / flip logic:**
- Lever slot at bottom (Y=0), rod in hole A (Y=15): pivot at world Y=25, slot at world Y=15 → normal route = lever UP
- Flip lever end-for-end: slot now at top (world Y=35), rod in hole B → normal route = lever DOWN
- Single pivot at Y=12.5 maintains 10mm arm to either rod hole in both orientations

**Lever geometry:**
- Arm length: 10mm (pivot to slot center)
- Cable travel: 5mm
- Swing angle: θ = arcsin(5/10) = **30° each way**
- Vertical slot displacement at ±30°: 10×(1−cos30°) ≈ **1.3mm** → 5mm slot gives ample clearance

---

## Cable Connection Detail

```
   BACK (Z=0)                                      FRONT (Z=15+)

 [foam] [fascia] ── Z=0 ── [shell back wall] ──── [front plate] ── [posts/lever]

  R/C outer sheath (glued in foam, not shown)

  2-56 rod ──→── through shell rod hole (Ø5mm) ──→── through lever cable slot ──→ 2-56 nut in lever slot
```

To connect: thread rod through shell hole and lever slot from back; slide 2-56 nut
into lever nut slot from bottom edge; rod engages nut threads.
To disconnect: unthread 2-56 nut and slide out.

---

## LED Electrical Design

### Circuit

```
Control panel (SPDT switch or DCC decoder output):

  5V ─── switch COM
         switch NC ─── R1(470Ω) ─── [LED1 wire] ────→ LED_TOP(+) ──→ GND wire
         switch NO ─── R1(470Ω) ─── [LED2 wire] ────→ LED_BOT(+) ──→ GND wire

  JST-XH 2.5mm 3-pin cable to SwitchToggle:
    Pin 1: LED1 signal
    Pin 2: LED2 signal
    Pin 3: GND (common cathode)
```

Resistor is at the control panel end — allows value changes without disturbing
the SwitchToggle. Both LEDs are red; only one is on at a time.

### Resistor Values (5V supply)

| Resistor | Current | Brightness |
|----------|---------|------------|
| 470Ω | ~6mA | Good indicator |
| 1kΩ  | ~3mA | Dim (dark room) |
| 10kΩ | ~0.3mA | Very dim |

---

## Fritzing Schematic

`SwitchToggle_LED_circuit.fzz` — to be created.

---

## Dimensions Summary

| Feature | Dimension |
|---------|-----------|
| Shell | 50 × 50 × 12mm |
| FrontPlate | 50 × 50 × 3mm |
| Pivot post height | 8mm (world Z=15..23) |
| Pivot post gap | 22mm (X=14 to X=36) |
| Pivot world position | X=25, Y=25, Z=19 |
| Rod hole A | Ø5mm, X=25, Y=15, back face |
| Rod hole B | Ø5mm, X=25, Y=35, back face |
| LED cable hole | Ø6mm, X=25, Y=25, back face |
| LED holes | Ø5.2mm, X=25, Y=top/bot walls, Z=9 |
| M3 corner holes | Ø3.4mm, (5,5)(5,45)(45,5)(45,45) |
| Lever | 15mm W × 25mm H × 4mm T |
| Lever cable slot | 2.5mm W × 5mm L, open bottom |
| Lever nut slot | 5.5mm W × 5mm D × 3mm T |
| Pivot pin | M2 × 25mm (or 2mm rod) |
| Arm length | 10mm (pivot to cable slot center) |
| Swing angle | ±30° for 5mm cable travel |

---

## Design Decisions Log

| # | Decision | Rationale |
|---|----------|-----------|
| 1 | Three-part split (Shell/FrontPlate/Lever) | Electronics access; eliminates 46×46mm unsupported bridge |
| 2 | Two rod holes (Y=15, Y=35) | Lever flip selects N/R orientation without extra hardware |
| 3 | Lever pivot at Y=12.5 | Symmetric center maintains 10mm arm in both flip orientations |
| 4 | JST-XH 2.5mm 3-pin | From existing PEBA brand inventory |
| 5 | Resistor at control panel end | Allows brightness adjustment without opening the toggle |
| 6 | Both LEDs red | Single color, one lit at a time — clear indication |
| 7 | 4×M3 corner screws for fascia mount | Simple, reliable v1 fastening |
| 8 | Nut slot from lever bottom edge | Smooth lever face; nut slides in sideways, locked by rod |

---

## v2 Improvement Candidates

See `PLAN_v2.md` for full details. Key items:

- JST-XH connector pocket in shell back wall (captive socket, quick disconnect)
- LED retention features (snap rim or bezel)
- Lever stop nubs on FrontPlate face (±35° limit for positive end feel)
- Thumb pad ergonomics (contoured recess or ribs)
- Shell-to-FrontPlate snap tabs (glue-free assembly, allows rework)
- Fascia-mount collet option (cleaner than 4 corner screws)
- Back face orientation labels (N/R markers near rod holes)
- Rod slot entry chamfer (easier rod threading)

---

*Created: 2026-03-16 | v1 CAD completed: 2026-03-16*
