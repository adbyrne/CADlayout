#!/usr/bin/env python3
"""Generate SwitchToggle v7 parametric model in FreeCAD.

THREE 3D-printable parts:

  Shell      — 50x50x12mm hollow tray, open front face (electronics access)
  FrontPlate — 50x50x3mm plate + 8mm pivot posts (closes the shell)
  Lever      — Ø8mm pivot cylinder as fulcrum (X-axis), upper thumb arm + lower rod arm

Changes from v6:
  - Geometry/quality: fillets added to all three parts
      Shell:      R1.5mm on 4 vertical exterior corners
      FrontPlate: R1.5mm on 4 vertical corners + R1.0mm on all 4 front-face edges
                  + R0.5mm on post top edges
      Lever:      R1.5mm on all 4 Z-direction corners (top and bottom)
  - Alignment pegs shortened: PEG_H 1.5→1.0mm, PEG_HOLE_DEPTH 2.0→1.0mm
      (required to clear the R1.0mm fillet zone on FrontPlate front face edges)

Changes from v5:
  - LED holes moved from top/bottom walls to side walls (diagonal placement)
      Top LED:    left wall (X=0..2),  Y=38 (7mm clear of M3 at Y=45)
      Bottom LED: right wall (X=48..50), Y=12 (7mm clear of M3 at Y=5)

Changes from v4:
  - Lever: wider (20mm), taller (35mm total)
  - Lever pivot is now a Ø8mm cylinder running X-axis as the fulcrum
      upper arm (21mm) rises above cylinder for thumb grip
      lower arm (6mm) drops below cylinder for rod connection
      cylinder protrudes 1mm each side of arm — symmetric fulcrum feature
  - Rod connection: blind Z-direction hole + nut slot in lower arm bottom face
      nut hidden behind 2mm front wall; nut slots in from Y=0 bottom edge
  - Shell: two round rod holes replaced by single vertical slot (5x14mm, Y=8..22)
      gives installer ±4mm vertical positioning tolerance
  - FrontPlate: matching rod clearance slot added
  - Cable hole: 5mm dia (same as rod slot width) — wires + rod same hole size

Key geometry:
  - Pivot cylinder center at world Y=25, world Z=19 (mid-post)
  - Arm = 10mm (cylinder center to rod hole); 5mm travel → 30° swing
  - Rod hole at world Y=17.5 (lower arm center, within rod slot Y=8..22)
  - Cylinder Ø8mm centered in Y (equal 13.5mm arms each side), 2mm proud at front face

Assembly: Shell (Z=0..12) + FrontPlate (Z=12..15) + Posts (Z=15..23) + Lever arms (Z=15..21)

Requires: FreeCAD 1.0.x with Part and MeshPart modules
"""

import os


def _try_fillet(shape, radius, edges, label=""):
    """Apply makeFillet; return original shape with a warning on failure."""
    if not edges:
        print(f"  fillet({label}): no edges matched, skipping")
        return shape
    try:
        result = shape.makeFillet(radius, edges)
        print(f"  fillet({label}): R{radius}mm on {len(edges)} edges OK")
        return result
    except Exception as ex:
        print(f"  fillet({label}): FAILED ({ex}), skipping")
        return shape


# =============================================================================
# PARAMETERS
# =============================================================================

# --- Common base dimensions ---
BASE_W = 50.0   # X: width
BASE_H = 50.0   # Y: height

# --- Shell (Part A) ---
SHELL_DEPTH = 12.0   # Z: back face Z=0, open front face at Z=12
WALL_T      =  2.0   # wall thickness on all sides

# --- LED holes in shell side walls (v6: top-left, bottom-right diagonal) ---
LED_DIA   =  5.2
LED_Z     =  9.0   # Z depth in shell (3mm from front rim)
LED_TOP_Y = 38.0   # top LED: left wall (X=0..2); M3 at Y=45 clears by 7mm (min 6.3mm)
LED_BOT_Y = 12.0   # bottom LED: right wall (X=48..50); M3 at Y=5 clears by 7mm

