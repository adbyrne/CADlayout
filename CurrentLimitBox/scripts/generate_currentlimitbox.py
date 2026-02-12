#!/usr/bin/env python3
"""
Generate CurrentLimitBox parametric model in FreeCAD.

Creates a 3D-printable box for DCC current-limiting components:
- 1156 (BA15S) taillight bulb with friction-fit clips
- Panel-mount slide switch with M3 screw holes
- 5-position terminal strip with cylindrical mounting posts

Usage:
    Run from FreeCAD Python console:
        exec(open("scripts/generate_currentlimitbox.py").read())

    Or via XML-RPC bridge:
        python3 scripts/generate_currentlimitbox.py

Requires: FreeCAD 1.0.x with Part module
"""

import math

# =============================================================================
# DESIGN PARAMETERS
# =============================================================================

# --- Box dimensions ---
BOX_WIDTH = 80.0        # X-axis, mm
BOX_LENGTH = 49.0       # Y-axis, mm (outer)
BOX_HEIGHT = 17.0       # Z-axis, mm (2mm floor + 15mm walls)
WALL_THICKNESS = 2.0    # mm, walls and floor

# --- Angled tab ---
TAB_ANGLE = 55.0        # degrees from horizontal (35 deg overhang)
TAB_FACE_LENGTH = 35.0  # mm along angled surface
TAB_WALL_THICKNESS = 5.0  # mm normal to face

# --- Terminal strip mounting posts (ElectricBox pattern) ---
POST_RADIUS = 1.95      # mm (3.9mm diameter)
POST_HEIGHT = 6.35      # mm
STRIP_CENTER_Y = 24.0   # mm from front edge
POST_X_SPACING = 57.0   # mm center-to-center along X
POST_Y_SPACING = 7.88   # mm center-to-center across strip

# --- Bulb holder ---
BULB_X = 20.0           # X position on tab face
BULB_HOLE_DIAMETER = 15.5  # mm (15mm base + 0.5mm clearance)
BULB_NOTCH_WIDTH = 3.0  # mm (2mm bayonet pin + 1mm tolerance)
BULB_NOTCH_DEPTH = 4.0  # mm radial extent beyond hole edge

# --- Bulb friction clips ---
CLIP_THICKNESS = 2.0    # mm in X direction
CLIP_WIDTH = 10.0       # mm along tab face direction
CLIP_DEPTH = 12.0       # mm protruding inward from inner face
CLIP_GAP = 0.5          # mm gap between clip and hole edge

# --- Slide switch ---
SWITCH_X = 55.0         # X center position on tab face
SWITCH_CUTOUT_WIDTH = 11.8   # mm in X direction (measured)
SWITCH_CUTOUT_HEIGHT = 6.3   # mm along tab face direction (measured)
SWITCH_SCREW_SPACING = 37.5  # mm center-to-center
SWITCH_SCREW_DIAMETER = 3.2  # mm (M3 clearance)

# --- Export paths ---
EXPORT_DIR = "printed_files"
FREECAD_DIR = "freecad"

# =============================================================================
# DERIVED VALUES
# =============================================================================

COS_A = math.cos(math.radians(TAB_ANGLE))
SIN_A = math.sin(math.radians(TAB_ANGLE))

CAVITY_WIDTH = BOX_WIDTH - 2 * WALL_THICKNESS
CAVITY_LENGTH = BOX_LENGTH - 2 * WALL_THICKNESS
CAVITY_DEPTH = BOX_HEIGHT - WALL_THICKNESS
FLOOR_Z = WALL_THICKNESS

# Tab face midpoint (where features are centered)
FACE_MID = TAB_FACE_LENGTH / 2
FACE_CENTER_Y = FACE_MID * COS_A
FACE_CENTER_Z = BOX_HEIGHT + FACE_MID * SIN_A

# Face and normal direction vectors (in YZ plane)
FACE_DIR_Y = COS_A
FACE_DIR_Z = SIN_A
INWARD_DIR_Y = SIN_A
INWARD_DIR_Z = -COS_A

# Post positions
POST_X1 = (BOX_WIDTH - POST_X_SPACING) / 2
POST_X2 = POST_X1 + POST_X_SPACING
POST_Y_HALF = POST_Y_SPACING / 2

# Bulb clip positions
BULB_RADIUS = BULB_HOLE_DIAMETER / 2
CLIP_OFFSET_X = BULB_RADIUS + CLIP_GAP + CLIP_THICKNESS / 2

# Switch screw positions
SWITCH_SCREW_X1 = SWITCH_X - SWITCH_SCREW_SPACING / 2
SWITCH_SCREW_X2 = SWITCH_X + SWITCH_SCREW_SPACING / 2

# Inner face center (offset from outer face by tab thickness)
INNER_CENTER_Y = FACE_CENTER_Y + TAB_WALL_THICKNESS * SIN_A
INNER_CENTER_Z = FACE_CENTER_Z - TAB_WALL_THICKNESS * COS_A


