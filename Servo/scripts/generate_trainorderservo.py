#!/usr/bin/env python3
"""Generate TrainOrderServo v2 parametric models.

Geometry reverse-engineered from TrainOrderServoInLine.FCStd (v1 manual PartDesign).

Key fix from v1: 4 mm +Y offset on bracket 2 eliminates servo arm interference.
Each servo arm (1.5 mm depth) now sweeps in a separate Y plane with 2.5 mm clearance.

Produces three output FCStd files:

  TrainOrderServoInLine_v2.FCStd
    Body            — B1 (left) + B2 (right, +4 mm Y) + PCA9685 board to +X
    Body_Flipped    — mirror of Body across YZ plane (board to -X)
    BodyBoardBehind — B1 + B2 + board in -Y direction (compact footprint)

  TrainOrderServoBracketsOnly_v1.FCStd
    Body            — B1 + B2 only, mast hole, minimized base plate

  TrainOrderServoSingleBracket_v1.FCStd
    Body            — B1 only, mast hole, minimal base plate

Coordinate system: X = right, Y = back (+) / front (-), Z = up.
Mast hole centre is at global origin (0, 0, 0).
All dimensions in mm.

Requires FreeCAD 1.0.x with Part and MeshPart modules.
"""

import os


# =============================================================================
# FILLET HELPER
# =============================================================================

def _try_fillet(shape, radius, edges, label=""):
    """Apply makeFillet; return original shape with a warning on failure."""
    if not edges:
        print(f"  fillet({label}): no edges matched, skipping")
        return shape
    try:
        result = shape.makeFillet(radius, edges)
        print(f"  fillet({label}): R{radius} mm on {len(edges)} edges OK")
        return result
    except Exception as ex:
        print(f"  fillet({label}): FAILED ({ex}), skipping")
        return shape


# =============================================================================
# PARAMETERS  (all mm)
# =============================================================================

# --- Base plate ---
BASE_T          =  5.0   # thickness (Z)
MAST_R          =  3.0   # mast hole radius (Ø6 mm)

# --- Bracket geometry ---
BRACKET_W       = 32.0   # X width of each bracket
BRACKET_H       = 25.0   # height above base plate (Z = BASE_T to BASE_T+BRACKET_H)
SHELF_D         =  4.0   # main shelf depth (Y), from y_back inward toward -Y
LEG_D           =  4.4   # leg extension past the shelf toward -Y
LEG_W           =  4.5   # X width of each leg

# Gap from mast centre to each bracket's inner edge (B1 ends at X=-MAST_GAP, B2 starts at +MAST_GAP)
MAST_GAP        =  5.0

# B1 (left bracket) back-face Y; B2 is shifted +BRACKET_Y_OFFSET
B1_Y_BACK       = -5.0
BRACKET_Y_OFFSET =  4.0   # +Y shift on B2 for arm clearance
B2_Y_BACK       = B1_Y_BACK + BRACKET_Y_OFFSET   # = -1.0

# --- Servo pocket (Y-axis cylinder, through the 4 mm shelf) ---
SERVO_R         =  5.95  # servo body radius → Ø11.9 mm
SERVO_CZ        = 13.0   # hole centre height above base bottom (Z = BASE_T + 8.0)
# Servo tangent to inner leg wall:
#   B1: inner right leg at X = -MAST_GAP - LEG_W = -9.5  → servo_cx = -9.5 - SERVO_R = -15.45
#   B2: inner left  leg at X = +MAST_GAP + LEG_W = +9.5  → servo_cx = +9.5 + SERVO_R = +15.45

# --- Wire / arm slot (Y-axis cylinder, same depth as servo pocket) ---
WIRE_R          =  3.0   # wire-slot radius → Ø6 mm
# Wire centre offset from outer-leg inner wall:
#   B1 outer inner wall = x_left + LEG_W = -37 + 4.5 = -32.5 → wire_cx = -32.5 + 10.55 = -21.95
#   B2 outer inner wall = x_right - LEG_W = +37 - 4.5 = +32.5 → wire_cx = +32.5 - 10.55 = +21.95
WIRE_OUTER_DIST = 10.55