# --- Shell back face features ---
# Rod slot (replaces two round holes from v4)
ROD_SLOT_W   =  5.0    # X: slot width
ROD_SLOT_H   = 14.0    # Y: slot height
ROD_SLOT_Y   =  8.0    # Y: slot bottom edge (top = 8+14 = 22)
ROD_SLOT_X   = (BASE_W - ROD_SLOT_W) / 2   # = 22.5, centered

# Cable hole (wires only — same 5mm as slot width)
CABLE_DIA =  5.0
CABLE_X   = 25.0
CABLE_Y   = 28.0    # moved up from center to clear rod slot (slot top = Y=22)

# Corner mount holes
M3_DIA = 3.4
MOUNT_CORNERS = [(5.0, 5.0), (5.0, 45.0), (45.0, 5.0), (45.0, 45.0)]

# --- Alignment pegs ---
PEG_DIA        = 2.0
PEG_H          = 1.0   # reduced from 1.5: hole top moves to Z=1.5, clears R=1.0 front-face fillet
PEG_HOLE_DIA   = 2.1
PEG_HOLE_DEPTH = 1.0   # reduced from 2.0: hole from Z=-0.5 to Z=1.5 (fillet zone Z=2..3 is clear)
PEG_POSITIONS  = [(5.0, 1.0), (45.0, 1.0), (5.0, 49.0), (45.0, 49.0)]

# --- FrontPlate (Part B) ---
PLATE_T       =  3.0
POST_W        =  4.0
POST_D        =  4.0
POST_H        =  8.0
POST_LEFT_X   = 10.0
POST_RIGHT_X  = 36.0
POST_Y_CENTER = 25.0
PIN_DIA       =  2.2

# --- Lever (Part C) ---
LEV_W = 20.0          # X: 1mm clearance each side in 22mm post gap
LEV_H = 35.0          # Y: total height
LEV_T =  6.0          # Z: arm thickness
LEV_PIVOT_Y   = LEV_H / 2   # = 17.5: cylinder centered in Y → equal arms above and below
LEV_PIVOT_DIA =  2.2  # pin hole through cylinder

# Pivot cylinder (the fulcrum — runs X-axis, visible feature)
CYL_PIVOT_DIA    =  8.0   # Ø8mm: 2mm proud at back (fascia side), flush at front operator face
CYL_PIVOT_Z_CTR  =  2.0   # local Z center: protrudes at Z=-2..0 (fascia), flush at Z=6 (operator)
# Cylinder occupies local Y = LEV_PIVOT_Y ± CYL_PIVOT_DIA/2 = 6..14
# Lower arm: Y=0..6  Upper arm: Y=14..35

# T-slot in lower arm for stud+nut connection (open at Y=0 bottom edge)
#   Narrow stud slot: 3mm wide, open at Z=0 back face → stud protrudes into shell
#   Wide nut pocket:  5.5mm wide at Z=1..4 → nut captured, can't pass back through stud slot
#   Front wall: Z=4..6 = 2mm solid
#   Assembly: slide pre-assembled stud+nut in from Y=0 edge; nut retains stud
NUT_POCKET_W   =  5.5   # X: nut corner-to-corner clearance
NUT_POCKET_Z   =  3.0   # Z: nut pocket depth (Z=1..4)
NUT_POCKET_Z0  =  1.0   # Z: nut pocket start (after narrow stud slot)
STUD_SLOT_W    =  3.0   # X: narrow stud clearance (open at Z=0 back face)
STUD_SLOT_Y    =  5.0   # Y: depth from bottom edge (same for both cuts)

