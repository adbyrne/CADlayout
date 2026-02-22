#!/usr/bin/env python3
"""
Generate SplineBracket parametric model in FreeCAD.

Creates a two-part 3D-printable bracket system (PETG) to hold premade spline
roadbed and attach it to a layout module edge:
- Part 1: Spline Holder — block with trapezoid groove and V-tongue
- Part 2: Gusset Bracket — L-shaped bracket with dual gusset ribs and V-groove

Assembly: single 6.35mm vertical bolt through spline + holder + bracket.
V-tongue/groove prevents rotation. Bracket mounts to module edge via horizontal bolt.

Note: Bracket is rotated 90deg around Y when assembled — bracket X corresponds
to holder Z and vice versa.

Usage:
    Run from FreeCAD Python console:
        exec(open("scripts/generate_splinebracket.py").read())

Requires: FreeCAD 1.0.x with Part module
"""

import os

# =============================================================================
# DESIGN PARAMETERS
# =============================================================================

# --- Common dimensions ---
PART_WIDTH = 60.0           # X-axis, mm (across the spline / bracket width)
PART_DEPTH = 60.0           # Z-axis, mm (along the spline / bracket depth)
BOLT_DIAMETER = 6.35        # mm (1/4 inch)
BOLT_RADIUS = BOLT_DIAMETER / 2

# --- Spline Holder (Part 1) ---
HOLDER_HEIGHT = 32.0        # Y-axis, mm
HOLDER_FLOOR = 10.0         # mm, solid floor below groove

# Groove profile (trapezoid, centered in X)
GROOVE_BOTTOM_WIDTH = 40.0  # mm at Y=HOLDER_FLOOR
GROOVE_STRAIGHT_HEIGHT = 17.0  # mm, vertical walls from floor to taper start
GROOVE_TAPER_HEIGHT = 5.0   # mm, 45-degree taper zone
GROOVE_TAPER_INSET = 5.0    # mm each side (45 deg: inset == taper height)

# V-tongue on holder bottom (anti-rotation)
TONGUE_WIDTH = 10.0         # mm base width
TONGUE_DEPTH = 3.0          # mm (apex extends below Y=0)

# --- Gusset Bracket (Part 2) ---
FLANGE_THICKNESS = 10.0     # mm (horizontal flange height in Y)
LEG_THICKNESS = 10.0        # mm (vertical leg width in X)
LEG_HEIGHT = 120.0          # mm (total vertical leg extent)
GUSSET_THICKNESS = 5.0      # mm (each rib wall thickness in Z)
FILLET_RADIUS = 3.0         # mm (inside corner fillets)

# V-groove on bracket flange top (mates with holder tongue)
VGROOVE_WIDTH = 11.0        # mm base width (1mm wider than tongue)
VGROOVE_DEPTH = 3.0         # mm (same depth as tongue)

# Bolt positions
HOLDER_BOLT_X = PART_WIDTH / 2   # centered
HOLDER_BOLT_Z = PART_DEPTH / 2   # centered
LOWER_BOLT_Y = -93.0        # mm from bracket top (125mm from holder top)
LOWER_BOLT_X = LEG_THICKNESS / 2  # centered in leg
LOWER_BOLT_Z = PART_DEPTH / 2     # centered

# --- Export paths ---
EXPORT_DIR = "printed_files"
FREECAD_DIR = "freecad"

# =============================================================================
# DERIVED VALUES
# =============================================================================

# Groove X extents
GROOVE_X_LEFT = (PART_WIDTH - GROOVE_BOTTOM_WIDTH) / 2      # 10
GROOVE_X_RIGHT = GROOVE_X_LEFT + GROOVE_BOTTOM_WIDTH         # 50

# Groove Y extents
GROOVE_Y_BOTTOM = HOLDER_FLOOR                                # 10
GROOVE_Y_TAPER_START = GROOVE_Y_BOTTOM + GROOVE_STRAIGHT_HEIGHT  # 27
GROOVE_Y_TOP = GROOVE_Y_TAPER_START + GROOVE_TAPER_HEIGHT     # 32

# Top opening after taper
GROOVE_TOP_LEFT = GROOVE_X_LEFT + GROOVE_TAPER_INSET          # 15
GROOVE_TOP_RIGHT = GROOVE_X_RIGHT - GROOVE_TAPER_INSET        # 45

# Tongue X extents (centered)
TONGUE_X_LEFT = HOLDER_BOLT_X - TONGUE_WIDTH / 2             # 25
TONGUE_X_RIGHT = HOLDER_BOLT_X + TONGUE_WIDTH / 2            # 35

# V-groove Z extents (centered, runs along bracket X)
VGROOVE_Z_LEFT = LOWER_BOLT_Z - VGROOVE_WIDTH / 2            # 24.5
VGROOVE_Z_RIGHT = LOWER_BOLT_Z + VGROOVE_WIDTH / 2           # 35.5

# Gusset triangle vertices (in XY plane)
GUSSET_V1 = (LEG_THICKNESS, -FLANGE_THICKNESS)               # (10, -10)
GUSSET_V2 = (PART_WIDTH, -FLANGE_THICKNESS)                  # (60, -10)
GUSSET_V3 = (LEG_THICKNESS, -LEG_HEIGHT)                     # (10, -220)