# --- Cable holes in legs (Y-axis, full bracket depth) ---
CABLE_R         =  1.0   # Ø2 mm — runs through both leg walls

# --- Bracket mount holes (Y-axis, through shelf only) ---
MOUNT_R         =  1.5   # Ø3 mm
MOUNT_Z         = 27.0   # hole centre Z (3 mm below top face at Z = BASE_T+BRACKET_H = 30)
# Offsets from leg inner walls:
#   B1 inner (right) wall at -9.5  → inner hole X = -9.5 - 6.0 = -15.5
#   B1 outer (left)  wall at -32.5 → outer hole X = -32.5 + 7.5 = -25.0
MOUNT_INNER_DIST =  6.0
MOUNT_OUTER_DIST =  7.5

# --- PCA9685 board standoffs ---
PCA_LOWER_R     =  1.75  # lower post radius (Ø3.5 mm), sits on base
PCA_LOWER_H     =  3.0   # lower post height → Z = BASE_T to BASE_T+3
PCA_UPPER_R     =  1.15  # upper post radius (Ø2.3 mm), through PCB hole
PCA_UPPER_H     =  3.0   # upper post height → Z = BASE_T+3 to BASE_T+6

# Board hole positions — InLine (+X side board), matching v1 geometry
PCA_X_INNER     = 50.8
PCA_X_OUTER     = 106.7
PCA_Y_NEAR      = -12.7
PCA_Y_FAR       = -31.7

# Board hole positions — BodyBoardBehind (-Y direction)
# Centred on bracket span (X = 0), 19 mm row spacing, starting past B1 front face (Y = -13.4)
PCA_BB_X        = 28.0   # half the 55.9 mm board hole X-spacing  (±28.0)
PCA_BB_Y1       = -18.0  # near row (4.6 mm past B1 front face)
PCA_BB_Y2       = -37.0  # far row

# --- Base plate extents (as distances from mast centre) ---
# InLine (+X board)
BASE_IL_LEFT    = 40.0   # mast → left  edge  (B1 left edge -37, +3 margin)
BASE_IL_RIGHT   = 110.0  # mast → right edge  (board outer X 106.7, +3 margin)
BASE_IL_YFRT    = 35.0   # mast → front edge  (board far Y -31.7, +3 margin)
BASE_IL_YBACK   =  7.0   # mast → back  edge

# Brackets-only / board-behind / single: compact
BASE_MIN_LEFT   = 40.0   # B1 left edge -37, +3 margin
BASE_MIN_RIGHT  = 40.0   # B2 right edge +37, +3 margin
BASE_MIN_YFRT   = 20.0   # B1 front face -13.4, +6.6 margin
BASE_BB_YFRT    = 40.0   # board far row -37, +3 margin
BASE_SGL_RIGHT  = 15.0   # single-bracket: just mast + margin

BASE_YBACK      =  7.0   # shared back extent (all variants)

# --- Fillets ---
FILLET_CORNER   =  1.0   # bracket tower outer vertical corners + base corners
FILLET_TOP      =  0.5   # bracket top-face perimeter edges


# =============================================================================
# BRACKET BUILDER
# =============================================================================