# =============================================================================
# BUILD FUNCTIONS
# =============================================================================

def build_model():
    """Build the complete CurrentLimitBox model. Returns the final shape."""
    import FreeCAD
    import Part

    # --- Box with cavity ---
    box = Part.makeBox(BOX_WIDTH, BOX_LENGTH, BOX_HEIGHT)
    cavity = Part.makeBox(
        CAVITY_WIDTH, CAVITY_LENGTH, CAVITY_DEPTH,
        FreeCAD.Vector(WALL_THICKNESS, WALL_THICKNESS, WALL_THICKNESS)
    )
    result = box.cut(cavity)

    # --- Angled tab ---
    v1 = FreeCAD.Vector(0, 0, BOX_HEIGHT)
    v2 = FreeCAD.Vector(0,
                         TAB_FACE_LENGTH * COS_A,
                         BOX_HEIGHT + TAB_FACE_LENGTH * SIN_A)
    v3 = FreeCAD.Vector(0,
                         v2.y + TAB_WALL_THICKNESS * SIN_A,
                         v2.z - TAB_WALL_THICKNESS * COS_A)
    v4 = FreeCAD.Vector(0,
                         v1.y + TAB_WALL_THICKNESS * SIN_A,
                         v1.z - TAB_WALL_THICKNESS * COS_A)

    wire = Part.makePolygon([v1, v2, v3, v4, v1])
    face = Part.Face(wire)
    tab = face.extrude(FreeCAD.Vector(BOX_WIDTH, 0, 0))
    result = result.fuse(tab)

    # --- 4 mounting posts (2x2 grid) ---
    for px in [POST_X1, POST_X2]:
        for py_offset in [-POST_Y_HALF, POST_Y_HALF]:
            post = Part.makeCylinder(
                POST_RADIUS, POST_HEIGHT,
                FreeCAD.Vector(px, STRIP_CENTER_Y + py_offset, FLOOR_Z),
                FreeCAD.Vector(0, 0, 1)
            )
            result = result.fuse(post)

    # --- Bulb hole ---
    hole_start = FreeCAD.Vector(
        BULB_X,
        FACE_CENTER_Y - 2 * SIN_A,
        FACE_CENTER_Z + 2 * COS_A
    )
    hole = Part.makeCylinder(BULB_RADIUS, 10.0, hole_start,
                              FreeCAD.Vector(0, INWARD_DIR_Y, INWARD_DIR_Z))
    result = result.cut(hole)

    # --- Bulb pin notches ---
    for sign in [-1, 1]:
        nc_offset = BULB_RADIUS + BULB_NOTCH_DEPTH / 2
        nc_y = FACE_CENTER_Y + sign * nc_offset * FACE_DIR_Y
        nc_z = FACE_CENTER_Z + sign * nc_offset * FACE_DIR_Z
        hw = BULB_NOTCH_WIDTH / 2
        hd = BULB_NOTCH_DEPTH / 2

        p1 = FreeCAD.Vector(BULB_X - hw,
                             nc_y - hd * FACE_DIR_Y - 2 * SIN_A,
                             nc_z - hd * FACE_DIR_Z + 2 * COS_A)
        p2 = FreeCAD.Vector(BULB_X - hw,
                             nc_y + hd * FACE_DIR_Y - 2 * SIN_A,
                             nc_z + hd * FACE_DIR_Z + 2 * COS_A)
        p3 = FreeCAD.Vector(BULB_X + hw,
                             nc_y + hd * FACE_DIR_Y - 2 * SIN_A,
                             nc_z + hd * FACE_DIR_Z + 2 * COS_A)
        p4 = FreeCAD.Vector(BULB_X + hw,
                             nc_y - hd * FACE_DIR_Y - 2 * SIN_A,
                             nc_z - hd * FACE_DIR_Z + 2 * COS_A)

        nw = Part.makePolygon([p1, p2, p3, p4, p1])
        nf = Part.Face(nw)
        notch = nf.extrude(FreeCAD.Vector(0, 10 * SIN_A, -10 * COS_A))
        result = result.cut(notch)

    # --- Bulb friction clips ---
    for sign in [-1, 1]:
        clip_x = BULB_X + sign * CLIP_OFFSET_X
        hw = CLIP_THICKNESS / 2
        hf = CLIP_WIDTH / 2

        p1 = FreeCAD.Vector(clip_x - hw,
                             INNER_CENTER_Y - hf * FACE_DIR_Y,
                             INNER_CENTER_Z - hf * FACE_DIR_Z)
        p2 = FreeCAD.Vector(clip_x - hw,
                             INNER_CENTER_Y + hf * FACE_DIR_Y,
                             INNER_CENTER_Z + hf * FACE_DIR_Z)
        p3 = FreeCAD.Vector(clip_x + hw,
                             INNER_CENTER_Y + hf * FACE_DIR_Y,
                             INNER_CENTER_Z + hf * FACE_DIR_Z)
        p4 = FreeCAD.Vector(clip_x + hw,
                             INNER_CENTER_Y - hf * FACE_DIR_Y,
                             INNER_CENTER_Z - hf * FACE_DIR_Z)

        cw = Part.makePolygon([p1, p2, p3, p4, p1])
        cf = Part.Face(cw)
        clip = cf.extrude(FreeCAD.Vector(
            0, CLIP_DEPTH * INWARD_DIR_Y, CLIP_DEPTH * INWARD_DIR_Z
        ))
        result = result.fuse(clip)

    # --- Switch cutout ---
    sw_hw = SWITCH_CUTOUT_WIDTH / 2
    sw_hh = SWITCH_CUTOUT_HEIGHT / 2

    p1 = FreeCAD.Vector(SWITCH_X - sw_hw,
                         FACE_CENTER_Y - sw_hh * FACE_DIR_Y - 2 * SIN_A,
                         FACE_CENTER_Z - sw_hh * FACE_DIR_Z + 2 * COS_A)
    p2 = FreeCAD.Vector(SWITCH_X - sw_hw,
                         FACE_CENTER_Y + sw_hh * FACE_DIR_Y - 2 * SIN_A,
                         FACE_CENTER_Z + sw_hh * FACE_DIR_Z + 2 * COS_A)
    p3 = FreeCAD.Vector(SWITCH_X + sw_hw,
                         FACE_CENTER_Y + sw_hh * FACE_DIR_Y - 2 * SIN_A,
                         FACE_CENTER_Z + sw_hh * FACE_DIR_Z + 2 * COS_A)
    p4 = FreeCAD.Vector(SWITCH_X + sw_hw,
                         FACE_CENTER_Y - sw_hh * FACE_DIR_Y - 2 * SIN_A,
                         FACE_CENTER_Z - sw_hh * FACE_DIR_Z + 2 * COS_A)

    sw_wire = Part.makePolygon([p1, p2, p3, p4, p1])
    sw_face = Part.Face(sw_wire)
    sw_cutout = sw_face.extrude(FreeCAD.Vector(0, 10 * SIN_A, -10 * COS_A))
    result = result.cut(sw_cutout)

    # --- Switch M3 screw holes ---
    for sx in [SWITCH_SCREW_X1, SWITCH_SCREW_X2]:
        start = FreeCAD.Vector(
            sx,
            FACE_CENTER_Y - 2 * SIN_A,
            FACE_CENTER_Z + 2 * COS_A
        )
        screw_hole = Part.makeCylinder(
            SWITCH_SCREW_DIAMETER / 2, 10.0, start,
            FreeCAD.Vector(0, INWARD_DIR_Y, INWARD_DIR_Z)
        )
        result = result.cut(screw_hole)

    # --- Clean up ---
    result = result.removeSplitter()

    solid_count = len(result.Solids)
    if solid_count != 1:
        print(f"WARNING: Expected 1 solid, got {solid_count}")

    return result


