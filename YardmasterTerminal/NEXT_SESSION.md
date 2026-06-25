# YardmasterTerminal — Next Session

## Open items (as of 2026-06-25)

### 1. Revert auto-touched FCStd files in CADlayout (housekeeping)
FreeCAD silently modified four tracked FCStd files when it opened on 2026-06-24.
These are NOT intentional edits — revert before doing any other CADlayout work:

```bash
cd /home/abyrne/Projects/Trains/CADlayout
git checkout -- CurrentLimitBox/freecad/CurrentLimitBox.FCStd \
                PowerBox/freecad/PowerBox.FCStd \
                Servo/freecad/TrainOrderServoInLine.FCStd \
                SplineBracket/freecad/SplineBracket.FCStd
```

### 2. Validate prints
Once Enclosure print completes, verify:
- Bezel rims close flush against enclosure (no gap — depth increased 12→13.6mm for BOARD_T=1.6mm)
- Connector slot is on the correct side (lower-left from front = −X in model)
- Enclosure corner chamfers seat cleanly in wedge V-groove
- M3×12 screws engage enclosure bosses (5mm thread depth, Ø2.5mm bore)
- HOLE_DIA=3.2mm confirmed correct (2026-06-25)

### 3. RPi3 dock (main remaining CAD work)
Design a dock at the wedge's Bs (deep/bottom) corner that mounts the RPi3 board.

Key constraints:
- Attaches to the wedge **bottom leg** via the 4× RPi3 clearance holes (M2.5, Ø3.0mm,
  added 2026-06-25): X=[-24.5, 33.5] mm, Y=[11.9, 60.9] mm (board centred on wedge)
- Small fans on hand — plan for fan mounting holes/vents
- RPi3 standard hole pattern: 85×56mm board, holes at
  (3.5,3.5)(3.5,52.5)(61.5,3.5)(61.5,52.5) Ø2.7mm (unconfirmed — measure to verify)
- Lock-screw bore at Y=81.8mm is accessible from below; confirm this is OK once
  dock is designed (may need clearance notch in dock)

## Completed this session (2026-06-25)
- ✅ Wedge bottom leg: 4× M2.5 clearance holes for RPi3 mounting (Ø3.0mm)
- ✅ TechDraw SVG: `drawings/YardmasterTerminal_v3.svg` (9-view, scale 1:3)
- ✅ Wedge STL re-exported: `YardmasterTerminal_Wedge_v3.stl`
