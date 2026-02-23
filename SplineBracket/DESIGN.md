# SplineBracket Design Specification

## Purpose

Two-part 3D-printable bracket system to hold premade spline roadbed and attach it to a layout module edge. A single 6.35mm (1/4") bolt clamps the spline through the holder and into the bracket. A triangular V-tongue/groove interface prevents the holder from twisting on the bolt.

## Assembly

The bracket mounts vertically to the module edge via a horizontal bolt through the vertical leg. The holder sits on top of the bracket flange, rotated 90° around Y — the holder's Z-axis aligns with the bracket's X-axis. The spline roadbed sits in the holder's groove.

```
        ┌─── Spline roadbed
        │
   ╔════╧════╗  ← Holder (groove cradles spline)
   ║  V-tongue║
   ╠═════════╣  ← Bolt clamps holder to bracket
   ║  V-groove║
   ╠════╤════╝  ← Bracket flange
   ║    │
   ║    │         Gusset ribs (front/back walls)
   ║    │
   ║──(•)───     ← Horizontal bolt to module edge
   ║    │
   ╚════╝        ← Bracket vertical leg
```

## Coordinate Systems

### Holder
- **X**: Width (across the spline), 60mm
- **Y**: Height (vertical), 0 to 32mm
- **Z**: Depth (along the spline), 60mm
- Origin: bottom-left-front of the block

### Bracket
- **X**: Width, 60mm (corresponds to holder Z when assembled)
- **Y**: Height, 0 (top/flange) to -220 (bottom of leg)
- **Z**: Depth, 60mm (corresponds to holder X when assembled)
- Origin: top-left-front of the flange

## Part 1: Spline Holder (60 × 32 × 60mm)

### Groove Profile (trapezoid, centered in X)

```
 X=0          X=60
  ┌────────────┐  Y=32
  │  ╲      ╱  │
  │   ╲    ╱   │  45° taper: Y=27 to Y=32
  │   │    │   │
  │   │    │   │  Straight walls: Y=10 to Y=27
  │   │    │   │
  │   ├────┤   │  Y=10 (groove bottom, 10mm floor)
  │   X=10 X=50│
  │    (•)     │  Bolt hole at X=30, Z=30
  └────────────┘  Y=0
  ├──V-tongue──┤  Y=-3 (apex)
```

| Feature | Value |
|---------|-------|
| Groove bottom width | 40mm (X=10 to X=50) |
| Groove top opening | 30mm (X=15 to X=45) |
| Straight wall height | 17mm (Y=10 to Y=27) |
| Taper zone | 5mm height, 45° (Y=27 to Y=32) |
| Floor thickness | 10mm |
| Bolt hole | 6.35mm dia, vertical (Y-axis), X=30 Z=30, through floor + tongue |

### V-Tongue (anti-rotation)
- Triangular ridge on bottom face, runs full depth along Z
- 10mm wide base (X=25 to X=35), 3mm tall apex at Y=-3
- Centered at X=30

## Part 2: Gusset Bracket

### L-Shape
| Component | Dimensions | Position |
|-----------|-----------|----------|
| Horizontal flange | 60 × 10 × 60mm | Y=-10 to Y=0 |
| Vertical leg | 10 × 120 × 60mm | X=0 to X=10, Y=-120 to Y=0 |

### Gusset Ribs
Two 5mm-thick triangular ribs (front at Z=0–5, back at Z=55–60) with center open for bolt access.

Triangle vertices (XY plane):
- (10, -10) — flange/leg junction
- (60, -10) — outer flange edge
- (10, -120) — leg bottom

### V-Groove (anti-rotation, mates with holder tongue)
- Triangular channel on flange top face, runs full width along X
- 11mm wide base (Z=24.5 to Z=35.5), 3mm deep apex at Y=-3
- Centered at Z=30
- 1mm wider than tongue for easy mating / self-centering

### Bolt Holes
| Bolt | Diameter | Direction | Position |
|------|----------|-----------|----------|
| Upper (to holder) | 6.35mm | Y-axis (vertical) | X=30, Z=30 |
| Lower (to module) | 6.35mm | X-axis (horizontal) | Y=-93, Z=30 |

### Inside Fillets
3mm radius on all inside corners:
- Flange-to-leg junction (between gusset ribs)
- Gusset rib to vertical leg (both ribs)
- Gusset rib to flange underside (both ribs)

## Print Settings

| Setting | Value |
|---------|-------|
| Material | PETG |
| Printer | Prusa Core One |
| Supports | None required |
| Holder orientation | Groove opening up (tongue on bed) |
| Bracket orientation | TBD after test print evaluation |

## Construction Method

Built with Part primitives and boolean operations in FreeCAD 1.0.2 via MCP bridge. See `scripts/generate_splinebracket.py` for the parametric build script.

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2026-02-21 | Initial design. Holder with trapezoid groove + V-tongue. L-bracket with dual full-height 5mm gusset ribs, V-groove, 3mm inside fillets. Test print in progress. |
| 1.0.1 | 2026-02-22 | Corrected bracket leg height 220→120mm and lower bolt hole Y=-193→Y=-93. Test prints successful — project complete. |