# --- Assembly placements (visual only; STLs export at origin) ---
LEV_ASM_X = (BASE_W - LEV_W) / 2                                    # = 15.0
LEV_ASM_Y = BASE_H / 2 - LEV_PIVOT_Y                                # = 15.0
LEV_ASM_Z = SHELL_DEPTH + PLATE_T + POST_H/2 - CYL_PIVOT_Z_CTR     # = 17.0

# --- Export ---
EXPORT_DIR  = "printed_files"
FREECAD_DIR = "freecad"


# =============================================================================
# BUILD FUNCTIONS
# =============================================================================

def build_shell():
    """Part A: hollow tray, open front face. Single rod slot replaces two holes."""
    import FreeCAD, Part

    # Outer box
    result = Part.makeBox(BASE_W, BASE_H, SHELL_DEPTH)

    # Interior cavity (open at Z=SHELL_DEPTH)
    cav_w = BASE_W - 2 * WALL_T
    cav_h = BASE_H - 2 * WALL_T
    cav_d = SHELL_DEPTH - WALL_T
    cavity = Part.makeBox(cav_w, cav_h, cav_d,
                          FreeCAD.Vector(WALL_T, WALL_T, WALL_T))
    result = result.cut(cavity)

    # LED holes in side walls (X direction): top-left and bottom-right
    led_top = Part.makeCylinder(
        LED_DIA / 2, WALL_T + 2,
        FreeCAD.Vector(-0.5, LED_TOP_Y, LED_Z),
        FreeCAD.Vector(1, 0, 0)
    )
    led_bot = Part.makeCylinder(
        LED_DIA / 2, WALL_T + 2,
        FreeCAD.Vector(BASE_W - WALL_T - 0.5, LED_BOT_Y, LED_Z),
        FreeCAD.Vector(1, 0, 0)
    )
    result = result.cut(led_top)
    result = result.cut(led_bot)

    # Back face: rod slot (replaces two round holes)
    rod_slot = Part.makeBox(
        ROD_SLOT_W, ROD_SLOT_H, WALL_T + 2,
        FreeCAD.Vector(ROD_SLOT_X, ROD_SLOT_Y, -0.5)
    )
    result = result.cut(rod_slot)

    # Back face: cable hole (5mm, same size as slot width)
    cable_hole = Part.makeCylinder(
        CABLE_DIA / 2, WALL_T + 2,
        FreeCAD.Vector(CABLE_X, CABLE_Y, -0.5),
        FreeCAD.Vector(0, 0, 1)
    )
    result = result.cut(cable_hole)

    # Back face: M3 corner mount holes
    for cx, cy in MOUNT_CORNERS:
        hole = Part.makeCylinder(
            M3_DIA / 2, WALL_T + 2,
            FreeCAD.Vector(cx, cy, -0.5),
            FreeCAD.Vector(0, 0, 1)
        )
        result = result.cut(hole)

    # Alignment pegs on front rim
    for px, py in PEG_POSITIONS:
        peg = Part.makeCylinder(
            PEG_DIA / 2, PEG_H,
            FreeCAD.Vector(px, py, SHELL_DEPTH),
            FreeCAD.Vector(0, 0, 1)
        )
        result = result.fuse(peg)

    result = result.removeSplitter()

    # --- Fillets ---
    # 4 vertical exterior corner edges only — back face stays sharp (fascia mount)
    _vc = [e for e in result.Edges
           if hasattr(e.Curve, 'Direction')
           and abs(abs(e.Curve.Direction.z) - 1.0) < 0.05
           and any(abs(e.CenterOfMass.x - cx) < 0.5 and abs(e.CenterOfMass.y - cy) < 0.5
                   for cx, cy in [(0, 0), (BASE_W, 0), (0, BASE_H), (BASE_W, BASE_H)])]
    result = _try_fillet(result, 1.5, _vc, "shell vert corners")

    sc = len(result.Solids)
    if sc != 1:
        print(f"WARNING: Shell has {sc} solids (expected 1)")
    return result