def create_document(doc_name="CurrentLimitBox"):
    """Create FreeCAD document with the model and return the document."""
    import FreeCAD

    doc = FreeCAD.newDocument(doc_name)
    shape = build_model()

    obj = doc.addObject("Part::Feature", "CurrentLimitBox")
    obj.Shape = shape
    doc.recompute()

    print(f"Created {doc_name}: {len(shape.Solids)} solid(s), "
          f"volume={shape.Volume:.1f}mm3")
    return doc


def export_stl(doc, path):
    """Export standard STL."""
    obj = doc.getObject("CurrentLimitBox")
    obj.Shape.exportStl(path)
    print(f"Exported STL: {path}")


def export_meshed_stl(doc, path, linear_deflection=0.05, angular_deflection=0.3):
    """Export fine-meshed STL via MeshPart."""
    import MeshPart

    obj = doc.getObject("CurrentLimitBox")
    mesh = MeshPart.meshFromShape(
        Shape=obj.Shape,
        LinearDeflection=linear_deflection,
        AngularDeflection=angular_deflection
    )
    mesh.write(path)
    print(f"Exported meshed STL ({mesh.CountFacets} triangles): {path}")


# =============================================================================
# MAIN
# =============================================================================

if __name__ == "__main__":
    import os
    import sys

    # Determine base directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    base_dir = os.path.dirname(script_dir)

    doc = create_document()

    # Save FreeCAD file
    fcstd_path = os.path.join(base_dir, FREECAD_DIR, "CurrentLimitBox.FCStd")
    doc.saveAs(fcstd_path)
    print(f"Saved: {fcstd_path}")

    # Export STLs
    stl_path = os.path.join(base_dir, EXPORT_DIR, "CurrentLimitBox.stl")
    export_stl(doc, stl_path)

    meshed_path = os.path.join(base_dir, EXPORT_DIR, "CurrentLimitBox (Meshed).stl")
    export_meshed_stl(doc, meshed_path)

    print("Done!")