# =============================================================================
# BUILD FUNCTIONS
# =============================================================================

def build_holder(doc):
    """Build the Spline Holder (Part 1)."""
    import Part
    import FreeCAD

    # Outer block
    block = Part.makeBox(PART_WIDTH, HOLDER_HEIGHT, PART_DEPTH)

    # Groove profile (trapezoid cross-section in XY, extruded along Z)
    groove_pts = [
        FreeCAD.Vector(GROOVE_X_LEFT, GROOVE_Y_BOTTOM, 0),
        FreeCAD.Vector(GROOVE_X_RIGHT, GROOVE_Y_BOTTOM, 0),
        FreeCAD.Vector(GROOVE_X_RIGHT, GROOVE_Y_TAPER_START, 0),
        FreeCAD.Vector(GROOVE_TOP_RIGHT, GROOVE_Y_TOP, 0),
        FreeCAD.Vector(GROOVE_TOP_RIGHT, GROOVE_Y_TOP + 1, 0),  # overshoot
        FreeCAD.Vector(GROOVE_TOP_LEFT, GROOVE_Y_TOP + 1, 0),
        FreeCAD.Vector(GROOVE_TOP_LEFT, GROOVE_Y_TOP, 0),
        FreeCAD.Vector(GROOVE_X_LEFT, GROOVE_Y_TAPER_START, 0),
        FreeCAD.Vector(GROOVE_X_LEFT, GROOVE_Y_BOTTOM, 0),
    ]
    groove_wire = Part.makePolygon(groove_pts)
    groove_face = Part.Face(groove_wire)
    groove_solid = groove_face.extrude(FreeCAD.Vector(0, 0, PART_DEPTH))
    result = block.cut(groove_solid)

    # V-tongue on bottom (anti-rotation, runs along Z at center X)
    tongue_pts = [
        FreeCAD.Vector(TONGUE_X_LEFT, 0, 0),
        FreeCAD.Vector(TONGUE_X_RIGHT, 0, 0),
        FreeCAD.Vector(HOLDER_BOLT_X, -TONGUE_DEPTH, 0),
        FreeCAD.Vector(TONGUE_X_LEFT, 0, 0),
    ]
    tongue_wire = Part.makePolygon(tongue_pts)
    tongue_face = Part.Face(tongue_wire)
    tongue_solid = tongue_face.extrude(FreeCAD.Vector(0, 0, PART_DEPTH))
    result = result.fuse(tongue_solid)

    # Bolt hole: vertical (Y axis), through floor + tongue
    bolt = Part.makeCylinder(
        BOLT_RADIUS, HOLDER_FLOOR + TONGUE_DEPTH + 2,
        FreeCAD.Vector(HOLDER_BOLT_X, -TONGUE_DEPTH - 1, HOLDER_BOLT_Z),
        FreeCAD.Vector(0, 1, 0),
    )
    result = result.cut(bolt)

    result = result.removeSplitter()
    assert len(result.Solids) == 1, f"Holder has {len(result.Solids)} solids, expected 1"

    obj = doc.addObject("Part::Feature", "HolderBlock")
    obj.Shape = result
    return obj


