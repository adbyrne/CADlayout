#!/usr/bin/env python3
"""Generate SwitchToggle v4 parametric model in FreeCAD.

THREE 3D-printable parts:

  Shell      — 50x50x12mm hollow tray, open front face (electronics access)
  FrontPlate — 50x50x3mm plate + 8mm pivot posts (closes the shell)
  Lever      — 25x15x4mm symmetric paddle (X-axis pivot, side nut slot)

Split rationale:
  - Shell prints open-face-up → zero bridging, no supports required
  - FrontPlate is a thin flat plate with posts → trivial print, no supports
  - Electronics (LEDs, wiring) installed through open front before closing
  - Shell + FrontPlate glued with CA after wiring; 4x M3 corner screws mount to fascia

Key geometry:
  - Lever pivot at world Y=25 (base center), world Z=19 (mid-post)
  - Arm = 10mm; 5mm cable travel at 30 deg swing (arcsin 5/10)
  - Rod hole A (Y=15): lever slot down  → "normal = lever UP"
  - Rod hole B (Y=35): lever slot down  → "normal = lever DOWN" (flip lever)
  - LEDs in shell top/bottom walls at Z=9 (pointing up/down)

Assembly: Shell (Z=0..12) + FrontPlate (Z=12..15) + Posts (Z=15..23) + Lever

Requires: FreeCAD 1.0.x with Part and MeshPart modules
"""

import os

# =============================================================================
# PARAMETERS
# =============================================================================

# --- Common base dimensions ---
BASE_W = 50.0   # X: width
BASE_H = 50.0   # Y: height

# --- Shell (Part A) ---
SHELL_DEPTH = 12.0   # Z: back face Z=0 (fascia), open front face at Z=12
WALL_T      =  2.0   # back wall, side walls, top and bottom walls
# Interior cavity: X=2..48, Y=2..48, Z=2..12 (open at Z=12)

# --- LED holes in shell top/bottom walls (Y direction) ---
LED_DIA =  5.2   # 5mm LED body + 0.2mm clearance
LED_X   = 25.0   # centered
LED_Z   =  9.0   # Z position in top/bottom wall (fully within shell, Z=9±2.6 = 6.4..11.6)

# --- Shell back face holes ---
ROD_DIA  =  5.0    # Gold-N-Rod #504 sheath OD
ROD_X    = 25.0
ROD_Y_A  = 15.0    # rod hole A: lever slot at bottom → "normal = UP"
ROD_Y_B  = 35.0    # rod hole B: lever slot at top (flipped) → "normal = DOWN"
CABLE_DIA =  6.0   # 3-wire LED cable pass-through (centered)
CABLE_X   = 25.0
CABLE_Y   = 25.0
M3_DIA    =  3.4   # M3 clearance (corner mount holes)
MOUNT_CORNERS = [(5.0, 5.0), (5.0, 45.0), (45.0, 5.0), (45.0, 45.0)]

# --- Alignment pegs (on shell front face Z=12, fit into FrontPlate) ---
# Positioned on wall rims (not over cavity opening)
PEG_DIA        = 2.0
PEG_H          = 1.5    # height above shell front face
PEG_HOLE_DIA   = 2.1    # clearance in FrontPlate
PEG_HOLE_DEPTH = 2.0    # depth into FrontPlate back face
PEG_POSITIONS  = [(5.0, 1.0), (45.0, 1.0), (5.0, 49.0), (45.0, 49.0)]

# --- FrontPlate (Part B) ---
PLATE_T      =  3.0   # Z: plate thickness (local Z=0 back, Z=3 front/operator face)
POST_W       =  4.0   # X: pivot post width
POST_D       =  4.0   # Y: pivot post depth
POST_H       =  8.0   # Z: post height above plate front face (local Z=3..11)
POST_LEFT_X  = 10.0   # left edge of left post  (X=10..14)
POST_RIGHT_X = 36.0   # left edge of right post (X=36..40)
POST_Y_CENTER = 25.0  # Y center of both posts  (Y=23..27)
PIN_DIA      =  2.2   # M2 clearance
# Pin in plate-local coords: Z = PLATE_T + POST_H/2 = 3 + 4 = 7
# Pin in world coords: SHELL_DEPTH + PLATE_T + POST_H/2 = 12 + 3 + 4 = 19

