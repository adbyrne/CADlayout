# SplineBracket

Two-part 3D-printable bracket system (PETG) to hold premade spline roadbed and attach it to a layout module edge. Uses a single 6.35mm (1/4") vertical bolt through the spline, holder, and bracket. A triangular tongue-and-groove interface prevents rotation.

## Parts

- **Spline Holder** — Block with trapezoid groove that cradles the spline roadbed. V-tongue on bottom for anti-rotation.
- **Gusset Bracket** — L-shaped bracket with dual full-height gusset ribs. Mounts to module edge via horizontal bolt. V-groove on flange top mates with holder tongue.

## Quick Start

### Print Settings
| Setting | Value |
|---------|-------|
| Material | PETG |
| Printer | Prusa Core One |
| Supports | None |
| Orientation | See DESIGN.md |

### Regenerate from Script
```bash
# From FreeCAD Python console:
exec(open("/path/to/scripts/generate_splinebracket.py").read())
```

## Project Structure

```
SplineBracket/
├── README.md              # This file
├── DESIGN.md              # Full technical specification
├── TODO.md                # Status and next steps
├── freecad/               # FreeCAD source files
│   └── SplineBracket.FCStd
├── printed_files/         # STL exports
│   ├── SplineBracket-Holder.stl
│   └── SplineBracket-GussetBracket.stl
└── scripts/               # Parametric build script
    └── generate_splinebracket.py
```

## License

GNU General Public License v3.0 - see repository root.
