# CurrentLimitBox

3D-printable mounting box for DCC current-limiting components on a model railroad layout module. Installs into foam under the layout with an angled tab that makes the indicator bulb and power switch visible from below.

## Components Held

- **1156 (BA15S) taillight bulb** - current limiter / indicator (friction-fit in angled tab)
- **Panel-mount slide switch** - power disconnect (M3 screwed to angled tab)
- **5-position terminal strip** - wiring connections (cylindrical post mount on floor)

## Quick Start

### Print Settings
| Setting | Value |
|---------|-------|
| Material | PETG |
| Printer | Prusa Core One |
| Supports | None |
| Orientation | Floor on bed |

### Regenerate from Script
```bash
# From FreeCAD Python console:
exec(open("/path/to/scripts/generate_currentlimitbox.py").read())
```

## Project Structure

```
CurrentLimitBox/
├── README.md              # This file
├── DESIGN.md              # Full technical specification
├── freecad/               # FreeCAD source files
│   └── CurrentLimitBox.FCStd
├── images/                # Design screenshots
├── printed_files/         # STL and 3MF exports
│   ├── CurrentLimitBox.stl
│   └── CurrentLimitBox (Meshed).stl
└── scripts/               # Parametric build script
    └── generate_currentlimitbox.py
```

## License

GNU General Public License v3.0 - see repository root.
