#!/usr/bin/env python3
"""Generate SwitchToggle v8 parametric model in FreeCAD.

FOUR 3D-printable parts:

  Shell      — 50x50x12mm hollow tray, open front face (electronics access)
  FrontPlate — 50x50x3mm plate + two 4x4mm mortise pockets (no integral posts)
  Lever      — Ø8mm pivot cylinder with Ø4mm stub axles at each end (no pin hole)
  PivotClip  — press-fit into FrontPlate mortise; snap-captures lever stub (print x2)

Changes from v7:
  - Fulcrum redesign: M2 pivot pin eliminated; no external hardware required
      Lever:       pin hole removed; Ø4mm×5mm stub axles added at each cylinder end
      FrontPlate:  integral 4×4×8mm posts removed; 4×4mm through-mortise pockets added
      PivotClip:   new 4th printed part (print x2):
                     body 4×6×8mm sits proud of plate (6mm Y for snap wall material)
                     tang 3.9×3.9×3mm press-fits into FrontPlate mortise
                     Ø4.2mm bore through X at body centre captures lever stub
                     3.5mm entry slot (< Ø4mm stub → snap feel) at body base

Assembly (v8):
  1. Position lever with stubs pointing left and right
  2. Press each PivotClip straight down over its stub — stub snaps through entry
     slot into bore; tang seats into FrontPlate mortise (press-fit)
  3. Proceed with normal LED install and Shell glue-up

Replacement: press new clip down over stub; no shell disassembly required.

Key geometry (unchanged from v7):
  - Pivot bore centre at world Y=25, world Z=19
  - Clip bores: world X=10..14 (left) and X=36..40 (right)
  - Lever stubs: world X=10..15 (left) and X=35..40 (right)

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

# --- LED holes in shell side walls (top-left, bottom-right diagonal) ---
LED_DIA   =  5.2
LED_Z     =  9.0
LED_TOP_Y = 38.0   # top LED: left wall (X=0..2); 7mm clear of M3 at Y=45
LED_BOT_Y = 12.0   # bottom LED: right wall (X=48..50); 7mm clear of M3 at Y=5

# --- Shell back face features ---
ROD_SLOT_W   =  5.0
ROD_SLOT_H   = 14.0
ROD_SLOT_Y   =  8.0
ROD_SLOT_X   = (BASE_W - ROD_SLOT_W) / 2   # = 22.5, centred

CABLE_DIA =  5.0
CABLE_X   = 25.0
CABLE_Y   = 28.0

M3_DIA = 3.4
MOUNT_CORNERS = [(5.0, 5.0), (5.0, 45.0), (45.0, 5.0), (45.0, 45.0)]

# --- Alignment pegs ---
PEG_DIA        = 2.0
PEG_H          = 1.0
PEG_HOLE_DIA   = 2.1
PEG_HOLE_DEPTH = 1.0
PEG_POSITIONS  = [(5.0, 1.0), (45.0, 1.0), (5.0, 49.0), (45.0, 49.0)]

# --- FrontPlate (Part B) ---
PLATE_T       =  3.0
POST_W        =  4.0   # mortise X width (= old post width)
POST_D        =  4.0   # mortise Y depth (= old post depth)
POST_H        =  8.0   # clip body height above plate
POST_LEFT_X   = 10.0   # left post/clip/mortise left edge
POST_RIGHT_X  = 36.0   # right post/clip/mortise left edge
POST_Y_CENTER = 25.0

# --- PivotClip (Part D, print x2) ---
STUB_DIA      =  4.0   # lever stub diameter
STUB_LEN      =  5.0   # stub length from lever face (1mm gap + 4mm into bore)
CLIP_BORE_DIA =  4.2   # bore through clip body (running fit on stub)
CLIP_BODY_Y   =  6.0   # clip body Y width (wider than mortise for snap walls)
CLIP_SNAP_W   =  3.5   # entry slot width in Y (< STUB_DIA → snap feel on install)
CLIP_TANG_W   =  3.9   # tang X/Y (press-fits into MORTISE_W pocket; tune ±0.1mm)
MORTISE_W     =  4.0   # through-pocket in FrontPlate

# --- Lever (Part C) ---
LEV_W = 20.0
LEV_H = 35.0
LEV_T =  6.0
LEV_PIVOT_Y   = LEV_H / 2   # = 17.5: equal arms above and below

CYL_PIVOT_DIA   =  8.0
CYL_PIVOT_Z_CTR =  2.0   # local Z centre: flush at back face, 2mm proud at front

# T-slot in lower arm for stud+nut connection
NUT_POCKET_W   =  5.5
NUT_POCKET_Z   =  3.0
NUT_POCKET_Z0  =  1.0
STUD_SLOT_W    =  3.0
STUD_SLOT_Y    =  5.0

# --- Assembly placements (visual only; STLs export at part origin) ---
LEV_ASM_X = (BASE_W - LEV_W) / 2                                # = 15.0
LEV_ASM_Y = BASE_H / 2 - LEV_PIVOT_Y                            # =  7.5
LEV_ASM_Z = SHELL_DEPTH + PLATE_T + POST_H / 2 - CYL_PIVOT_Z_CTR  # = 17.0

# --- Export ---
EXPORT_DIR  = "printed_files"
FREECAD_DIR = "freecad"


# =============================================================================
# BUILD FUNCTIONS
# =============================================================================

def build_shell():
    """Part A: hollow tray, open front face. Unchanged from v7."""
    import FreeCAD, Part

    result = Part.makeBox(BASE_W, BASE_H, SHELL_DEPTH)

    cav_w = BASE_W - 2 * WALL_T
    cav_h = BASE_H - 2 * WALL_T
    cav_d = SHELL_DEPTH - WALL_T
    cavity = Part.makeBox(cav_w, cav_h, cav_d,
                          FreeCAD.Vector(WALL_T, WALL_T, WALL_T))
    result = result.cut(cavity)

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

    rod_slot = Part.makeBox(
        ROD_SLOT_W, ROD_SLOT_H, WALL_T + 2,
        FreeCAD.Vector(ROD_SLOT_X, ROD_SLOT_Y, -0.5)
    )
    result = result.cut(rod_slot)

    cable_hole = Part.makeCylinder(
        CABLE_DIA / 2, WALL_T + 2,
        FreeCAD.Vector(CABLE_X, CABLE_Y, -0.5),
        FreeCAD.Vector(0, 0, 1)
    )
    result = result.cut(cable_hole)

    for cx, cy in MOUNT_CORNERS:
        hole = Part.makeCylinder(
            M3_DIA / 2, WALL_T + 2,
            FreeCAD.Vector(cx, cy, -0.5),
            FreeCAD.Vector(0, 0, 1)
        )
        result = result.cut(hole)

    for px, py in PEG_POSITIONS:
        peg = Part.makeCylinder(
            PEG_DIA / 2, PEG_H,
            FreeCAD.Vector(px, py, SHELL_DEPTH),
            FreeCAD.Vector(0, 0, 1)
        )
        result = result.fuse(peg)

    result = result.removeSplitter()

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
    """Part B: 3mm plate with mortise pockets for PivotClips (no integral posts)."""
    import FreeCAD, Part

    result = Part.makeBox(BASE_W, BASE_H, PLATE_T)

    # Through-mortise pockets for clip tangs (centred on old post footprints)
    for post_cx in [POST_LEFT_X + POST_W / 2, POST_RIGHT_X + POST_W / 2]:
        mortise = Part.makeBox(
            MORTISE_W, MORTISE_W, PLATE_T + 2,
            FreeCAD.Vector(post_cx - MORTISE_W / 2, POST_Y_CENTER - MORTISE_W / 2, -0.5)
        )
        result = result.cut(mortise)

    # Rod clearance slot (matches shell slot)
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

    # M3 corner clearance holes
    for cx, cy in MOUNT_CORNERS:
        hole = Part.makeCylinder(
            M3_DIA / 2, PLATE_T + 2,
            FreeCAD.Vector(cx, cy, -0.5),
            FreeCAD.Vector(0, 0, 1)
        )
        result = result.cut(hole)

    result = result.removeSplitter()

    # Fillets — corners and front face edges (no post-top fillet in v8)
    _vc = [e for e in result.Edges
           if hasattr(e.Curve, 'Direction')
           and abs(abs(e.Curve.Direction.z) - 1.0) < 0.05
           and abs(e.CenterOfMass.z - PLATE_T / 2) < PLATE_T / 2 + 0.1
           and any(abs(e.CenterOfMass.x - cx) < 0.5 and abs(e.CenterOfMass.y - cy) < 0.5
                   for cx, cy in [(0, 0), (BASE_W, 0), (0, BASE_H), (BASE_W, BASE_H)])]
    result = _try_fillet(result, 1.5, _vc, "plate vert corners")

    _pf = [e for e in result.Edges
           if hasattr(e.Curve, 'Direction')
           and abs(e.Curve.Direction.z) < 0.05
           and abs(e.CenterOfMass.z - PLATE_T) < 0.2
           and (abs(e.CenterOfMass.x) < 0.5 or abs(e.CenterOfMass.x - BASE_W) < 0.5
                or abs(e.CenterOfMass.y) < 0.5 or abs(e.CenterOfMass.y - BASE_H) < 0.5)]
    result = _try_fillet(result, 1.0, _pf, "plate front edges")

    sc = len(result.Solids)
    if sc != 1:
        print(f"WARNING: FrontPlate has {sc} solids (expected 1)")
    return result


def build_lever():
    """Part C: Ø8mm pivot cylinder with Ø4mm stub axles; upper thumb arm, lower rod arm.

    v8: pin hole removed; Ø4mm×5mm stubs at each cylinder end captured by PivotClips.
    Stubs protrude outward in X (left stub X=-5..0, right stub X=20..25 in local coords).
    """
    import FreeCAD, Part

    cyl_r = CYL_PIVOT_DIA / 2   # = 4.0
    cyl_y = LEV_PIVOT_Y          # = 17.5
    cyl_z = CYL_PIVOT_Z_CTR      # = 2.0

    # Full-height arm plate
    result = Part.makeBox(LEV_W, LEV_H, LEV_T)

    # Pivot cylinder — Ø8mm × 20mm, axis +X
    pivot_cyl = Part.makeCylinder(
        cyl_r, LEV_W,
        FreeCAD.Vector(0, cyl_y, cyl_z),
        FreeCAD.Vector(1, 0, 0)
    )
    result = result.fuse(pivot_cyl)

    # Stub axles (v8): Ø4mm × 5mm protruding outward from each cylinder end
    left_stub = Part.makeCylinder(
        STUB_DIA / 2, STUB_LEN,
        FreeCAD.Vector(-STUB_LEN, cyl_y, cyl_z),
        FreeCAD.Vector(1, 0, 0)
    )
    right_stub = Part.makeCylinder(
        STUB_DIA / 2, STUB_LEN,
        FreeCAD.Vector(LEV_W, cyl_y, cyl_z),
        FreeCAD.Vector(1, 0, 0)
    )
    result = result.fuse(left_stub)
    result = result.fuse(right_stub)

    # T-slot: stud+nut slides in from Y=0 bottom edge
    stud_slot = Part.makeBox(
        STUD_SLOT_W, STUD_SLOT_Y, NUT_POCKET_Z0 + 0.5,
        FreeCAD.Vector(LEV_W / 2 - STUD_SLOT_W / 2, 0, -0.5)
    )
    result = result.cut(stud_slot)

    nut_pocket = Part.makeBox(
        NUT_POCKET_W, STUD_SLOT_Y, NUT_POCKET_Z,
        FreeCAD.Vector(LEV_W / 2 - NUT_POCKET_W / 2, 0, NUT_POCKET_Z0)
    )
    result = result.cut(nut_pocket)

    result = result.removeSplitter()

    # Fillets on arm corners (_try_fillet skips gracefully if stub topology interferes)
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


def build_pivot_clip():
    """Part D (print x2): press-fit into FrontPlate mortise; snap-captures lever stub.

    Local coords: Z=0 at body base (rests on FrontPlate front face).
      Body:      POST_W × CLIP_BODY_Y × POST_H  (4×6×8mm, above plate)
      Tang:      CLIP_TANG_W × CLIP_TANG_W × PLATE_T  (3.9×3.9×3mm, below Z=0)
      Bore:      Ø4.2mm through X at Y=CLIP_BODY_Y/2, Z=POST_H/2
      Entry slot: CLIP_SNAP_W wide in Y, from Z=0 to bore centre (Z=POST_H/2)
                  Full X width; 1.25mm snap walls on each Y side.

    Assembly: press clip straight down; stub squeezes through 3.5mm slot and
    snaps into the 4.2mm bore. Tang seats in FrontPlate mortise (press-fit).
    """
    import FreeCAD, Part

    bore_y = CLIP_BODY_Y / 2   # = 3.0 — bore Y centre in clip local
    bore_z = POST_H / 2        # = 4.0 — bore Z centre in clip local

    # Body
    result = Part.makeBox(POST_W, CLIP_BODY_Y, POST_H)

    # Tang: centred in body XY, extends below Z=0 into FrontPlate mortise
    tang_x0 = (POST_W    - CLIP_TANG_W) / 2   # = 0.05
    tang_y0 = (CLIP_BODY_Y - CLIP_TANG_W) / 2  # = 1.05
    tang = Part.makeBox(
        CLIP_TANG_W, CLIP_TANG_W, PLATE_T,
        FreeCAD.Vector(tang_x0, tang_y0, -PLATE_T)
    )
    result = result.fuse(tang)

    # Bore through X direction at body centre
    bore = Part.makeCylinder(
        CLIP_BORE_DIA / 2, POST_W + 2,
        FreeCAD.Vector(-1, bore_y, bore_z),
        FreeCAD.Vector(1, 0, 0)
    )
    result = result.cut(bore)

    # Entry slot: open at body base (Z=0), runs to bore centre (Z=bore_z)
    # Full X width so X-axis stub enters freely as clip descends.
    # CLIP_SNAP_W in Y → 1.25mm snap walls each side → snap feel on install.
    slot = Part.makeBox(
        POST_W + 2, CLIP_SNAP_W, bore_z,
        FreeCAD.Vector(-1, bore_y - CLIP_SNAP_W / 2, 0)
    )
    result = result.cut(slot)

    result = result.removeSplitter()

    sc = len(result.Solids)
    if sc != 1:
        print(f"WARNING: PivotClip has {sc} solids (expected 1)")
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

    # PivotClips: same shape, mirrored X placement
    clip_shape = build_pivot_clip()
    clip_asm_y = POST_Y_CENTER - CLIP_BODY_Y / 2   # = 22.0
    clip_asm_z = SHELL_DEPTH + PLATE_T              # = 15.0

    left_clip  = doc.addObject("Part::Feature", "LeftPivotClip")
    right_clip = doc.addObject("Part::Feature", "RightPivotClip")
    left_clip.Shape  = clip_shape
    right_clip.Shape = clip_shape
    left_clip.Placement = FreeCAD.Placement(
        FreeCAD.Vector(POST_LEFT_X, clip_asm_y, clip_asm_z),
        FreeCAD.Rotation()
    )
    right_clip.Placement = FreeCAD.Placement(
        FreeCAD.Vector(POST_RIGHT_X, clip_asm_y, clip_asm_z),
        FreeCAD.Rotation()
    )

    doc.recompute()

    if FreeCAD.GuiUp:
        import FreeCADGui
        shell_obj.ViewObject.ShapeColor  = (0.4,  0.6,  1.0,  0.0)
        plate_obj.ViewObject.ShapeColor  = (0.25, 0.45, 0.85, 0.0)
        lever_obj.ViewObject.ShapeColor  = (1.0,  0.65, 0.2,  0.0)
        left_clip.ViewObject.ShapeColor  = (0.2,  0.75, 0.35, 0.0)
        right_clip.ViewObject.ShapeColor = (0.2,  0.75, 0.35, 0.0)
        FreeCADGui.ActiveDocument.ActiveView.fitAll()
        FreeCADGui.ActiveDocument.ActiveView.viewIsometric()

    print(f"Created {doc_name}: "
          f"Shell {shell_shape.Volume:.1f} mm³  "
          f"FrontPlate {plate_shape.Volume:.1f} mm³  "
          f"Lever {lever_shape.Volume:.1f} mm³  "
          f"PivotClip {clip_shape.Volume:.1f} mm³ (×2)")
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
    # PivotClip: export once (print x2)
    export_meshed_stl(doc.getObject("LeftPivotClip").Shape,
                      os.path.join(printed_dir, "SwitchToggle_PivotClip (Meshed).stl"))
    print("Done!")


if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    run(os.path.dirname(script_dir))