# --- Lever ---
LEV_W = 15.0
LEV_H = 25.0
LEV_T  =  4.0
LEV_PIVOT_Y   = LEV_H / 2    # = 12.5: center — flip end-for-end to use other rod hole
LEV_PIVOT_DIA =  2.2          # pivot hole runs in X direction at Z=LEV_T/2=2 (mid-thickness)
LEV_SLOT_W    =  2.5          # cable slot X width (2-56 rod clearance)
LEV_SLOT_H    =  5.0          # cable slot Y length (open at Y=0 edge, Y=0..5)
LEV_SLOT_Y    =  2.5          # slot center from lever bottom (10mm below pivot)
# World-Y when slot at bottom: LEV_ASM_Y + 2.5 = 12.5 + 2.5 = 15.0 = ROD_Y_A ✓
# World-Y when flipped:        LEV_ASM_Y + 22.5 = 35.0 = ROD_Y_B ✓
NUT_SLOT_W =  5.5   # X: 2-56 hex nut pocket width (corner-to-corner = 5.50mm)
NUT_SLOT_T =  3.0   # Z: nut pocket height (nut thickness 2.38mm + clearance)
NUT_SLOT_D =  5.0   # Y: pocket depth from lever bottom edge

# --- Assembly placements (visual only; STLs export at origin) ---
LEV_ASM_X = (BASE_W - LEV_W) / 2                        # = 17.5
LEV_ASM_Y = BASE_H / 2 - LEV_PIVOT_Y                    # = 12.5
LEV_ASM_Z = SHELL_DEPTH + PLATE_T + POST_H/2 - LEV_T/2  # = 17.0

# --- Export ---
EXPORT_DIR  = "printed_files"
FREECAD_DIR = "freecad"


# =============================================================================
# BUILD FUNCTIONS
# =============================================================================

def build_shell():
    """Part A: hollow tray, open front face at Z=SHELL_DEPTH. No bridging needed."""
    import FreeCAD, Part

    # Outer box
    result = Part.makeBox(BASE_W, BASE_H, SHELL_DEPTH)

    # Interior cavity — open at front face (Z=SHELL_DEPTH), no front wall
    cav_w = BASE_W - 2 * WALL_T          # = 46
    cav_h = BASE_H - 2 * WALL_T          # = 46
    cav_d = SHELL_DEPTH - WALL_T         # = 10 (Z=2 to Z=12, opens at front)
    cavity = Part.makeBox(cav_w, cav_h, cav_d,
                          FreeCAD.Vector(WALL_T, WALL_T, WALL_T))
    result = result.cut(cavity)

    # LED holes in top/bottom walls (Y direction, at Z=LED_Z)
    led_top = Part.makeCylinder(
        LED_DIA / 2, WALL_T + 2,
        FreeCAD.Vector(LED_X, BASE_H - WALL_T - 0.5, LED_Z),
        FreeCAD.Vector(0, 1, 0)
    )
    led_bot = Part.makeCylinder(
        LED_DIA / 2, WALL_T + 2,
        FreeCAD.Vector(LED_X, -0.5, LED_Z),
        FreeCAD.Vector(0, 1, 0)
    )
    result = result.cut(led_top)
    result = result.cut(led_bot)

    # Back face holes (Z direction through 2mm back wall)
    def back_hole(x, y, dia):
        return Part.makeCylinder(
            dia / 2, WALL_T + 2,
            FreeCAD.Vector(x, y, -0.5),
            FreeCAD.Vector(0, 0, 1)
        )

    result = result.cut(back_hole(ROD_X,   ROD_Y_A,  ROD_DIA))    # rod hole A
    result = result.cut(back_hole(ROD_X,   ROD_Y_B,  ROD_DIA))    # rod hole B
    result = result.cut(back_hole(CABLE_X, CABLE_Y,  CABLE_DIA))  # LED cable
    for cx, cy in MOUNT_CORNERS:
        result = result.cut(back_hole(cx, cy, M3_DIA))             # M3 mount

    # Alignment pegs on front rim (Z=SHELL_DEPTH), positioned on wall rims
    for px, py in PEG_POSITIONS:
        peg = Part.makeCylinder(
            PEG_DIA / 2, PEG_H,
            FreeCAD.Vector(px, py, SHELL_DEPTH),
            FreeCAD.Vector(0, 0, 1)
        )
        result = result.fuse(peg)

    result = result.removeSplitter()

    sc = len(result.Solids)
    if sc != 1:
        print(f"WARNING: Shell has {sc} solids (expected 1)")
    return result