def make_bracket(x_left, x_right, y_back, z_base, mast_side):
    """Build one servo bracket tower with all features.

    Parameters
    ----------
    x_left, x_right : float  — X extents of this bracket
    y_back          : float  — back face Y position (most-positive Y)
    z_base          : float  — Z where bracket starts (top of base plate)
    mast_side       : 'right' | 'left'
                      'right' → B1: inner leg on right (toward +X / mast)
                      'left'  → B2: inner leg on left  (toward -X / mast)
    """
    import FreeCAD
    import Part

    y_shelf = y_back - SHELF_D          # inner shelf face (Y where legs begin)
    y_front = y_shelf - LEG_D           # front face of legs
    z_top   = z_base + BRACKET_H

    # ── U-shape: shelf (full width) + two legs ────────────────────────────────
    shelf = Part.makeBox(
        x_right - x_left, SHELF_D, BRACKET_H,
        FreeCAD.Vector(x_left, y_shelf, z_base)
    )
    left_leg = Part.makeBox(
        LEG_W, SHELF_D + LEG_D, BRACKET_H,
        FreeCAD.Vector(x_left, y_front, z_base)
    )
    right_leg = Part.makeBox(
        LEG_W, SHELF_D + LEG_D, BRACKET_H,
        FreeCAD.Vector(x_right - LEG_W, y_front, z_base)
    )

    # Apply corner fillets to each sub-box BEFORE fusing (avoids lost-edge problem)
    def _corner_edges(box, x0, x1, y0, y1):
        return [e for e in box.Edges
                if hasattr(e.Curve, 'Direction')
                and abs(abs(e.Curve.Direction.z) - 1.0) < 0.05
                and any(abs(e.CenterOfMass.x - cx) < 0.3 and abs(e.CenterOfMass.y - cy) < 0.3
                        for cx, cy in [(x0, y0), (x0, y1), (x1, y0), (x1, y1)])]

    shelf     = _try_fillet(shelf,     FILLET_CORNER,
                            _corner_edges(shelf,     x_left, x_right, y_shelf, y_back),
                            "shelf corners")
    left_leg  = _try_fillet(left_leg,  FILLET_CORNER,
                            _corner_edges(left_leg,  x_left, x_left + LEG_W, y_front, y_back),
                            "left-leg corners")
    right_leg = _try_fillet(right_leg, FILLET_CORNER,
                            _corner_edges(right_leg, x_right - LEG_W, x_right, y_front, y_back),
                            "right-leg corners")

    bracket = shelf.fuse(left_leg).fuse(right_leg).removeSplitter()

    # ── Derived X positions ───────────────────────────────────────────────────
    if mast_side == 'right':
        # B1: inner leg = right leg, outer leg = left leg
        inner_wall_x   = x_right - LEG_W         # = -9.5
        outer_wall_x   = x_left  + LEG_W         # = -32.5
        servo_cx       = inner_wall_x - SERVO_R  # = -15.45
        wire_cx        = outer_wall_x + WIRE_OUTER_DIST  # = -21.95
        mount_inner_x  = inner_wall_x - MOUNT_INNER_DIST  # = -15.5
        mount_outer_x  = outer_wall_x + MOUNT_OUTER_DIST  # = -25.0
        cable_outer_x  = x_left  + LEG_W / 2    # = -34.75
        cable_inner_x  = x_right - LEG_W / 2    # = -7.25
    else:
        # B2: inner leg = left leg, outer leg = right leg
        inner_wall_x   = x_left  + LEG_W         # = +9.5
        outer_wall_x   = x_right - LEG_W         # = +32.5
        servo_cx       = inner_wall_x + SERVO_R  # = +15.45
        wire_cx        = outer_wall_x - WIRE_OUTER_DIST  # = +21.95
        mount_inner_x  = inner_wall_x + MOUNT_INNER_DIST  # = +15.5
        mount_outer_x  = outer_wall_x - MOUNT_OUTER_DIST  # = +25.0
        cable_outer_x  = x_right - LEG_W / 2    # = +34.75
        cable_inner_x  = x_left  + LEG_W / 2    # = +7.25

    # ── Servo pocket + wire/arm slot (fused, Y-axis, through shelf) ───────────
    # Cylinder starts 1 mm in front of y_shelf to ensure clean cut through shelf
    y_cut_start = y_shelf - 1.0
    y_cut_len   = SHELF_D + 2.0

    servo_cyl = Part.makeCylinder(
        SERVO_R, y_cut_len,
        FreeCAD.Vector(servo_cx, y_cut_start, z_base + SERVO_CZ),
        FreeCAD.Vector(0, 1, 0)
    )
    wire_cyl = Part.makeCylinder(
        WIRE_R, y_cut_len,
        FreeCAD.Vector(wire_cx, y_cut_start, z_base + SERVO_CZ),
        FreeCAD.Vector(0, 1, 0)
    )
    bracket = bracket.cut(servo_cyl.fuse(wire_cyl))

    # ── Mount holes (Y-axis, through shelf) ───────────────────────────────────
    for mx in [mount_inner_x, mount_outer_x]:
        hole = Part.makeCylinder(
            MOUNT_R, y_cut_len,
            FreeCAD.Vector(mx, y_cut_start, z_base + MOUNT_Z - z_base),
            FreeCAD.Vector(0, 1, 0)
        )
        bracket = bracket.cut(hole)

    # ── Cable holes in legs (Y-axis, full bracket depth) ─────────────────────
    y_cable_len = SHELF_D + LEG_D + 2.0
    for cx in [cable_outer_x, cable_inner_x]:
        hole = Part.makeCylinder(
            CABLE_R, y_cable_len,
            FreeCAD.Vector(cx, y_front - 1.0, z_base + SERVO_CZ),
            FreeCAD.Vector(0, 1, 0)
        )
        bracket = bracket.cut(hole)

    # ── Top-face edge fillets ─────────────────────────────────────────────────
    top_edges = [e for e in bracket.Edges
                 if hasattr(e.Curve, 'Direction')
                 and abs(e.Curve.Direction.z) < 0.05
                 and abs(e.CenterOfMass.z - z_top) < 0.3]
    bracket = _try_fillet(bracket, FILLET_TOP, top_edges, "bracket top edges")

    return bracket