def build_front_plate():
    """Part B: 3mm plate with pivot posts and rod clearance slot."""
    import FreeCAD, Part

    result = Part.makeBox(BASE_W, BASE_H, PLATE_T)

    # Pivot posts
    post_left = Part.makeBox(
        POST_W, POST_D, POST_H,
        FreeCAD.Vector(POST_LEFT_X,  POST_Y_CENTER - POST_D / 2, PLATE_T)
    )
    post_right = Part.makeBox(
        POST_W, POST_D, POST_H,
        FreeCAD.Vector(POST_RIGHT_X, POST_Y_CENTER - POST_D / 2, PLATE_T)
    )
    result = result.fuse(post_left)
    result = result.fuse(post_right)

    # Pin hole (X direction through both posts)
    pin_z = PLATE_T + POST_H / 2
    pin_hole = Part.makeCylinder(
        PIN_DIA / 2, BASE_W + 2,
        FreeCAD.Vector(-1, POST_Y_CENTER, pin_z),
        FreeCAD.Vector(1, 0, 0)
    )
    result = result.cut(pin_hole)

    # Rod clearance slot (matches shell slot position)
    rod_slot = Part.makeBox(
        ROD_SLOT_W, ROD_SLOT_H, PLATE_T + 2,
        FreeCAD.Vector(ROD_SLOT_X, ROD_SLOT_Y, -0.5)
    )
    result = result.cut(rod_slot)

    # Alignment peg holes
    for px, py in PEG_POSITIONS:
        hole = Part.makeCylinder(
            PEG_HOLE_DIA / 2, PEG_HOLE_DEPTH + 1,
            FreeCAD.Vector(px, py, -0.5),
            FreeCAD.Vector(0, 0, 1)
        )
        result = result.cut(hole)

    # M3 clearance holes at corners
    for cx, cy in MOUNT_CORNERS:
        hole = Part.makeCylinder(
            M3_DIA / 2, PLATE_T + 2,
            FreeCAD.Vector(cx, cy, -0.5),
            FreeCAD.Vector(0, 0, 1)
        )
        result = result.cut(hole)

    result = result.removeSplitter()

    # --- Fillets ---
    # Back face (Z=0) stays sharp — glued to shell rim.
    # All plate outer edges in one fillet call — FreeCAD resolves shared corner vertices.
    # Peg holes now stop at Z=1.5 (PEG_HOLE_DEPTH reduced), so fillet zone Z=2..3 is clear.
    # R=1.5mm corners to match shell; R=1.0mm front face edges (different call to avoid conflict).
    # Z-direction corner edges (full plate height Z=0..PLATE_T)
    _vc = [e for e in result.Edges
           if hasattr(e.Curve, 'Direction')
           and abs(abs(e.Curve.Direction.z) - 1.0) < 0.05
           and abs(e.CenterOfMass.z - PLATE_T / 2) < PLATE_T / 2 + 0.1
           and any(abs(e.CenterOfMass.x - cx) < 0.5 and abs(e.CenterOfMass.y - cy) < 0.5
                   for cx, cy in [(0, 0), (BASE_W, 0), (0, BASE_H), (BASE_W, BASE_H)])]
    result = _try_fillet(result, 1.5, _vc, "plate vert corners")
    # All 4 front face (Z=PLATE_T) perimeter edges — peg holes no longer reach this zone
    _pf = [e for e in result.Edges
           if hasattr(e.Curve, 'Direction')
           and abs(e.Curve.Direction.z) < 0.05
           and abs(e.CenterOfMass.z - PLATE_T) < 0.2
           and (abs(e.CenterOfMass.x) < 0.5 or abs(e.CenterOfMass.x - BASE_W) < 0.5
                or abs(e.CenterOfMass.y) < 0.5 or abs(e.CenterOfMass.y - BASE_H) < 0.5)]
    result = _try_fillet(result, 1.0, _pf, "plate front edges")

    # Post top face edges (Z = PLATE_T + POST_H)
    _pt = [e for e in result.Edges
           if hasattr(e.Curve, 'Direction')
           and abs(e.Curve.Direction.z) < 0.05
           and abs(e.CenterOfMass.z - (PLATE_T + POST_H)) < 0.2
           and abs(e.CenterOfMass.y - POST_Y_CENTER) < POST_D / 2 + 0.5]
    result = _try_fillet(result, 0.5, _pt, "post tops")

    sc = len(result.Solids)
    if sc != 1:
        print(f"WARNING: FrontPlate has {sc} solids (expected 1)")
    return result


