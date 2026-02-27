# ElectricBox

3D-printable parametric box for mounting barrier/terminal strip connectors on a model railroad layout. Generated in four slot-count variants from a single FreeCAD model.

## Parts

- **ElectricBox2Slot** — 2-position terminal strip mount
- **ElectricBox4Slot** — 4-position terminal strip mount
- **ElectricBox6Slot** — 6-position terminal strip mount
- **ElectricBox8Slot** — 8-position terminal strip mount

## Quick Start

### Print Settings
| Setting | Value |
|---------|-------|
| Material | PETG |
| Printer | Prusa Core One |
| Supports | None |

## Project Structure

```
ElectricBox/
├── README.md              # This file
├── freecad/               # FreeCAD source files
│   └── ElectricBox.FCStd
├── printed_files/         # STL exports
│   ├── ElectricBox2Slot.stl
│   ├── ElectricBox4Slot.stl
│   ├── ElectricBox6Slot.stl
│   └── ElectricBox8Slot.stl
└── docs/                  # Reference datasheets
    └── barrierstrip.pdf
```

## License

GNU General Public License v3.0 - see repository root.