# =============================================================================
# PCA9685 STANDOFFS
# =============================================================================

def make_pca_standoffs(positions):
    """Four stepped standoffs at the given (x, y) positions."""
    import FreeCAD
    import Part

    z0    = BASE_T
    z_mid = BASE_T + PCA_LOWER_H
    z_top = z_mid  + PCA_UPPER_H

    result = None
    for x, y in positions:
        lower = Part.makeCylinder(PCA_LOWER_R, PCA_LOWER_H,
                                   FreeCAD.Vector(x, y, z0),
                                   FreeCAD.Vector(0, 0, 1))
        upper = Part.makeCylinder(PCA_UPPER_R, PCA_UPPER_H,
                                   FreeCAD.Vector(x, y, z_mid),
                                   FreeCAD.Vector(0, 0, 1))
        post = lower.fuse(upper).removeSplitter()
        result = post if result is None else result.fuse(post)

    return result.removeSplitter()


# =============================================================================
# BASE PLATE
# =============================================================================

def make_base(x_left, x_right, y_front, y_back):
    """Rectangular base plate with mast hole."""
    import FreeCAD
    import Part

    base = Part.makeBox(
        x_right - x_left,
        y_back - y_front,
        BASE_T,
        FreeCAD.Vector(x_left, y_front, 0)
    )

    # Mast hole (runs full depth)
    mast = Part.makeCylinder(MAST_R, BASE_T + 2,
                              FreeCAD.Vector(0, 0, -1),
                              FreeCAD.Vector(0, 0, 1))
    base = base.cut(mast)

    # Base outer corner fillets (apply before returning)
    corners = [(x_left, y_front), (x_left, y_back),
               (x_right, y_front), (x_right, y_back)]
    base_vedges = [e for e in base.Edges
                   if hasattr(e.Curve, 'Direction')
                   and abs(abs(e.Curve.Direction.z) - 1.0) < 0.05
                   and any(abs(e.CenterOfMass.x - cx) < 0.3
                           and abs(e.CenterOfMass.y - cy) < 0.3
                           for cx, cy in corners)]
    base = _try_fillet(base, FILLET_CORNER, base_vedges, "base corners")

    return base


