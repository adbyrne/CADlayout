# YardmasterTerminal — Next Session

## Open items (as of 2026-06-24)

### 1. Revert auto-touched FCStd files in CADlayout (housekeeping)
FreeCAD silently modified four tracked FCStd files when it opened today.
These are NOT intentional edits — revert before doing any other CADlayout work:

```bash
cd /home/abyrne/Projects/Trains/CADlayout
git checkout -- CurrentLimitBox/freecad/CurrentLimitBox.FCStd \
                PowerBox/freecad/PowerBox.FCStd \
                Servo/freecad/TrainOrderServoInLine.FCStd \
                SplineBracket/freecad/SplineBracket.FCStd
```

### 2. TechDraw SVG for drawings/ (low priority)
`YardmasterTerminal/drawings/` is empty. Per project convention a TechDraw
6-view SVG should live here before the project is fully closed out. Not
blocking printing, but worth doing before RPi3 dock work starts.

### 3. RPi3 dock (main remaining CAD work)
Design a dock at the wedge's Bs (deep/bottom) corner that mounts the RPi3 board.

Key constraints already settled:
- Attaches to the wedge **bottom leg**, near the Bs deep end (most material there)
- Small fans on hand — plan for fan mounting holes/vents
- Wedge bottom leg has solid material from Y=88 to Y=LEG (≈101.8mm) reserved
  for this (lightening holes stopped at Y=88 in v2; v3 wedge bottom leg is
  fully solid — confirm before drilling holes)
- RPi3 standard hole pattern: 85×56mm board, holes at
  (3.5,3.5)(3.5,52.5)(61.5,3.5)(61.5,52.5) Ø2.7mm (unconfirmed — measure)
- Confirm lock-screw bore at Y=81.8mm is accessible from below once installed;
  may need to relocate to end cap

### 4. Validate prints
Once Bezel and Enclosure prints complete, verify:
- Board tabs seat on bezel standoffs correctly
- M3×12 screws engage enclosure bosses (5mm thread depth, Ø2.5mm bore)
- Enclosure corner seats cleanly in wedge V-groove (R3mm fillet)
- Confirm BOARD_T=1.5mm and HOLE_DIA=3.2mm placeholders match physical board
