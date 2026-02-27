# CADlayout

FreeCAD parametric designs for model railroad layout infrastructure. All components are 3D-printable on a Prusa Core One (250x210mm build plate), primarily in PETG.

## Projects

| Project | Description |
|---------|-------------|
| [CableClip](CableClip/) | Cable clip for managing layout wiring; standard and extended body variants |
| [CurrentLimitBox](CurrentLimitBox/) | Mounting box for DCC current-limiting components (1156 bulb, slide switch, terminal strip) |
| [ElectricBox](ElectricBox/) | Parametric terminal strip box; 2/4/6/8-slot variants |
| [PowerBox](PowerBox/) | Power distribution box for a layout module |
| [Servo](Servo/) | Servo mount designs for turnout and train order signal control |
| [SplineBracket](SplineBracket/) | Two-part bracket to hold spline roadbed and attach it to a module edge |

## Project Structure Convention

Each project follows a standard layout:

```
ProjectName/
├── README.md              # Overview and print settings
├── DESIGN.md              # Full technical specification (if present)
├── TODO.md                # Status and next steps (if present)
├── freecad/               # FreeCAD source files (.FCStd)
├── printed_files/         # STL and 3MF exports
├── images/                # Screenshots and reference drawings (if present)
├── docs/                  # Reference datasheets (if present)
└── scripts/               # Parametric build scripts (if present)
```

## License

GNU General Public License v3.0
