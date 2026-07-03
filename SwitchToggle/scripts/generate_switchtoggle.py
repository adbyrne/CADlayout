#!/usr/bin/env python3
"""Generate SwitchToggle v9 parametric model in FreeCAD.

FOUR 3D-printable parts:

  Shell      — 50x50x12mm hollow tray, open front face (electronics access)
  FrontPlate — 50x50x3mm plate + two 4x4mm mortise pockets (no integral posts)
  Lever      — Ø8mm pivot cylinder with Ø4mm stub axles at each end (no pin hole)
  PivotClip  — press-fit into FrontPlate mortise; snap-captures lever stub (print x2)

Changes from v8:
  - Toggle swing clearance: PivotClip body height (POST_H) 8mm → 10mm, moving the
    pivot bore centre 1mm further from the FrontPlate face (world Z 19 → 20).
    Lever placement (LEV_ASM_Z) shifts to match automatically. Addresses the lever
    rubbing against the FrontPlate/clip base through its ~20° swing.
  - PivotClip tang/wall connection: the material bridging the tang to the snap-wall
    pillars, at the Z=0 body/tang transition, was only 0.2mm thick (CLIP_TANG_W
    3.9mm vs CLIP_SNAP_W 3.5mm) — thinner than one nozzle line, a likely print/
    breakage point. CLIP_SNAP_W 3.5→3.0mm and CLIP_TANG_W 3.9→3.95mm widen that
    overlap to ~0.475mm each side (snap now needs ~0.5mm wall flex per side,
    up from 0.25mm).
  - PivotClip fillets/chamfers: previously had none, unlike the other three parts.
    Added cosmetic R0.5mm fillet on outer corners/top cap, functional chamfers at
    the bore mouths (0.3mm) and tang lead-in (0.4mm), and an R0.2mm fillet at the
    snap wall's Z=0 root (its inner, slot-facing surface — the face actually
    pushed by the stub during snap-through, fixed at its base) to relieve the
    real bending stress-concentration point, distinct from the tang/wall overlap
    reinforced above.

Changes from v7:
  - Fulcrum redesign: M2 pivot pin eliminated; no external hardware required
      Lever:       pin hole removed; Ø4mm×5mm stub axles added at each cylinder end
      FrontPlate:  integral 4×4×8mm posts removed; 4×4mm through-mortise pockets added
      PivotClip:   new 4th printed part (print x2):
                     body 4×6×10mm sits proud of plate (6mm Y for snap wall material)
                     tang 3.95×3.95×3mm press-fits into FrontPlate mortise
                     Ø4.2mm bore through X at body centre captures lever stub
                     3.0mm entry slot (< Ø4mm stub → snap feel) at body base

Assembly (v8):
  1. Position lever with stubs pointing left and right
  2. Press each PivotClip straight down over its stub — stub snaps through entry
     slot into bore; tang seats into FrontPlate mortise (press-fit)
  3. Proceed with normal LED install and Shell glue-up

Replacement: press new clip down over stub; no shell disassembly required.

Key geometry:
  - Pivot bore centre at world Y=25, world Z=20 (v9: was Z=19; +1mm plate clearance)
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


def _edge_curve(e):
    """Return e.Curve, or None if FreeCAD can't resolve the curve type
    (some fillet/chamfer blend edges raise TypeError on access)."""
    try:
        return e.Curve
    except Exception:
        return None


def _try_chamfer(shape, size, edges, label=""):
    """Apply makeChamfer; return original shape with a warning on failure."""
    if not edges:
        print(f"  chamfer({label}): no edges matched, skipping")
        return shape
    try:
        result = shape.makeChamfer(size, edges)
        print(f"  chamfer({label}): {size}mm on {len(edges)} edges OK")
        return result
    except Exception as ex:
        print(f"  chamfer({label}): FAILED ({ex}), skipping")
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
POST_H        = 10.0   # clip body height above plate (v9: +2mm → toggle pivot centre sits 1mm further from plate face for swing clearance)
POST_LEFT_X   = 10.0   # left post/clip/mortise left edge
POST_RIGHT_X  = 36.0   # right post/clip/mortise left edge
POST_Y_CENTER = 25.0

# --- PivotClip (Part D, print x2) ---
STUB_DIA      =  4.0   # lever stub diameter
STUB_LEN      =  5.0   # stub length from lever face (1mm gap + 4mm into bore)
CLIP_BORE_DIA =  4.2   # bore through clip body (running fit on stub)
CLIP_BODY_Y   =  6.0   # clip body Y width (wider than mortise for snap walls)
CLIP_SNAP_W   =  3.0   # entry slot width in Y (< STUB_DIA → snap feel on install)
                        # (v9: 3.5→3.0mm — widens tang/wall overlap at Z=0, see CLIP_TANG_W)
CLIP_TANG_W   =  3.95  # tang X/Y (press-fits into MORTISE_W pocket; tune ±0.1mm)
                        # (v9: 3.9→3.95mm — with narrower CLIP_SNAP_W, tang/wall overlap
                        #  at the Z=0 transition grows from 0.2mm to ~0.475mm each side —
                        #  the prior 0.2mm sliver was thinner than one nozzle line width)
MORTISE_W     =  4.0   # through-pocket in FrontPlate

# --- PivotClip fillets/chamfers (v9 — clip previously had none) ---
CLIP_CORNER_FILLET  = 0.5   # cosmetic outer corners + top cap (scaled down from the
                             # 1.5mm used on Shell/FrontPlate/Lever — clip cross-section
                             # is only 4x6mm)
CLIP_BORE_CHAMFER   = 0.3   # bore mouths (both ends) — eases stub engagement, reduces
                             # edge scrape against the stub during lever rotation
CLIP_TANG_CHAMFER   = 0.4   # tang leading edge — lead-in for FrontPlate mortise press-fit
CLIP_SLOT_ROOT_FILLET = 0.2 # root of the snap wall's inner (slot-facing) face at Z=0,
                             # where the entry slot meets the tang plane — the surface
                             # actually pushed by the stub during snap-through, fixed at
                             # its base; the real bending stress-concentration point
                             # (kept small so it doesn't widen the slot)

# --- Lever (Part C) ---
LEV_W = 20.0
LEV_H = 35.0
LEV_T =  6.0
LEV_PIVOT_Y   = LEV_H / 2   # = 17.5: equal arms above and below

CYL_PIVOT_DIA   =  8.0
CYL_PIVOT_Z_CTR =  2.0   # local Z centre: flush at back face, 2mm proud at front

# T-slot in lower arm for stud+nut connection
NUT_POCKET_W   =  5.5
NUT_POCKET_Z   =  2.0
NUT_POCKET_Z0  =  1.0
STUD_SLOT_W    =  3.0
STUD_SLOT_Y    =  5.0

# --- Assembly placements (visual only; STLs export at part origin) ---
LEV_ASM_X = (BASE_W - LEV_W) / 2                                # = 15.0
LEV_ASM_Y = BASE_H / 2 - LEV_PIVOT_Y                            # =  7.5
LEV_ASM_Z = SHELL_DEPTH + PLATE_T + POST_H / 2 - CYL_PIVOT_Z_CTR  # = 18.0

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
      Body:      POST_W × CLIP_BODY_Y × POST_H  (4×6×10mm, above plate)
      Tang:      CLIP_TANG_W × CLIP_TANG_W × PLATE_T  (3.95×3.95×3mm, below Z=0)
      Bore:      Ø4.2mm through X at Y=CLIP_BODY_Y/2, Z=POST_H/2
      Entry slot: CLIP_SNAP_W wide in Y, from Z=0 to bore centre (Z=POST_H/2)
                  Full X width; 1.5mm snap walls on each Y side (v9: was 1.25mm),
                  giving ~0.475mm tang/wall overlap at Z=0 (v9: was 0.2mm).

    Assembly: press clip straight down; stub squeezes through 3.0mm slot and
    snaps into the 4.2mm bore. Tang seats in FrontPlate mortise (press-fit).
    """
    import FreeCAD, Part

    bore_y = CLIP_BODY_Y / 2   # = 3.0 — bore Y centre in clip local
    bore_z = POST_H / 2        # = 5.0 — bore Z centre in clip local (v9: +1mm from plate face)

    # Body
    result = Part.makeBox(POST_W, CLIP_BODY_Y, POST_H)

    # Tang: centred in body XY, extends below Z=0 into FrontPlate mortise
    tang_x0 = (POST_W    - CLIP_TANG_W) / 2   # = 0.025
    tang_y0 = (CLIP_BODY_Y - CLIP_TANG_W) / 2  # = 1.025
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
    # CLIP_SNAP_W in Y → 1.5mm snap walls each side → snap feel on install.
    slot = Part.makeBox(
        POST_W + 2, CLIP_SNAP_W, bore_z,
        FreeCAD.Vector(-1, bore_y - CLIP_SNAP_W / 2, 0)
    )
    result = result.cut(slot)

    result = result.removeSplitter()

    # Cosmetic: soften outer corners and top cap edges (small radius — this
    # part's cross-section is only 4x6mm, unlike the 1.5mm used elsewhere)
    _vc = [e for e in result.Edges
           if hasattr(_edge_curve(e), 'Direction')
           and abs(abs(e.Curve.Direction.z) - 1.0) < 0.05
           and any(abs(e.CenterOfMass.x - cx) < 0.3 and abs(e.CenterOfMass.y - cy) < 0.3
                   for cx, cy in [(0, 0), (POST_W, 0), (0, CLIP_BODY_Y), (POST_W, CLIP_BODY_Y)])]
    result = _try_fillet(result, CLIP_CORNER_FILLET, _vc, "clip outer corners")

    _tc = [e for e in result.Edges
           if hasattr(_edge_curve(e), 'Direction')
           and abs(e.Curve.Direction.z) < 0.05
           and abs(e.CenterOfMass.z - POST_H) < 0.2]
    result = _try_fillet(result, CLIP_CORNER_FILLET, _tc, "clip top cap edges")

    # Functional: chamfer bore mouths (both ends) — eases stub engagement and
    # reduces edge scrape against the stub during lever rotation
    _bm = [e for e in result.Edges
           if hasattr(_edge_curve(e), 'Radius')
           and abs(e.Curve.Radius - CLIP_BORE_DIA / 2) < 0.05
           and (abs(e.CenterOfMass.x) < 0.3 or abs(e.CenterOfMass.x - POST_W) < 0.3)]
    result = _try_chamfer(result, CLIP_BORE_CHAMFER, _bm, "clip bore mouths")

    # Functional: chamfer tang's leading (bottom) edge — lead-in for the
    # FrontPlate mortise press-fit
    _tg = [e for e in result.Edges
           if hasattr(_edge_curve(e), 'Direction')
           and abs(e.Curve.Direction.z) < 0.05
           and abs(e.CenterOfMass.z - (-PLATE_T)) < 0.2]
    result = _try_chamfer(result, CLIP_TANG_CHAMFER, _tg, "clip tang lead-in")

    # Functional: fillet the root of the snap wall's inner (slot-facing) face,
    # at Z=0 where the entry slot meets the tang plane. This is the surface
    # that's actually pushed by the stub during snap-through, fixed at its
    # base (Z=0) — the real bending stress-concentration point, distinct from
    # the tang's own (outer) edge at Y=tang_y0 handled by decision #16.
    # (excludes sub-1mm fragments at the X ends, where the slot cut meets the
    # tang's corner — filleting those tiny slivers fails: BRep_API not-done)
    _sb = [e for e in result.Edges
           if hasattr(_edge_curve(e), 'Direction')
           and abs(abs(e.Curve.Direction.x) - 1.0) < 0.05
           and abs(e.CenterOfMass.z) < 0.2
           and e.Length > 1.0
           and (abs(e.CenterOfMass.y - (bore_y - CLIP_SNAP_W / 2)) < 0.2
                or abs(e.CenterOfMass.y - (bore_y + CLIP_SNAP_W / 2)) < 0.2)]
    result = _try_fillet(result, CLIP_SLOT_ROOT_FILLET, _sb, "clip slot wall root")

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