def build_front_plate():
    """Part B: 3mm plate with pivot posts. Closes the shell after electronics install."""
    import FreeCAD, Part

    # Solid plate
    result = Part.makeBox(BASE_W, BASE_H, PLATE_T)

    # Pivot posts on front face (local Z=PLATE_T)
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

    # Pin hole (X direction through both posts, at local Z = PLATE_T + POST_H/2 = 7)
    pin_z = PLATE_T + POST_H / 2
    pin_hole = Part.makeCylinder(
        PIN_DIA / 2, BASE_W + 2,
        FreeCAD.Vector(-1, POST_Y_CENTER, pin_z),
        FreeCAD.Vector(1, 0, 0)
    )
    result = result.cut(pin_hole)

    # Alignment peg holes (Z direction, from back face into plate)
    for px, py in PEG_POSITIONS:
        hole = Part.makeCylinder(
            PEG_HOLE_DIA / 2, PEG_HOLE_DEPTH + 1,
            FreeCAD.Vector(px, py, -0.5),
            FreeCAD.Vector(0, 0, 1)
        )
        result = result.cut(hole)

    # M3 clearance holes at corners (Z direction, through full plate thickness)
    # Screws pass through fascia → shell back wall → shell interior → plate → nut on front
    for cx, cy in MOUNT_CORNERS:
        hole = Part.makeCylinder(
            M3_DIA / 2, PLATE_T + 2,
            FreeCAD.Vector(cx, cy, -0.5),
            FreeCAD.Vector(0, 0, 1)
        )
        result = result.cut(hole)

    result = result.removeSplitter()

    sc = len(result.Solids)
    if sc != 1:
        print(f"WARNING: FrontPlate has {sc} solids (expected 1)")
    return result


def build_lever():
    """Seesaw lever: X-axis pivot, single cable slot (bottom), side nut slot."""
    import FreeCAD, Part

    result = Part.makeBox(LEV_W, LEV_H, LEV_T)

    # Pivot hole — X direction through full lever width at Y=center, Z=mid-thickness
    pivot = Part.makeCylinder(
        LEV_PIVOT_DIA / 2, LEV_W + 2,
        FreeCAD.Vector(-1, LEV_PIVOT_Y, LEV_T / 2),
        FreeCAD.Vector(1, 0, 0)
    )
    result = result.cut(pivot)

    # Cable slot — Z direction through lever thickness, opens at Y=0 (bottom edge)
    sx = (LEV_W - LEV_SLOT_W) / 2   # = 6.25: X-centered
    cable_slot = Part.makeBox(
        LEV_SLOT_W, LEV_SLOT_H, LEV_T + 2,
        FreeCAD.Vector(sx, 0, -1)    # Y=0..5, through Z
    )
    result = result.cut(cable_slot)

    # Nut slot from bottom edge (Y=0): 2-56 nut slides in, rod locks it
    # Slot: 5.5mm wide × 3mm tall × 5mm deep, centered on cable slot
    nut_x = (LEV_W - NUT_SLOT_W) / 2    # = 4.75: X start
    nut_z = (LEV_T - NUT_SLOT_T) / 2    # = 0.5:  Z start (centered at Z=2)
    nut_slot = Part.makeBox(
        NUT_SLOT_W, NUT_SLOT_D, NUT_SLOT_T,
        FreeCAD.Vector(nut_x, 0, nut_z)  # Y=0..5, Z=0.5..3.5
    )
    result = result.cut(nut_slot)

    result = result.removeSplitter()

    sc = len(result.Solids)
    if sc != 1:
        print(f"WARNING: Lever has {sc} solids (expected 1)")
    return result


# =============================================================================
# DOCUMENT + EXPORT
# =============================================================================

def create_document(doc_name="SwitchToggle"):
    """Create FreeCAD document with all three parts at assembly positions."""
    import FreeCAD

    doc = FreeCAD.newDocument(doc_name)

    shell_shape = build_shell()
    shell_obj   = doc.addObject("Part::Feature", "Shell")
    shell_obj.Shape = shell_shape

    plate_shape = build_front_plate()
    plate_obj   = doc.addObject("Part::Feature", "FrontPlate")
    plate_obj.Shape = plate_shape
    plate_obj.Placement = FreeCAD.Placement(
        FreeCAD.Vector(0, 0, SHELL_DEPTH),   # sits at Z=12 on shell
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
        shell_obj.ViewObject.ShapeColor  = (0.4,  0.6,  1.0,  0.0)  # blue
        plate_obj.ViewObject.ShapeColor  = (0.25, 0.45, 0.85, 0.0)  # darker blue
        lever_obj.ViewObject.ShapeColor  = (1.0,  0.65, 0.2,  0.0)  # orange
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

    # Export each part at origin (print orientation)
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