def build_bracket(doc):
    """Build the Gusset Bracket (Part 2)."""
    import Part
    import FreeCAD

    # Horizontal flange
    flange = Part.makeBox(
        PART_WIDTH, FLANGE_THICKNESS, PART_DEPTH,
        FreeCAD.Vector(0, -FLANGE_THICKNESS, 0),
    )

    # Vertical leg
    leg = Part.makeBox(
        LEG_THICKNESS, LEG_HEIGHT, PART_DEPTH,
        FreeCAD.Vector(0, -LEG_HEIGHT, 0),
    )

    bracket = flange.fuse(leg)

    # Gusset rib 1 (front, Z=0 to Z=GUSSET_THICKNESS)
    gusset_pts = [
        FreeCAD.Vector(GUSSET_V1[0], GUSSET_V1[1], 0),
        FreeCAD.Vector(GUSSET_V2[0], GUSSET_V2[1], 0),
        FreeCAD.Vector(GUSSET_V3[0], GUSSET_V3[1], 0),
        FreeCAD.Vector(GUSSET_V1[0], GUSSET_V1[1], 0),
    ]
    gusset_wire = Part.makePolygon(gusset_pts)
    gusset_face = Part.Face(gusset_wire)
    gusset1 = gusset_face.extrude(FreeCAD.Vector(0, 0, GUSSET_THICKNESS))

    # Gusset rib 2 (back)
    gusset2 = gusset_face.extrude(FreeCAD.Vector(0, 0, GUSSET_THICKNESS))
    gusset2.translate(FreeCAD.Vector(0, 0, PART_DEPTH - GUSSET_THICKNESS))

    bracket = bracket.fuse(gusset1)
    bracket = bracket.fuse(gusset2)

    # V-groove on flange top (runs along bracket X at Z=center)
    vgroove_pts = [
        FreeCAD.Vector(0, 1, VGROOVE_Z_LEFT),
        FreeCAD.Vector(0, 1, VGROOVE_Z_RIGHT),
        FreeCAD.Vector(0, -VGROOVE_DEPTH, LOWER_BOLT_Z),
        FreeCAD.Vector(0, 1, VGROOVE_Z_LEFT),
    ]
    vgroove_wire = Part.makePolygon(vgroove_pts)
    vgroove_face = Part.Face(vgroove_wire)
    vgroove_solid = vgroove_face.extrude(FreeCAD.Vector(PART_WIDTH, 0, 0))
    bracket = bracket.cut(vgroove_solid)

    # Upper bolt hole: vertical (Y axis), through flange at center
    upper_bolt = Part.makeCylinder(
        BOLT_RADIUS, FLANGE_THICKNESS + 2,
        FreeCAD.Vector(HOLDER_BOLT_X, -FLANGE_THICKNESS - 1, HOLDER_BOLT_Z),
        FreeCAD.Vector(0, 1, 0),
    )
    bracket = bracket.cut(upper_bolt)

    # Lower bolt hole: horizontal (X axis), through vertical leg
    lower_bolt = Part.makeCylinder(
        BOLT_RADIUS, LEG_THICKNESS + 2,
        FreeCAD.Vector(-1, LOWER_BOLT_Y, LOWER_BOLT_Z),
        FreeCAD.Vector(1, 0, 0),
    )
    bracket = bracket.cut(lower_bolt)

    bracket = bracket.removeSplitter()
    assert len(bracket.Solids) == 1, f"Bracket has {len(bracket.Solids)} solids, expected 1"

    # Apply inside fillets
    # Find inside edges: L-junction, gusset-to-leg, gusset-to-flange
    fillet_edges = []
    for edge in bracket.Edges:
        if edge.Curve.__class__.__name__ != "Line":
            continue
        mid_param = (edge.FirstParameter + edge.LastParameter) / 2
        mid = edge.valueAt(mid_param)

        # L-junction: X≈LEG_THICKNESS, Y≈-FLANGE_THICKNESS, runs along Z
        if (abs(mid.x - LEG_THICKNESS) < 1 and abs(mid.y - (-FLANGE_THICKNESS)) < 1
                and edge.Length > 10):
            fillet_edges.append(edge)
        # Gusset-to-leg: X≈LEG_THICKNESS, runs along Y, at Z≈5 or Z≈55
        elif (abs(mid.x - LEG_THICKNESS) < 1 and edge.Length > 50
                and (abs(mid.z - GUSSET_THICKNESS) < 1
                     or abs(mid.z - (PART_DEPTH - GUSSET_THICKNESS)) < 1)):
            fillet_edges.append(edge)
        # Gusset-to-flange: Y≈-FLANGE_THICKNESS, runs along X, at Z≈5 or Z≈55
        elif (abs(mid.y - (-FLANGE_THICKNESS)) < 1 and edge.Length > 10
                and (abs(mid.z - GUSSET_THICKNESS) < 1
                     or abs(mid.z - (PART_DEPTH - GUSSET_THICKNESS)) < 1)):
            fillet_edges.append(edge)

    if fillet_edges:
        bracket = bracket.makeFillet(FILLET_RADIUS, fillet_edges)
        bracket = bracket.removeSplitter()
        assert len(bracket.Solids) == 1, f"Filleted bracket has {len(bracket.Solids)} solids"

    obj = doc.addObject("Part::Feature", "GussetBracket")
    obj.Shape = bracket
    return obj


def export_parts(doc):
    """Export STL files for 3D printing."""
    import MeshPart

    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_dir = os.path.dirname(script_dir)
    export_dir = os.path.join(project_dir, EXPORT_DIR)
    os.makedirs(export_dir, exist_ok=True)

    for obj_name, filename in [
        ("HolderBlock", "SplineBracket-Holder.stl"),
        ("GussetBracket", "SplineBracket-GussetBracket.stl"),
    ]:
        obj = doc.getObject(obj_name)
        mesh = MeshPart.meshFromShape(
            Shape=obj.Shape, LinearDeflection=0.1, AngularDeflection=0.5,
        )
        path = os.path.join(export_dir, filename)
        mesh.write(path)
        print(f"Exported: {path}")


def save_document(doc):
    """Save the FreeCAD document."""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_dir = os.path.dirname(script_dir)
    freecad_dir = os.path.join(project_dir, FREECAD_DIR)
    os.makedirs(freecad_dir, exist_ok=True)

    path = os.path.join(freecad_dir, "SplineBracket.FCStd")
    doc.saveAs(path)
    print(f"Saved: {path}")


# =============================================================================
# MAIN
# =============================================================================

if __name__ == "__main__" or True:  # Always run when exec'd
    import FreeCAD

    doc = FreeCAD.newDocument("SplineBracket")

    holder = build_holder(doc)
    bracket = build_bracket(doc)
    doc.recompute()

    save_document(doc)
    export_parts(doc)

    print(f"Holder volume: {holder.Shape.Volume:.0f} mm³")
    print(f"Bracket volume: {bracket.Shape.Volume:.0f} mm³")
    print("Done.")