def build_lever():
    """Part C: Ø8mm pivot cylinder as X-axis fulcrum, upper thumb arm, lower rod arm.

    Structure:
      Upper arm (Y=14..35, Z=0..6): thumb grip paddle
      Pivot cylinder (center Y=10, Z=4): Ø8mm × 20mm along X-axis
          flush at back face (Z=0), protrudes 2mm at front (Z=8) — visible fulcrum
      Lower arm (Y=0..6, Z=0..6): rod connection area
          rod hole: blind Z-direction from back face at Y=3
          nut slot: from bottom face (Y=0), hidden behind 2mm front wall
    """
    import FreeCAD, Part

    cyl_r   = CYL_PIVOT_DIA / 2   # = 4.0
    cyl_y   = LEV_PIVOT_Y          # = 10.0 (local Y center of cylinder)
    cyl_z   = CYL_PIVOT_Z_CTR      # = 4.0  (local Z center)

    # Full-height arm plate — single box spanning entire lever height
    # Cylinder is fused on top; clean single-solid result
    result = Part.makeBox(LEV_W, LEV_H, LEV_T)

    # Pivot cylinder — Ø8mm × 20mm, axis +X, centered at (Y=10, Z=4)
    # Extends Z=0..8: flush at back face, 2mm proud at front face
    pivot_cyl = Part.makeCylinder(
        cyl_r, LEV_W,
        FreeCAD.Vector(0, cyl_y, cyl_z),
        FreeCAD.Vector(1, 0, 0)
    )
    result = result.fuse(pivot_cyl)

    # Pin hole through cylinder center (X direction)
    pin_hole = Part.makeCylinder(
        LEV_PIVOT_DIA / 2, LEV_W + 2,
        FreeCAD.Vector(-1, cyl_y, cyl_z),
        FreeCAD.Vector(1, 0, 0)
    )
    result = result.cut(pin_hole)

    # T-slot: stud+nut slides in from Y=0 bottom edge
    # Narrow stud slot (3mm) — open at back face (Z=0), stud protrudes into shell
    stud_slot = Part.makeBox(
        STUD_SLOT_W, STUD_SLOT_Y, NUT_POCKET_Z0 + 0.5,
        FreeCAD.Vector(LEV_W / 2 - STUD_SLOT_W / 2, 0, -0.5)
    )
    result = result.cut(stud_slot)

    # Wide nut pocket (5.5mm) — starts at Z=NUT_POCKET_Z0, nut captured behind stud slot
    nut_pocket = Part.makeBox(
        NUT_POCKET_W, STUD_SLOT_Y, NUT_POCKET_Z,
        FreeCAD.Vector(LEV_W / 2 - NUT_POCKET_W / 2, 0, NUT_POCKET_Z0)
    )
    result = result.cut(nut_pocket)

    result = result.removeSplitter()

    # --- Fillets ---
    # All 4 Z-direction corner edges (top Y=LEV_H and bottom Y=0).
    # Top face / bottom face X-direction edges skipped — share vertices with cylinder junction.
    # T-slot is center-only; corners at X=0 and X=LEV_W are clear at both ends.
    _tc = [e for e in result.Edges
           if hasattr(e.Curve, 'Direction')
           and abs(abs(e.Curve.Direction.z) - 1.0) < 0.05
           and (abs(e.CenterOfMass.y - LEV_H) < 0.5 or abs(e.CenterOfMass.y) < 0.5)
           and (abs(e.CenterOfMass.x) < 0.5 or abs(e.CenterOfMass.x - LEV_W) < 0.5)]
    result = _try_fillet(result, 1.5, _tc, "lever corners")

    sc = len(result.Solids)
    if sc != 1:
        print(f"WARNING: Lever has {sc} solids (expected 1)")
    return result


