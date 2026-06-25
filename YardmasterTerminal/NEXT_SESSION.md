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
- HOLE_DIA=3.2mm placeholder — confirm against physical board before final print

### 3. TechDraw SVG for drawings/ (low priority)
`YardmasterTerminal/drawings/` is empty. Per project convention a TechDraw
6-view SVG should live here before the project is fully closed out.

### 4. RPi3 dock (main remaining CAD work)
Design a dock at the wedge's Bs (deep/bottom) corner that mounts the RPi3 board.

Key constraints:
- Attaches to the wedge **bottom leg**, near the Bs deep end
- Small fans on hand — plan for fan mounting holes/vents
- Wedge bottom leg is fully solid (v3) — no existing lightening holes to work around
- RPi3 standard hole pattern: 85×56mm board, holes at
  (3.5,3.5)(3.5,52.5)(61.5,3.5)(61.5,52.5) Ø2.7mm (unconfirmed — measure)
- Confirm lock-screw bore at Y=81.8mm is accessible from below once installed;
  may need to relocate to end cap
