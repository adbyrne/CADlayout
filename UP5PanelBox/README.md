# UP5PanelBox

Mounting box for the Digitrax UP5 Universal LocoNet Panel. Two-piece design:
a front bezel that mounts permanently to the layout frame, and a component box
that slides in from the open end carrying the UP5 board.

![UP5PanelBox ISO view](images/up5panelbox_iso.png)

## Parts

| Part | File | Description |
|------|------|-------------|
| **Bezel** | `UP5_V4_Final-Bezel.stl` | 82×64×10mm; panel slot + brim slot; mounts to frame |
| **Box** | `UP5_V4_Final-Box.stl` | Brim 75×36×2mm + body 65×26×59mm; holds UP5 board |

The UP5 panel slides into the bezel's panel slot (Z=2–3.7mm); the box brim captures in the brim slot (Z=3.5–5.6mm). Box side-wall tabs accept #6 wood screws into the 1×2 frame.

## Quick Start

### Print Settings

| Setting | Bezel | Box |
|---------|-------|-----|
| Orientation | X=0 end-cap face on bed | Z=0 brim face on bed |
| Material | PETG | PETG |
| Supports | None | None |
| Print height | 82mm | 59mm |

### Regenerate from Script

```bash
# From FreeCAD Python console:
exec(open("/home/abyrne/Projects/Trains/CADlayout/UP5PanelBox/scripts/generate_up5panelbox.py").read())
```

### Assembly

1. Place UP5 panel flat against box brim face
2. Slide assembly (panel + box) into bezel from X=82 open end, in −X direction
3. Assembly stops at X=0 end cap
4. Press up against 1×2 frame bottom face (Y=64)
5. Drive #6 wood screws from below through box tabs into frame

## Project Structure

```
UP5PanelBox/
├── README.md              # This file
├── DESIGN.md              # Full technical specification
├── drawings/
│   └── UP5PanelBox_V4.svg # TechDraw 6-view drawing
├── freecad/               # FreeCAD source files
│   └── UP5PanelBox_V4.FCStd
├── images/                # ISO screenshots
│   └── up5panelbox_iso.png
├── printed_files/         # Production STL exports
│   ├── UP5_V4_Final-Bezel.stl
│   ├── UP5_V4_Final-Box.stl
│   └── UP5_V4_Final.3mf
└── scripts/               # Parametric build script
    └── generate_up5panelbox.py
```

## License

GNU General Public License v3.0 — see repository root.