# =============================================================================
# DOCUMENT + EXPORT
# =============================================================================

def create_document(doc_name="SwitchToggle"):
    import FreeCAD

    doc = FreeCAD.newDocument(doc_name)

    shell_shape = build_shell()
    shell_obj   = doc.addObject("Part::Feature", "Shell")
    shell_obj.Shape = shell_shape

    plate_shape = build_front_plate()
    plate_obj   = doc.addObject("Part::Feature", "FrontPlate")
    plate_obj.Shape = plate_shape
    plate_obj.Placement = FreeCAD.Placement(
        FreeCAD.Vector(0, 0, SHELL_DEPTH),
        FreeCAD.Rotation()
    )

    lever_shape = build_lever()
    lever_obj   = doc.addObject("Part::Feature", "Lever")
    lever_obj.Shape = lever_shape
    lever_obj.Placement = FreeCAD.Placement(
        FreeCAD.Vector(LEV_ASM_X, LEV_ASM_Y, LEV_ASM_Z),
        FreeCAD.Rotation()
    )

    doc.recompute()

    if FreeCAD.GuiUp:
        import FreeCADGui
        shell_obj.ViewObject.ShapeColor  = (0.4,  0.6,  1.0,  0.0)
        plate_obj.ViewObject.ShapeColor  = (0.25, 0.45, 0.85, 0.0)
        lever_obj.ViewObject.ShapeColor  = (1.0,  0.65, 0.2,  0.0)
        FreeCADGui.ActiveDocument.ActiveView.fitAll()
        FreeCADGui.ActiveDocument.ActiveView.viewIsometric()

    print(f"Created {doc_name}: "
          f"Shell {shell_shape.Volume:.1f} mm³  "
          f"FrontPlate {plate_shape.Volume:.1f} mm³  "
          f"Lever {lever_shape.Volume:.1f} mm³")
    return doc


def export_meshed_stl(shape, path, linear_deflection=0.05, angular_deflection=0.3):
    import MeshPart
    mesh = MeshPart.meshFromShape(
        Shape=shape,
        LinearDeflection=linear_deflection,
        AngularDeflection=angular_deflection
    )
    mesh.write(path)
    print(f"  {mesh.CountFacets:4d} triangles → {path}")


def run(base_dir):
    import FreeCAD

    freecad_dir = os.path.join(base_dir, FREECAD_DIR)
    printed_dir = os.path.join(base_dir, EXPORT_DIR)
    os.makedirs(freecad_dir, exist_ok=True)
    os.makedirs(printed_dir, exist_ok=True)

    doc = create_document()
    fcstd_path = os.path.join(freecad_dir, "SwitchToggle.FCStd")
    doc.saveAs(fcstd_path)
    print(f"Saved: {fcstd_path}")

    print("Exporting STLs:")
    export_meshed_stl(doc.getObject("Shell").Shape,
                      os.path.join(printed_dir, "SwitchToggle_Shell (Meshed).stl"))
    export_meshed_stl(doc.getObject("FrontPlate").Shape,
                      os.path.join(printed_dir, "SwitchToggle_FrontPlate (Meshed).stl"))
    export_meshed_stl(doc.getObject("Lever").Shape,
                      os.path.join(printed_dir, "SwitchToggle_Lever (Meshed).stl"))
    print("Done!")


if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    run(os.path.dirname(script_dir))
