# Servo

3D-printable servo mount designs for model railroad layout control. Contains FreeCAD projects for different servo mounting applications.

## Parts

- **SwitchServo** — Servo mount for turnout/switch control
- **TrainOrderServo** — Original servo mount for train order signal mechanism (straddles roadbed edge)
- **TrainOrderServoInLine** — Compact variant with both servo brackets and PCA9685 tabs on the same side of the mast hole (nothing under the tracks). Two mirrored versions in one FCStd file:
  - `Body` — PCA9685 tabs to the right of the servo brackets
  - `Body_Flipped` — PCA9685 tabs to the left of the servo brackets (mirrored across YZ plane)

## Quick Start

### Print Settings
| Setting | Value |
|---------|-------|
| Material | PLA |
| Printer | Prusa Core One |
| Supports | None |

## Project Structure

```
Servo/
├── README.md              # This file
├── freecad/               # FreeCAD source files
│   ├── SwitchServo.FCStd
│   ├── TrainOrderServo.FCStd
│   └── TrainOrderServoInLine.FCStd   # Contains Body + Body_Flipped
├── images/                # Reference drawings
│   ├── base_print.pdf
│   ├── bottom_print.pdf
│   └── servo_print.pdf
└── printed_files/         # STL, 3MF, and slicer exports
    ├── TrainOrderServo-Pad003 (Meshed).stl
    ├── TrainOrderServo-Pad003 (Meshed).3mf
    ├── TrainOrderServo-Pad003 (Meshed)_0.4n_0.2mm_PLA_MK4S_59m.bgcode
    ├── TrainOrderServoInLine (Meshed).stl
    └── TrainOrderServoInLine_Flipped (Meshed).stl
```

## License

GNU General Public License v3.0 - see repository root.