# =============================================================================
# FULL ASSEMBLY BUILDERS
# =============================================================================

def _b1():
    return make_bracket(-(MAST_GAP + BRACKET_W), -MAST_GAP, B1_Y_BACK, BASE_T, 'right')


def _b2():
    return make_bracket(+MAST_GAP, +(MAST_GAP + BRACKET_W), B2_Y_BACK, BASE_T, 'left')


def build_inline_shape():
    """Body: B1 + B2 (staggered) + PCA9685 board standoffs to +X side."""
    base      = make_base(-BASE_IL_LEFT, +BASE_IL_RIGHT, -BASE_IL_YFRT, +BASE_YBACK)
    b1        = _b1()
    b2        = _b2()
    standoffs = make_pca_standoffs([
        (PCA_X_INNER, PCA_Y_NEAR), (PCA_X_INNER, PCA_Y_FAR),
        (PCA_X_OUTER, PCA_Y_NEAR), (PCA_X_OUTER, PCA_Y_FAR),
    ])
    return base.fuse(b1).fuse(b2).fuse(standoffs).removeSplitter()


def build_board_behind_shape():
    """BodyBoardBehind: B1 + B2 + board standoffs in -Y direction."""
    base      = make_base(-BASE_MIN_LEFT, +BASE_MIN_RIGHT, -BASE_BB_YFRT, +BASE_YBACK)
    b1        = _b1()
    b2        = _b2()
    standoffs = make_pca_standoffs([
        (-PCA_BB_X, PCA_BB_Y1), (+PCA_BB_X, PCA_BB_Y1),
        (-PCA_BB_X, PCA_BB_Y2), (+PCA_BB_X, PCA_BB_Y2),
    ])
    return base.fuse(b1).fuse(b2).fuse(standoffs).removeSplitter()


def build_brackets_only_shape():
    """Two staggered brackets + minimal base (no board)."""
    base = make_base(-BASE_MIN_LEFT, +BASE_MIN_RIGHT, -BASE_MIN_YFRT, +BASE_YBACK)
    b1   = _b1()
    b2   = _b2()
    return base.fuse(b1).fuse(b2).removeSplitter()


def build_single_bracket_shape():
    """Single bracket (B1 only) + minimal base."""
    base = make_base(-BASE_MIN_LEFT, +BASE_SGL_RIGHT, -BASE_MIN_YFRT, +BASE_YBACK)
    b1   = _b1()
    return base.fuse(b1).removeSplitter()


# =============================================================================
# DOCUMENT CREATION
# =============================================================================

def _mirror_x(shape):
    """Mirror shape across the YZ plane (negate all X coordinates)."""
    import FreeCAD
    m = FreeCAD.Matrix()
    m.A11 = -1   # flip X
    return shape.transformGeometry(m)


def _add_shape(doc, name, shape, color=None):
    obj = doc.addObject("Part::Feature", name)
    obj.Shape = shape
    doc.recompute()
    if color and __import__('FreeCAD').GuiUp:
        obj.ViewObject.ShapeColor = color
    return obj


def create_inline_doc(doc_name="TrainOrderServoInLine_v2"):
    import FreeCAD

    doc = FreeCAD.newDocument(doc_name)
    blue   = (0.40, 0.60, 1.00, 0.0)
    dblue  = (0.25, 0.45, 0.85, 0.0)
    green  = (0.30, 0.70, 0.40, 0.0)

    print(f"Building {doc_name}::Body …")
    inline = build_inline_shape()
    _add_shape(doc, "Body", inline, blue)

    print(f"Building {doc_name}::Body_Flipped …")
    flipped = _mirror_x(inline)
    _add_shape(doc, "Body_Flipped", flipped, dblue)

    print(f"Building {doc_name}::BodyBoardBehind …")
    behind = build_board_behind_shape()
    _add_shape(doc, "BodyBoardBehind", behind, green)

    doc.recompute()
    print(f"  Body            {inline.Volume:.0f} mm³")
    print(f"  Body_Flipped    {flipped.Volume:.0f} mm³")
    print(f"  BodyBoardBehind {behind.Volume:.0f} mm³")
    return doc, {"Body": inline, "Body_Flipped": flipped, "BodyBoardBehind": behind}


def create_brackets_only_doc(doc_name="TrainOrderServoBracketsOnly_v1"):
    import FreeCAD

    doc = FreeCAD.newDocument(doc_name)
    print(f"Building {doc_name}::Body …")
    shape = build_brackets_only_shape()
    _add_shape(doc, "Body", shape, (0.40, 0.60, 1.00, 0.0))
    doc.recompute()
    print(f"  Body {shape.Volume:.0f} mm³")
    return doc, {"Body": shape}


def create_single_bracket_doc(doc_name="TrainOrderServoSingleBracket_v1"):
    import FreeCAD

    doc = FreeCAD.newDocument(doc_name)
    print(f"Building {doc_name}::Body …")
    shape = build_single_bracket_shape()
    _add_shape(doc, "Body", shape, (0.40, 0.60, 1.00, 0.0))
    doc.recompute()
    print(f"  Body {shape.Volume:.0f} mm³")
    return doc, {"Body": shape}


# =============================================================================
# MESH / STL EXPORT
# =============================================================================

def export_stl(shape, path, linear=0.05, angular=0.3):
    import MeshPart
    mesh = MeshPart.meshFromShape(Shape=shape,
                                  LinearDeflection=linear,
                                  AngularDeflection=angular)
    mesh.write(path)
    print(f"  {mesh.CountFacets:5d} triangles → {path}")


# =============================================================================
# RUN
# =============================================================================

def run(base_dir):
    import FreeCAD

    freecad_dir  = os.path.join(base_dir, FREECAD_DIR)
    printed_dir  = os.path.join(base_dir, EXPORT_DIR)
    os.makedirs(freecad_dir,  exist_ok=True)
    os.makedirs(printed_dir,  exist_ok=True)

    # ── InLine v2 ──────────────────────────────────────────────────────────────
    doc_il, shapes_il = create_inline_doc()
    path_il = os.path.join(freecad_dir, "TrainOrderServoInLine_v2.FCStd")
    doc_il.saveAs(path_il)
    print(f"Saved: {path_il}")

    print("Exporting STLs (InLine):")
    for name, shape in shapes_il.items():
        export_stl(shape, os.path.join(printed_dir, f"TrainOrderServoInLine_v2_{name} (Meshed).stl"))

    # ── Brackets Only v1 ──────────────────────────────────────────────────────
    doc_bo, shapes_bo = create_brackets_only_doc()
    path_bo = os.path.join(freecad_dir, "TrainOrderServoBracketsOnly_v1.FCStd")
    doc_bo.saveAs(path_bo)
    print(f"Saved: {path_bo}")

    print("Exporting STLs (BracketsOnly):")
    for name, shape in shapes_bo.items():
        export_stl(shape, os.path.join(printed_dir, f"TrainOrderServoBracketsOnly_v1_{name} (Meshed).stl"))

    # ── Single Bracket v1 ─────────────────────────────────────────────────────
    doc_sb, shapes_sb = create_single_bracket_doc()
    path_sb = os.path.join(freecad_dir, "TrainOrderServoSingleBracket_v1.FCStd")
    doc_sb.saveAs(path_sb)
    print(f"Saved: {path_sb}")

    print("Exporting STLs (SingleBracket):")
    for name, shape in shapes_sb.items():
        export_stl(shape, os.path.join(printed_dir, f"TrainOrderServoSingleBracket_v1_{name} (Meshed).stl"))

    print("\nAll done.")


EXPORT_DIR  = "printed_files"
FREECAD_DIR = "freecad"

if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    run(os.path.dirname(script_dir))
